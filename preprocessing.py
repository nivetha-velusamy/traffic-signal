
from pathlib import Path
import re
import pandas as pd

INTERSECTIONS = ["AlankarChowk", "JehangirChowk", "RTOChowk"]

ALIASES = {
    "car": ["car", "cars"],
    "motorbike": ["motorbike", "motor_bike", "motorcycle", "motorcycles", "bike"],
    "bus": ["bus", "buses"],
    "truck": ["truck", "trucks", "lorry", "lorries"],
}


def norm(value):
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def infer_date(path):
    match = re.search(r"_(\d{1,2})(?:_one)?$", path.stem, re.I)
    if match and 1 <= int(match.group(1)) <= 31:
        return pd.Timestamp(2023, 1, int(match.group(1)))
    return pd.NaT


def read_one(path, root, chunksize=100_000):
    # Read only the required columns, in manageable chunks.
    header = pd.read_csv(path, nrows=0, encoding="utf-8-sig")
    original_columns = list(header.columns)
    lookup = {norm(col): col for col in original_columns}

    time_col = next(
        (lookup[k] for k in ("time", "timestamp", "observation_time") if k in lookup),
        None
    )
    direction_col = next(
        (lookup[k] for k in ("direction", "movement", "turn") if k in lookup),
        None
    )

    if time_col is None or direction_col is None:
        raise ValueError("Missing required Time or Direction column")

    vehicle_columns = {}
    for target, aliases in ALIASES.items():
        vehicle_columns[target] = next(
            (lookup[name] for name in aliases if name in lookup),
            None
        )

    usecols = [time_col, direction_col]
    usecols += [c for c in vehicle_columns.values() if c is not None]

    intersection = path.relative_to(root).parts[0]
    approach = path.parent.name
    observation_date = infer_date(path)
    source_file = str(path.relative_to(root)).replace("\\", "/")

    results = []
    raw_rows = 0

    for chunk in pd.read_csv(
        path,
        usecols=usecols,
        chunksize=chunksize,
        encoding="utf-8-sig"
    ):
        raw_rows += len(chunk)

        chunk = chunk.rename(
            columns={time_col: "time", direction_col: "direction"}
        )

        for target, source in vehicle_columns.items():
            if source and source in chunk.columns:
                if source != target:
                    chunk = chunk.rename(columns={source: target})
            else:
                chunk[target] = 0

            chunk[target] = pd.to_numeric(
                chunk[target], errors="coerce"
            ).fillna(0)

        chunk["time"] = chunk["time"].astype(str).str.strip()
        chunk["direction"] = (
            chunk["direction"].astype(str).str.strip().str.upper()
        )

        parsed = pd.to_datetime(chunk["time"], format="mixed", errors="coerce")
        chunk["hour"] = parsed.dt.hour
        chunk["minute"] = parsed.dt.minute

        chunk["intersection"] = intersection
        chunk["approach"] = approach
        chunk["observation_date"] = observation_date
        chunk["source_file"] = source_file

        chunk["total_vehicles"] = chunk[
            ["car", "motorbike", "bus", "truck"]
        ].sum(axis=1)

        # Aggregate each chunk to hourly traffic summaries.
        keys = [
            "observation_date", "hour", "intersection",
            "approach", "direction", "source_file"
        ]

        grouped = chunk.groupby(
            keys, dropna=False, observed=True
        ).agg(
            car=("car", "sum"),
            motorbike=("motorbike", "sum"),
            bus=("bus", "sum"),
            truck=("truck", "sum"),
            total_vehicles=("total_vehicles", "sum"),
            observation_count=("time", "size")
        ).reset_index()

        results.append(grouped)

    if not results:
        return pd.DataFrame(), 0

    return pd.concat(results, ignore_index=True), raw_rows


def load_traffic_data(data_dir, variant="standard"):
    root = Path(data_dir)
    frames = []
    reports = []

    # Only inspect the three intended intersection folders.
    for intersection in INTERSECTIONS:
        folder = root / intersection

        if not folder.is_dir():
            reports.append({
                "file": intersection,
                "rows": 0,
                "status": "missing",
                "message": "Intersection folder not found"
            })
            continue

        paths = sorted(folder.rglob("*.csv"))

        for path in paths:
            is_one = path.stem.lower().endswith("_one")

            if variant == "standard" and is_one:
                continue
            if variant == "one" and not is_one:
                continue

            try:
                part, raw_rows = read_one(path, root)

                if not part.empty:
                    frames.append(part)

                reports.append({
                    "file": str(path.relative_to(root)),
                    "rows": raw_rows,
                    "status": "loaded",
                    "message": "Hourly summaries created"
                })

            except Exception as exc:
                reports.append({
                    "file": str(path.relative_to(root)),
                    "rows": 0,
                    "status": "skipped",
                    "message": str(exc)
                })

    data = (
        pd.concat(frames, ignore_index=True)
        if frames else pd.DataFrame()
    )

    report = pd.DataFrame(
        reports,
        columns=["file", "rows", "status", "message"]
    )

    return data, report


def summarize_quality(df):
    total_cells = df.shape[0] * df.shape[1]
    missing = int(df.isna().sum().sum())

    return {
        "missing_cells": missing,
        "duplicate_rows": int(df.duplicated().sum()),
        "completeness": (
            (total_cells - missing) / total_cells * 100
            if total_cells else 0
        )
    }

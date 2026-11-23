# Smart Traffic Signal Efficiency & Congestion Analysis

Streamlit EDA dashboard for real heterogeneous traffic-count observations from three Pune intersections.

## Dataset placement
Copy the extracted `AlankarChowk`, `JehangirChowk`, and `RTOChowk` folders into:

```text
dataset/raw/traffic/
├── AlankarChowk/
├── JehangirChowk/
└── RTOChowk/
```

Keep their nested `a2`, `a3`, etc. folders and original CSV names. The loader scans recursively.

The source contains standard CSVs and alternate filenames ending `_one.csv`. The app defaults to standard files and lets you switch variants. Avoid selecting **All CSV files** until you verify that the alternate versions do not overlap or duplicate observations.

Expected columns: `Time`, `Direction`, `car`, `motorbike`, `bus`, `truck`. Files missing Time or Direction are skipped and shown in the file report.

## Run on Windows
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Dashboard
Overview, Vehicle Analysis, Direction Analysis, Time Analysis, Intersection Comparison, Data Quality and Export.

## Important limitation
The dataset records vehicle counts and movement directions. It does not directly measure signal-cycle duration, queue length, waiting time or signal timing plans. Analyse traffic-volume patterns and discuss possible improvements; do not claim actual signal efficiency was measured.

The date parser interprets filename day numbers such as `_11` as January 2023. Verify this against the original README/data dictionary before making date-specific claims.


from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Smart Traffic Analysis",
    page_icon="🚦",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "dataset" / "processed" / "traffic_summary.csv"

st.title("🚦 Smart Traffic Signal Efficiency & Congestion Analysis")
st.caption(
    "Exploratory analysis of real traffic-count observations "
    "from Pune intersections."
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    if "observation_date" in df.columns:
        df["observation_date"] = pd.to_datetime(
            df["observation_date"], errors="coerce"
        )

    numeric_columns = [
        "car", "motorbike", "bus", "truck",
        "total_vehicles", "hour", "observation_count"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


if not DATA_FILE.exists():
    st.error("Processed dataset not found!")
    st.info(
        "Expected location: dataset/processed/traffic_summary.csv"
    )
    st.stop()

try:
    df = load_data()
except Exception as error:
    st.error("Unable to load the processed dataset.")
    st.exception(error)
    st.stop()

required_columns = [
    "intersection", "direction",
    "car", "motorbike", "bus", "truck",
    "total_vehicles", "source_file"
]

missing_columns = [c for c in required_columns if c not in df.columns]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()

vehicle_columns = ["car", "motorbike", "bus", "truck"]

# Sidebar filters
with st.sidebar:
    st.header("🚦 Dashboard Filters")

    intersections = sorted(df["intersection"].dropna().unique())

    selected_intersections = st.multiselect(
        "Select intersections",
        intersections,
        default=intersections
    )

    directions = sorted(df["direction"].dropna().unique())

    selected_directions = st.multiselect(
        "Select directions",
        directions,
        default=directions
    )

filtered = df[
    df["intersection"].isin(selected_intersections)
    & df["direction"].isin(selected_directions)
].copy()

if filtered.empty:
    st.warning("No traffic records match the selected filters.")
    st.stop()

# KPI calculations
total_vehicles = int(filtered[vehicle_columns].sum().sum())

if "observation_count" in filtered.columns:
    total_observations = int(filtered["observation_count"].sum())
else:
    total_observations = len(filtered)

total_intersections = filtered["intersection"].nunique()
total_files = filtered["source_file"].nunique()

st.subheader("📊 Traffic Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Vehicles", f"{total_vehicles:,}")
c2.metric("Observations", f"{total_observations:,}")
c3.metric("Intersections", total_intersections)
c4.metric("CSV Files", total_files)

# Prepare loading report
if "observation_count" in filtered.columns:
    report = (
        filtered.groupby("source_file", as_index=False)
        ["observation_count"].sum()
        .rename(columns={"observation_count": "rows"})
    )
else:
    report = (
        filtered.groupby("source_file")
        .size()
        .reset_index(name="rows")
    )

report["status"] = "loaded"
report["message"] = "Hourly summaries available"

# Dashboard tabs
tabs = st.tabs([
    "Overview",
    "Vehicle Analysis",
    "Direction Analysis",
    "Time Analysis",
    "Intersection Comparison",
    "Data Quality",
    "Export"
])

# 1. Overview
with tabs[0]:
    st.subheader("Traffic Overview")

    vehicle_summary = (
        filtered[vehicle_columns].sum()
        .rename_axis("Vehicle")
        .reset_index(name="Count")
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            vehicle_summary,
            names="Vehicle",
            values="Count",
            hole=0.4,
            title="Vehicle Category Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        intersection_summary = (
            filtered.groupby("intersection")["total_vehicles"]
            .sum().reset_index()
        )

        fig = px.bar(
            intersection_summary,
            x="intersection",
            y="total_vehicles",
            color="intersection",
            title="Traffic Across Intersections"
        )
        st.plotly_chart(fig, use_container_width=True)

    if "observation_date" in filtered.columns:
        daily = (
            filtered.dropna(subset=["observation_date"])
            .groupby("observation_date")["total_vehicles"]
            .sum().reset_index()
        )

        if not daily.empty:
            fig = px.line(
                daily,
                x="observation_date",
                y="total_vehicles",
                markers=True,
                title="Traffic by Observation Date"
            )
            st.plotly_chart(fig, use_container_width=True)

# 2. Vehicle Analysis
with tabs[1]:
    st.subheader("Vehicle Category Analysis")

    vehicle_summary = (
        filtered[vehicle_columns].sum()
        .rename_axis("Vehicle Type")
        .reset_index(name="Count")
    )

    fig = px.bar(
        vehicle_summary,
        x="Vehicle Type",
        y="Count",
        color="Vehicle Type",
        title="Vehicle Count by Category"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(vehicle_summary, hide_index=True, use_container_width=True)

# 3. Direction Analysis
with tabs[2]:
    st.subheader("Direction-wise Traffic Analysis")

    direction_summary = (
        filtered.groupby("direction")["total_vehicles"]
        .sum().reset_index()
        .sort_values("total_vehicles", ascending=False)
    )

    fig = px.bar(
        direction_summary,
        x="direction",
        y="total_vehicles",
        color="direction",
        title="Traffic by Movement Direction"
    )

    st.plotly_chart(fig, use_container_width=True)

    direction_table = filtered.pivot_table(
        index="intersection",
        columns="direction",
        values="total_vehicles",
        aggfunc="sum",
        fill_value=0
    )

    st.dataframe(direction_table, use_container_width=True)

# 4. Time Analysis
with tabs[3]:
    st.subheader("Hourly Traffic Analysis")

    if "hour" in filtered.columns:
        hourly = (
            filtered.dropna(subset=["hour"])
            .groupby("hour")["total_vehicles"]
            .sum()
            .reindex(range(24), fill_value=0)
            .reset_index()
        )

        if hourly["total_vehicles"].sum() > 0:
            fig = px.line(
                hourly,
                x="hour",
                y="total_vehicles",
                markers=True,
                title="Traffic Volume by Hour"
            )

            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, use_container_width=True)

            peak = hourly.loc[hourly["total_vehicles"].idxmax()]

            st.info(
                f"Highest recorded traffic hour: "
                f"{int(peak['hour']):02d}:00"
            )
        else:
            st.info("No valid hourly observations found.")
    else:
        st.warning("Hourly data is not available.")

# 5. Intersection Comparison
with tabs[4]:
    st.subheader("Intersection Comparison")

    comparison = (
        filtered.groupby("intersection")["total_vehicles"]
        .sum().reset_index()
        .sort_values("total_vehicles", ascending=False)
    )

    fig = px.bar(
        comparison,
        x="intersection",
        y="total_vehicles",
        color="intersection",
        title="Traffic Volume Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(comparison, hide_index=True, use_container_width=True)

# 6. Data Quality
with tabs[5]:
    st.subheader("Data Quality Report")

    missing = int(filtered.isna().sum().sum())
    duplicates = int(filtered.duplicated().sum())

    cells = filtered.shape[0] * filtered.shape[1]
    completeness = (
        ((cells - missing) / cells) * 100 if cells else 0
    )

    a, b, c = st.columns(3)

    a.metric("Missing Cells", f"{missing:,}")
    b.metric("Duplicate Rows", f"{duplicates:,}")
    c.metric("Completeness", f"{completeness:.2f}%")

    missing_summary = (
        filtered.isna().sum()
        .rename_axis("Column")
        .reset_index(name="Missing Values")
    )

    fig = px.bar(
        missing_summary,
        x="Column",
        y="Missing Values",
        title="Missing Values by Column"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Processed File Report")
    st.dataframe(report, hide_index=True, use_container_width=True)

# 7. Export
with tabs[6]:
    st.subheader("Download Traffic Data")

    st.download_button(
        "⬇️ Download Cleaned Traffic Data",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="cleaned_traffic_data.csv",
        mime="text/csv"
    )

    st.download_button(
        "⬇️ Download File Loading Report",
        data=report.to_csv(index=False).encode("utf-8"),
        file_name="traffic_file_report.csv",
        mime="text/csv"
    )

    st.subheader("Data Preview")
    st.dataframe(filtered.head(100), use_container_width=True)

# Dataset limitations
with st.expander("ℹ️ Dataset Limitations"):
    st.write(
        "This dataset contains traffic counts and movement directions. "
        "It does not directly measure signal-cycle duration, queue length "
        "or waiting time. The dashboard analyses traffic-volume patterns "
        "and supports discussion of possible signal improvements. "
        "It does not claim measured signal efficiency."
    )

st.caption("Smart Traffic Analysis | Pune Traffic Dataset")

import pandas as pd

def add_analysis_columns(df):
    result = df.copy()
    vehicle_cols = ["car", "motorbike", "bus", "truck"]
    result["total_vehicles"] = result[vehicle_cols].sum(axis=1)
    return result

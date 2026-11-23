# SMART TRAFFIC SIGNAL EFFICIENCY AND CONGESTION ANALYSIS

## Official EDA Project Executive Report

### 1. Project Abstract

This study investigates traffic volume patterns, vehicle distribution, directional movement, and time-based traffic variations across three major intersections in Pune, India. The project uses heterogeneous traffic count data collected during January 2023 and applies Exploratory Data Analysis (EDA) techniques using Python.

The analysis examines cars, motorbikes, buses, and trucks to understand traffic composition and compare vehicle movement across different intersections and directions. The project combines data preprocessing, statistical analysis, and interactive visualizations through a Streamlit dashboard.

The objective is to identify traffic-volume patterns and potential congestion indicators that can support data-driven traffic management and future signal-planning decisions.

### 2. Dataset Metrics & Quality Audit

- **Dataset Source:** Heterogeneous Traffic Count Dataset, Pune (January 2023), Mendeley Data
- **Intersections Analyzed:** 3
- **Intersections:** AlankarChowk, JehangirChowk, RTOChowk
- **Source CSV Files Processed:** 56
- **Processed Observations:** 3,253 rows × 12 attributes
- **Duplicate Records Identified:** 13
- **Missing Values:** 130 cells (approximately 0.33% of all dataset cells)
- **Missing Hour Values:** 65
- **Missing Direction Values:** 65
- **Processed Dataset Memory Footprint:** Approximately 1.09 MB
- **Date Range in Processed Data:** 11 January 2023 – 18 January 2023

**Data Quality Note:** The supplied processed dataset contains missing values and duplicate records. These should be reviewed before final statistical interpretation. No claim of complete missing-value imputation or duplicate removal is made.

### 3. Core Descriptive Statistics

The following table presents the descriptive statistics calculated from the supplied `traffic_summary.csv`.

| Attribute | Count | Mean | Median | Mode | Std Dev | Variance | Min | Q1 | Q2 | Q3 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hour | 3,188 | 9.77 | 10 | 10 | 0.92 | 0.84 | 8 | 9 | 10 | 10 | 12 |
| Car | 3,253 | 6,553,142.90 | 1,396,841 | 0 | 14,276,834.17 | 2.04e14 | 0 | 144,225 | 1,396,841 | 6,793,813 | 186,411,857 |
| Motorbike | 3,253 | 5,505,995.10 | 1,345,593 | 0 | 10,006,209.29 | 1.00e14 | 0 | 66,410 | 1,345,593 | 6,191,164 | 78,618,915 |
| Bus | 3,253 | 598,067.36 | 104,242 | 0 | 1,164,291.21 | 1.36e12 | 0 | 0 | 104,242 | 580,200 | 9,021,217 |
| Truck | 3,253 | 1,115,420.17 | 271,306 | 0 | 1,964,775.85 | 3.86e12 | 0 | 25,000 | 271,306 | 1,269,343 | 14,633,568 |
| Total Vehicles | 3,253 | 13,772,625.53 | 4,048,423 | 0 | 22,741,587.41 | 5.17e14 | 0 | 424,005 | 4,048,423 | 16,386,919 | 194,806,047 |
| Observation Count | 3,253 | 17,809.41 | 23,975 | 25,000 | 8,917.79 | 7.95e7 | 3 | 9,975 | 23,975 | 25,000 | 48,572 |

*Note: Statistics are calculated from the supplied processed file. Variance is expressed in squared units. Q1, Q2, and Q3 represent the 25th, 50th, and 75th percentiles respectively. Large traffic-count values should be validated against the original dataset's measurement and aggregation methodology before interpreting them as literal vehicle totals.*

### 4. Key Traffic & Congestion Insights

1. **Vehicle Composition:** Cars account for approximately 47.58% of the recorded vehicle-category totals, followed by motorbikes at 39.98%, trucks at 8.10%, and buses at 4.34%.

2. **Traffic Distribution:** The processed dataset contains 3,253 records distributed across three intersections: RTOChowk (1,248), JehangirChowk (1,233), and AlankarChowk (772).

3. **Peak Hour Pattern:** Based on the sum of recorded `total_vehicles` values, 10:00 has the highest aggregate value, followed by 11:00 and 09:00.

4. **Directional Traffic:** The LEFT direction has the highest aggregate recorded traffic volume, followed by DOWN, UP, and RIGHT.

5. **Intersection Comparison:** AlankarChowk has the highest aggregate recorded `total_vehicles` value, followed by JehangirChowk and RTOChowk.

6. **Data Quality:** The dataset contains 13 duplicate rows and 130 missing cells. These records require quality checks before drawing final conclusions.

7. **Traffic Analysis Opportunity:** Vehicle composition, hourly variations, directional distribution, and intersection comparisons provide useful indicators for further investigation of urban traffic patterns.

### 5. Technologies & Analytical Tools

| Technology | Application |
|---|---|
| Python | Core data analysis |
| Pandas | Data cleaning and aggregation |
| NumPy | Numerical computations |
| Streamlit | Interactive dashboard |
| Plotly | Interactive data visualization |
| CSV | Dataset storage and processing |
| Git & GitHub | Version control and project hosting |

### 6. Dashboard Features

The Streamlit dashboard contains seven major analytical sections:

- **Overview:** Displays key traffic indicators and overall traffic patterns.
- **Vehicle Analysis:** Compares cars, motorbikes, buses, and trucks.
- **Direction Analysis:** Examines directional traffic distribution.
- **Time Analysis:** Explores hourly traffic variations.
- **Intersection Comparison:** Compares traffic patterns across three intersections.
- **Data Quality:** Presents information about the processed dataset.
- **Export:** Allows users to download processed traffic summaries.

### 7. Conclusion

This project demonstrates the application of Exploratory Data Analysis and interactive visualization to understand heterogeneous urban traffic patterns.

The analysis of vehicle categories, traffic directions, hourly variations, and intersection-level differences provides a structured understanding of the recorded traffic data. The Streamlit dashboard makes these findings accessible through interactive charts, filters, comparisons, and downloadable data.

The project establishes a foundation for future work involving traffic congestion prediction, vehicle queue estimation, traffic signal optimization, and intelligent transportation management.

**Project Type:** Python-Based Exploratory Data Analysis and Interactive Traffic Dashboard.

**Repository:** https://github.com/nivetha-velusamy/traffic-signal

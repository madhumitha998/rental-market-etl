# 🏠 Rental Analytics & Geospatial ETL Pipeline

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Snowflake](https://img.shields.io/badge/Data%20Warehouse-Snowflake-blue)](https://www.snowflake.com/)
[![dbt](https://img.shields.io/badge/Transformation-dbt-orange)](https://www.getdbt.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)](https://streamlit.io/)

An end-to-end data engineering pipeline designed to extract rental listing data, transform it through a multi-layered dbt architecture within a Snowflake cloud warehouse, and visualize market trends through an interactive Streamlit dashboard.

## 🔗 Live Demo
**View the interactive dashboard here: [https://rental-market-etl.streamlit.app/](https://rental-market-etl.streamlit.app/)**

---

## 🏗 System Architecture
The project follows a classic **ETL (Extract, Transform, Load)** pattern optimized for cloud-native analytics:


1.  **Extract**: Ingests raw real estate data into **Snowflake**.
2.  **Transform (dbt)**: Cleans and models data using staging and analytics layers.
3.  **Load/Visualize**: Streams the final data into a **Streamlit** dashboard for real-time analysis.

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Environment for Streamlit and data scripts. |
| **Data Warehouse**| Snowflake | Centralized cloud storage and compute. |
| **Transformation** | dbt (Core) | SQL-based modeling and schema enforcement. |
| **Frontend** | Streamlit | UI/UX for interactive geospatial exploration. |
| **Visualization** | Plotly Express | Dynamic heatmaps and scatter analysis. |

---

## 💎 Data Modeling with dbt

### 1. Staging Layer (`stg_rentals.sql`)
Data hygiene:
*   **Cleaning**: Renames raw columns to standardized headers (e.g., `sq_ft` → `SQUAREFOOTAGE`).
*   **Schema Enforcement**: Casts numerical strings to integers to optimize query performance.
*   **Data Integrity**: Filters out records missing critical geospatial coordinates (`LATITUDE`/`LONGITUDE`).

### 2. Analytics Layer (`rental_costs.sql`)
For final business metrics:
*   **Cost Calculation**: Implements business logic: `TOTAL_MONTHLY_COST = BASE_RENT + COALESCE(MONTHLY_HOA, 0)`.
*   **Efficiency Metrics**: Pre-calculates `COST_PER_SQFT` to identify market value outliers.

---

## 🚀 Dashboard Features

### 📍 Geospatial Heatmap
Utilizes Plotly Mapbox to visualize property density. Points are dynamically sized and colored based on the `TOTAL_MONTHLY_COST` metric.

### 🔍 Advanced Filtering
*   **Multi-Select**: Filter by **Bedrooms** and **Bathrooms** simultaneously.
*   **Real-time Metrics**: A result counter displays the total properties found matching the current filter criteria.

### 📊 Statistical Insights
Includes a **Price Distribution Histogram** and a **Cost vs. Size Scatter Plot** to analyze property ROI.

---

## 🔧 Installation & Setup

### 1. Environment Configuration
This project requires **Python 3.11** to support modern Streamlit caching mechanisms.
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

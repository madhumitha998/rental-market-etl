import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Rental Analytics", layout="wide")

# 1. Connection Function
@st.cache_resource # Keeps the connection alive without reconnecting every click
def get_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

# 2. Data Fetching
@st.cache_data # High-performance: doesn't re-run the query unless the data changes
def load_data():
    conn = get_connection()
    query = "SELECT * FROM rental_costs" # dbt model output
    return pd.read_sql(query, conn)

st.title("🏙️ Rental Cost Analytics")
df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filters")
# Bedroom filter
bedroom_options = sorted(df['BEDROOMS'].unique())
selected_bedrooms = st.sidebar.multiselect("Bedrooms", bedroom_options, default=bedroom_options)

# Add Bathroom filter
bathroom_options = sorted(df['BATHROOMS'].unique())
selected_bathrooms = st.sidebar.multiselect("Bathrooms", bathroom_options, default=bathroom_options)

# Filter the dataframe
filtered_df = df[
    (df['BEDROOMS'].isin(selected_bedrooms)) & 
    (df['BATHROOMS'].isin(selected_bathrooms))
]

st.metric(label="Properties Found", value=len(filtered_df))

# 4. Visualization 
st.subheader("Property Locations")
fig_map = px.scatter_mapbox(
    filtered_df,
    lat="LATITUDE",
    lon="LONGITUDE",
    size="TOTAL_MONTHLY_COST",
    color="TOTAL_MONTHLY_COST",
    hover_name="ADDRESS",
    zoom=12,
    mapbox_style="carto-positron"
)
st.plotly_chart(fig_map, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Distribution")
    fig_hist = px.histogram(
        filtered_df, 
        x="TOTAL_MONTHLY_COST", 
        nbins=20, 
        title="Monthly Cost Spread",
        color_discrete_sequence=['#636EFA']
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("Cost vs. Square Footage")
    fig_scatter = px.scatter(
        filtered_df, 
        x="SQUAREFOOTAGE", 
        y="TOTAL_MONTHLY_COST",
        color="BEDROOMS",
        hover_data=['ADDRESS'],
        title="Price per Size Analysis"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# 5. Data Preview
st.dataframe(filtered_df)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- Configuration & Theme ---
st.set_page_config(
    page_title="Sri Lanka Retail Prices", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom color palette for consistency
CHART_THEME = px.colors.qualitative.Prism

@st.cache_data
def load_data():
    path = Path("data/processed/retail_prices_cleaned.csv")
    if not path.exists():
        st.error(f"Processed dataset not found at {path}. Please run the cleaning pipeline first.")
        st.stop()
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# --- Header Section ---
st.title("📊 Sri Lankan Retail Price Intelligence")
st.markdown("""
<div style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">
    An interactive analysis of weekly retail prices for essential consumer items in Colombo (2020-2024).
</div>
""", unsafe_allow_html=True)

# --- Sidebar Filters ---
st.sidebar.header("🔍 Global Filters")
st.sidebar.markdown("Use these filters to adjust the dataset across all dashboard sections.")

min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input(
    "Date Range", 
    [min_date, max_date], 
    min_value=min_date, 
    max_value=max_date,
    help="Select the start and end dates for the analysis."
)

items = sorted(df['item'].dropna().unique())
selected_items = st.sidebar.multiselect(
    "Select Items", 
    items, 
    default=items[:4] if len(items) > 4 else items,
    help="Choose which consumer goods to include in the charts."
)

units = sorted(df['unit'].dropna().unique())
selected_units = st.sidebar.multiselect(
    "Select Units", 
    units, 
    default=units,
    help="Filter by measurement unit (e.g., 1 kg, Bunch)."
)

# --- 6. Limitations and Assumptions (Sidebar) ---
with st.sidebar.expander("⚠️ Limitations & Assumptions", expanded=False):
    st.markdown("""
    - **No Category/Market:** Analysis is limited to item-level metrics as broader groupings are unavailable.
    - **No Volume Data:** Revenue, profit, and demand cannot be calculated without sales volume.
    - **Missing Ranges:** Missing 'low' or 'high' price boundaries are ignored, not imputed.
    - **Week Parsing:** Week identifiers (e.g., W1) are approximated to specific dates.
    """)

# Apply Global Filters
if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
else:
    mask = pd.Series(True, index=df.index)
    start_date, end_date = min_date, max_date

if not selected_items or not selected_units:
    st.warning("⚠️ **No data available.** Please select at least one Item and one Unit from the sidebar.")
    st.stop()

mask = mask & (df['item'].isin(selected_items))
mask = mask & (df['unit'].isin(selected_units))

df_filtered = df[mask].copy()

if df_filtered.empty:
    st.warning("⚠️ **No records match the current filters.** Try expanding the date range or selecting different items.")
    st.stop()

# --- 1. Overview Section ---
st.subheader("1. Executive Overview")
st.markdown("High-level snapshot of the currently filtered dataset.")

# Responsive 3-column layout over 2 rows for better mobile readability
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Date Range", f"{start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}")
kpi2.metric("Total Observations", f"{len(df_filtered):,}")
kpi3.metric("Unique Items", df_filtered['item'].nunique())

kpi4, kpi5, kpi6 = st.columns(3)
kpi4.metric("Unique Units", df_filtered['unit'].nunique())
kpi5.metric("Overall Average Price", f"Rs. {df_filtered['avg_price'].mean():,.2f}")
kpi6.metric("Missing Avg Prices", f"{df_filtered['avg_price'].isna().sum():,}")

st.divider()

# --- 2. Price Trends Section ---
st.subheader("2. Longitudinal Price Trends")
st.markdown("Track the trajectory of average retail prices over time. Hover over the lines for specific dates and values.")

if len(selected_items) > 0:
    fig_trends = px.line(
        df_filtered, 
        x='date', y='avg_price', color='item', 
        labels={'avg_price': 'Average Price (LKR)', 'date': 'Date', 'item': 'Item'},
        color_discrete_sequence=CHART_THEME
    )
    fig_trends.update_layout(
        hovermode="x unified",
        yaxis_tickformat=",.2f",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Range overlay for single item
    if len(selected_items) == 1:
        st.markdown(f"**Price Range Envelope:** Displaying the High and Low observed bounds for **{selected_items[0]}**.")
        single_item_data = df_filtered[df_filtered['item'] == selected_items[0]].sort_values('date')
        if not single_item_data['min_price'].isna().all() and not single_item_data['max_price'].isna().all():
            fig_range = go.Figure()
            fig_range.add_trace(go.Scatter(
                x=single_item_data['date'], y=single_item_data['max_price'], 
                name='Maximum Price', line=dict(color='rgba(239, 85, 59, 0.5)', width=1)
            ))
            fig_range.add_trace(go.Scatter(
                x=single_item_data['date'], y=single_item_data['min_price'], 
                name='Minimum Price', fill='tonexty', fillcolor='rgba(150, 150, 150, 0.1)',
                line=dict(color='rgba(0, 204, 150, 0.5)', width=1)
            ))
            fig_range.add_trace(go.Scatter(
                x=single_item_data['date'], y=single_item_data['avg_price'], 
                name='Average Price', line=dict(color='#636EFA', width=3)
            ))
            fig_range.update_layout(
                yaxis_title="Price (LKR)", 
                yaxis_tickformat=",.2f",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_range, use_container_width=True)

st.divider()

# --- 3. Item Comparison Section ---
st.subheader("3. Cross-Sectional Item Comparison")
st.markdown("Contrast absolute pricing and relative weekly changes across selected items.")

col_c1, col_c2 = st.columns(2)

# Latest Price Comparison
latest_dates = df_filtered.groupby('item')['date'].max().reset_index()
latest_prices = pd.merge(latest_dates, df_filtered, on=['item', 'date'], how='left')
fig_latest = px.bar(
    latest_prices, x='item', y='avg_price', text='avg_price', 
    title="Most Recent Average Price", 
    labels={'avg_price': 'Latest Price (LKR)', 'item': 'Item'},
    color='item', color_discrete_sequence=CHART_THEME
)
fig_latest.update_traces(texttemplate='Rs. %{text:,.2f}', textposition='outside')
fig_latest.update_layout(showlegend=False, yaxis_tickformat=",.0f")
col_c1.plotly_chart(fig_latest, use_container_width=True)

# Percentage Change Ranking
pct_change_comp = df_filtered.groupby('item')['price_change_percentage'].mean().reset_index().rename(columns={'price_change_percentage': 'Avg Weekly % Change'})
pct_change_comp = pct_change_comp.dropna().sort_values(by='Avg Weekly % Change', ascending=False)
if not pct_change_comp.empty:
    fig_pct = px.bar(
        pct_change_comp, x='item', y='Avg Weekly % Change', 
        title="Average Weekly Price % Change", 
        labels={'item': 'Item'},
        color='Avg Weekly % Change',
        color_continuous_scale=px.colors.diverging.RdYlGn[::-1] # Red for high increase, green for decrease
    )
    fig_pct.update_layout(coloraxis_showscale=False)
    col_c2.plotly_chart(fig_pct, use_container_width=True)
else:
    col_c2.info("Not enough weekly sequential data to calculate percentage changes.")

st.divider()

# --- 4. Volatility Section ---
st.subheader("4. Price Volatility Analysis")
st.markdown("""
Evaluate market stability. **Coefficient of Variation (CV)** represents relative volatility (standard deviation divided by the mean), making it ideal for comparing items with vastly different base prices.
""")

volatility_data = []
for item in selected_items:
    item_df = df_filtered[df_filtered['item'] == item]
    if len(item_df) > 1:
        std_dev = item_df['avg_price'].std()
        mean_price = item_df['avg_price'].mean()
        cv = (std_dev / mean_price) * 100 if mean_price > 0 else np.nan
        avg_price_range = item_df['price_range'].mean()
        
        volatility_data.append({
            'Item': item,
            'Standard Deviation (LKR)': std_dev,
            'Coefficient of Variation (%)': cv,
            'Average Price Range (LKR)': avg_price_range
        })

volatility_df = pd.DataFrame(volatility_data)

if not volatility_df.empty:
    volatility_df = volatility_df.dropna().sort_values(by='Coefficient of Variation (%)', ascending=False)
    
    col_v1, col_v2 = st.columns(2)
    
    fig_cv = px.bar(
        volatility_df, x='Item', y='Coefficient of Variation (%)', 
        title="Relative Volatility (Coefficient of Variation)",
        color='Coefficient of Variation (%)',
        color_continuous_scale="Reds"
    )
    col_v1.plotly_chart(fig_cv, use_container_width=True)
    
    fig_std = px.bar(
        volatility_df, x='Item', y='Standard Deviation (LKR)', 
        title="Absolute Volatility (Standard Deviation)",
        color='Standard Deviation (LKR)',
        color_continuous_scale="Blues"
    )
    col_v2.plotly_chart(fig_std, use_container_width=True)
    
    with st.expander("View Volatility Data Table"):
        st.dataframe(volatility_df.set_index('Item').style.format("{:.2f}"), use_container_width=True)
else:
    st.info("Insufficient data points to compute standard deviation and volatility.")

st.divider()

# --- 5. Data Explorer Section ---
st.subheader("5. Data Explorer")
st.markdown("Examine the underlying filtered dataset. Use the columns to sort or download the data for offline processing.")

columns_to_show = ['date', 'original_week', 'item', 'unit', 'avg_price', 'min_price', 'max_price', 'price_change', 'price_change_percentage']
st.dataframe(
    df_filtered[columns_to_show], 
    use_container_width=True,
    height=300
)

csv = df_filtered[columns_to_show].to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv,
    file_name='retail_prices_filtered.csv',
    mime='text/csv',
    help="Download the current data table as a CSV file."
)

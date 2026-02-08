"""
Climate & Environment Metrics Page
Track CO2 emissions, renewable energy, and climate trends
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.generate_data import get_data
from utils.helpers import set_page_config, add_un_logo, apply_un_theme, format_number

# Page configuration
set_page_config("Climate & Environment", "🌡️")
apply_un_theme()

# Header
st.title("🌡️ Climate & Environment Metrics")
st.markdown("Monitor global climate change indicators and environmental trends")

# Sidebar
add_un_logo()

# Load data
@st.cache_data
def load_climate_data():
    climate_df = get_data('climate')
    temp_df = get_data('temperature')
    return climate_df, temp_df

climate_df, temp_df = load_climate_data()

# Filters
st.sidebar.markdown("### 🔍 Filters")

years = sorted(climate_df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

regions = ['All'] + sorted(climate_df['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Filter data
filtered_df = climate_df[climate_df['Year'] == selected_year]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

# Key Metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_co2 = filtered_df['CO2_Emissions_MT'].sum()
    st.metric("Total CO2 Emissions", f"{format_number(total_co2, 1)} MT")

with col2:
    avg_renewable = filtered_df['Renewable_Energy_Pct'].mean()
    st.metric("Avg Renewable Energy", f"{avg_renewable:.1f}%")

with col3:
    if temp_df is not None and selected_year in temp_df['Year'].values:
        temp_anomaly = temp_df[temp_df['Year'] == selected_year]['Temperature_Anomaly_C'].iloc[0]
        st.metric("Temperature Anomaly", f"+{temp_anomaly:.2f}°C")
    else:
        st.metric("Temperature Anomaly", "N/A")

with col4:
    avg_deforest = filtered_df['Deforestation_Rate'].mean()
    st.metric("Avg Deforestation Rate", f"{avg_deforest:.2f}%")

st.markdown("---")

# Global Temperature Anomaly
st.subheader("🌡️ Global Temperature Anomaly Trend")

if temp_df is not None:
    fig = px.line(
        temp_df,
        x='Year',
        y='Temperature_Anomaly_C',
        labels={'Temperature_Anomaly_C': 'Temperature Anomaly (°C)', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(color='#E74C3C', width=3))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Baseline")
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# CO2 Emissions Over Time
st.subheader("💨 Global CO2 Emissions Trend")

co2_trend = climate_df.groupby('Year')['CO2_Emissions_MT'].sum().reset_index()

fig = px.area(
    co2_trend,
    x='Year',
    y='CO2_Emissions_MT',
    labels={'CO2_Emissions_MT': 'Total CO2 Emissions (Million Tonnes)', 'Year': 'Year'},
    template='plotly_white'
)
fig.update_traces(fillcolor='rgba(231, 76, 60, 0.3)', line=dict(color='#E74C3C', width=2))
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)
st.plotly_chart(fig, use_container_width=True)

# CO2 Emissions by Country - World Map
st.subheader(f"🗺️ CO2 Emissions by Country ({selected_year})")

fig = px.choropleth(
    filtered_df,
    locations='Country',
    locationmode='country names',
    color='CO2_Emissions_MT',
    hover_name='Country',
    hover_data=['CO2_Emissions_MT', 'Renewable_Energy_Pct'],
    title=f'CO2 Emissions World Map ({selected_year})',
    color_continuous_scale='Reds',
    template='plotly_white'
)
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    ),
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# Top Emitters
st.subheader("🏭 Top CO2 Emitting Countries")

col1, col2 = st.columns([2, 1])

with col1:
    top_emitters = filtered_df.nlargest(15, 'CO2_Emissions_MT')
    
    fig = px.bar(
        top_emitters,
        x='CO2_Emissions_MT',
        y='Country',
        orientation='h',
        labels={'CO2_Emissions_MT': 'CO2 Emissions (Million Tonnes)', 'Country': 'Country'},
        template='plotly_white',
        color='CO2_Emissions_MT',
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        title='Top 15 CO2 Emitters',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Top 10 Emitters**")
    top_10_table = filtered_df.nlargest(10, 'CO2_Emissions_MT')[['Country', 'CO2_Emissions_MT']]
    top_10_table['CO2_Emissions_MT'] = top_10_table['CO2_Emissions_MT'].round(1)
    top_10_table['Rank'] = range(1, 11)
    st.dataframe(
        top_10_table[['Rank', 'Country', 'CO2_Emissions_MT']].rename(columns={'CO2_Emissions_MT': 'CO2 (MT)'}),
        hide_index=True,
        use_container_width=True
    )

# Renewable Energy Adoption
st.subheader("♻️ Renewable Energy Adoption")

col1, col2 = st.columns(2)

with col1:
    renewable_trend = climate_df.groupby('Year')['Renewable_Energy_Pct'].mean().reset_index()
    
    fig = px.line(
        renewable_trend,
        x='Year',
        y='Renewable_Energy_Pct',
        labels={'Renewable_Energy_Pct': 'Average Renewable Energy (%)', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(color='#2ECC71', width=3))
    fig.update_layout(
        title='Global Renewable Energy Trend',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    renewable_by_region = filtered_df.groupby('Region')['Renewable_Energy_Pct'].mean().reset_index()
    renewable_by_region = renewable_by_region.sort_values('Renewable_Energy_Pct', ascending=False)
    
    fig = px.bar(
        renewable_by_region,
        x='Renewable_Energy_Pct',
        y='Region',
        orientation='h',
        labels={'Renewable_Energy_Pct': 'Renewable Energy (%)', 'Region': 'Region'},
        template='plotly_white',
        color='Renewable_Energy_Pct',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        title=f'Renewable Energy by Region ({selected_year})',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Top Renewable Energy Adopters
st.subheader("🌱 Leading Countries in Renewable Energy")

top_renewable = filtered_df.nlargest(10, 'Renewable_Energy_Pct')[['Country', 'Renewable_Energy_Pct', 'CO2_Emissions_MT']]

fig = px.scatter(
    top_renewable,
    x='Renewable_Energy_Pct',
    y='CO2_Emissions_MT',
    size='CO2_Emissions_MT',
    color='Renewable_Energy_Pct',
    hover_name='Country',
    labels={
        'Renewable_Energy_Pct': 'Renewable Energy (%)',
        'CO2_Emissions_MT': 'CO2 Emissions (MT)'
    },
    template='plotly_white',
    color_continuous_scale='Greens'
)
fig.update_layout(
    title='Renewable Energy vs CO2 Emissions',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)
st.plotly_chart(fig, use_container_width=True)

# Deforestation Rates
st.subheader("🌳 Deforestation Trends")

col1, col2 = st.columns(2)

with col1:
    deforest_trend = climate_df.groupby('Year')['Deforestation_Rate'].mean().reset_index()
    
    fig = px.line(
        deforest_trend,
        x='Year',
        y='Deforestation_Rate',
        labels={'Deforestation_Rate': 'Average Deforestation Rate (%)', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(color='#E67E22', width=3))
    fig.update_layout(
        title='Global Deforestation Trend',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Countries with highest deforestation
    high_deforest = filtered_df.nlargest(10, 'Deforestation_Rate')[['Country', 'Deforestation_Rate']]
    
    fig = px.bar(
        high_deforest,
        x='Country',
        y='Deforestation_Rate',
        labels={'Deforestation_Rate': 'Deforestation Rate (%)', 'Country': 'Country'},
        template='plotly_white',
        color='Deforestation_Rate',
        color_continuous_scale='Oranges'
    )
    fig.update_layout(
        title=f'Top 10 Countries by Deforestation ({selected_year})',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Country Comparison Tool
st.subheader("📊 Country Climate Metrics Comparison")

comparison_countries = st.multiselect(
    "Select Countries for Comparison",
    options=sorted(climate_df['Country'].unique()),
    default=['United States', 'China', 'Germany', 'India']
)

if comparison_countries:
    comparison_df = climate_df[climate_df['Country'].isin(comparison_countries)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            comparison_df,
            x='Year',
            y='CO2_Emissions_MT',
            color='Country',
            labels={'CO2_Emissions_MT': 'CO2 Emissions (MT)', 'Year': 'Year'},
            template='plotly_white'
        )
        fig.update_traces(line=dict(width=2))
        fig.update_layout(
            title='CO2 Emissions Comparison',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            comparison_df,
            x='Year',
            y='Renewable_Energy_Pct',
            color='Country',
            labels={'Renewable_Energy_Pct': 'Renewable Energy (%)', 'Year': 'Year'},
            template='plotly_white'
        )
        fig.update_traces(line=dict(width=2))
        fig.update_layout(
            title='Renewable Energy Adoption Comparison',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)

# Regional Breakdown
st.subheader("🌍 Regional Climate Metrics")

regional_summary = filtered_df.groupby('Region').agg({
    'CO2_Emissions_MT': 'sum',
    'Renewable_Energy_Pct': 'mean',
    'Deforestation_Rate': 'mean'
}).reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=regional_summary['Region'],
    y=regional_summary['CO2_Emissions_MT'],
    name='Total CO2 (MT)',
    marker_color='#E74C3C'
))

fig.update_layout(
    title=f'Total CO2 Emissions by Region ({selected_year})',
    xaxis_title='Region',
    yaxis_title='CO2 Emissions (Million Tonnes)',
    template='plotly_white',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.info("💡 **Note:** Climate data is generated for demonstration purposes based on realistic environmental trends.")

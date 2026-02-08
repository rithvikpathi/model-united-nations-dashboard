"""
UN Data Analytics Dashboard - Main Landing Page
Interactive dashboard for UN data across 6 major domains
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from data.generate_data import get_data
from utils.helpers import set_page_config, add_un_logo, apply_un_theme, format_number

# Page configuration
set_page_config("UN Data Analytics Dashboard", "🌍")
apply_un_theme()

# Header
st.title("🌍 United Nations Data Analytics Dashboard")
st.markdown("""
    Welcome to the comprehensive UN Data Analytics Platform. Explore global data across six major domains:
    SDG Progress, Population, Climate, Human Development, Peacekeeping, and Health.
""")

# Sidebar
add_un_logo()
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dashboard Sections")
st.sidebar.markdown("""
- 🎯 **SDG Progress Tracking**
- 👥 **Population & Demographics**
- 🌡️ **Climate & Environment**
- 📊 **Human Development Index**
- 🕊️ **Peacekeeping Operations**
- 🏥 **Global Health Statistics**
""")

st.sidebar.markdown("---")
st.sidebar.info("Navigate to different sections using the pages in the sidebar above.")

# Load data for overview
@st.cache_data
def load_overview_data():
    sdg_df = get_data('sdg')
    pop_df = get_data('population')
    climate_df = get_data('climate')
    hdi_df = get_data('hdi')
    peace_df = get_data('peacekeeping')
    health_df = get_data('health')
    return sdg_df, pop_df, climate_df, hdi_df, peace_df, health_df

with st.spinner('Loading data...'):
    sdg_df, pop_df, climate_df, hdi_df, peace_df, health_df = load_overview_data()

# Key Metrics Overview
st.header("📈 Global Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_pop = pop_df[pop_df['Year'] == 2025]['Population'].sum()
    st.metric(
        "Global Population (2025)", 
        format_number(total_pop, 2),
        delta=None
    )

with col2:
    avg_sdg = sdg_df[sdg_df['Year'] == 2025]['Score'].mean()
    prev_avg_sdg = sdg_df[sdg_df['Year'] == 2024]['Score'].mean()
    st.metric(
        "Avg SDG Score (2025)", 
        f"{avg_sdg:.1f}/100",
        delta=f"{avg_sdg - prev_avg_sdg:.1f}"
    )

with col3:
    active_missions = len(peace_df[peace_df['Status'] == 'Active'])
    total_personnel = peace_df['Troops'].sum() + peace_df['Police'].sum()
    st.metric(
        "Active Peacekeeping Missions", 
        active_missions,
        delta=None
    )

with col4:
    avg_hdi = hdi_df[hdi_df['Year'] == 2025]['HDI'].mean()
    st.metric(
        "Global Avg HDI (2025)", 
        f"{avg_hdi:.3f}",
        delta=None
    )

st.markdown("---")

# Recent Trends
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Global Population Trend (1960-2025)")
    pop_trend = pop_df.groupby('Year')['Population'].sum().reset_index()
    pop_trend['Population_B'] = pop_trend['Population'] / 1_000_000_000
    
    fig = px.line(
        pop_trend, 
        x='Year', 
        y='Population_B',
        labels={'Population_B': 'Population (Billions)', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(color='#009EDB', width=3))
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 HDI by Region (2025)")
    hdi_2025 = hdi_df[hdi_df['Year'] == 2025]
    hdi_region = hdi_2025.groupby('Region')['HDI'].mean().reset_index()
    hdi_region = hdi_region.sort_values('HDI', ascending=False)
    
    fig = px.bar(
        hdi_region, 
        x='HDI', 
        y='Region',
        orientation='h',
        labels={'HDI': 'Average HDI', 'Region': 'Region'},
        template='plotly_white',
        color='HDI',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# SDG Progress Overview
st.subheader("🎯 SDG Progress Overview (2025)")

sdg_2025 = sdg_df[sdg_df['Year'] == 2025]
sdg_avg = sdg_2025.groupby('SDG_Goal')['Score'].mean().reset_index()
sdg_avg = sdg_avg.sort_values('Score', ascending=True)

fig = px.bar(
    sdg_avg,
    x='Score',
    y='SDG_Goal',
    orientation='h',
    labels={'Score': 'Average Score (0-100)', 'SDG_Goal': 'Sustainable Development Goal'},
    template='plotly_white',
    color='Score',
    color_continuous_scale='RdYlGn'
)
fig.update_layout(
    height=600,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Climate Data Overview
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Global CO2 Emissions Trend")
    climate_trend = climate_df.groupby('Year')['CO2_Emissions_MT'].sum().reset_index()
    
    fig = px.area(
        climate_trend,
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

with col2:
    st.subheader("🏥 Life Expectancy by Region (2025)")
    health_2025 = health_df[health_df['Year'] == 2025]
    health_region = health_2025.groupby('Region')['Life_Expectancy'].mean().reset_index()
    health_region = health_region.sort_values('Life_Expectancy', ascending=False)
    
    fig = px.bar(
        health_region,
        x='Region',
        y='Life_Expectancy',
        labels={'Life_Expectancy': 'Average Life Expectancy (Years)', 'Region': 'Region'},
        template='plotly_white',
        color='Life_Expectancy',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🌍 UN Data Analytics Dashboard | Built with Streamlit & Python</p>
        <p style='font-size: 12px;'>Data is generated for demonstration purposes</p>
    </div>
""", unsafe_allow_html=True)

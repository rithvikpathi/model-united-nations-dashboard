"""
Global Health Statistics Page
Life expectancy, disease prevalence, and healthcare metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.generate_data import get_data
from utils.helpers import set_page_config, add_un_logo, apply_un_theme, format_number

# Page configuration
set_page_config("Global Health Statistics", "🏥")
apply_un_theme()

# Header
st.title("🏥 Global Health Statistics")
st.markdown("Explore global health indicators, life expectancy, and healthcare access metrics")

# Sidebar
add_un_logo()

# Load data
@st.cache_data
def load_health_data():
    return get_data('health')

health_df = load_health_data()

# Filters
st.sidebar.markdown("### 🔍 Filters")

years = sorted(health_df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

regions = ['All'] + sorted(health_df['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Filter data
filtered_df = health_df[health_df['Year'] == selected_year]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

# Key Metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_life_exp = filtered_df['Life_Expectancy'].mean()
    st.metric("Avg Life Expectancy", f"{avg_life_exp:.1f} yrs")

with col2:
    avg_physicians = filtered_df['Physicians_Per_1000'].mean()
    st.metric("Avg Physicians/1000", f"{avg_physicians:.2f}")

with col3:
    avg_vaccination = filtered_df['Vaccination_Coverage_Pct'].mean()
    st.metric("Avg Vaccination Rate", f"{avg_vaccination:.1f}%")

with col4:
    avg_maternal_mort = filtered_df['Maternal_Mortality_Rate'].mean()
    st.metric("Avg Maternal Mortality", f"{avg_maternal_mort:.1f}")

st.markdown("---")

# Life Expectancy World Map
st.subheader(f"🗺️ Life Expectancy World Map ({selected_year})")

fig = px.choropleth(
    filtered_df,
    locations='Country',
    locationmode='country names',
    color='Life_Expectancy',
    hover_name='Country',
    hover_data=['Life_Expectancy', 'Physicians_Per_1000', 'Hospital_Beds_Per_1000'],
    title=f'Life Expectancy by Country ({selected_year})',
    color_continuous_scale='Greens',
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

# Life Expectancy Trends
st.subheader("📈 Life Expectancy Trends")

col1, col2 = st.columns(2)

with col1:
    # Global trend
    life_exp_trend = health_df.groupby('Year')['Life_Expectancy'].mean().reset_index()
    
    fig = px.line(
        life_exp_trend,
        x='Year',
        y='Life_Expectancy',
        labels={'Life_Expectancy': 'Average Life Expectancy (Years)', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(color='#2ECC71', width=3))
    fig.update_layout(
        title='Global Life Expectancy Trend',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # By region
    life_exp_region = filtered_df.groupby('Region')['Life_Expectancy'].mean().reset_index()
    life_exp_region = life_exp_region.sort_values('Life_Expectancy', ascending=False)
    
    fig = px.bar(
        life_exp_region,
        x='Life_Expectancy',
        y='Region',
        orientation='h',
        labels={'Life_Expectancy': 'Average Life Expectancy (Years)', 'Region': 'Region'},
        template='plotly_white',
        color='Life_Expectancy',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        title=f'Life Expectancy by Region ({selected_year})',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Top and Bottom Countries
st.subheader("🏆 Life Expectancy Rankings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 Countries**")
    top_10 = filtered_df.nlargest(10, 'Life_Expectancy')[['Country', 'Life_Expectancy']]
    
    fig = px.bar(
        top_10,
        x='Country',
        y='Life_Expectancy',
        labels={'Life_Expectancy': 'Life Expectancy (Years)', 'Country': 'Country'},
        template='plotly_white',
        color='Life_Expectancy',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Bottom 10 Countries**")
    bottom_10 = filtered_df.nsmallest(10, 'Life_Expectancy')[['Country', 'Life_Expectancy']]
    
    fig = px.bar(
        bottom_10,
        x='Country',
        y='Life_Expectancy',
        labels={'Life_Expectancy': 'Life Expectancy (Years)', 'Country': 'Country'},
        template='plotly_white',
        color='Life_Expectancy',
        color_continuous_scale='Reds_r'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

# Healthcare Access Metrics
st.subheader("🏥 Healthcare Access & Infrastructure")

col1, col2, col3 = st.columns(3)

with col1:
    # Physicians per 1000
    top_physicians = filtered_df.nlargest(10, 'Physicians_Per_1000')[['Country', 'Physicians_Per_1000']]
    
    fig = px.bar(
        top_physicians,
        x='Country',
        y='Physicians_Per_1000',
        labels={'Physicians_Per_1000': 'Physicians per 1000', 'Country': 'Country'},
        template='plotly_white',
        color='Physicians_Per_1000',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        title='Top 10: Physicians per 1000 People',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Hospital beds per 1000
    top_beds = filtered_df.nlargest(10, 'Hospital_Beds_Per_1000')[['Country', 'Hospital_Beds_Per_1000']]
    
    fig = px.bar(
        top_beds,
        x='Country',
        y='Hospital_Beds_Per_1000',
        labels={'Hospital_Beds_Per_1000': 'Hospital Beds per 1000', 'Country': 'Country'},
        template='plotly_white',
        color='Hospital_Beds_Per_1000',
        color_continuous_scale='Purples'
    )
    fig.update_layout(
        title='Top 10: Hospital Beds per 1000 People',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    # Vaccination coverage
    top_vaccination = filtered_df.nlargest(10, 'Vaccination_Coverage_Pct')[['Country', 'Vaccination_Coverage_Pct']]
    
    fig = px.bar(
        top_vaccination,
        x='Country',
        y='Vaccination_Coverage_Pct',
        labels={'Vaccination_Coverage_Pct': 'Vaccination Coverage (%)', 'Country': 'Country'},
        template='plotly_white',
        color='Vaccination_Coverage_Pct',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        title='Top 10: Vaccination Coverage',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

# Disease Prevalence
st.subheader("🦠 Disease Prevalence")

col1, col2 = st.columns(2)

with col1:
    # HIV prevalence trend
    hiv_trend = health_df.groupby('Year')['HIV_Prevalence_Pct'].mean().reset_index()
    
    fig = px.line(
        hiv_trend,
        x='Year',
        y='HIV_Prevalence_Pct',
        labels={'HIV_Prevalence_Pct': 'Average HIV Prevalence (%)', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(color='#E74C3C', width=3))
    fig.update_layout(
        title='Global HIV Prevalence Trend',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # HIV by region
    hiv_region = filtered_df.groupby('Region')['HIV_Prevalence_Pct'].mean().reset_index()
    hiv_region = hiv_region.sort_values('HIV_Prevalence_Pct', ascending=False)
    
    fig = px.bar(
        hiv_region,
        x='HIV_Prevalence_Pct',
        y='Region',
        orientation='h',
        labels={'HIV_Prevalence_Pct': 'HIV Prevalence (%)', 'Region': 'Region'},
        template='plotly_white',
        color='HIV_Prevalence_Pct',
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        title=f'HIV Prevalence by Region ({selected_year})',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Maternal and Infant Health
st.subheader("👶 Maternal & Infant Health")

col1, col2 = st.columns(2)

with col1:
    # Maternal mortality trend
    maternal_trend = health_df.groupby('Year')['Maternal_Mortality_Rate'].mean().reset_index()
    
    fig = px.line(
        maternal_trend,
        x='Year',
        y='Maternal_Mortality_Rate',
        labels={'Maternal_Mortality_Rate': 'Maternal Mortality Rate (per 100k)', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(color='#E67E22', width=3))
    fig.update_layout(
        title='Global Maternal Mortality Trend',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Countries with highest maternal mortality
    high_maternal = filtered_df.nlargest(10, 'Maternal_Mortality_Rate')[['Country', 'Maternal_Mortality_Rate']]
    
    fig = px.bar(
        high_maternal,
        x='Country',
        y='Maternal_Mortality_Rate',
        labels={'Maternal_Mortality_Rate': 'Maternal Mortality Rate', 'Country': 'Country'},
        template='plotly_white',
        color='Maternal_Mortality_Rate',
        color_continuous_scale='Oranges'
    )
    fig.update_layout(
        title=f'Top 10: Highest Maternal Mortality ({selected_year})',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

# Vaccination Coverage
st.subheader("💉 Vaccination Coverage Trends")

vaccination_trend = health_df.groupby('Year')['Vaccination_Coverage_Pct'].mean().reset_index()

fig = px.area(
    vaccination_trend,
    x='Year',
    y='Vaccination_Coverage_Pct',
    labels={'Vaccination_Coverage_Pct': 'Average Vaccination Coverage (%)', 'Year': 'Year'},
    template='plotly_white'
)
fig.update_traces(fillcolor='rgba(46, 204, 113, 0.3)', line=dict(color='#2ECC71', width=2))
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)
st.plotly_chart(fig, use_container_width=True)

# Country Comparison
st.subheader("📊 Country Health Comparison")

comparison_countries = st.multiselect(
    "Select Countries for Health Metrics Comparison",
    options=sorted(health_df['Country'].unique()),
    default=['United States', 'China', 'Germany', 'India']
)

if comparison_countries:
    comparison_df = health_df[health_df['Country'].isin(comparison_countries)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            comparison_df,
            x='Year',
            y='Life_Expectancy',
            color='Country',
            labels={'Life_Expectancy': 'Life Expectancy (Years)', 'Year': 'Year'},
            template='plotly_white'
        )
        fig.update_traces(line=dict(width=2))
        fig.update_layout(
            title='Life Expectancy Comparison',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            comparison_df,
            x='Year',
            y='Vaccination_Coverage_Pct',
            color='Country',
            labels={'Vaccination_Coverage_Pct': 'Vaccination Coverage (%)', 'Year': 'Year'},
            template='plotly_white'
        )
        fig.update_traces(line=dict(width=2))
        fig.update_layout(
            title='Vaccination Coverage Comparison',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)

# Healthcare Infrastructure Correlation
st.subheader("🔬 Healthcare Infrastructure vs Life Expectancy")

fig = px.scatter(
    filtered_df,
    x='Physicians_Per_1000',
    y='Life_Expectancy',
    size='Hospital_Beds_Per_1000',
    color='Region',
    hover_name='Country',
    labels={
        'Physicians_Per_1000': 'Physicians per 1000 People',
        'Life_Expectancy': 'Life Expectancy (Years)',
        'Hospital_Beds_Per_1000': 'Hospital Beds per 1000'
    },
    template='plotly_white'
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)
st.plotly_chart(fig, use_container_width=True)

# Regional Summary Table
st.subheader("🌍 Regional Health Summary")

regional_summary = filtered_df.groupby('Region').agg({
    'Life_Expectancy': 'mean',
    'Physicians_Per_1000': 'mean',
    'Hospital_Beds_Per_1000': 'mean',
    'HIV_Prevalence_Pct': 'mean',
    'Maternal_Mortality_Rate': 'mean',
    'Vaccination_Coverage_Pct': 'mean'
}).reset_index()

regional_summary = regional_summary.round(2)
regional_summary.columns = [
    'Region', 'Life Expectancy', 'Physicians/1000', 'Beds/1000',
    'HIV Prevalence %', 'Maternal Mortality', 'Vaccination %'
]

st.dataframe(
    regional_summary,
    hide_index=True,
    use_container_width=True
)

# Footer
st.markdown("---")
st.info("💡 **Note:** Health data is generated for demonstration purposes based on realistic global health statistics.")

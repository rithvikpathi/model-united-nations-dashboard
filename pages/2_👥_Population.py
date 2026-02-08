"""
Population & Demographics Page
Global population trends and demographic analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.generate_data import get_data
from utils.helpers import set_page_config, add_un_logo, apply_un_theme, format_number

# Page configuration
set_page_config("Population & Demographics", "👥")
apply_un_theme()

# Header
st.title("👥 Population & Demographics")
st.markdown("Explore global population trends, distribution, and demographic insights")

# Sidebar
add_un_logo()

# Load data
@st.cache_data
def load_population_data():
    return get_data('population')

pop_df = load_population_data()

# Filters
st.sidebar.markdown("### 🔍 Filters")

years = sorted(pop_df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

regions = ['All'] + sorted(pop_df['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Filter data
filtered_df = pop_df[pop_df['Year'] == selected_year]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

# Key Metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_pop = filtered_df['Population'].sum()
    st.metric("Total Population", format_number(total_pop, 2))

with col2:
    avg_growth = filtered_df['Growth_Rate'].mean()
    st.metric("Avg Growth Rate", f"{avg_growth:.2f}%")

with col3:
    avg_urban = filtered_df['Urban_Percentage'].mean()
    st.metric("Avg Urbanization", f"{avg_urban:.1f}%")

with col4:
    countries_count = filtered_df['Country'].nunique()
    st.metric("Countries", countries_count)

st.markdown("---")

# Global Population Trend
st.subheader("🌍 Global Population Trend (1960-2025)")

pop_trend = pop_df.groupby('Year').agg({
    'Population': 'sum',
    'Growth_Rate': 'mean'
}).reset_index()

pop_trend['Population_B'] = pop_trend['Population'] / 1_000_000_000

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=pop_trend['Year'],
    y=pop_trend['Population_B'],
    mode='lines+markers',
    name='Population',
    line=dict(color='#009EDB', width=3),
    yaxis='y1'
))

fig.add_trace(go.Scatter(
    x=pop_trend['Year'],
    y=pop_trend['Growth_Rate'],
    mode='lines',
    name='Growth Rate',
    line=dict(color='#E74C3C', width=2, dash='dash'),
    yaxis='y2'
))

fig.update_layout(
    title='Global Population and Growth Rate',
    yaxis=dict(title='Population (Billions)', side='left'),
    yaxis2=dict(title='Growth Rate (%)', side='right', overlaying='y'),
    hovermode='x unified',
    template='plotly_white',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig, use_container_width=True)

# Population by Continent/Region
st.subheader(f"📊 Population Distribution by Region ({selected_year})")

col1, col2 = st.columns(2)

with col1:
    region_pop = filtered_df.groupby('Region')['Population'].sum().reset_index()
    region_pop = region_pop.sort_values('Population', ascending=False)
    
    fig = px.pie(
        region_pop,
        names='Region',
        values='Population',
        title='Population Share by Region',
        template='plotly_white',
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        region_pop,
        x='Region',
        y='Population',
        labels={'Population': 'Population', 'Region': 'Region'},
        template='plotly_white',
        color='Population',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        title='Population by Region',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Urban vs Rural Population
st.subheader("🏙️ Urban vs Rural Population Distribution")

urban_rural_df = filtered_df.copy()
urban_rural_df['Urban_Population'] = urban_rural_df['Population'] * urban_rural_df['Urban_Percentage'] / 100
urban_rural_df['Rural_Population'] = urban_rural_df['Population'] * urban_rural_df['Rural_Percentage'] / 100

col1, col2 = st.columns(2)

with col1:
    total_urban = urban_rural_df['Urban_Population'].sum()
    total_rural = urban_rural_df['Rural_Population'].sum()
    
    urban_rural_summary = pd.DataFrame({
        'Type': ['Urban', 'Rural'],
        'Population': [total_urban, total_rural]
    })
    
    fig = px.pie(
        urban_rural_summary,
        names='Type',
        values='Population',
        title='Global Urban vs Rural Split',
        template='plotly_white',
        color='Type',
        color_discrete_map={'Urban': '#3498DB', 'Rural': '#2ECC71'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    region_urban = urban_rural_df.groupby('Region')['Urban_Percentage'].mean().reset_index()
    region_urban = region_urban.sort_values('Urban_Percentage', ascending=False)
    
    fig = px.bar(
        region_urban,
        x='Urban_Percentage',
        y='Region',
        orientation='h',
        labels={'Urban_Percentage': 'Urbanization Rate (%)', 'Region': 'Region'},
        template='plotly_white',
        color='Urban_Percentage',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        title='Urbanization Rate by Region',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Age Distribution Pyramid (Simulated)
st.subheader("👶👴 Population Age Distribution Pyramid")

# Generate simulated age distribution
age_groups = ['0-14', '15-24', '25-54', '55-64', '65+']
male_percentages = [18, 13, 38, 12, 10]  # Simulated percentages
female_percentages = [17, 12, 37, 13, 11]  # Simulated percentages

# Calculate actual populations
total_pop_selected = filtered_df['Population'].sum()
male_values = [total_pop_selected * 0.5 * p / 100 for p in male_percentages]
female_values = [total_pop_selected * 0.5 * p / 100 for p in female_percentages]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=age_groups,
    x=[-val for val in male_values],
    name='Male',
    orientation='h',
    marker=dict(color='#009EDB')
))

fig.add_trace(go.Bar(
    y=age_groups,
    x=female_values,
    name='Female',
    orientation='h',
    marker=dict(color='#E03C31')
))

fig.update_layout(
    title=f'Population Pyramid ({selected_year})',
    barmode='relative',
    bargap=0.1,
    xaxis=dict(title='Population'),
    yaxis=dict(title='Age Group'),
    template='plotly_white',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig, use_container_width=True)

# Top Populated Countries
st.subheader("🏆 Most Populated Countries")

col1, col2 = st.columns([2, 1])

with col1:
    top_countries = filtered_df.nlargest(15, 'Population')[['Country', 'Population', 'Growth_Rate', 'Urban_Percentage']]
    
    fig = px.bar(
        top_countries,
        x='Population',
        y='Country',
        orientation='h',
        labels={'Population': 'Population', 'Country': 'Country'},
        template='plotly_white',
        color='Population',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        title='Top 15 Countries by Population',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Top 10 by Population**")
    top_10_table = filtered_df.nlargest(10, 'Population')[['Country', 'Population']]
    top_10_table['Population'] = top_10_table['Population'].apply(lambda x: format_number(x, 1))
    top_10_table['Rank'] = range(1, 11)
    st.dataframe(
        top_10_table[['Rank', 'Country', 'Population']],
        hide_index=True,
        use_container_width=True
    )

# Population Growth Comparison
st.subheader("📈 Population Growth Rate Comparison")

# Select countries for comparison
comparison_countries = st.multiselect(
    "Select Countries for Growth Comparison",
    options=sorted(pop_df['Country'].unique()),
    default=['China', 'India', 'United States', 'Nigeria']
)

if comparison_countries:
    comparison_df = pop_df[pop_df['Country'].isin(comparison_countries)]
    
    fig = px.line(
        comparison_df,
        x='Year',
        y='Population',
        color='Country',
        labels={'Population': 'Population', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        title='Population Trend Comparison',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Urbanization Trends
st.subheader("🏙️ Urbanization Trends Over Time")

urbanization_trend = pop_df.groupby('Year')['Urban_Percentage'].mean().reset_index()

fig = px.area(
    urbanization_trend,
    x='Year',
    y='Urban_Percentage',
    labels={'Urban_Percentage': 'Average Urbanization Rate (%)', 'Year': 'Year'},
    template='plotly_white'
)
fig.update_traces(fillcolor='rgba(52, 152, 219, 0.3)', line=dict(color='#3498DB', width=2))
fig.update_layout(
    title='Global Urbanization Trend',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.info("💡 **Note:** Data is generated for demonstration purposes based on realistic population trends.")

"""
Human Development Index (HDI) Page
Track HDI rankings, trends, and component analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.generate_data import get_data
from utils.helpers import set_page_config, add_un_logo, apply_un_theme, format_number

# Page configuration
set_page_config("Human Development Index", "📊")
apply_un_theme()

# Header
st.title("📊 Human Development Index (HDI)")
st.markdown("Explore HDI rankings, trends, and component breakdowns across countries")

# Sidebar
add_un_logo()

# Load data
@st.cache_data
def load_hdi_data():
    return get_data('hdi')

hdi_df = load_hdi_data()

# Filters
st.sidebar.markdown("### 🔍 Filters")

years = sorted(hdi_df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

regions = ['All'] + sorted(hdi_df['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

# HDI Categories
hdi_categories = st.sidebar.radio(
    "HDI Category",
    ["All", "Very High (≥0.800)", "High (0.700-0.799)", "Medium (0.550-0.699)", "Low (<0.550)"]
)

# Filter data
filtered_df = hdi_df[hdi_df['Year'] == selected_year]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if hdi_categories != "All":
    if hdi_categories == "Very High (≥0.800)":
        filtered_df = filtered_df[filtered_df['HDI'] >= 0.800]
    elif hdi_categories == "High (0.700-0.799)":
        filtered_df = filtered_df[(filtered_df['HDI'] >= 0.700) & (filtered_df['HDI'] < 0.800)]
    elif hdi_categories == "Medium (0.550-0.699)":
        filtered_df = filtered_df[(filtered_df['HDI'] >= 0.550) & (filtered_df['HDI'] < 0.700)]
    else:  # Low
        filtered_df = filtered_df[filtered_df['HDI'] < 0.550]

# Key Metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_hdi = filtered_df['HDI'].mean()
    st.metric("Average HDI", f"{avg_hdi:.3f}")

with col2:
    avg_life_exp = filtered_df['Life_Expectancy'].mean()
    st.metric("Avg Life Expectancy", f"{avg_life_exp:.1f} yrs")

with col3:
    avg_edu = filtered_df['Expected_Education_Years'].mean()
    st.metric("Avg Education Years", f"{avg_edu:.1f} yrs")

with col4:
    avg_gni = filtered_df['GNI_Per_Capita'].mean()
    st.metric("Avg GNI per Capita", f"${format_number(avg_gni, 1)}")

st.markdown("---")

# HDI World Map
st.subheader(f"🗺️ HDI World Map ({selected_year})")

fig = px.choropleth(
    filtered_df,
    locations='Country',
    locationmode='country names',
    color='HDI',
    hover_name='Country',
    hover_data=['HDI', 'Life_Expectancy', 'Expected_Education_Years', 'GNI_Per_Capita'],
    title=f'Human Development Index by Country ({selected_year})',
    color_continuous_scale='RdYlGn',
    range_color=[0, 1],
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

# HDI Rankings Table
st.subheader(f"🏆 HDI Rankings ({selected_year})")

# Add search functionality
search_term = st.text_input("🔍 Search for a country:", "")

rankings_df = filtered_df.copy()
rankings_df = rankings_df.sort_values('HDI', ascending=False)
rankings_df['Rank'] = range(1, len(rankings_df) + 1)

if search_term:
    rankings_df = rankings_df[rankings_df['Country'].str.contains(search_term, case=False)]

# Display table
st.dataframe(
    rankings_df[['Rank', 'Country', 'HDI', 'Life_Expectancy', 'Expected_Education_Years', 'GNI_Per_Capita']].rename(
        columns={
            'Life_Expectancy': 'Life Exp. (yrs)',
            'Expected_Education_Years': 'Education (yrs)',
            'GNI_Per_Capita': 'GNI per Capita ($)'
        }
    ),
    hide_index=True,
    use_container_width=True,
    height=400
)

st.markdown("---")

# Top and Bottom Performers
col1, col2 = st.columns(2)

with col1:
    st.subheader("🥇 Top 10 Countries")
    top_10 = hdi_df[hdi_df['Year'] == selected_year].nlargest(10, 'HDI')
    
    fig = px.bar(
        top_10,
        x='HDI',
        y='Country',
        orientation='h',
        labels={'HDI': 'HDI Score', 'Country': 'Country'},
        template='plotly_white',
        color='HDI',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📉 Bottom 10 Countries")
    bottom_10 = hdi_df[hdi_df['Year'] == selected_year].nsmallest(10, 'HDI')
    
    fig = px.bar(
        bottom_10,
        x='HDI',
        y='Country',
        orientation='h',
        labels={'HDI': 'HDI Score', 'Country': 'Country'},
        template='plotly_white',
        color='HDI',
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# HDI by Region
st.subheader("🌍 HDI by Region")

regional_hdi = hdi_df[hdi_df['Year'] == selected_year].groupby('Region')['HDI'].mean().reset_index()
regional_hdi = regional_hdi.sort_values('HDI', ascending=False)

fig = px.bar(
    regional_hdi,
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

# HDI Components Breakdown
st.subheader("🔍 HDI Components Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    top_life_exp = filtered_df.nlargest(10, 'Life_Expectancy')[['Country', 'Life_Expectancy']]
    
    fig = px.bar(
        top_life_exp,
        x='Country',
        y='Life_Expectancy',
        labels={'Life_Expectancy': 'Life Expectancy (years)', 'Country': 'Country'},
        template='plotly_white',
        color='Life_Expectancy',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        title='Top 10: Life Expectancy',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    top_edu = filtered_df.nlargest(10, 'Expected_Education_Years')[['Country', 'Expected_Education_Years']]
    
    fig = px.bar(
        top_edu,
        x='Country',
        y='Expected_Education_Years',
        labels={'Expected_Education_Years': 'Education Years', 'Country': 'Country'},
        template='plotly_white',
        color='Expected_Education_Years',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        title='Top 10: Education Years',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    top_gni = filtered_df.nlargest(10, 'GNI_Per_Capita')[['Country', 'GNI_Per_Capita']]
    
    fig = px.bar(
        top_gni,
        x='Country',
        y='GNI_Per_Capita',
        labels={'GNI_Per_Capita': 'GNI per Capita ($)', 'Country': 'Country'},
        template='plotly_white',
        color='GNI_Per_Capita',
        color_continuous_scale='Purples'
    )
    fig.update_layout(
        title='Top 10: GNI per Capita',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    st.plotly_chart(fig, use_container_width=True)

# HDI Trends Over Time
st.subheader("📈 HDI Trends Over Time")

# Country selection for trend analysis
trend_countries = st.multiselect(
    "Select Countries for Trend Comparison",
    options=sorted(hdi_df['Country'].unique()),
    default=['Norway', 'United States', 'China', 'India']
)

if trend_countries:
    trend_df = hdi_df[hdi_df['Country'].isin(trend_countries)]
    
    fig = px.line(
        trend_df,
        x='Year',
        y='HDI',
        color='Country',
        labels={'HDI': 'HDI Score', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        title='HDI Trend Comparison',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Scatter Plot: HDI Components Relationship
st.subheader("🔬 HDI Components Relationship")

col1, col2 = st.columns(2)

with col1:
    fig = px.scatter(
        filtered_df,
        x='Life_Expectancy',
        y='HDI',
        size='GNI_Per_Capita',
        color='Region',
        hover_name='Country',
        labels={'Life_Expectancy': 'Life Expectancy (years)', 'HDI': 'HDI Score'},
        template='plotly_white'
    )
    fig.update_layout(
        title='Life Expectancy vs HDI',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(
        filtered_df,
        x='Expected_Education_Years',
        y='HDI',
        size='GNI_Per_Capita',
        color='Region',
        hover_name='Country',
        labels={'Expected_Education_Years': 'Education Years', 'HDI': 'HDI Score'},
        template='plotly_white'
    )
    fig.update_layout(
        title='Education vs HDI',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Country Comparison Tool
st.subheader("⚖️ Country Comparison Tool")

col1, col2 = st.columns(2)

with col1:
    country_1 = st.selectbox("Select First Country", sorted(hdi_df['Country'].unique()), index=0)

with col2:
    country_2 = st.selectbox("Select Second Country", sorted(hdi_df['Country'].unique()), index=1)

if country_1 and country_2:
    comp_df = hdi_df[hdi_df['Country'].isin([country_1, country_2]) & (hdi_df['Year'] == selected_year)]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        c1_hdi = comp_df[comp_df['Country'] == country_1]['HDI'].iloc[0]
        c2_hdi = comp_df[comp_df['Country'] == country_2]['HDI'].iloc[0]
        st.metric(f"{country_1} - HDI", f"{c1_hdi:.3f}")
        st.metric(f"{country_2} - HDI", f"{c2_hdi:.3f}")
    
    with col2:
        c1_life = comp_df[comp_df['Country'] == country_1]['Life_Expectancy'].iloc[0]
        c2_life = comp_df[comp_df['Country'] == country_2]['Life_Expectancy'].iloc[0]
        st.metric(f"{country_1} - Life Exp.", f"{c1_life:.1f} yrs")
        st.metric(f"{country_2} - Life Exp.", f"{c2_life:.1f} yrs")
    
    with col3:
        c1_edu = comp_df[comp_df['Country'] == country_1]['Expected_Education_Years'].iloc[0]
        c2_edu = comp_df[comp_df['Country'] == country_2]['Expected_Education_Years'].iloc[0]
        st.metric(f"{country_1} - Education", f"{c1_edu:.1f} yrs")
        st.metric(f"{country_2} - Education", f"{c2_edu:.1f} yrs")
    
    with col4:
        c1_gni = comp_df[comp_df['Country'] == country_1]['GNI_Per_Capita'].iloc[0]
        c2_gni = comp_df[comp_df['Country'] == country_2]['GNI_Per_Capita'].iloc[0]
        st.metric(f"{country_1} - GNI", f"${format_number(c1_gni, 1)}")
        st.metric(f"{country_2} - GNI", f"${format_number(c2_gni, 1)}")
    
    # Comparison chart
    comp_full = hdi_df[hdi_df['Country'].isin([country_1, country_2])]
    
    fig = px.line(
        comp_full,
        x='Year',
        y='HDI',
        color='Country',
        labels={'HDI': 'HDI Score', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        title=f'HDI Comparison: {country_1} vs {country_2}',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.info("💡 **Note:** HDI data is generated for demonstration purposes. HDI ranges from 0 to 1, with higher values indicating better human development.")

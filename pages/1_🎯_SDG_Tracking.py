"""
SDG Progress Tracking Page
Track progress across all 17 Sustainable Development Goals
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.generate_data import get_data
from utils.helpers import set_page_config, add_un_logo, apply_un_theme
from utils.charts import create_radar_chart

# Page configuration
set_page_config("SDG Progress Tracking", "🎯")
apply_un_theme()

# Header
st.title("🎯 Sustainable Development Goals (SDG) Progress Tracking")
st.markdown("Track progress across all 17 SDGs with global and regional insights")

# Sidebar
add_un_logo()

# Load data
@st.cache_data
def load_sdg_data():
    return get_data('sdg')

sdg_df = load_sdg_data()

# Filters
st.sidebar.markdown("### 🔍 Filters")

years = sorted(sdg_df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

regions = ['All'] + sorted(sdg_df['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

sdg_goals = sorted(sdg_df['SDG_Number'].unique())
selected_sdgs = st.sidebar.multiselect(
    "Select SDG Goals", 
    sdg_goals, 
    default=sdg_goals[:5]
)

# Filter data
filtered_df = sdg_df[sdg_df['Year'] == selected_year]

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

# Key Metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_score = filtered_df['Score'].mean()
    st.metric("Average SDG Score", f"{avg_score:.1f}/100")

with col2:
    highest_score = filtered_df.groupby('SDG_Goal')['Score'].mean().max()
    st.metric("Highest Goal Score", f"{highest_score:.1f}")

with col3:
    lowest_score = filtered_df.groupby('SDG_Goal')['Score'].mean().min()
    st.metric("Lowest Goal Score", f"{lowest_score:.1f}")

with col4:
    countries_count = filtered_df['Country'].nunique()
    st.metric("Countries Tracked", countries_count)

st.markdown("---")

# SDG Overview - All 17 Goals
st.subheader(f"📈 SDG Progress Overview ({selected_year})")

sdg_summary = filtered_df.groupby(['SDG_Number', 'SDG_Goal'])['Score'].mean().reset_index()
sdg_summary = sdg_summary.sort_values('SDG_Number')

fig = px.bar(
    sdg_summary,
    x='SDG_Number',
    y='Score',
    color='Score',
    color_continuous_scale='RdYlGn',
    labels={'Score': 'Average Score', 'SDG_Number': 'SDG Goal Number'},
    hover_data=['SDG_Goal'],
    template='plotly_white'
)
fig.update_layout(
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(tickmode='linear', tick0=1, dtick=1)
)
st.plotly_chart(fig, use_container_width=True)

# Radar Chart for Selected SDGs
if selected_sdgs:
    st.subheader("🕸️ SDG Radar Chart")
    
    radar_df = filtered_df[filtered_df['SDG_Number'].isin(selected_sdgs)]
    radar_summary = radar_df.groupby('SDG_Goal')['Score'].mean().reset_index()
    
    fig = create_radar_chart(
        categories=radar_summary['SDG_Goal'].tolist(),
        values=radar_summary['Score'].tolist(),
        title=f"Selected SDG Goals Performance ({selected_year})"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Regional Comparison
st.subheader("🌍 Regional SDG Performance")

regional_df = sdg_df[sdg_df['Year'] == selected_year]
regional_summary = regional_df.groupby('Region')['Score'].mean().reset_index()
regional_summary = regional_summary.sort_values('Score', ascending=False)

fig = px.bar(
    regional_summary,
    x='Score',
    y='Region',
    orientation='h',
    labels={'Score': 'Average SDG Score', 'Region': 'Region'},
    template='plotly_white',
    color='Score',
    color_continuous_scale='Blues'
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# Heatmap - Countries vs SDG Goals
st.subheader("🔥 SDG Heatmap by Country")

# Select top 15 countries by average score for better visualization
country_avg = filtered_df.groupby('Country')['Score'].mean().reset_index()
top_countries = country_avg.nlargest(15, 'Score')['Country'].tolist()

heatmap_df = filtered_df[filtered_df['Country'].isin(top_countries)]
heatmap_pivot = heatmap_df.pivot_table(
    values='Score', 
    index='Country', 
    columns='SDG_Number', 
    aggfunc='mean'
)

fig = px.imshow(
    heatmap_pivot,
    labels=dict(x="SDG Goal Number", y="Country", color="Score"),
    x=[f"SDG {i}" for i in heatmap_pivot.columns],
    y=heatmap_pivot.index,
    color_continuous_scale='RdYlGn',
    aspect='auto',
    template='plotly_white'
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Trend Analysis
st.subheader("📊 SDG Progress Over Time")

col1, col2 = st.columns(2)

with col1:
    # Select a specific SDG for trend
    trend_sdg = st.selectbox(
        "Select SDG for Trend Analysis",
        options=sorted(sdg_df['SDG_Number'].unique()),
        format_func=lambda x: f"SDG {x}: {sdg_df[sdg_df['SDG_Number']==x]['SDG_Goal'].iloc[0]}"
    )

with col2:
    # Select countries for comparison
    trend_countries = st.multiselect(
        "Select Countries",
        options=sorted(sdg_df['Country'].unique()),
        default=['United States', 'China', 'Germany', 'India']
    )

if trend_countries:
    trend_df = sdg_df[
        (sdg_df['SDG_Number'] == trend_sdg) & 
        (sdg_df['Country'].isin(trend_countries))
    ]
    
    fig = px.line(
        trend_df,
        x='Year',
        y='Score',
        color='Country',
        labels={'Score': 'SDG Score', 'Year': 'Year'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Country Rankings
st.subheader("🏆 Top Performing Countries")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 Countries**")
    top_10 = filtered_df.groupby('Country')['Score'].mean().reset_index()
    top_10 = top_10.sort_values('Score', ascending=False).head(10)
    top_10['Rank'] = range(1, 11)
    top_10['Score'] = top_10['Score'].round(2)
    st.dataframe(
        top_10[['Rank', 'Country', 'Score']],
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.markdown("**Bottom 10 Countries**")
    bottom_10 = filtered_df.groupby('Country')['Score'].mean().reset_index()
    bottom_10 = bottom_10.sort_values('Score', ascending=True).head(10)
    bottom_10['Rank'] = range(1, 11)
    bottom_10['Score'] = bottom_10['Score'].round(2)
    st.dataframe(
        bottom_10[['Rank', 'Country', 'Score']],
        hide_index=True,
        use_container_width=True
    )

# Footer
st.markdown("---")
st.info("💡 **Note:** Data is generated for demonstration purposes. SDG scores represent progress on a 0-100 scale.")

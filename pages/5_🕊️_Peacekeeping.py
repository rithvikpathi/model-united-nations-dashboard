"""
UN Peacekeeping Operations Page
Overview of active peacekeeping missions and deployments
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from data.generate_data import get_data
from utils.helpers import set_page_config, add_un_logo, apply_un_theme, format_number

# Page configuration
set_page_config("Peacekeeping Operations", "🕊️")
apply_un_theme()

# Header
st.title("🕊️ UN Peacekeeping Operations")
st.markdown("Monitor active UN peacekeeping missions, deployments, and budgets worldwide")

# Sidebar
add_un_logo()

# Load data
@st.cache_data
def load_peacekeeping_data():
    return get_data('peacekeeping')

peace_df = load_peacekeeping_data()

# Filters
st.sidebar.markdown("### 🔍 Filters")

status_filter = st.sidebar.selectbox("Mission Status", ['All', 'Active', 'Completed'])
region_filter = st.sidebar.multiselect(
    "Select Regions",
    options=sorted(peace_df['Region'].unique()),
    default=sorted(peace_df['Region'].unique())
)

# Filter data
filtered_df = peace_df.copy()

if status_filter != 'All':
    filtered_df = filtered_df[filtered_df['Status'] == status_filter]

if region_filter:
    filtered_df = filtered_df[filtered_df['Region'].isin(region_filter)]

# Key Metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    active_missions = len(filtered_df[filtered_df['Status'] == 'Active'])
    st.metric("Active Missions", active_missions)

with col2:
    total_troops = filtered_df['Troops'].sum()
    st.metric("Total Troops", format_number(total_troops, 1))

with col3:
    total_personnel = filtered_df['Troops'].sum() + filtered_df['Police'].sum() + filtered_df['Civilians'].sum()
    st.metric("Total Personnel", format_number(total_personnel, 1))

with col4:
    total_budget = filtered_df['Budget_M'].sum()
    st.metric("Total Budget", f"${format_number(total_budget, 1)}M")

st.markdown("---")

# Mission Overview Map
st.subheader("🗺️ Peacekeeping Mission Locations")

# Create a simplified map showing mission locations
# For demonstration, we'll use scatter geo plot
location_coords = {
    'Mali': {'lat': 17.5707, 'lon': -3.9962},
    'DR Congo': {'lat': -4.0383, 'lon': 21.7587},
    'South Sudan': {'lat': 6.8770, 'lon': 31.3070},
    'Lebanon': {'lat': 33.8547, 'lon': 35.8623},
    'Cyprus': {'lat': 35.1264, 'lon': 33.4299},
    'Golan Heights': {'lat': 32.8737, 'lon': 35.8329},
    'Western Sahara': {'lat': 24.2155, 'lon': -12.8858},
    'Kosovo': {'lat': 42.6026, 'lon': 20.9030},
    'Abyei': {'lat': 9.6000, 'lon': 28.4000},
    'Central African Republic': {'lat': 6.6111, 'lon': 20.9394}
}

map_df = filtered_df.copy()
map_df['Latitude'] = map_df['Location'].map(lambda x: location_coords.get(x, {}).get('lat', 0))
map_df['Longitude'] = map_df['Location'].map(lambda x: location_coords.get(x, {}).get('lon', 0))
map_df['Total_Personnel'] = map_df['Troops'] + map_df['Police'] + map_df['Civilians']

fig = px.scatter_geo(
    map_df,
    lat='Latitude',
    lon='Longitude',
    size='Total_Personnel',
    color='Region',
    hover_name='Name',
    hover_data=['Location', 'Troops', 'Police', 'Civilians', 'Budget_M'],
    title='UN Peacekeeping Missions Worldwide',
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

# Mission Details Table
st.subheader("📋 Mission Details")

mission_table = filtered_df.copy()
mission_table['Total_Personnel'] = mission_table['Troops'] + mission_table['Police'] + mission_table['Civilians']

st.dataframe(
    mission_table[['Name', 'Location', 'Region', 'Start', 'Status', 'Total_Personnel', 'Budget_M']].rename(
        columns={
            'Total_Personnel': 'Personnel',
            'Budget_M': 'Budget ($M)'
        }
    ),
    hide_index=True,
    use_container_width=True,
    height=400
)

st.markdown("---")

# Personnel Deployment
st.subheader("👥 Personnel Deployment Statistics")

col1, col2 = st.columns(2)

with col1:
    # Personnel breakdown
    personnel_breakdown = pd.DataFrame({
        'Category': ['Troops', 'Police', 'Civilians'],
        'Count': [
            filtered_df['Troops'].sum(),
            filtered_df['Police'].sum(),
            filtered_df['Civilians'].sum()
        ]
    })
    
    fig = px.pie(
        personnel_breakdown,
        names='Category',
        values='Count',
        title='Personnel Distribution',
        template='plotly_white',
        color='Category',
        color_discrete_map={'Troops': '#009EDB', 'Police': '#2ECC71', 'Civilians': '#E67E22'}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Personnel by mission
    mission_personnel = filtered_df.copy()
    mission_personnel['Total_Personnel'] = mission_personnel['Troops'] + mission_personnel['Police'] + mission_personnel['Civilians']
    mission_personnel = mission_personnel.sort_values('Total_Personnel', ascending=False)
    
    fig = px.bar(
        mission_personnel,
        x='Total_Personnel',
        y='Name',
        orientation='h',
        labels={'Total_Personnel': 'Total Personnel', 'Name': 'Mission'},
        template='plotly_white',
        color='Total_Personnel',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        title='Personnel by Mission',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Detailed Personnel Breakdown by Mission
st.subheader("📊 Detailed Personnel Breakdown")

personnel_detail = filtered_df[['Name', 'Troops', 'Police', 'Civilians']].melt(
    id_vars=['Name'],
    var_name='Type',
    value_name='Count'
)

fig = px.bar(
    personnel_detail,
    x='Name',
    y='Count',
    color='Type',
    barmode='stack',
    labels={'Count': 'Number of Personnel', 'Name': 'Mission'},
    template='plotly_white',
    color_discrete_map={'Troops': '#009EDB', 'Police': '#2ECC71', 'Civilians': '#E67E22'}
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis={'tickangle': -45}
)
st.plotly_chart(fig, use_container_width=True)

# Budget Allocation
st.subheader("💰 Budget Allocation by Mission")

col1, col2 = st.columns(2)

with col1:
    budget_sorted = filtered_df.sort_values('Budget_M', ascending=False)
    
    fig = px.bar(
        budget_sorted,
        x='Budget_M',
        y='Name',
        orientation='h',
        labels={'Budget_M': 'Budget (Million USD)', 'Name': 'Mission'},
        template='plotly_white',
        color='Budget_M',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        title='Mission Budgets',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Budget by region
    region_budget = filtered_df.groupby('Region')['Budget_M'].sum().reset_index()
    region_budget = region_budget.sort_values('Budget_M', ascending=False)
    
    fig = px.pie(
        region_budget,
        names='Region',
        values='Budget_M',
        title='Budget Distribution by Region',
        template='plotly_white'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

# Mission Timeline
st.subheader("📅 Mission Timeline")

timeline_df = filtered_df.copy()
timeline_df['Start_Date'] = pd.to_datetime(timeline_df['Start'])
timeline_df['Duration_Years'] = (datetime.now() - timeline_df['Start_Date']).dt.days / 365.25

# Sort by start date
timeline_df = timeline_df.sort_values('Start_Date')

fig = px.bar(
    timeline_df,
    x='Duration_Years',
    y='Name',
    orientation='h',
    labels={'Duration_Years': 'Duration (Years)', 'Name': 'Mission'},
    hover_data=['Start', 'Location'],
    template='plotly_white',
    color='Duration_Years',
    color_continuous_scale='Viridis'
)
fig.update_layout(
    title='Mission Duration (Years)',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# Regional Statistics
st.subheader("🌍 Statistics by Region")

regional_stats = filtered_df.groupby('Region').agg({
    'Name': 'count',
    'Troops': 'sum',
    'Police': 'sum',
    'Civilians': 'sum',
    'Budget_M': 'sum'
}).reset_index()

regional_stats.columns = ['Region', 'Missions', 'Troops', 'Police', 'Civilians', 'Budget ($M)']
regional_stats['Total Personnel'] = regional_stats['Troops'] + regional_stats['Police'] + regional_stats['Civilians']

st.dataframe(
    regional_stats,
    hide_index=True,
    use_container_width=True
)

# Mission Details Expandable Sections
st.subheader("🔍 Detailed Mission Information")

for idx, mission in filtered_df.iterrows():
    with st.expander(f"🕊️ {mission['Name']} - {mission['Location']}"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Mission Details**")
            st.write(f"**Location:** {mission['Location']}")
            st.write(f"**Region:** {mission['Region']}")
            st.write(f"**Start Date:** {mission['Start']}")
            st.write(f"**Status:** {mission['Status']}")
        
        with col2:
            st.markdown("**Personnel Deployment**")
            st.write(f"**Troops:** {mission['Troops']:,}")
            st.write(f"**Police:** {mission['Police']:,}")
            st.write(f"**Civilians:** {mission['Civilians']:,}")
            total_pers = mission['Troops'] + mission['Police'] + mission['Civilians']
            st.write(f"**Total:** {total_pers:,}")
        
        with col3:
            st.markdown("**Budget**")
            st.write(f"**Annual Budget:** ${mission['Budget_M']:.1f}M")
            if total_pers > 0:
                cost_per_person = (mission['Budget_M'] * 1000000) / total_pers
                st.write(f"**Cost per Person:** ${cost_per_person:,.0f}")

# Comparison Chart
st.subheader("⚖️ Mission Comparison")

col1, col2 = st.columns(2)

with col1:
    selected_missions = st.multiselect(
        "Select Missions to Compare",
        options=filtered_df['Name'].tolist(),
        default=filtered_df['Name'].head(3).tolist()
    )

if selected_missions:
    comparison_df = filtered_df[filtered_df['Name'].isin(selected_missions)]
    
    # Create comparison metrics
    metrics = ['Troops', 'Police', 'Civilians', 'Budget_M']
    
    fig = go.Figure()
    
    for metric in metrics:
        fig.add_trace(go.Bar(
            name=metric.replace('_', ' '),
            x=comparison_df['Name'],
            y=comparison_df[metric]
        ))
    
    fig.update_layout(
        title='Mission Comparison',
        barmode='group',
        xaxis_title='Mission',
        yaxis_title='Count / Budget ($M)',
        template='plotly_white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.info("💡 **Note:** Peacekeeping data is generated for demonstration purposes based on realistic UN mission profiles.")

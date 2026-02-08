"""
Reusable chart functions for the UN Dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_line_chart(df, x, y, color=None, title="", labels=None):
    """Create an interactive line chart"""
    fig = px.line(
        df, x=x, y=y, color=color,
        title=title,
        labels=labels or {},
        template='plotly_white'
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def create_bar_chart(df, x, y, color=None, title="", orientation='v', labels=None):
    """Create an interactive bar chart"""
    fig = px.bar(
        df, x=x, y=y, color=color,
        title=title,
        orientation=orientation,
        labels=labels or {},
        template='plotly_white'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def create_pie_chart(df, names, values, title=""):
    """Create an interactive pie chart"""
    fig = px.pie(
        df, names=names, values=values,
        title=title,
        template='plotly_white'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def create_choropleth_map(df, locations, z, title="", color_scale='Blues'):
    """Create a choropleth world map"""
    fig = px.choropleth(
        df,
        locations=locations,
        locationmode='country names',
        color=z,
        title=title,
        color_continuous_scale=color_scale,
        template='plotly_white'
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    return fig


def create_heatmap(df, x, y, z, title="", color_scale='RdYlGn'):
    """Create a heatmap"""
    fig = px.density_heatmap(
        df, x=x, y=y, z=z,
        title=title,
        color_continuous_scale=color_scale,
        template='plotly_white'
    )
    return fig


def create_scatter(df, x, y, color=None, size=None, title="", labels=None):
    """Create a scatter plot"""
    fig = px.scatter(
        df, x=x, y=y, color=color, size=size,
        title=title,
        labels=labels or {},
        template='plotly_white'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def create_radar_chart(categories, values, title=""):
    """Create a radar chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title=title
    )
    
    return fig


def create_population_pyramid(df, age_groups, male_values, female_values, title=""):
    """Create a population pyramid"""
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
        title=title,
        barmode='relative',
        bargap=0.1,
        xaxis=dict(title='Population'),
        yaxis=dict(title='Age Group'),
        template='plotly_white'
    )
    
    return fig


def create_metric_card_html(value, label, delta=None, delta_color="normal"):
    """Create HTML for a metric card"""
    delta_html = ""
    if delta is not None:
        color = "green" if delta_color == "normal" and delta > 0 else "red" if delta < 0 else "gray"
        arrow = "▲" if delta > 0 else "▼" if delta < 0 else "●"
        delta_html = f'<div style="color: {color}; font-size: 14px;">{arrow} {abs(delta):.1f}%</div>'
    
    return f"""
    <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; text-align: center; color: white;">
        <div style="font-size: 32px; font-weight: bold;">{value}</div>
        <div style="font-size: 14px; margin-top: 5px;">{label}</div>
        {delta_html}
    </div>
    """

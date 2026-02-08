"""
Utility helper functions for the UN Dashboard
"""

import streamlit as st


def set_page_config(page_title, page_icon="🌍"):
    """Set standard page configuration"""
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )


def add_un_logo():
    """Add UN branding to sidebar"""
    st.sidebar.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #009EDB;'>🌍 UN Dashboard</h1>
            <p style='color: #666;'>Data Analytics Platform</p>
        </div>
    """, unsafe_allow_html=True)


def format_number(num, precision=0):
    """Format large numbers with commas and suffixes"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.{precision}f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.{precision}f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.{precision}f}K"
    else:
        return f"{num:.{precision}f}"


def show_metric_cards(metrics):
    """Display metric cards in columns"""
    cols = st.columns(len(metrics))
    for col, (label, value, delta) in zip(cols, metrics):
        with col:
            if delta is not None:
                st.metric(label=label, value=value, delta=f"{delta:+.1f}%")
            else:
                st.metric(label=label, value=value)


def create_info_box(title, content, type="info"):
    """Create an informational box"""
    colors = {
        "info": "#D1ECF1",
        "success": "#D4EDDA",
        "warning": "#FFF3CD",
        "danger": "#F8D7DA"
    }
    
    st.markdown(f"""
        <div style='padding: 15px; background-color: {colors.get(type, colors["info"])}; 
                    border-radius: 5px; margin: 10px 0;'>
            <h4 style='margin: 0 0 10px 0;'>{title}</h4>
            <p style='margin: 0;'>{content}</p>
        </div>
    """, unsafe_allow_html=True)


def apply_un_theme():
    """Apply UN color theme styling"""
    st.markdown("""
        <style>
        .main {
            background-color: #F8F9FA;
        }
        .stButton>button {
            background-color: #009EDB;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #0077B6;
        }
        div[data-testid="metric-container"] {
            background-color: white;
            border: 1px solid #E0E0E0;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #009EDB;
        }
        </style>
    """, unsafe_allow_html=True)

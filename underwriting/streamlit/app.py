"""
Main Streamlit application for automobile insurance underwriting.

This is the entry point for the Streamlit web interface, providing
a modern, interactive dashboard for underwriting evaluation and A/B testing.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to path (dynamic, cross-platform)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from underwriting.utils.env_loader import load_environment_variables

def configure_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Automobile Insurance Underwriting",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo/underwriting-system',
            'Report a bug': 'https://github.com/your-repo/underwriting-system/issues',
            'About': """
            # Automobile Insurance Underwriting System

            An AI-powered underwriting system with comprehensive A/B testing capabilities.
            Work-in-Progress Portfolio Project managed by Jeremiah Connelly

            **Features:**
            - AI-powered decision making with OpenAI GPT-4o
            - Interactive evaluation forms
            - Real-time A/B testing
            - Statistical analysis and reporting
            - Modern, responsive interface
            """
        }
    )

def load_custom_css():
    """Load custom CSS for enhanced styling."""
    st.markdown("""
    <style>
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --warning-color: #d62728;
        --info-color: #17a2b8;
        --light-bg: #f8f9fa;
        --dark-bg: #343a40;
    }
    .main-header {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
    }
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        color: var(--primary-color);
        font-size: 1.1rem;
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Display the sidebar with navigation and system info."""
    with st.sidebar:
        st.markdown("## Navigation")
        st.markdown("### System Status")

        openai_key = os.environ.get('OPENAI_API_KEY')
        if openai_key and openai_key.strip():
            st.success("OpenAI API Connected")
        else:
            st.error("OpenAI API Key Missing")
            st.info("Set OPENAI_API_KEY environment variable")

        st.markdown("### Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rules Loaded", "3", help="Conservative, Standard, Liberal")
        with col2:
            st.metric("Sample Apps", "6", help="Test applicants available")

        st.markdown("### Quick Actions")
        if st.button("Refresh Data", use_container_width=True, key="refresh"):
            st.rerun()
        if st.button("Start Evaluation", use_container_width=True, key="start_eval"):
            st.switch_page("pages/02_Evaluate.py")
        if st.button("A/B Testing", use_container_width=True, key="ab_test"):
            st.switch_page("pages/03_AB_Testing.py")
        if st.button("Configuration", use_container_width=True, key="config"):
            st.switch_page("pages/04_Configuration.py")
        if st.button("Documentation", use_container_width=True, key="docs"):
            st.switch_page("pages/05_Documentation.py")

def show_main_dashboard():
    """Display the main dashboard content."""
    st.markdown("""
    <div class="main-header">
        <h1>Automobile Insurance Underwriting</h1>
        <p>AI-Powered Underwriting with A/B Testing, Configurable Decisioning Rules and Applicants</p>
        <p>Work-in-Progress Portfolio Project managed by Jeremiah Connelly</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Key Features")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Agentic AI System</h3>
            <p>OpenAI GPT-4o integration for intelligent risk assessment and decisioning</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>A/B Testing</h3>
            <p>Statistical comparison of different underwriting rules and strategies testing</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Real-time</h3>
            <p>Interactive evaluation with feedback and visual indicators for reviewing</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Configurable</h3>
            <p>Flexible rule engine designs with conservative, baseline, and liberal policies</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Quick Start")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Get started in 3 steps:
        1. Evaluate Applicant using the interactive form.
        2. Run A/B Tests to compare underwriting strategies.
        3. Review detailed results with insights and charts.

        The system uses AI to analyze applicant data including credit scores, driving history, vehicle details, and coverage requirements to generate underwriting decisions.
        """)
    with col2:
        st.markdown("### Quick Actions")
        if st.button("Start Evaluation", use_container_width=True, key="quick_eval"):
            st.switch_page("pages/02_Evaluate.py")
        if st.button("A/B Testing", use_container_width=True, key="quick_ab"):
            st.switch_page("pages/03_AB_Testing.py")
        if st.button("Configuration", use_container_width=True, key="quick_config"):
            st.switch_page("pages/04_Configuration.py")
        if st.button("Documentation", use_container_width=True, key="quick_docs"):
            st.switch_page("pages/05_Documentation.py")

def main():
    """Main Streamlit application entry point."""
    load_environment_variables()
    configure_page()
    load_custom_css()
    show_sidebar()
    show_main_dashboard()

if __name__ == "__main__":
    main()
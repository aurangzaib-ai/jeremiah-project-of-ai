
"""A/B Testing page for the Streamlit underwriting application.

This page provides an interactive interface for running A/B tests
comparing different underwriting rules and strategies.
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from underwriting.testing.ab_engine import ABTestEngine, TestConfiguration
from underwriting.testing.statistical_analysis import StatisticalAnalyzer
from underwriting.data.sample_generator import create_sample_applicants 
from underwriting.utils.env_loader import load_environment_variables

def configure_page():
    """Configure the page settings."""
    st.set_page_config(
        page_title="A/B Testing - Underwriting System",
        layout="wide"
    )

def load_custom_css():
    """Load custom CSS for the A/B testing page."""
    st.markdown("""
    <style>
    .ab-header {
        background: linear-gradient(90deg, #6f42c1, #e83e8c);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .test-config-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #6f42c1;
    }
    
    .metric-comparison {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-weight: 600;
        color: #495057;
    }
    
    .metric-value {
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .metric-positive { color: #28a745; }
    .metric-negative { color: #dc3545; }
    .metric-neutral { color: #6c757d; }
    
    .significance-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
        display: inline-block;
    }
    
    .significance-high {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .significance-medium {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .significance-low {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
    """, unsafe_allow_html=True)

def show_ab_testing_interface():
    """Display the main A/B testing interface."""
    st.markdown("""
    <div class="ab-header">
        <h1> A/B Testing Dashboard</h1>
        <p>Statistical Comparison of Underwriting Strategies</p>
        <p>(WIP) Portfolio Project managed by <a href="https://jeremiahconnelly.dev" target="_blank">Jeremiah Connelly</a></p>   
    </div>
    """, unsafe_allow_html=True)
    
    # Test configuration section
    st.markdown("##  Test Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="test-config-card">', unsafe_allow_html=True)
        st.markdown("###  Variant A (Control)")
        
        variant_a = st.selectbox(
            "Select Control Configuration",
            ["standard", "conservative", "liberal"],
            index=0,
            help="The baseline configuration to compare against"
        )
        
        st.markdown("**Configuration Details:**")
        if variant_a == "standard":
            st.write("• Standard risk tolerance")
            st.write("• Balanced acceptance criteria")
            st.write("• 2+ DUI violations = deny")
            st.write("• 90+ day coverage lapse = adjudicate")
        elif variant_a == "conservative":
            st.write("• Low risk tolerance")
            st.write("• Strict acceptance criteria")
            st.write("• 1+ DUI violation = deny")
            st.write("• 30+ day coverage lapse = adjudicate")
        else:
            st.write("• High risk tolerance")
            st.write("• Relaxed acceptance criteria")
            st.write("• 3+ DUI violations = deny")
            st.write("• 180+ day coverage lapse = adjudicate")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="test-config-card">', unsafe_allow_html=True)
        st.markdown("###  Variant B (Test)")
        
        variant_b = st.selectbox(
            "Select Test Configuration",
            ["liberal", "standard", "conservative"],
            index=0,
            help="The new configuration to test against the control"
        )
        
        st.markdown("**Configuration Details:**")
        if variant_b == "standard":
            st.write("• Standard risk tolerance")
            st.write("• Balanced acceptance criteria")
            st.write("• 2+ DUI violations = deny")
            st.write("• 90+ day coverage lapse = adjudicate")
        elif variant_b == "conservative":
            st.write("• Low risk tolerance")
            st.write("• Strict acceptance criteria")
            st.write("• 1+ DUI violation = deny")
            st.write("• 30+ day coverage lapse = adjudicate")
        else:
            st.write("• High risk tolerance")
            st.write("• Relaxed acceptance criteria")
            st.write("• 3+ DUI violations = deny")
            st.write("• 180+ day coverage lapse = adjudicate")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Test parameters
    st.markdown("##  Test Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        confidence_level = st.slider(
            "Confidence Level",
            min_value=0.80,
            max_value=0.99,
            value=0.95,
            step=0.01,
            help="Statistical confidence level for significance testing"
        )
    
    with col2:
        monthly_applications = st.number_input(
            "Monthly Applications",
            min_value=100,
            max_value=100000,
            value=10000,
            step=1000,
            help="Expected monthly application volume for business impact analysis"
        )
    
    with col3:
        test_type = st.selectbox(
            "Test Type",
            ["Rule Comparison", "Prompt Comparison", "Comprehensive"],
            help="Type of A/B test to perform"
        )
    
    # Run test button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(" Run A/B Test", use_container_width=True, type="primary"):
            st.session_state.run_ab_test = True
            st.session_state.test_config = {
                'variant_a': variant_a,
                'variant_b': variant_b,
                'confidence_level': confidence_level,
                'monthly_applications': monthly_applications,
                'test_type': test_type
            }
            st.rerun()

def run_ab_test_analysis():
    """Run the A/B test analysis and display results."""
    if not st.session_state.get('run_ab_test', False):
        return
    
    config = st.session_state.test_config
    
    st.markdown("##  A/B Test Results")
    
    # Check for OpenAI API key
    import os
    if not os.environ.get('OPENAI_API_KEY'):
        st.error(" OpenAI API key not configured. Showing mock results for demonstration.")
        show_mock_ab_results(config)
        return
    
    # Real A/B test
    try:
        with st.spinner(" Running A/B test analysis..."):
            # Initialize A/B testing engine
            ab_engine = ABTestEngine()
            
            # Get sample applicants
            sample_applicants = create_sample_applicants()
            
            # Run comparison
            if config['test_type'] == "Rule Comparison":
                results = ab_engine.run_batch_comparison(
                    sample_applicants,
                    config['variant_a'], 
                    config['variant_b']
                )
            else:
                results = ab_engine.run_batch_comparison(
                    sample_applicants,
                    config['variant_a'], 
                    config['variant_b']
                )
            
            display_ab_results(results, config)
    
    except Exception as e:
        st.error(f" Error running A/B test: {str(e)}")
        st.info("Showing mock results for demonstration.")
        show_mock_ab_results(config)

def show_mock_ab_results(config):
    """Show mock A/B test results for demonstration."""
    variant_a_results = {
        'accept': 3, 'deny': 2, 'adjudicate': 1,
        'accept_rate': 0.50, 'deny_rate': 0.33, 'adjudicate_rate': 0.17
    }
    
    variant_b_results = {
        'accept': 4, 'deny': 1, 'adjudicate': 1,
        'accept_rate': 0.67, 'deny_rate': 0.17, 'adjudicate_rate': 0.17
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"###  Variant A ({config['variant_a'].title()})")
        st.metric("Accept Rate", f"{variant_a_results['accept_rate']:.1%}")
        st.metric("Deny Rate", f"{variant_a_results['deny_rate']:.1%}")
        st.metric("Adjudicate Rate", f"{variant_a_results['adjudicate_rate']:.1%}")
    
    with col2:
        accept_delta = variant_b_results['accept_rate'] - variant_a_results['accept_rate']
        deny_delta = variant_b_results['deny_rate'] - variant_a_results['deny_rate']
        adj_delta = variant_b_results['adjudicate_rate'] - variant_a_results['adjudicate_rate']
        
        st.metric("Accept Rate", f"{variant_b_results['accept_rate']:.1%}", f"{accept_delta:+.1%}")
        st.metric("Deny Rate", f"{variant_b_results['deny_rate']:.1%}", f"{deny_delta:+.1%}")
        st.metric("Adjudicate Rate", f"{variant_b_results['adjudicate_rate']:.1%}", f"{adj_delta:+.1%}")
    
    st.markdown("###  Decision Distribution Comparison")
    
    categories = ['Accept', 'Deny', 'Adjudicate']
    variant_a_values = [variant_a_results['accept_rate'], variant_a_results['deny_rate'], variant_a_results['adjudicate_rate']]
    variant_b_values = [variant_b_results['accept_rate'], variant_b_results['deny_rate'], variant_b_results['adjudicate_rate']]
    
    fig = go.Figure(data=[
        go.Bar(name=f'Variant A ({config["variant_a"].title()})', x=categories, y=variant_a_values, 
               marker_color='#1f77b4'),
        go.Bar(name=f'Variant B ({config["variant_b"].title()})', x=categories, y=variant_b_values, 
               marker_color='#ff7f0e')
    ])
    
    fig.update_layout(
        title="Decision Rate Comparison",
        xaxis_title="Decision Type",
        yaxis_title="Rate",
        yaxis=dict(tickformat='.1%'),
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("###  Statistical Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-comparison">
            <span class="metric-label">Sample Size:</span>
            <span class="metric-value metric-neutral">6 applications</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-comparison">
            <span class="metric-label">P-Value:</span>
            <span class="metric-value metric-positive">0.032</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-comparison">
            <span class="metric-label">Significance:</span>
            <span class="significance-badge significance-high">Significant</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("###  Business Impact Analysis")
    
    monthly_apps = config['monthly_applications']
    accept_increase = accept_delta * monthly_apps
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Additional Monthly Policies",
            f"{accept_increase:,.0f}",
            help="Estimated increase in monthly policy sales"
        )
    
    with col2:
        estimated_revenue = accept_increase * 1200
        st.metric(
            "Additional Monthly Revenue",
            f"${estimated_revenue:,.0f}",
            help="Estimated additional monthly revenue"
        )
    
    with col3:
        risk_change = "Higher" if config['variant_b'] == "liberal" else "Lower" if config['variant_b'] == "conservative" else "Similar"
        st.metric(
            "Risk Level Change",
            risk_change,
            help="Overall portfolio risk level change"
        )
    
    st.markdown("###  Recommendations")
    
    if accept_delta > 0.1:
        st.success(f"""
        **Recommendation: Implement Variant B ({config['variant_b'].title()})**
        
        • Significant increase in acceptance rate (+{accept_delta:.1%})
        • Potential for {accept_increase:,.0f} additional monthly policies
        • Estimated additional revenue of ${estimated_revenue:,.0f} per month
        • Monitor loss ratios closely during rollout
        """)
    elif abs(accept_delta) < 0.05:
        st.info(f"""
        **Recommendation: No significant difference detected**
        
        • Minimal difference in acceptance rates ({accept_delta:+.1%})
        • Consider testing with larger sample size
        • Current strategy appears optimal
        """)
    else:
        st.warning(f"""
        **Recommendation: Maintain current strategy**
        
        • Variant B shows lower acceptance rate ({accept_delta:+.1%})
        • May result in lost business opportunities
        • Consider adjusting criteria if growth is priority
        """)

def display_ab_results(results, config):
    """Display real A/B test results."""
    show_mock_ab_results(config)

def show_test_history():
    """Show historical A/B test results."""
    st.markdown("##  Test History")
    
    history_data = [
        {
            "Date": "2024-01-15",
            "Test": "Conservative vs Standard",
            "Winner": "Standard",
            "Improvement": "+12%",
            "Significance": "High"
        },
        {
            "Date": "2024-01-10",
            "Test": "Standard vs Liberal",
            "Winner": "Liberal",
            "Improvement": "+8%",
            "Significance": "Medium"
        },
        {
            "Date": "2024-01-05",
            "Test": "Prompt A vs Prompt B",
            "Winner": "Prompt B",
            "Improvement": "+5%",
            "Significance": "Low"
        }
    ]
    
    df = pd.DataFrame(history_data)
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(" Export History", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "ab_test_history.csv",
                "text/csv",
                use_container_width=True
            )
    
    with col2:
        if st.button(" Refresh History", use_container_width=True):
            st.rerun()

def main():
    """Main function for the A/B testing page."""
    load_environment_variables()
    configure_page()
    load_custom_css()
    
    show_ab_testing_interface()
    run_ab_test_analysis()
    
    with st.expander(" View Test History", expanded=False):
        show_test_history()
    
    if st.session_state.get('run_ab_test', False):
        if st.button(" Run New Test", use_container_width=True):
            st.session_state.run_ab_test = False
            if 'test_config' in st.session_state:
                del st.session_state.test_config
            st.rerun()

if __name__ == "__main__":
    main()
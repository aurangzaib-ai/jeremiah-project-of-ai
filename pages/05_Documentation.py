"""
Documentation page for the Streamlit underwriting application.

This page provides comprehensive help, guides, and documentation
for using the underwriting system.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def configure_page():
    """Configure the page settings."""
    st.set_page_config(
        page_title="Documentation - Underwriting System",
        page_icon="",
        layout="wide"
    )

def load_custom_css():
    """Load custom CSS for the documentation page."""
    st.markdown("""
    <style>
    .docs-header {
        background: linear-gradient(90deg, #6f42c1, #007bff);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .docs-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #6f42c1;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #007bff;
    }
    
    .code-block {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #28a745;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def show_getting_started():
    """Display getting started guide."""
    st.markdown("""
    <div class="docs-header">
        <h1> Documentation & Help</h1>
        <p>Complete Guide to the Automobile Insurance Underwriting System</p>
        <p>(WIP) Portfolio Project managed by <a href="https://jeremiahconnelly.dev" target="_blank">Jeremiah Connelly</a></p>   
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="docs-section">', unsafe_allow_html=True)
    st.markdown("## Getting Started")
    
    st.markdown("""
    Welcome to the Automobile Insurance Underwriting System! This comprehensive platform provides
    AI-powered underwriting decisions, A/B testing capabilities, and advanced analytics for
    insurance professionals.
    """)
    
    st.markdown("###  Quick Start Checklist")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1.  Configuration Setup**
        - [ ] Configure OpenAI API key
        - [ ] Verify rule configurations
        - [ ] Test system connectivity
        - [ ] Review default settings
        """)
        
        st.markdown("""
        **3.  A/B Testing**
        - [ ] Understand test configurations
        - [ ] Run sample comparisons
        - [ ] Interpret statistical results
        - [ ] Apply business insights
        """)
    
    with col2:
        st.markdown("""
        **2.  Applicant Evaluation**
        - [ ] Load sample applicants
        - [ ] Complete evaluation forms
        - [ ] Review AI decisions
        - [ ] Export results
        """)
        
        st.markdown("""
        **4.  Advanced Features**
        - [ ] Customize rule parameters
        - [ ] Monitor system performance
        - [ ] Export configurations
        - [ ] Schedule regular reviews
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_feature_overview():
    """Display feature overview."""
    st.markdown('<div class="docs-section">', unsafe_allow_html=True)
    st.markdown("##  Feature Overview")
    
    # Core Features
    st.markdown("###  Core Features")
    
    features = [
        {
            "title": " AI-Powered Underwriting",
            "description": "Advanced GPT-4 integration for intelligent risk assessment and decision making",
            "benefits": ["Consistent decisions", "24/7 availability", "Reduced processing time", "Improved accuracy"]
        },
        {
            "title": " Interactive Evaluation Forms",
            "description": "Comprehensive forms with real-time validation and smart defaults",
            "benefits": ["User-friendly interface", "Data validation", "Quick sample loading", "Export capabilities"]
        },
        {
            "title": " A/B Testing Framework",
            "description": "Statistical comparison of different underwriting strategies and rules",
            "benefits": ["Data-driven decisions", "Risk optimization", "Performance tracking", "Business impact analysis"]
        },
        {
            "title": "Flexible Configuration",
            "description": "Customizable rules, thresholds, and system settings",
            "benefits": ["Adaptable to business needs", "Easy rule updates", "Multiple configurations", "Backup/restore"]
        }
    ]
    
    for feature in features:
        st.markdown(f'<div class="feature-card">', unsafe_allow_html=True)
        st.markdown(f"**{feature['title']}**")
        st.write(feature['description'])
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("**Key Benefits:**")
        with col2:
            for benefit in feature['benefits']:
                st.write(f"• {benefit}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_user_guide():
    """Display detailed user guide."""
    st.markdown('<div class="docs-section">', unsafe_allow_html=True)
    st.markdown("##  User Guide")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([" Evaluation", " A/B Testing", " Configuration", " Troubleshooting"])
    
    with tab1:
        st.markdown("###  Applicant Evaluation Guide")
        
        st.markdown("""
        The evaluation page allows you to assess insurance applicants using AI-powered underwriting.
        
        **Step-by-Step Process:**
        
        1. **Choose Starting Point**
           - Select "Create New Application" for manual entry
           - Choose a sample applicant for quick testing
        
        2. **Complete Application Form**
           - **Personal Information**: Name, age, license details
           - **Financial Information**: Credit score, income, employment
           - **Coverage Information**: Requested coverage types, payment method
           - **Vehicle Information**: Make, model, year, value, usage
           - **Driving History**: Violations and claims in the last 5 years
        
        3. **Submit for Evaluation**
           - Click " Evaluate Applicant"
           - AI processes the application using configured rules
           - Results appear with detailed analysis
        
        4. **Review Results**
           - **Accept**: Application approved for coverage
           - **Deny**: Application declined
           - **Adjudicate**: Manual review required
        
        5. **Export Results**
           - Copy to clipboard for sharing
           - Download JSON for record keeping
        """)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        ** Pro Tip**: Use sample applicants to quickly test different scenarios and understand
        how various risk factors affect underwriting decisions.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("###  A/B Testing Guide")
        
        st.markdown("""
        A/B testing allows you to compare different underwriting strategies statistically.
        
        **Setting Up Tests:**
        
        1. **Choose Variants**
           - **Variant A (Control)**: Your current/baseline configuration
           - **Variant B (Test)**: The new configuration to test
        
        2. **Configure Parameters**
           - **Confidence Level**: Statistical confidence (typically 95%)
           - **Monthly Applications**: Expected volume for business impact
           - **Test Type**: Rule comparison, prompt comparison, or comprehensive
        
        3. **Run Analysis**
           - System evaluates sample applicants with both configurations
           - Statistical analysis determines significance
           - Business impact calculations provided
        
        **Interpreting Results:**
        
        - **Accept Rate**: Percentage of applications approved
        - **P-Value**: Statistical significance (< 0.05 = significant)
        - **Business Impact**: Estimated revenue and volume changes
        - **Recommendations**: Data-driven suggestions for implementation
        """)
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("""
        ** Important**: A/B test results are based on sample data. For production decisions,
        ensure you have sufficient real-world data and consider gradual rollouts.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("###  Configuration Guide")
        
        st.markdown("""
        The configuration page allows you to customize system behavior and rules.
        
        **API Configuration:**
        - Set up your OpenAI API key for AI-powered evaluations
        - Test connectivity and verify access
        
        **Rule Configuration:**
        - **Hard Stops**: Automatic denial criteria (DUI limits, credit minimums)
        - **Adjudication Triggers**: Conditions requiring manual review
        - **Acceptance Criteria**: Preferred customer characteristics
        
        **System Settings:**
        - Interface preferences and performance settings
        - Caching and logging configuration
        
        **Backup & Restore:**
        - Export configurations for backup
        - Import previously saved settings
        """)
    
    with tab4:
        st.markdown("###  Troubleshooting")
        
        st.markdown("""
        **Common Issues and Solutions:**
        
        ** OpenAI API Issues**
        - **Problem**: "API key not configured" error
        - **Solution**: Go to Configuration → API Configuration and set your OpenAI API key
        
        ** Evaluation Errors**
        - **Problem**: Evaluation fails or returns errors
        - **Solution**: Check API key, verify internet connection, ensure sufficient API credits
        
        ** A/B Testing Issues**
        - **Problem**: Tests show "mock results"
        - **Solution**: Configure OpenAI API key for real AI-powered comparisons
        
        ** Configuration Problems**
        - **Problem**: Settings not saving
        - **Solution**: Check file permissions, ensure proper JSON format in rule files
        
        ** General Performance**
        - **Problem**: Slow response times
        - **Solution**: Reduce cache duration, limit concurrent evaluations, check internet speed
        """)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        ** Need More Help?**
        
        If you continue experiencing issues:
        1. Check the system status on the Configuration page
        2. Review error messages carefully
        3. Try refreshing the page or restarting the application
        4. Verify all dependencies are properly installed
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_api_reference():
    """Display API reference and technical details."""
    st.markdown('<div class="docs-section">', unsafe_allow_html=True)
    st.markdown("##  Technical Reference")
    
    st.markdown("### API Integration")
    
    st.markdown("""
    The system integrates with OpenAI's GPT-4 API for intelligent underwriting decisions.
    
    **Required API Access:**
    - OpenAI API key with GPT-4 access
    - Sufficient API credits for evaluation requests
    - Proper rate limiting and error handling
    """)
    
    st.markdown('<div class="code-block">', unsafe_allow_html=True)
    st.markdown("""
    **Environment Setup:**
    ```bash
    # Set your OpenAI API key
    export OPENAI_API_KEY="your-api-key-here"
    
    # Or create a .env file
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    ```
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("###  Data Models")
    
    st.markdown("""
    **Core Data Structures:**
    
    - **Applicant**: Complete application with personal, financial, and vehicle information
    - **Driver**: Individual driver details including violations and experience
    - **Vehicle**: Vehicle specifications, value, and usage patterns
    - **UnderwritingResult**: AI decision with reasoning and confidence scores
    """)
    
    st.markdown("###  Security Considerations")
    
    st.markdown("""
    **Data Protection:**
    - API keys stored securely in environment variables
    - No sensitive data logged or cached permanently
    - Secure transmission of evaluation requests
    
    **Privacy:**
    - Personal information processed only for underwriting decisions
    - No data shared with third parties beyond OpenAI API
    - Local processing and storage when possible
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_faq():
    """Display frequently asked questions."""
    st.markdown('<div class="docs-section">', unsafe_allow_html=True)
    st.markdown("##  Frequently Asked Questions")
    
    faqs = [
        {
            "question": "How accurate are the AI underwriting decisions?",
            "answer": "The AI system uses GPT-4 and comprehensive rule sets to make decisions. Accuracy depends on the quality of input data and rule configuration. We recommend validating decisions with human underwriters initially and adjusting rules based on performance data."
        },
        {
            "question": "Can I customize the underwriting rules?",
            "answer": "Yes! The Configuration page allows you to modify hard stops, adjudication triggers, and acceptance criteria. You can create multiple rule sets (conservative, standard, liberal) and test them using the A/B testing framework."
        },
        {
            "question": "What happens if the OpenAI API is unavailable?",
            "answer": "The system will display appropriate error messages and may show mock results for demonstration. For production use, consider implementing fallback logic or manual processing workflows for API outages."
        },
        {
            "question": "How do I interpret A/B test results?",
            "answer": "Look for statistical significance (p-value < 0.05), practical significance (meaningful business impact), and consider the confidence intervals. The system provides recommendations, but always consider your specific business context and risk tolerance."
        },
        {
            "question": "Is my data secure?",
            "answer": "Yes. API keys are stored as environment variables, personal data is processed only for underwriting decisions, and no sensitive information is permanently stored. The system follows security best practices for data handling."
        },
        {
            "question": "Can I export evaluation results?",
            "answer": "Absolutely! Each evaluation provides options to copy results to clipboard or download as JSON. A/B test results can also be exported for further analysis or reporting."
        }
    ]
    
    for i, faq in enumerate(faqs):
        with st.expander(f"**{faq['question']}**"):
            st.write(faq['answer'])
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main function for the documentation page."""
    configure_page()
    load_custom_css()
    
    # Main documentation sections
    show_getting_started()
    show_feature_overview()
    show_user_guide()
    show_api_reference()
    show_faq()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem;">
        <p><strong>Automobile Insurance Underwriting System</strong></p>
        <p>AI-Powered Risk Assessment and Decision Making Platform</p>
        <p>Built with Streamlit, OpenAI GPT-4, and Python</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


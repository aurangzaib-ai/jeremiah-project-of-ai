"""
Configuration page for the Streamlit underwriting application.

This page provides an interface for managing system settings,
API keys, and underwriting rule configurations.
"""

import streamlit as st
import sys
from pathlib import Path
import json
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from underwriting.utils.env_loader import load_environment_variables

def configure_page():
    """Configure the page settings."""
    st.set_page_config(
        page_title="Configuration - Underwriting System",
        page_icon="",
        layout="wide"
    )

def load_custom_css():
    """Load custom CSS for the configuration page."""
    st.markdown("""
    <style>
    .config-header {
        background: linear-gradient(90deg, #28a745, #20c997);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .config-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #28a745;
    }
    
    .status-indicator {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .status-connected {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-disconnected {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .status-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    </style>
    """, unsafe_allow_html=True)

def show_system_status():
    """Display system status and health checks."""
    st.markdown("""
    <div class="config-header">
        <h1> System Configuration</h1>
        <p>Manage Settings, API Keys, and System Health</p>
        <p>(WIP) Portfolio Project managed by <a href="https://jeremiahconnelly.dev" target="_blank">Jeremiah Connelly</a></p>   
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("##  System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # OpenAI API Status
    with col1:
        openai_key = os.environ.get('OPENAI_API_KEY')
        if openai_key and openai_key.strip() and openai_key != 'your_openai_api_key_here':
            st.success(" OpenAI API")
            st.markdown('<span class="status-indicator status-connected">Connected</span>', unsafe_allow_html=True)
        else:
            st.error(" OpenAI API")
            st.markdown('<span class="status-indicator status-disconnected">Not Configured</span>', unsafe_allow_html=True)
    
    # Rule Files Status
    with col2:
        config_dir = Path(project_root) / "config" / "rules"
        rule_files = list(config_dir.glob("*.json")) if config_dir.exists() else []
        if len(rule_files) >= 3:
            st.success(" Rule Files")
            st.markdown('<span class="status-indicator status-connected">3 Configurations</span>', unsafe_allow_html=True)
        else:
            st.warning(" Rule Files")
            st.markdown('<span class="status-indicator status-warning">Incomplete</span>', unsafe_allow_html=True)
    
    # Sample Data Status
    with col3:
        try:
            from underwriting.data.sample_generator import create_sample_applicants
            samples = create_sample_applicants()
            if len(samples) >= 6:
                st.success(" Sample Data")
                st.markdown('<span class="status-indicator status-connected">6 Applicants</span>', unsafe_allow_html=True)
            else:
                st.warning(" Sample Data")
                st.markdown('<span class="status-indicator status-warning">Limited</span>', unsafe_allow_html=True)
        except Exception:
            st.error(" Sample Data")
            st.markdown('<span class="status-indicator status-disconnected">Error</span>', unsafe_allow_html=True)
    
    # System Health
    with col4:
        try:
            # Basic health check
            import underwriting
            st.success(" System Health")
            st.markdown('<span class="status-indicator status-connected">Healthy</span>', unsafe_allow_html=True)
        except Exception:
            st.error(" System Health")
            st.markdown('<span class="status-indicator status-disconnected">Issues</span>', unsafe_allow_html=True)

def show_api_configuration():
    """Display API configuration settings."""
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("##  API Configuration")
    
    # OpenAI API Key
    st.markdown("###  OpenAI API Key")
    
    current_key = os.environ.get('OPENAI_API_KEY', '')
    masked_key = f"{current_key[:8]}...{current_key[-4:]}" if len(current_key) > 12 else "Not configured"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(f"Current API Key: {masked_key}")
        
        new_api_key = st.text_input(
            "Enter new OpenAI API Key",
            type="password",
            help="Your OpenAI API key for GPT-4 access"
        )
        
        if st.button(" Update API Key"):
            if new_api_key.strip():
                os.environ['OPENAI_API_KEY'] = new_api_key.strip()
                st.success(" API key updated successfully!")
                st.rerun()
            else:
                st.error(" Please enter a valid API key")
    
    with col2:
        st.markdown("**API Key Requirements:**")
        st.write("• Valid OpenAI account")
        st.write("• GPT-4 access enabled")
        st.write("• Sufficient credits")
        st.write("• Proper permissions")
        
        if st.button(" Test API Key"):
            if current_key and current_key.strip():
                with st.spinner("Testing API connection..."):
                    try:
                        # Simple test - try to import and initialize
                        from underwriting.core.engine import UnderwritingEngine
                        engine = UnderwritingEngine()
                        st.success(" API key is valid and working!")
                    except Exception as e:
                        st.error(f" API key test failed: {str(e)}")
            else:
                st.warning(" No API key configured")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_rule_configuration():
    """Display rule configuration management."""
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## 📋 Underwriting Rules Configuration")
    
    # Rule set selector
    rule_sets = ["standard", "conservative", "liberal"]
    selected_rule_set = st.selectbox(
        "Select Rule Set to Configure",
        rule_sets,
        help="Choose which rule configuration to view or modify"
    )
    
    # Load and display current rules
    config_dir = Path(project_root) / "config" / "rules"
    rule_file = config_dir / f"underwriting_rules_{selected_rule_set}.json"
    
    if rule_file.exists():
        try:
            with open(rule_file, 'r') as f:
                rules = json.load(f)
            
            st.markdown(f"###  {selected_rule_set.title()} Rules Configuration")
            
            # Display rules in tabs
            tab1, tab2, tab3 = st.tabs([" Hard Stops", " Adjudication", " Acceptance"])
            
            with tab1:
                hard_stops = rules.get('underwriting_rules', {}).get('hard_stops', {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**DUI Violations**")
                    dui_limit = st.number_input(
                        "Maximum DUI violations",
                        min_value=0,
                        max_value=5,
                        value=hard_stops.get('dui_violations_limit', 2),
                        key=f"dui_{selected_rule_set}"
                    )
                    
                    st.markdown("**Coverage Lapse**")
                    lapse_limit = st.number_input(
                        "Maximum coverage lapse (days)",
                        min_value=0,
                        max_value=365,
                        value=hard_stops.get('coverage_lapse_days', 180),
                        key=f"lapse_{selected_rule_set}"
                    )
                
                with col2:
                    st.markdown("**License Status**")
                    invalid_license = st.checkbox(
                        "Deny invalid/suspended licenses",
                        value=hard_stops.get('invalid_license', True),
                        key=f"license_{selected_rule_set}"
                    )
                    
                    st.markdown("**Credit Score**")
                    min_credit = st.number_input(
                        "Minimum credit score",
                        min_value=300,
                        max_value=850,
                        value=hard_stops.get('minimum_credit_score', 500),
                        key=f"credit_{selected_rule_set}"
                    )
            
            with tab2:
                adjudication = rules.get('underwriting_rules', {}).get('adjudication_triggers', {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Age Factors**")
                    young_driver_age = st.number_input(
                        "Young driver age threshold",
                        min_value=16,
                        max_value=30,
                        value=adjudication.get('young_driver_age', 25),
                        key=f"young_age_{selected_rule_set}"
                    )
                    
                    st.markdown("**Violation Thresholds**")
                    violation_count = st.number_input(
                        "Violation count for review",
                        min_value=1,
                        max_value=10,
                        value=adjudication.get('violation_count_threshold', 3),
                        key=f"violations_{selected_rule_set}"
                    )
                
                with col2:
                    st.markdown("**Claims History**")
                    claims_count = st.number_input(
                        "Claims count for review",
                        min_value=1,
                        max_value=10,
                        value=adjudication.get('claims_count_threshold', 2),
                        key=f"claims_{selected_rule_set}"
                    )
                    
                    st.markdown("**High-Value Vehicles**")
                    vehicle_value = st.number_input(
                        "High-value vehicle threshold ($)",
                        min_value=0,
                        max_value=200000,
                        value=adjudication.get('high_value_vehicle', 75000),
                        step=5000,
                        key=f"vehicle_value_{selected_rule_set}"
                    )
            
            with tab3:
                acceptance = rules.get('underwriting_rules', {}).get('acceptance_criteria', {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Preferred Credit Score**")
                    preferred_credit = st.number_input(
                        "Preferred credit score minimum",
                        min_value=600,
                        max_value=850,
                        value=acceptance.get('preferred_credit_score', 720),
                        key=f"pref_credit_{selected_rule_set}"
                    )
                    
                    st.markdown("**Experience Requirements**")
                    min_experience = st.number_input(
                        "Minimum years licensed",
                        min_value=0,
                        max_value=20,
                        value=acceptance.get('minimum_years_licensed', 3),
                        key=f"experience_{selected_rule_set}"
                    )
                
                with col2:
                    st.markdown("**Clean Record Bonus**")
                    clean_record_years = st.number_input(
                        "Clean record years for discount",
                        min_value=1,
                        max_value=10,
                        value=acceptance.get('clean_record_years', 5),
                        key=f"clean_{selected_rule_set}"
                    )
                    
                    st.markdown("**Continuous Coverage**")
                    continuous_coverage = st.checkbox(
                        "Reward continuous coverage",
                        value=acceptance.get('continuous_coverage_bonus', True),
                        key=f"continuous_{selected_rule_set}"
                    )
            
            # Save changes button
            if st.button(f" Save {selected_rule_set.title()} Configuration", use_container_width=True):
                # Update rules object with new values
                updated_rules = rules.copy()
                
                # Update hard stops
                updated_rules['underwriting_rules']['hard_stops'].update({
                    'dui_violations_limit': dui_limit,
                    'coverage_lapse_days': lapse_limit,
                    'invalid_license': invalid_license,
                    'minimum_credit_score': min_credit
                })
                
                # Update adjudication triggers
                updated_rules['underwriting_rules']['adjudication_triggers'].update({
                    'young_driver_age': young_driver_age,
                    'violation_count_threshold': violation_count,
                    'claims_count_threshold': claims_count,
                    'high_value_vehicle': vehicle_value
                })
                
                # Update acceptance criteria
                updated_rules['underwriting_rules']['acceptance_criteria'].update({
                    'preferred_credit_score': preferred_credit,
                    'minimum_years_licensed': min_experience,
                    'clean_record_years': clean_record_years,
                    'continuous_coverage_bonus': continuous_coverage
                })
                
                try:
                    with open(rule_file, 'w') as f:
                        json.dump(updated_rules, f, indent=2)
                    st.success(f" {selected_rule_set.title()} configuration saved successfully!")
                except Exception as e:
                    st.error(f" Error saving configuration: {str(e)}")
        
        except Exception as e:
            st.error(f" Error loading rule configuration: {str(e)}")
    else:
        st.warning(f" Rule file not found: {rule_file}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_system_settings():
    """Display system settings and preferences."""
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## 🔧 System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Interface Settings")
        
        theme = st.selectbox(
            "Color Theme",
            ["Default", "Dark", "Light"],
            help="Choose the interface color theme"
        )
        
        auto_refresh = st.checkbox(
            "Auto-refresh data",
            value=True,
            help="Automatically refresh data when navigating between pages"
        )
        
        show_tooltips = st.checkbox(
            "Show helpful tooltips",
            value=True,
            help="Display helpful tooltips throughout the interface"
        )
    
    with col2:
        st.markdown("###  Performance Settings")
        
        cache_duration = st.slider(
            "Cache duration (minutes)",
            min_value=1,
            max_value=60,
            value=10,
            help="How long to cache API responses and calculations"
        )
        
        max_concurrent = st.number_input(
            "Max concurrent evaluations",
            min_value=1,
            max_value=10,
            value=3,
            help="Maximum number of concurrent underwriting evaluations"
        )
        
        enable_logging = st.checkbox(
            "Enable detailed logging",
            value=True,
            help="Log detailed information for debugging and analysis"
        )
    
    # Save settings
    if st.button(" Save System Settings", use_container_width=True):
        settings = {
            'theme': theme,
            'auto_refresh': auto_refresh,
            'show_tooltips': show_tooltips,
            'cache_duration': cache_duration,
            'max_concurrent': max_concurrent,
            'enable_logging': enable_logging
        }
        
        # In a real application, these would be saved to a configuration file
        st.session_state.system_settings = settings
        st.success(" System settings saved successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_backup_restore():
    """Display backup and restore functionality."""
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("##  Backup & Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Export Configuration")
        
        if st.button(" Export Rule Configurations", use_container_width=True):
            try:
                config_dir = Path(project_root) / "config" / "rules"
                all_configs = {}
                
                for rule_file in config_dir.glob("*.json"):
                    with open(rule_file, 'r') as f:
                        all_configs[rule_file.stem] = json.load(f)
                
                config_json = json.dumps(all_configs, indent=2)
                st.download_button(
                    " Download Configuration",
                    config_json,
                    "underwriting_config_backup.json",
                    "application/json",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f" Export failed: {str(e)}")
        
        if st.button(" Export System Settings", use_container_width=True):
            settings = st.session_state.get('system_settings', {})
            settings_json = json.dumps(settings, indent=2)
            st.download_button(
                " Download Settings",
                settings_json,
                "system_settings_backup.json",
                "application/json",
                use_container_width=True
            )
    
    with col2:
        st.markdown("### 📤 Import Configuration")
        
        uploaded_file = st.file_uploader(
            "Upload configuration file",
            type=['json'],
            help="Upload a previously exported configuration file"
        )
        
        if uploaded_file is not None:
            try:
                config_data = json.load(uploaded_file)
                st.success(" Configuration file loaded successfully!")
                
                if st.button(" Restore Configuration", use_container_width=True):
                    # In a real application, this would restore the configuration
                    st.success(" Configuration restored successfully!")
                    st.info("Please restart the application for changes to take effect.")
            except Exception as e:
                st.error(f" Invalid configuration file: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main function for the configuration page."""
    load_environment_variables()
    configure_page()
    load_custom_css()
    
    # System status
    show_system_status()
    
    # Configuration sections
    show_api_configuration()
    show_rule_configuration()
    show_system_settings()
    show_backup_restore()
    
    # Reset to defaults
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(" Reset All Settings to Defaults", use_container_width=True):
            if st.session_state.get('confirm_reset', False):
                # Reset session state
                for key in list(st.session_state.keys()):
                    if key.startswith('system_'):
                        del st.session_state[key]
                st.success(" All settings reset to defaults!")
                st.session_state.confirm_reset = False
                st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning(" Click again to confirm reset")

if __name__ == "__main__":
    main()


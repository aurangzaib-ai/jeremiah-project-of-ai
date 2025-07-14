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
import time
from datetime import datetime
import shutil

# Set up fixed path for rules directory
config_dir = Path(r"C:\Users\LAPTOP OUTLET\config")
rules_dir = config_dir / "rules"

# Create directories if they don't exist
rules_dir.mkdir(parents=True, exist_ok=True)

# Try to import git (make it optional)
GIT_AVAILABLE = False
try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    pass

from underwriting.utils.env_loader import load_environment_variables

def configure_page():
    """Configure the page settings."""
    st.set_page_config(
        page_title="Configuration - Underwriting System",
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
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background-color: #20c997;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #1aa179;
        transform: translateY(-2px);
    }
    .danger-zone {
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 1.5rem;
        background-color: #fff5f5;
    }
    .rule-item {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .rule-item:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def show_system_status():
    """Display system status and health checks with enhanced visuals."""
    st.markdown("""
    <div class="config-header">
        <h1>System Configuration</h1>
        <p>Manage Settings, API Keys, and System Health</p>
        <p>(WIP) Portfolio Project managed by <a href="https://jeremiahconnelly.dev" target="_blank" style="color: white; text-decoration: underline;">Jeremiah Connelly</a></p>   
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Rules Directory", str(rules_dir))
        if rules_dir.exists():
            st.success("✓ Directory accessible")
        else:
            st.error("Directory not found")
    
    with col2:
        rule_count = len(list(rules_dir.glob("underwriting_rules_standard_*.json")))
        st.metric("Rule Sets Available", rule_count)
    
    with col3:
        try:
            st.metric("System Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except:
            st.error("System time unavailable")

def show_api_configuration():
    """Display API configuration settings with enhanced interface."""
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## API Configuration Center")
    
    with st.expander("External Service APIs", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Credit Score API Key", 
                        value=os.getenv("CREDIT_SCORE_API_KEY", ""),
                        type="password",
                        help="API key for credit score verification service")
            
            st.text_input("Fraud Detection API Key", 
                        value=os.getenv("FRAUD_API_KEY", ""),
                        type="password",
                        help="API key for fraud detection service")
        
        with col2:
            st.text_input("Bank Verification API Key", 
                        value=os.getenv("BANK_VERIFICATION_API_KEY", ""),
                        type="password",
                        help="API key for bank account verification")
            
            st.text_input("Identity Verification API Key", 
                        value=os.getenv("IDENTITY_API_KEY", ""),
                        type="password",
                        help="API key for identity verification service")
    
    with st.expander("Internal Service Configuration"):
        st.text_input("Underwriting Engine URL",
                     value=os.getenv("UNDERWRITING_ENGINE_URL", "http://localhost:8000"),
                     help="URL for the underwriting decision engine")
        
        st.number_input("Decision Timeout (seconds)",
                      min_value=1,
                      max_value=60,
                      value=int(os.getenv("DECISION_TIMEOUT", 10)),
                      help="Timeout for underwriting decisions")
    
    st.markdown("</div>", unsafe_allow_html=True)

def load_rules_file(rule_set):
    """Safely load rules file with proper error handling."""
    rule_file = rules_dir / f"underwriting_rules_standard_{rule_set}.json"
    
    if not rule_file.exists():
        return None, f"Rule file not found: {rule_file}"
    
    try:
        with open(rule_file, 'r', encoding='utf-8') as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON in rule file: {str(e)}"
    except Exception as e:
        return None, f"Error loading rule file: {str(e)}"

def save_rules_file(rule_set, rules):
    """Save rules to file with proper error handling."""
    rule_file = rules_dir / f"underwriting_rules_standard_{rule_set}.json"
    
    try:
        with open(rule_file, 'w', encoding='utf-8') as f:
            json.dump(rules, f, indent=4)
        return True, None
    except Exception as e:
        return False, f"Error saving rule file: {str(e)}"

def show_rule_configuration():
    """Display comprehensive rule configuration management."""
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## Underwriting Rules Configuration Center")
    
    rule_sets = ["standard", "conservative", "liberal", "custom1", "custom2"]
    selected_rule_set = st.selectbox(
        "Select Rule Set to Configure",
        rule_sets,
        help="Choose which rule configuration to view or modify",
        key="rule_set_selector"
    )
    
    rules, error = load_rules_file(selected_rule_set)
    
    if error:
        st.error(error)
        if st.button(f"Create New {selected_rule_set.title()} Rule Set", key=f"create_{selected_rule_set}"):
            try:
                default_rules = {
                    "ruleset_name": f"{selected_rule_set.title()} Underwriting Rules",
                    "version": "1.0",
                    "last_updated": datetime.now().isoformat(),
                    "criteria": [
                        {
                            "name": "Minimum Credit Score",
                            "description": "Applicant must have a credit score of at least 650 to qualify.",
                            "field": "credit_score",
                            "operator": ">=",
                            "value": 650
                        }
                    ],
                    "decision_logic": {
                        "accept_if_all_true": True,
                        "deny_if_any_false": True
                    }
                }
                rule_file = rules_dir / f"underwriting_rules_standard_{selected_rule_set}.json"
                with open(rule_file, 'w', encoding='utf-8') as f:
                    json.dump(default_rules, f, indent=4)
                st.success(f"Created new {selected_rule_set} rule set at: {rule_file}")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating new rule set: {str(e)}")
    else:
        st.markdown(f"### Editing: {rules.get('ruleset_name', selected_rule_set.title())}")
        col1, col2 = st.columns(2)
        with col1:
            rules["ruleset_name"] = st.text_input("Rule Set Name", value=rules.get("ruleset_name", ""))
        with col2:
            rules["version"] = st.text_input("Version", value=rules.get("version", "1.0"))
        st.markdown("### Decision Logic")
        col1, col2 = st.columns(2)
        with col1:
            rules["decision_logic"]["accept_if_all_true"] = st.checkbox(
                "Accept if all criteria are met",
                value=rules.get("decision_logic", {}).get("accept_if_all_true", True)
            )
        with col2:
            rules["decision_logic"]["deny_if_any_false"] = st.checkbox(
                "Deny if any criteria fail",
                value=rules.get("decision_logic", {}).get("deny_if_any_false", True)
            )
        st.markdown("### Underwriting Criteria")
        st.markdown("Add, edit, or remove the criteria used for underwriting decisions.")
        if "criteria" not in rules:
            rules["criteria"] = []
        for i, criterion in enumerate(rules["criteria"]):
            with st.expander(f"Criterion {i+1}: {criterion.get('name', 'Unnamed')}", expanded=True):
                st.markdown('<div class="rule-item">', unsafe_allow_html=True)
                col1, col2 = st.columns([3, 1])
                with col1:
                    criterion["name"] = st.text_input("Criterion Name", value=criterion.get("name", ""), key=f"name_{i}")
                with col2:
                    criterion["field"] = st.text_input("Data Field", value=criterion.get("field", ""), key=f"field_{i}")
                criterion["description"] = st.text_area("Description", value=criterion.get("description", ""), key=f"desc_{i}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    criterion["operator"] = st.selectbox(
                        "Operator",
                        options=[">", ">=", "<", "<=", "==", "!=", "in", "not in"],
                        index=[">", ">=", "<", "<=", "==", "!=", "in", "not in"].index(criterion.get("operator", ">=")),
                        key=f"op_{i}"
                    )
                with col2:
                    if isinstance(criterion.get("value"), bool):
                        criterion["value"] = st.checkbox("Value", value=criterion.get("value", False), key=f"val_{i}")
                    elif isinstance(criterion.get("value"), (int, float)):
                        criterion["value"] = st.number_input("Value", value=criterion.get("value", 0), key=f"val_{i}")
                    else:
                        criterion["value"] = st.text_input("Value", value=str(criterion.get("value", "")), key=f"val_{i}")
                with col3:
                    if st.button(" Remove", key=f"remove_{i}"):
                        rules["criteria"].pop(i)
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        if st.button(" Add New Criterion"):
            rules["criteria"].append({
                "name": "New Criterion",
                "description": "",
                "field": "",
                "operator": ">=",
                "value": 0
            })
            st.rerun()
        if st.button(" Save Changes", type="primary"):
            rules["last_updated"] = datetime.now().isoformat()
            success, error = save_rules_file(selected_rule_set, rules)
            if success:
                st.success("Rules saved successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(error)
    st.markdown('</div>', unsafe_allow_html=True)

def show_system_settings():
    """Display comprehensive system settings and preferences."""
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## System Settings Configuration")
    with st.expander("General Settings"):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Maximum Concurrent Requests", min_value=1, max_value=100, value=int(os.getenv("MAX_CONCURRENT_REQUESTS", 10)), key="max_concurrent")
            st.selectbox("Logging Level", options=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], index=1, key="log_level")
        with col2:
            st.number_input("Data Retention Days", min_value=1, max_value=3650, value=int(os.getenv("DATA_RETENTION_DAYS", 90)), key="data_retention")
            st.checkbox("Enable Audit Logging", value=os.getenv("AUDIT_LOGGING", "true").lower() == "true", key="audit_logging")
    with st.expander("Notification Settings"):
        st.text_input("Admin Email", value=os.getenv("ADMIN_EMAIL", "admin@example.com"), key="admin_email")
        st.checkbox("Email Alerts for Critical Issues", value=os.getenv("EMAIL_ALERTS", "true").lower() == "true", key="email_alerts")
    if st.button("Save System Settings", type="primary"):
        st.success("System settings updated (simulated)")
    st.markdown('</div>', unsafe_allow_html=True)

def show_backup_restore():
    """Display comprehensive backup and restore functionality."""
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## Backup & Restore Center")
    tab1, tab2 = st.tabs(["Backup", "Restore"])
    with tab1:
        st.markdown("### Create System Backup")
        if GIT_AVAILABLE:
            try:
                repo = git.Repo(search_parent_directories=True)
                st.markdown(f"**Git Repository Detected:** `{repo.working_dir}`")
                if st.button("Create Git Commit Backup"):
                    with st.spinner("Creating backup commit..."):
                        try:
                            repo.git.add(all=True)
                            repo.index.commit(f"Backup {datetime.now().isoformat()}")
                            st.success("Backup commit created successfully")
                        except Exception as e:
                            st.error(f"Error creating backup commit: {str(e)}")
            except:
                st.warning("No Git repository found in parent directories")
        st.markdown("### Manual Backup")
        if st.button("Download Rules Backup"):
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"underwriting_rules_standard_backup_{timestamp}.zip"
                backup_path = Path(backup_name)
                with st.spinner("Creating backup archive..."):
                    shutil.make_archive(backup_path.stem, 'zip', rules_dir)
                    with open(backup_name, "rb") as f:
                        st.download_button(label="Download Backup", data=f, file_name=backup_name, mime="application/zip")
            except Exception as e:
                st.error(f"Backup failed: {str(e)}")
    with tab2:
        st.markdown("### Restore from Backup")
        uploaded_file = st.file_uploader("Upload Backup ZIP", type="zip")
        if uploaded_file is not None:
            st.warning("Restoring will overwrite all current rules. Continue?")
            if st.button("Confirm Restore"):
                try:
                    for file in rules_dir.glob("underwriting_rules_standard_*.json"):
                        file.unlink()
                    with st.spinner("Restoring backup..."):
                        with open("temp_backup.zip", "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        shutil.unpack_archive("temp_backup.zip", rules_dir)
                        os.remove("temp_backup.zip")
                    st.success("Restore completed successfully!")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"Restore failed: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main function for the configuration page."""
    try:
        load_environment_variables()
    except Exception as e:
        st.warning(f"Could not load environment variables: {str(e)}")
    configure_page()
    load_custom_css()
    show_system_status()
    show_api_configuration()
    show_rule_configuration()
    show_system_settings()
    show_backup_restore()
    st.markdown("---")
    st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
    st.markdown("## Danger Zone")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.get('confirm_reset', False):
            st.warning("Are you sure you want to reset ALL settings to defaults?")
            if st.button("Confirm Reset All Settings", type="primary", use_container_width=True):
                st.error("Reset functionality not implemented in this demo")
                st.session_state.confirm_reset = False
        else:
            if st.button("Reset All Settings to Defaults", type="secondary", use_container_width=True):
                st.session_state.confirm_reset = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()


"""
Homepage for the Streamlit underwriting application.

This is the main landing page that users see when they access the application.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the main app
from underwriting.streamlit.app import main

if __name__ == "__main__":
    main()



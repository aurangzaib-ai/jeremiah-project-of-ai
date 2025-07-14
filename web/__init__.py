"""
Web interface for the underwriting system.

This module provides a Flask-based web interface for the automobile insurance
underwriting system, including forms for applicant input, result display,
and A/B testing functionality.
"""

from .app import create_app, app
from .forms import ApplicantForm, ABTestForm
from .routes import main_bp, api_bp

__all__ = [
    "create_app",
    "app", 
    "ApplicantForm",
    "ABTestForm",
    "main_bp",
    "api_bp"
]


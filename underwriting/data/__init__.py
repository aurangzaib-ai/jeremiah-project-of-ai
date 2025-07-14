"""
Data handling and management.

This module provides functionality for managing applicant data, generating
test samples, and handling data validation. It serves as the data layer
for the underwriting system.
"""

from .sample_generator import (
    create_sample_applicants,
    print_applicant_summary
)

__all__ = [
    "create_sample_applicants",
    "print_applicant_summary"
]


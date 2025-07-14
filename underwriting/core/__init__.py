"""
Core underwriting business logic and models.

This module contains the fundamental components of the underwriting system:
- Data models for applicants, drivers, vehicles, violations, and claims
- Main underwriting engine with LLM integration
- Business rule processing logic
- Custom exceptions for error handling

The core module is designed to be independent of specific AI providers,
testing frameworks, or user interfaces.
"""

from .models import (
    Applicant,
    Driver,
    Vehicle, 
    Violation,
    Claim,
    UnderwritingResult,
    UnderwritingDecision
)

from .engine import UnderwritingEngine
from .exceptions import (
    UnderwritingError,
    RuleValidationError,
    LLMError,
    ConfigurationError
)

__all__ = [
    # Models
    "Applicant",
    "Driver",
    "Vehicle",
    "Violation", 
    "Claim",
    "UnderwritingResult",
    "UnderwritingDecision",
    
    # Engine
    "UnderwritingEngine",
    
    # Exceptions
    "UnderwritingError",
    "RuleValidationError",
    "LLMError", 
    "ConfigurationError"
]


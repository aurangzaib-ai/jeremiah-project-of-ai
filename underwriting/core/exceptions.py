"""
Custom exceptions for the underwriting system.

This module defines specific exception classes for different types of errors
that can occur during underwriting operations. Using custom exceptions allows
for more precise error handling and better debugging.
"""

class UnderwritingError(Exception):
    """Base exception class for all underwriting-related errors."""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        """
        Initialize underwriting error.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code for categorization
            details: Additional error details for debugging
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNDERWRITING_ERROR"
        self.details = details or {}
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class RuleValidationError(UnderwritingError):
    """Raised when underwriting rules are invalid or cannot be processed."""
    
    def __init__(self, message: str, rule_id: str = None, rule_file: str = None):
        """
        Initialize rule validation error.
        
        Args:
            message: Error description
            rule_id: ID of the problematic rule
            rule_file: Path to the rule file
        """
        details = {}
        if rule_id:
            details["rule_id"] = rule_id
        if rule_file:
            details["rule_file"] = rule_file
            
        super().__init__(
            message=message,
            error_code="RULE_VALIDATION_ERROR", 
            details=details
        )
        self.rule_id = rule_id
        self.rule_file = rule_file


class LLMError(UnderwritingError):
    """Raised when LLM operations fail or return invalid responses."""
    
    def __init__(self, message: str, provider: str = None, model: str = None, 
                 response_text: str = None):
        """
        Initialize LLM error.
        
        Args:
            message: Error description
            provider: LLM provider (e.g., "openai")
            model: Model name (e.g., "gpt-4")
            response_text: Raw LLM response that caused the error
        """
        details = {}
        if provider:
            details["provider"] = provider
        if model:
            details["model"] = model
        if response_text:
            details["response_text"] = response_text[:500]  # Truncate for logging
            
        super().__init__(
            message=message,
            error_code="LLM_ERROR",
            details=details
        )
        self.provider = provider
        self.model = model
        self.response_text = response_text


class ConfigurationError(UnderwritingError):
    """Raised when configuration is missing, invalid, or inconsistent."""
    
    def __init__(self, message: str, config_key: str = None, config_file: str = None):
        """
        Initialize configuration error.
        
        Args:
            message: Error description
            config_key: Specific configuration key that's problematic
            config_file: Path to the configuration file
        """
        details = {}
        if config_key:
            details["config_key"] = config_key
        if config_file:
            details["config_file"] = config_file
            
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            details=details
        )
        self.config_key = config_key
        self.config_file = config_file


class ApplicantValidationError(UnderwritingError):
    """Raised when applicant data is invalid or incomplete."""
    
    def __init__(self, message: str, applicant_id: str = None, field_name: str = None):
        """
        Initialize applicant validation error.
        
        Args:
            message: Error description
            applicant_id: ID of the problematic applicant
            field_name: Specific field that failed validation
        """
        details = {}
        if applicant_id:
            details["applicant_id"] = applicant_id
        if field_name:
            details["field_name"] = field_name
            
        super().__init__(
            message=message,
            error_code="APPLICANT_VALIDATION_ERROR",
            details=details
        )
        self.applicant_id = applicant_id
        self.field_name = field_name


class TestingError(UnderwritingError):
    """Raised when A/B testing operations fail."""
    
    def __init__(self, message: str, test_id: str = None, variant_id: str = None):
        """
        Initialize testing error.
        
        Args:
            message: Error description
            test_id: ID of the test that failed
            variant_id: ID of the variant that caused the error
        """
        details = {}
        if test_id:
            details["test_id"] = test_id
        if variant_id:
            details["variant_id"] = variant_id
            
        super().__init__(
            message=message,
            error_code="TESTING_ERROR",
            details=details
        )
        self.test_id = test_id
        self.variant_id = variant_id


# Exception hierarchy for easy catching
CORE_EXCEPTIONS = (
    UnderwritingError,
    RuleValidationError,
    LLMError,
    ConfigurationError,
    ApplicantValidationError
)

TESTING_EXCEPTIONS = (
    TestingError,
)

ALL_EXCEPTIONS = CORE_EXCEPTIONS + TESTING_EXCEPTIONS


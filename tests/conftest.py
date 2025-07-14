"""
Test configuration and fixtures.

This module provides pytest configuration and shared fixtures for testing
the underwriting system.
"""

import pytest
import os
from pathlib import Path

# Test configuration
pytest_plugins = []

# Set test environment variables
os.environ["UNDERWRITING_LOG_LEVEL"] = "DEBUG"
os.environ["UNDERWRITING_TEST_MODE"] = "true"


@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return {
        "rules": {
            "hard_stops": {
                "rules": [
                    {
                        "rule_id": "TEST001",
                        "name": "Test Rule",
                        "description": "Test rule for unit testing"
                    }
                ]
            }
        }
    }


@pytest.fixture
def temp_config_file(tmp_path, sample_config):
    """Create temporary configuration file for testing."""
    import json
    
    config_file = tmp_path / "test_config.json"
    with open(config_file, 'w') as f:
        json.dump(sample_config, f)
    
    return str(config_file)


@pytest.fixture
def mock_openai_response():
    """Provide mock OpenAI response for testing."""
    return """Decision: ACCEPT
Primary Reason: Clean record mature driver
Triggered Rules: ACC001
Risk Factors: None
Additional Notes: Excellent credit score and driving history"""


# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "fixtures"


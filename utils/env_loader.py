"""
Environment configuration loader with fallback support.

This module provides utilities for loading environment variables
from .env files with proper fallback handling.
"""

import os
from pathlib import Path
from typing import Optional


def load_environment_variables(env_file: Optional[str] = None) -> None:
    """
    Load environment variables from .env file if available.
    
    This function provides a safe way to load environment variables
    without requiring python-dotenv as a hard dependency.
    
    Args:
        env_file: Path to .env file (defaults to .env in current directory)
    """
    if env_file is None:
        env_file = ".env"
    
    env_path = Path(env_file)
    
    # Try to use python-dotenv if available
    try:
        from dotenv import load_dotenv
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Loaded environment variables from {env_path}")
        else:
            print(f"No .env file found at {env_path}")
    except ImportError:
        # Fallback: manually parse .env file
        if env_path.exists():
            _load_env_file_manually(env_path)
            print(f"Loaded environment variables from {env_path} (manual parsing)")
        else:
            print(f"No .env file found at {env_path}")


def _load_env_file_manually(env_path: Path) -> None:
    """
    Manually parse and load .env file without python-dotenv.
    
    Args:
        env_path: Path to the .env file
    """
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE format
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Set environment variable if not already set
                    if key and key not in os.environ:
                        os.environ[key] = value
                        
    except Exception as e:
        print(f"Warning: Could not parse .env file: {e}")


def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get environment variable with optional default and validation.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        
    Returns:
        Environment variable value or default
        
    Raises:
        ValueError: If required variable is not found
    """
    value = os.environ.get(key, default)
    
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' not found")
    
    return value


def get_openai_api_key() -> str:
    """
    Get OpenAI API key from environment.
    
    Returns:
        OpenAI API key
        
    Raises:
        ValueError: If API key is not found
    """
    api_key = get_env_var('OPENAI_API_KEY', required=True)
    
    if not api_key or api_key.strip() == '':
        raise ValueError(
            "OpenAI API key is required. Please set OPENAI_API_KEY environment variable."
        )
    
    return api_key.strip()


def is_debug_mode() -> bool:
    """
    Check if debug mode is enabled.
    
    Returns:
        True if debug mode is enabled
    """
    debug_value = get_env_var('FLASK_DEBUG', 'false').lower()
    return debug_value in ('true', '1', 'yes', 'on')


def get_flask_secret_key() -> str:
    """
    Get Flask secret key from environment with fallback.
    
    Returns:
        Flask secret key
    """
    return get_env_var(
        'SECRET_KEY', 
        'dev-secret-key-change-in-production-' + str(hash('underwriting'))
    )



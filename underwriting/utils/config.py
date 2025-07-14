"""
Configuration management utilities.

This module provides functions for loading, validating, and accessing
configuration data from various sources including JSON files, YAML files,
and environment variables.
"""

import json
import os
from typing import Any, Dict, Optional, Union
from pathlib import Path

from ..core.exceptions import ConfigurationError


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration data
        
    Raises:
        ConfigurationError: If file cannot be loaded or parsed
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise ConfigurationError(
            f"Configuration file not found: {config_path}",
            config_file=str(config_path)
        )
    
    try:
        with open(config_path, 'r') as f:
            if config_path.suffix.lower() == '.json':
                return json.load(f)
            else:
                raise ConfigurationError(
                    f"Unsupported configuration file format: {config_path.suffix}",
                    config_file=str(config_path)
                )
    except json.JSONDecodeError as e:
        raise ConfigurationError(
            f"Invalid JSON in configuration file: {e}",
            config_file=str(config_path)
        )
    except Exception as e:
        raise ConfigurationError(
            f"Error loading configuration file: {e}",
            config_file=str(config_path)
        )


def get_config_value(config: Dict[str, Any], key_path: str, 
                    default: Any = None) -> Any:
    """
    Get a configuration value using dot notation.
    
    Args:
        config: Configuration dictionary
        key_path: Dot-separated path to the value (e.g., "database.host")
        default: Default value if key is not found
        
    Returns:
        Configuration value or default
        
    Example:
        >>> config = {"database": {"host": "localhost", "port": 5432}}
        >>> get_config_value(config, "database.host")
        "localhost"
        >>> get_config_value(config, "database.timeout", 30)
        30
    """
    keys = key_path.split('.')
    value = config
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default


def validate_config(config: Dict[str, Any], required_keys: list) -> None:
    """
    Validate that required configuration keys are present.
    
    Args:
        config: Configuration dictionary to validate
        required_keys: List of required key paths (dot notation supported)
        
    Raises:
        ConfigurationError: If any required key is missing
    """
    missing_keys = []
    
    for key_path in required_keys:
        if get_config_value(config, key_path) is None:
            missing_keys.append(key_path)
    
    if missing_keys:
        raise ConfigurationError(
            f"Missing required configuration keys: {', '.join(missing_keys)}",
            config_key=missing_keys[0] if len(missing_keys) == 1 else None
        )


def get_env_config(prefix: str = "UNDERWRITING_") -> Dict[str, str]:
    """
    Get configuration values from environment variables.
    
    Args:
        prefix: Prefix for environment variable names
        
    Returns:
        Dictionary of environment configuration values
        
    Example:
        >>> # With UNDERWRITING_API_KEY=abc123 in environment
        >>> get_env_config()
        {"API_KEY": "abc123"}
    """
    env_config = {}
    
    for key, value in os.environ.items():
        if key.startswith(prefix):
            config_key = key[len(prefix):]
            env_config[config_key] = value
    
    return env_config


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple configuration dictionaries.
    
    Later configurations override earlier ones for conflicting keys.
    
    Args:
        *configs: Configuration dictionaries to merge
        
    Returns:
        Merged configuration dictionary
    """
    merged = {}
    
    for config in configs:
        if config:
            merged.update(config)
    
    return merged


# Default configuration paths
DEFAULT_CONFIG_PATHS = [
    "config/underwriting.json",
    "underwriting.json",
    os.path.expanduser("~/.underwriting/config.json")
]


def load_default_config() -> Dict[str, Any]:
    """
    Load configuration from default locations.
    
    Searches for configuration files in order of preference and loads
    the first one found.
    
    Returns:
        Configuration dictionary
        
    Raises:
        ConfigurationError: If no configuration file is found
    """
    for config_path in DEFAULT_CONFIG_PATHS:
        if os.path.exists(config_path):
            return load_config(config_path)
    
    raise ConfigurationError(
        f"No configuration file found in default locations: {DEFAULT_CONFIG_PATHS}"
    )


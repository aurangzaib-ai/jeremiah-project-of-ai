"""
A/B Testing Framework.

This module provides comprehensive A/B testing capabilities for underwriting
rules and prompt templates. It includes statistical analysis, business impact
assessment, and detailed reporting functionality.

The testing framework is designed to support data-driven decision making
for underwriting optimization while maintaining statistical rigor.
"""

from .ab_engine import (
    ABTestEngine,
    TestConfiguration,
    TestResult,
    ComparisonMetrics
)

from .statistical_analysis import (
    StatisticalAnalyzer,
    BusinessImpactCalculator,
    StatisticalTest,
    BusinessImpactAnalysis
)

__all__ = [
    # A/B Testing Engine
    "ABTestEngine",
    "TestConfiguration", 
    "TestResult",
    "ComparisonMetrics",
    
    # Statistical Analysis
    "StatisticalAnalyzer",
    "BusinessImpactCalculator",
    "StatisticalTest",
    "BusinessImpactAnalysis",

    # Underwriting Rules and Prompts
    "underwriting_rules_standard",
    "underwriting_rules_conservative",
    "underwriting_rules_liberal"
]


#!/usr/bin/env python3
"""
Comprehensive A/B Testing Framework for Automobile Insurance Underwriting
Command-line interface for running various A/B tests and generating reports.
"""

import os
import sys
import argparse
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from underwriting.testing.ab_engine import ABTestEngine, TestConfiguration
from underwriting.testing.statistical_analysis import StatisticalAnalyzer, BusinessImpactCalculator
from underwriting.ai.prompts import PromptTemplateFactory, PromptTestConfiguration, PromptVariant
from underwriting.data.sample_generator import create_sample_applicants
from underwriting.core.models import Applicant

class ABTestRunner:
    """Main A/B testing framework runner."""
    
    def __init__(self):
        """Initialize the A/B test runner."""
        self.ab_engine = ABTestEngine()
        self.statistical_analyzer = StatisticalAnalyzer()
        self.business_calculator = BusinessImpactCalculator()
        self.applicants = create_sample_applicants()
        
        # Register default configurations
        self._register_default_configurations()
    
    def _register_default_configurations(self):
        """Register default test configurations."""
        
        # Rule-based configurations
        rule_configs = [
            TestConfiguration(
                variant_id="standard",
                name="Standard Rules",
                description="Original balanced underwriting rules",
                rules_file="underwriting_rules.json"
            ),
            TestConfiguration(
                variant_id="conservative",
                name="Conservative Rules", 
                description="Stricter underwriting criteria",
                rules_file="underwriting_rules_conservative.json"
            ),
            TestConfiguration(
                variant_id="liberal",
                name="Liberal Rules",
                description="More accepting underwriting criteria", 
                rules_file="underwriting_rules_liberal.json"
            )
        ]
        
        for config in rule_configs:
            self.ab_engine.register_test_configuration(config)
        
        # Prompt-based configurations
        prompt_config = PromptTestConfiguration()
        for variant_id, config_data in prompt_config.get_all_configurations().items():
            test_config = TestConfiguration(
                variant_id=f"prompt_{variant_id}",
                name=config_data['name'],
                description=config_data['description'],
                rules_file=config_data['rules_file'],
                prompt_template=config_data['prompt_template'],
                parameters=config_data['parameters']
            )
            self.ab_engine.register_test_configuration(test_config)
    
    def run_rule_comparison(self, variant_a: str, variant_b: str, 
                           applicants: Optional[List[Applicant]] = None) -> Dict[str, Any]:
        """Run A/B test comparing different rule configurations."""
        
        if applicants is None:
            applicants = self.applicants
        
        print(f"\n{'='*80}")
        print(f"RULE COMPARISON A/B TEST")
        print(f"{'='*80}")
        print(f"Variant A: {variant_a}")
        print(f"Variant B: {variant_b}")
        print(f"Sample Size: {len(applicants)} applicants")
        
        # Run comparison
        batch_results = self.ab_engine.run_batch_comparison(applicants, variant_a, variant_b)
        
        # Calculate metrics
        metrics = self.ab_engine.calculate_comparison_metrics(variant_a, variant_b)
        
        # Print comparison report
        self.ab_engine.print_comparison_report(metrics)
        
        # Statistical analysis
        results_a = [r for r in self.ab_engine.test_results if r.variant_id == variant_a]
        results_b = [r for r in self.ab_engine.test_results if r.variant_id == variant_b]
        
        print(f"\n{'-'*50}")
        print("STATISTICAL ANALYSIS")
        print(f"{'-'*50}")
        
        # Chi-square test for decision distribution
        chi_square_test = self.statistical_analyzer.chi_square_test(results_a, results_b)
        print(f"\n{chi_square_test.test_name}:")
        print(f"  {chi_square_test.interpretation}")
        
        # Proportion tests for each decision type
        for decision_type in ['accept', 'deny', 'adjudicate']:
            prop_test = self.statistical_analyzer.proportion_z_test(results_a, results_b, decision_type)
            print(f"\n{prop_test.test_name}:")
            print(f"  {prop_test.interpretation}")
        
        # Processing time test
        time_test = self.statistical_analyzer.t_test_processing_time(results_a, results_b)
        print(f"\n{time_test.test_name}:")
        print(f"  {time_test.interpretation}")
        
        # Business impact analysis
        business_impact = self.business_calculator.calculate_impact(metrics)
        self._print_business_impact(business_impact)
        
        return {
            'metrics': metrics,
            'statistical_tests': [chi_square_test, time_test],
            'business_impact': business_impact,
            'batch_results': batch_results
        }
    
    def run_prompt_comparison(self, variant_a: str, variant_b: str,
                             applicants: Optional[List[Applicant]] = None) -> Dict[str, Any]:
        """Run A/B test comparing different prompt templates."""
        
        # Add prompt_ prefix if not present
        if not variant_a.startswith('prompt_'):
            variant_a = f"prompt_{variant_a}"
        if not variant_b.startswith('prompt_'):
            variant_b = f"prompt_{variant_b}"
        
        return self.run_rule_comparison(variant_a, variant_b, applicants)
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run a comprehensive suite of A/B tests."""
        
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE A/B TEST SUITE")
        print(f"{'='*80}")
        
        results = {}
        
        # Rule comparison tests
        rule_comparisons = [
            ("standard", "conservative"),
            ("standard", "liberal"),
            ("conservative", "liberal")
        ]
        
        print(f"\n{'-'*60}")
        print("RULE COMPARISON TESTS")
        print(f"{'-'*60}")
        
        for variant_a, variant_b in rule_comparisons:
            print(f"\nRunning: {variant_a} vs {variant_b}")
            test_key = f"rules_{variant_a}_vs_{variant_b}"
            results[test_key] = self.run_rule_comparison(variant_a, variant_b)
            
            # Clear results between tests
            self.ab_engine.clear_results()
        
        # Prompt comparison tests
        prompt_comparisons = [
            ("conservative", "liberal"),
            ("balanced", "detailed"),
            ("detailed", "concise")
        ]
        
        print(f"\n{'-'*60}")
        print("PROMPT TEMPLATE TESTS")
        print(f"{'-'*60}")
        
        for variant_a, variant_b in prompt_comparisons:
            print(f"\nRunning: {variant_a} vs {variant_b} prompts")
            test_key = f"prompts_{variant_a}_vs_{variant_b}"
            results[test_key] = self.run_prompt_comparison(variant_a, variant_b)
            
            # Clear results between tests
            self.ab_engine.clear_results()
        
        return results
    
    def run_single_variant_analysis(self, variant_id: str,
                                   applicants: Optional[List[Applicant]] = None) -> Dict[str, Any]:
        """Run analysis on a single variant to understand its behavior."""
        
        if applicants is None:
            applicants = self.applicants
        
        print(f"\n{'='*80}")
        print(f"SINGLE VARIANT ANALYSIS: {variant_id.upper()}")
        print(f"{'='*80}")
        
        # Run all applicants through the variant
        results = []
        for applicant in applicants:
            result_a, _ = self.ab_engine.run_single_comparison(applicant, variant_id, variant_id)
            results.append(result_a)
        
        # Calculate decision distribution
        total = len(results)
        accept_count = sum(1 for r in results if r.decision.value == 'accept')
        deny_count = sum(1 for r in results if r.decision.value == 'deny')
        adjudicate_count = sum(1 for r in results if r.decision.value == 'adjudicate')
        
        print(f"\nDECISION DISTRIBUTION:")
        print(f"  Accept: {accept_count}/{total} ({accept_count/total*100:.1f}%)")
        print(f"  Deny: {deny_count}/{total} ({deny_count/total*100:.1f}%)")
        print(f"  Adjudicate: {adjudicate_count}/{total} ({adjudicate_count/total*100:.1f}%)")
        
        # Performance metrics
        avg_time = sum(r.processing_time_ms for r in results) / len(results)
        error_count = sum(1 for r in results if r.error)
        
        print(f"\nPERFORMANCE METRICS:")
        print(f"  Average Processing Time: {avg_time:.1f}ms")
        print(f"  Error Rate: {error_count}/{total} ({error_count/total*100:.1f}%)")
        
        # Detailed results
        print(f"\nDETAILED RESULTS:")
        for result in results:
            status = "ERROR" if result.error else result.decision.value.upper()
            print(f"  {result.applicant_id}: {status} - {result.reason}")
        
        return {
            'variant_id': variant_id,
            'results': results,
            'decision_distribution': {
                'accept': accept_count,
                'deny': deny_count, 
                'adjudicate': adjudicate_count,
                'total': total
            },
            'performance': {
                'avg_processing_time_ms': avg_time,
                'error_count': error_count,
                'error_rate': error_count/total*100
            }
        }
    
    def _print_business_impact(self, impact):
        """Print business impact analysis."""
        
        print(f"\n{'-'*50}")
        print("BUSINESS IMPACT ANALYSIS")
        print(f"{'-'*50}")
        
        print(f"Monthly Application Volume: {impact.estimated_monthly_applications:,}")
        print(f"Risk Level: {impact.risk_level}")
        
        print(f"\nDecision Rate Changes:")
        print(f"  Accept Rate: {impact.accept_rate_change:+.1f}% ({impact.additional_accepts_monthly:+,} monthly)")
        print(f"  Deny Rate: {impact.deny_rate_change:+.1f}% ({impact.additional_denies_monthly:+,} monthly)")
        print(f"  Adjudicate Rate: {impact.adjudicate_rate_change:+.1f}% ({impact.additional_adjudications_monthly:+,} monthly)")
        
        print(f"\nEstimated Business Impact:")
        print(f"  Loss Ratio Change: {impact.estimated_loss_ratio_change:+.3f}")
        print(f"  Processing Cost Change: ${impact.estimated_processing_cost_change:+,.0f}/month")
        print(f"  Market Share Impact: {impact.estimated_market_share_impact:+.2f}%")
        
        if impact.risk_factors:
            print(f"\nRisk Factors:")
            for factor in impact.risk_factors:
                print(f"  • {factor}")
        
        if impact.recommendations:
            print(f"\nRecommendations:")
            for rec in impact.recommendations:
                print(f"  • {rec}")
    
    def export_comprehensive_report(self, results: Dict[str, Any], filename: str):
        """Export comprehensive test results to file."""
        
        # Prepare export data
        export_data = {
            'test_suite_timestamp': datetime.now().isoformat(),
            'test_configuration': {
                'sample_size': len(self.applicants),
                'confidence_level': self.statistical_analyzer.confidence_level,
                'monthly_applications': self.business_calculator.monthly_applications
            },
            'test_results': {}
        }
        
        # Process each test result
        for test_key, test_data in results.items():
            export_data['test_results'][test_key] = {
                'metrics': {
                    'variant_a_id': test_data['metrics'].variant_a_id,
                    'variant_b_id': test_data['metrics'].variant_b_id,
                    'total_tests': test_data['metrics'].total_tests,
                    'agreement_rate': test_data['metrics'].agreement_rate,
                    'decision_rates_a': {
                        'accept': test_data['metrics'].accept_rate_a,
                        'deny': test_data['metrics'].deny_rate_a,
                        'adjudicate': test_data['metrics'].adjudicate_rate_a
                    },
                    'decision_rates_b': {
                        'accept': test_data['metrics'].accept_rate_b,
                        'deny': test_data['metrics'].deny_rate_b,
                        'adjudicate': test_data['metrics'].adjudicate_rate_b
                    },
                    'performance': {
                        'avg_processing_time_a': test_data['metrics'].avg_processing_time_a,
                        'avg_processing_time_b': test_data['metrics'].avg_processing_time_b,
                        'error_rate_a': test_data['metrics'].error_rate_a,
                        'error_rate_b': test_data['metrics'].error_rate_b
                    }
                },
                'statistical_significance': [
                    {
                        'test_name': test.test_name,
                        'p_value': test.p_value,
                        'is_significant': test.is_significant,
                        'effect_size': test.effect_size,
                        'interpretation': test.interpretation
                    }
                    for test in test_data['statistical_tests']
                ],
                'business_impact': {
                    'risk_level': test_data['business_impact'].risk_level,
                    'accept_rate_change': test_data['business_impact'].accept_rate_change,
                    'deny_rate_change': test_data['business_impact'].deny_rate_change,
                    'adjudicate_rate_change': test_data['business_impact'].adjudicate_rate_change,
                    'estimated_loss_ratio_change': test_data['business_impact'].estimated_loss_ratio_change,
                    'estimated_processing_cost_change': test_data['business_impact'].estimated_processing_cost_change,
                    'risk_factors': test_data['business_impact'].risk_factors,
                    'recommendations': test_data['business_impact'].recommendations
                }
            }
        
        # Write to file
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\nComprehensive report exported to: {filename}")

def main():
    """Main CLI entry point."""
    
    parser = argparse.ArgumentParser(
        description="A/B Testing Framework for Automobile Insurance Underwriting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run rule comparison
  python ab_test_runner.py --rule-comparison standard conservative
  
  # Run prompt comparison  
  python ab_test_runner.py --prompt-comparison balanced liberal
  
  # Run comprehensive test suite
  python ab_test_runner.py --comprehensive
  
  # Analyze single variant
  python ab_test_runner.py --single-variant conservative
  
  # List available configurations
  python ab_test_runner.py --list-configs
        """
    )
    
    # Test type arguments
    parser.add_argument('--rule-comparison', nargs=2, metavar=('VARIANT_A', 'VARIANT_B'),
                       help='Compare two rule configurations')
    parser.add_argument('--prompt-comparison', nargs=2, metavar=('VARIANT_A', 'VARIANT_B'),
                       help='Compare two prompt templates')
    parser.add_argument('--comprehensive', action='store_true',
                       help='Run comprehensive test suite')
    parser.add_argument('--single-variant', metavar='VARIANT',
                       help='Analyze single variant behavior')
    
    # Configuration arguments
    parser.add_argument('--list-configs', action='store_true',
                       help='List available test configurations')
    parser.add_argument('--export', metavar='FILENAME',
                       help='Export results to JSON file')
    
    # Analysis parameters
    parser.add_argument('--confidence-level', type=float, default=0.95,
                       help='Statistical confidence level (default: 0.95)')
    parser.add_argument('--monthly-applications', type=int, default=10000,
                       help='Estimated monthly applications for business impact (default: 10000)')
    
    args = parser.parse_args()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key before running A/B tests.")
        sys.exit(1)
    
    # Initialize runner
    runner = ABTestRunner()
    runner.statistical_analyzer.confidence_level = args.confidence_level
    runner.business_calculator.monthly_applications = args.monthly_applications
    
    # Handle list configs
    if args.list_configs:
        print("Available Test Configurations:")
        print("=" * 50)
        
        print("\nRule Configurations:")
        for config_id, config in runner.ab_engine.test_configurations.items():
            if not config_id.startswith('prompt_'):
                print(f"  {config_id}: {config.name}")
                print(f"    {config.description}")
        
        print("\nPrompt Template Configurations:")
        for config_id, config in runner.ab_engine.test_configurations.items():
            if config_id.startswith('prompt_'):
                print(f"  {config_id.replace('prompt_', '')}: {config.name}")
                print(f"    {config.description}")
        
        return
    
    # Run tests based on arguments
    results = None
    
    if args.rule_comparison:
        variant_a, variant_b = args.rule_comparison
        results = {f"rule_comparison_{variant_a}_vs_{variant_b}": 
                  runner.run_rule_comparison(variant_a, variant_b)}
    
    elif args.prompt_comparison:
        variant_a, variant_b = args.prompt_comparison
        results = {f"prompt_comparison_{variant_a}_vs_{variant_b}": 
                  runner.run_prompt_comparison(variant_a, variant_b)}
    
    elif args.comprehensive:
        results = runner.run_comprehensive_test_suite()
    
    elif args.single_variant:
        variant = args.single_variant
        result = runner.run_single_variant_analysis(variant)
        print(f"\nSingle variant analysis completed for: {variant}")
    
    else:
        parser.print_help()
        return
    
    # Export results if requested
    if args.export and results:
        runner.export_comprehensive_report(results, args.export)

if __name__ == "__main__":
    main()


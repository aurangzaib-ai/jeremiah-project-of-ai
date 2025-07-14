from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import json
import time
import os
from enum import Enum

from underwriting.core.engine import UnderwritingEngine
from underwriting.core.models import Applicant, UnderwritingResult, UnderwritingDecision

class TestVariant(str, Enum):
    """Test variant identifiers."""
    CONTROL = "control"
    VARIANT_A = "variant_a"
    VARIANT_B = "variant_b"
    VARIANT_C = "variant_c"

@dataclass
class TestConfiguration:
    """Configuration for a single test variant."""
    variant_id: str
    name: str
    description: str
    rules_file: str
    prompt_template: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class TestResult:
    """Result from a single applicant evaluation."""
    applicant_id: str
    variant_id: str
    decision: UnderwritingDecision
    reason: str
    triggered_rules: List[str]
    risk_factors: List[str]
    processing_time_ms: float
    timestamp: datetime
    error: Optional[str] = None

@dataclass
class ComparisonMetrics:
    """Metrics comparing two test variants."""
    variant_a_id: str
    variant_b_id: str
    total_tests: int
    
    # Decision distribution
    accept_rate_a: float
    deny_rate_a: float
    adjudicate_rate_a: float
    
    accept_rate_b: float
    deny_rate_b: float
    adjudicate_rate_b: float
    
    # Performance metrics
    avg_processing_time_a: float
    avg_processing_time_b: float
    error_rate_a: float
    error_rate_b: float
    
    # Agreement metrics
    agreement_rate: float
    disagreement_details: List[Dict[str, Any]]

class ABTestEngine:
    """A/B testing engine for underwriting rule comparisons."""
    
    def __init__(self):
        """Initialize the A/B testing engine."""
        print("Initializing A/B Test Engine...")
        self.test_configurations: Dict[str, TestConfiguration] = {}
        self.test_results: List[TestResult] = []
        self.engines: Dict[str, UnderwritingEngine] = {}
    
    def register_test_configuration(self, config: TestConfiguration):
        """Register a test configuration."""
        print("Registering test configuration:")
        self.test_configurations[config.variant_id] = config
        
        # Create underwriting engine for this configuration
        if config.rules_file:
            engine = UnderwritingEngine(rules_file=config.rules_file)
            
            # Apply custom prompt template if provided
            if config.prompt_template:
                engine.prompt_template = config.prompt_template
            
            self.engines[config.variant_id] = engine
    
    def run_single_comparison(self, applicant: Applicant, variant_a: str, variant_b: str) -> Tuple[TestResult, TestResult]:
        """Run a single applicant through two variants and return results."""
        
        results = []
        self.__init__()
        self.register_test_configuration(TestConfiguration(
            variant_id="underwriting_rules_standard",
            name="Standard Underwriting Rules",
            description="Default underwriting rules for standard evaluation.",
            rules_file="underwriting_rules_standard.json"
        ))
        self.register_test_configuration(TestConfiguration(
            variant_id="underwriting_rules_conservative",
            name="Conservative Underwriting Rules",
            description="More conservative underwriting rules for risk-averse evaluation.",
            rules_file="underwriting_rules_conservative.json"
        ))
        self.register_test_configuration(TestConfiguration(
            variant_id="underwriting_rules_liberal",
            name="Liberal Underwriting Rules",
            description="Liberal automobile insurance underwriting rules for risk-tolerant evaluation.",
            rules_file="underwriting_rules_liberal.json"
        ))

        variant_map = {
            "standard": "underwriting_rules_standard",
            "conservative": "underwriting_rules_conservative",
            "liberal": "underwriting_rules_liberal"
        }
        variant_a = variant_map.get(variant_a, variant_a)
        variant_b = variant_map.get(variant_b, variant_b)

        for variant_id in [variant_a, variant_b]:
            print(f"\nRunning evaluation for variant: {variant_id}")
            if variant_id not in self.engines:
                raise ValueError(f"Variant {variant_id} is not registered in the test configurations.")
            
            engine = self.engines[variant_id]
            start_time = time.time()
            
            try:
                # Run evaluation
                underwriting_result = engine.evaluate_applicant(applicant)
                processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Create test result
                test_result = TestResult(
                    applicant_id=applicant.applicant_id,
                    variant_id=variant_id,
                    decision=underwriting_result.decision,
                    reason=underwriting_result.reason,
                    triggered_rules=underwriting_result.triggered_rules,
                    risk_factors=underwriting_result.risk_factors,
                    processing_time_ms=processing_time,
                    timestamp=datetime.now(),
                    error=None
                )
                
            except Exception as e:
                processing_time = (time.time() - start_time) * 1000
                
                test_result = TestResult(
                    applicant_id=applicant.applicant_id,
                    variant_id=variant_id,
                    decision=UnderwritingDecision.ADJUDICATE,
                    reason=f"Error: {str(e)}",
                    triggered_rules=[],
                    risk_factors=["System Error"],
                    processing_time_ms=processing_time,
                    timestamp=datetime.now(),
                    error=str(e)
                )
            
            results.append(test_result)
            self.test_results.append(test_result)
        
        return results[0], results[1]
    
    def run_batch_comparison(self, applicants: List[Applicant], variant_a: str, variant_b: str) -> List[Tuple[TestResult, TestResult]]:
        """Run a batch of applicants through two variants."""
        
        print(f"\n{'='*80}")
        print(f"A/B TEST: {variant_a.upper()} vs {variant_b.upper()}")
        print(f"{'='*80}")
        print(f"Testing {len(applicants)} applicants...")
        
        batch_results = []
        
        for i, applicant in enumerate(applicants):
            print(f"\nProcessing applicant {i+1}/{len(applicants)}: {applicant.applicant_id}")
            
            result_a, result_b = self.run_single_comparison(applicant, variant_a, variant_b)
            batch_results.append((result_a, result_b))
            
            # Show quick comparison
            agreement = "✓" if result_a.decision == result_b.decision else "✗"
            print(f"  {variant_a}: {result_a.decision.value.upper()}")
            print(f"  {variant_b}: {result_b.decision.value.upper()}")
            print(f"  Agreement: {agreement}")
        
        return batch_results
    
    def calculate_comparison_metrics(self, variant_a: str, variant_b: str) -> ComparisonMetrics:
        """Calculate comparison metrics between two variants."""
        
        # Filter results for the two variants
        results_a = [r for r in self.test_results if r.variant_id == variant_a]
        results_b = [r for r in self.test_results if r.variant_id == variant_b]
        
        # Ensure we have matching applicants
        applicant_ids_a = {r.applicant_id for r in results_a}
        applicant_ids_b = {r.applicant_id for r in results_b}
        common_applicants = applicant_ids_a.intersection(applicant_ids_b)
        
        if not common_applicants:
            raise ValueError("No common applicants found between variants")
        
        # Filter to common applicants only
        results_a = [r for r in results_a if r.applicant_id in common_applicants]
        results_b = [r for r in results_b if r.applicant_id in common_applicants]
        
        total_tests = len(common_applicants)
        
        # Calculate decision distributions
        def calculate_rates(results):
            total = len(results)
            if total == 0:
                return 0.0, 0.0, 0.0
            
            accept_count = sum(1 for r in results if r.decision == UnderwritingDecision.ACCEPT)
            deny_count = sum(1 for r in results if r.decision == UnderwritingDecision.DENY)
            adjudicate_count = sum(1 for r in results if r.decision == UnderwritingDecision.ADJUDICATE)
            
            return (accept_count / total * 100, 
                   deny_count / total * 100, 
                   adjudicate_count / total * 100)
        
        accept_rate_a, deny_rate_a, adjudicate_rate_a = calculate_rates(results_a)
        accept_rate_b, deny_rate_b, adjudicate_rate_b = calculate_rates(results_b)
        
        # Calculate performance metrics
        avg_processing_time_a = sum(r.processing_time_ms for r in results_a) / len(results_a) if results_a else 0
        avg_processing_time_b = sum(r.processing_time_ms for r in results_b) / len(results_b) if results_b else 0
        
        error_rate_a = sum(1 for r in results_a if r.error) / len(results_a) * 100 if results_a else 0
        error_rate_b = sum(1 for r in results_b if r.error) / len(results_b) * 100 if results_b else 0
        
        # Calculate agreement metrics
        agreements = 0
        disagreement_details = []
        
        # Create lookup for results_b
        results_b_lookup = {r.applicant_id: r for r in results_b}
        
        for result_a in results_a:
            result_b = results_b_lookup.get(result_a.applicant_id)
            if result_b:
                if result_a.decision == result_b.decision:
                    agreements += 1
                else:
                    disagreement_details.append({
                        'applicant_id': result_a.applicant_id,
                        f'{variant_a}_decision': result_a.decision.value,
                        f'{variant_b}_decision': result_b.decision.value,
                        f'{variant_a}_reason': result_a.reason,
                        f'{variant_b}_reason': result_b.reason
                    })
        
        agreement_rate = (agreements / total_tests * 100) if total_tests > 0 else 0
        
        return ComparisonMetrics(
            variant_a_id=variant_a,
            variant_b_id=variant_b,
            total_tests=total_tests,
            accept_rate_a=accept_rate_a,
            deny_rate_a=deny_rate_a,
            adjudicate_rate_a=adjudicate_rate_a,
            accept_rate_b=accept_rate_b,
            deny_rate_b=deny_rate_b,
            adjudicate_rate_b=adjudicate_rate_b,
            avg_processing_time_a=avg_processing_time_a,
            avg_processing_time_b=avg_processing_time_b,
            error_rate_a=error_rate_a,
            error_rate_b=error_rate_b,
            agreement_rate=agreement_rate,
            disagreement_details=disagreement_details
        )
    
    def print_comparison_report(self, metrics: ComparisonMetrics):
        """Print a detailed comparison report."""
        
        print(f"\n{'='*80}")
        print(f"A/B TEST COMPARISON REPORT")
        print(f"{'='*80}")
        print(f"Variant A: {metrics.variant_a_id.upper()}")
        print(f"Variant B: {metrics.variant_b_id.upper()}")
        print(f"Total Tests: {metrics.total_tests}")
        print(f"Agreement Rate: {metrics.agreement_rate:.1f}%")
        
        print(f"\n{'-'*50}")
        print("DECISION DISTRIBUTION")
        print(f"{'-'*50}")
        print(f"{'Decision':<12} {'Variant A':<12} {'Variant B':<12} {'Difference':<12}")
        print("-" * 50)
        
        accept_diff = metrics.accept_rate_b - metrics.accept_rate_a
        deny_diff = metrics.deny_rate_b - metrics.deny_rate_a
        adj_diff = metrics.adjudicate_rate_b - metrics.adjudicate_rate_a
        
        print(f"{'Accept':<12} {metrics.accept_rate_a:<11.1f}% {metrics.accept_rate_b:<11.1f}% {accept_diff:+.1f}%")
        print(f"{'Deny':<12} {metrics.deny_rate_a:<11.1f}% {metrics.deny_rate_b:<11.1f}% {deny_diff:+.1f}%")
        print(f"{'Adjudicate':<12} {metrics.adjudicate_rate_a:<11.1f}% {metrics.adjudicate_rate_b:<11.1f}% {adj_diff:+.1f}%")
        
        print(f"\n{'-'*50}")
        print("PERFORMANCE METRICS")
        print(f"{'-'*50}")
        print(f"Average Processing Time:")
        print(f"  Variant A: {metrics.avg_processing_time_a:.1f}ms")
        print(f"  Variant B: {metrics.avg_processing_time_b:.1f}ms")
        print(f"  Difference: {metrics.avg_processing_time_b - metrics.avg_processing_time_a:+.1f}ms")
        
        print(f"\nError Rates:")
        print(f"  Variant A: {metrics.error_rate_a:.1f}%")
        print(f"  Variant B: {metrics.error_rate_b:.1f}%")
        
        if metrics.disagreement_details:
            print(f"\n{'-'*50}")
            print(f"DISAGREEMENTS ({len(metrics.disagreement_details)} cases)")
            print(f"{'-'*50}")
            
            for disagreement in metrics.disagreement_details[:10]:  # Show first 10
                print(f"\nApplicant: {disagreement['applicant_id']}")
                print(f"  {metrics.variant_a_id}: {disagreement[f'{metrics.variant_a_id}_decision'].upper()}")
                print(f"  {metrics.variant_b_id}: {disagreement[f'{metrics.variant_b_id}_decision'].upper()}")
            
            if len(metrics.disagreement_details) > 10:
                print(f"\n... and {len(metrics.disagreement_details) - 10} more disagreements")
        
        print(f"\n{'='*80}")
    
    def export_results(self, filename: str):
        """Export test results to JSON file."""
        
        export_data = {
            'test_configurations': {
                variant_id: {
                    'name': config.name,
                    'description': config.description,
                    'rules_file': config.rules_file,
                    'parameters': config.parameters
                }
                for variant_id, config in self.test_configurations.items()
            },
            'test_results': [
                {
                    'applicant_id': result.applicant_id,
                    'variant_id': result.variant_id,
                    'decision': result.decision.value,
                    'reason': result.reason,
                    'triggered_rules': result.triggered_rules,
                    'risk_factors': result.risk_factors,
                    'processing_time_ms': result.processing_time_ms,
                    'timestamp': result.timestamp.isoformat(),
                    'error': result.error
                }
                for result in self.test_results
            ],
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\nResults exported to: {filename}")
    
    def clear_results(self):
        """Clear all test results."""
        self.test_results.clear()
        print("Test results cleared.")


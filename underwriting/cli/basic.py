#!/usr/bin/env python3
"""
Main application for automobile insurance underwriting system.
Tests sample applicants through the LangChain/OpenAI underwriting engine.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any

from underwriting.core.engine import UnderwritingEngine
from underwriting.data.sample_generator import create_sample_applicants, print_applicant_summary
from underwriting.core.models import Applicant, UnderwritingResult, UnderwritingDecision

class UnderwritingTestFramework:
    """Framework for testing underwriting decisions."""
    
    def __init__(self):
        """Initialize the test framework."""
        self.engine = UnderwritingEngine()
        self.test_results: List[Dict[str, Any]] = []
    
    def run_single_test(self, applicant: Applicant, expected_decision: str = None) -> UnderwritingResult:
        """Run underwriting evaluation for a single applicant."""
        
        print(f"\n{'='*60}")
        print(f"EVALUATING APPLICANT: {applicant.applicant_id}")
        print(f"{'='*60}")
        
        # Display applicant summary
        print_applicant_summary(applicant)
        
        print(f"\n{'-'*40}")
        print("UNDERWRITING EVALUATION IN PROGRESS...")
        print(f"{'-'*40}")
        
        # Run evaluation
        try:
            result = self.engine.evaluate_applicant(applicant)
            
            # Display results
            print(f"\n*** UNDERWRITING DECISION ***")
            print(f"Decision: {result.decision.value.upper()}")
            print(f"Reason: {result.reason}")
            
            if result.triggered_rules:
                print(f"Triggered Rules: {', '.join(result.triggered_rules)}")
            
            if result.risk_factors:
                print(f"Risk Factors: {', '.join(result.risk_factors)}")
            
            print(f"Timestamp: {result.timestamp}")
            
            # Check against expected result if provided
            if expected_decision:
                expected = expected_decision.lower()
                actual = result.decision.value
                match_status = "✓ MATCH" if expected == actual else "✗ MISMATCH"
                print(f"Expected: {expected.upper()} | Actual: {actual.upper()} | {match_status}")
            
            # Store result for summary
            self.test_results.append({
                'applicant_id': applicant.applicant_id,
                'applicant_name': f"{applicant.primary_driver.first_name} {applicant.primary_driver.last_name}",
                'expected': expected_decision,
                'actual': result.decision.value,
                'reason': result.reason,
                'match': expected_decision.lower() == result.decision.value if expected_decision else None
            })
            
            return result
            
        except Exception as e:
            print(f"\n*** ERROR DURING EVALUATION ***")
            print(f"Error: {str(e)}")
            
            # Create error result
            error_result = UnderwritingResult(
                applicant_id=applicant.applicant_id,
                decision=UnderwritingDecision.ADJUDICATE,
                reason=f"System error: {str(e)}",
                triggered_rules=[],
                risk_factors=["System Error"]
            )
            
            self.test_results.append({
                'applicant_id': applicant.applicant_id,
                'applicant_name': f"{applicant.primary_driver.first_name} {applicant.primary_driver.last_name}",
                'expected': expected_decision,
                'actual': 'ERROR',
                'reason': str(e),
                'match': False
            })
            
            return error_result
    
    def run_full_test_suite(self):
        """Run the complete test suite with all sample applicants."""
        
        print("AUTOMOBILE INSURANCE UNDERWRITING SYSTEM")
        print("LangChain + OpenAI Integration Test")
        print("=" * 60)
        
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("\n*** ERROR: OPENAI_API_KEY not found in environment ***")
            print("Please set your OpenAI API key in the .env file or environment variables.")
            return False
        
        # Create sample applicants
        applicants = create_sample_applicants()
        
        # Expected results for validation
        expected_results = [
            "accept",    # APP001 - Clean record mature driver
            "accept",    # APP002 - Good driver with minimal issues  
            "deny",      # APP003 - Multiple DUI violations
            "deny",      # APP004 - Extended coverage lapse + excessive claims
            "adjudicate", # APP005 - Young driver with violations
            "adjudicate"  # APP006 - Single major violation
        ]
        
        print(f"\nTesting {len(applicants)} sample applicants...")
        print(f"Expected results: 2 Accept, 2 Deny, 2 Adjudicate")
        
        # Run tests
        for i, applicant in enumerate(applicants):
            expected = expected_results[i] if i < len(expected_results) else None
            self.run_single_test(applicant, expected)
            
            # Pause between tests for readability
            if i < len(applicants) - 1:
                input("\nPress Enter to continue to next applicant...")
        
        # Display summary
        self.print_test_summary()
        
        return True
    
    def print_test_summary(self):
        """Print a summary of all test results."""
        
        print(f"\n{'='*80}")
        print("TEST SUMMARY")
        print(f"{'='*80}")
        
        total_tests = len(self.test_results)
        matches = sum(1 for r in self.test_results if r['match'] is True)
        errors = sum(1 for r in self.test_results if r['actual'] == 'ERROR')
        
        print(f"Total Tests: {total_tests}")
        print(f"Correct Predictions: {matches}")
        print(f"Errors: {errors}")
        print(f"Accuracy: {(matches/total_tests)*100:.1f}%" if total_tests > 0 else "N/A")
        
        print(f"\n{'ID':<8} {'Name':<20} {'Expected':<12} {'Actual':<12} {'Match':<8}")
        print("-" * 70)
        
        for result in self.test_results:
            match_symbol = "✓" if result['match'] is True else "✗" if result['match'] is False else "-"
            expected_str = result['expected'].upper() if result['expected'] else "N/A"
            actual_str = result['actual'].upper()
            
            print(f"{result['applicant_id']:<8} {result['applicant_name']:<20} {expected_str:<12} {actual_str:<12} {match_symbol:<8}")
        
        print(f"\n{'='*80}")
        
        # Detailed results
        print("\nDETAILED RESULTS:")
        for result in self.test_results:
            print(f"\n{result['applicant_id']} - {result['applicant_name']}:")
            print(f"  Decision: {result['actual'].upper()}")
            print(f"  Reason: {result['reason']}")

def main():
    """Main entry point for the application."""
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("Automobile Insurance Underwriting System")
            print("Usage: python main.py [options]")
            print("\nOptions:")
            print("  -h, --help     Show this help message")
            print("  --test         Run full test suite")
            print("  --interactive  Run interactive mode")
            return
        
        elif sys.argv[1] == '--test':
            # Run automated test suite
            framework = UnderwritingTestFramework()
            success = framework.run_full_test_suite()
            sys.exit(0 if success else 1)
        
        elif sys.argv[1] == '--interactive':
            # Interactive mode - let user select applicants
            framework = UnderwritingTestFramework()
            applicants = create_sample_applicants()
            
            while True:
                print(f"\n{'='*50}")
                print("INTERACTIVE UNDERWRITING SYSTEM")
                print(f"{'='*50}")
                print("Available applicants:")
                
                for i, applicant in enumerate(applicants):
                    driver = applicant.primary_driver
                    print(f"{i+1}. {applicant.applicant_id} - {driver.first_name} {driver.last_name} (Age {driver.age})")
                
                print("0. Exit")
                
                try:
                    choice = int(input("\nSelect applicant to evaluate (0-6): "))
                    
                    if choice == 0:
                        break
                    elif 1 <= choice <= len(applicants):
                        framework.run_single_test(applicants[choice-1])
                    else:
                        print("Invalid choice. Please try again.")
                        
                except (ValueError, KeyboardInterrupt):
                    print("\nExiting...")
                    break
            
            return
    
    # Default: run full test suite
    framework = UnderwritingTestFramework()
    framework.run_full_test_suite()

if __name__ == "__main__":
    main()


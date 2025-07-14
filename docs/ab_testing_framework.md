# A/B Testing Framework for Underwriting Rules

This document outlines the A/B testing framework design for the automobile insurance underwriting system.

## A/B Testing Scenarios

### Scenario A: Rule Threshold Modifications

**Current Rules vs. Modified Rules**

1. **Violation Thresholds**:
   - Current: 2+ DUI violations = deny
   - Test: 3+ DUI violations = deny
   
2. **Claims History**:
   - Current: 3+ at-fault claims = deny
   - Test: 4+ at-fault claims = deny

3. **Coverage Lapse**:
   - Current: 90+ days lapse = deny
   - Test: 120+ days lapse = deny

### Scenario B: Prompt Template Variations

**Current Prompt vs. Alternative Prompts**

1. **Conservative Prompt**: Emphasizes risk aversion
2. **Balanced Prompt**: Current implementation
3. **Liberal Prompt**: More accepting of borderline cases

### Scenario C: Business Logic Changes

**Decision Categories**:
- Current: Accept/Deny/Adjudicate
- Test: Accept/Conditional Accept/Deny/Adjudicate

## Implementation Framework

### 1. Rule Versioning System

```python
class RuleVersion:
    def __init__(self, version_name: str, rules_file: str):
        self.version_name = version_name
        self.rules_file = rules_file
        self.results = []

# Example usage:
version_a = RuleVersion("conservative", "rules_conservative.json")
version_b = RuleVersion("liberal", "rules_liberal.json")
```

### 2. A/B Test Runner

```python
class ABTestRunner:
    def __init__(self, version_a: RuleVersion, version_b: RuleVersion):
        self.version_a = version_a
        self.version_b = version_b
    
    def run_comparison_test(self, applicants: List[Applicant]):
        # Run both versions on same applicants
        # Compare results
        # Generate statistical analysis
```

### 3. Results Analysis

- Decision distribution comparison
- Processing time analysis
- Accuracy metrics (if ground truth available)
- Business impact simulation

## Test Configuration Files

### Conservative Rules (rules_conservative.json)
- Stricter thresholds
- More adjudication triggers
- Higher denial rates

### Liberal Rules (rules_liberal.json)  
- Relaxed thresholds
- Fewer adjudication triggers
- Higher acceptance rates

## Metrics to Track

1. **Decision Distribution**:
   - Accept rate
   - Deny rate  
   - Adjudicate rate

2. **Processing Metrics**:
   - Average response time
   - Error rates
   - Consistency scores

3. **Business Metrics**:
   - Estimated loss ratios
   - Market penetration
   - Customer satisfaction proxy

## Statistical Analysis

- Chi-square tests for decision distribution differences
- T-tests for continuous metrics
- Confidence intervals for rate differences
- Power analysis for sample size requirements

## Implementation Steps

1. Create alternative rule sets
2. Implement A/B test runner
3. Define success metrics
4. Run controlled experiments
5. Analyze results
6. Make data-driven recommendations


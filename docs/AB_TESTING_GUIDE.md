# A/B Testing Framework for Automobile Insurance Underwriting

## 🎯 Overview

This comprehensive A/B testing framework allows you to test different underwriting approaches and measure their impact on business metrics. The system supports testing both **rule variations** and **prompt template variations** with full statistical analysis and business impact assessment.

## 🚀 Quick Start

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your_api_key_here"
# OR create .env file with: OPENAI_API_KEY=your_api_key_here
```

### 2. List Available Configurations
```bash
python ab_test_runner.py --list-configs
```

### 3. Run Your First A/B Test
```bash
# Compare conservative vs liberal rules
python ab_test_runner.py --rule-comparison conservative liberal

# Compare different prompt approaches
python ab_test_runner.py --prompt-comparison conservative liberal

# Run comprehensive test suite
python ab_test_runner.py --comprehensive
```

## 📊 A/B Testing Capabilities

### Rule-Based Testing
Test different underwriting rule configurations:

- **Conservative Rules**: Stricter criteria, lower acceptance rates
- **Standard Rules**: Balanced approach (baseline)
- **Liberal Rules**: More accepting criteria, higher acceptance rates

### Prompt Template Testing
Test different LLM instruction approaches:

- **Conservative Prompt**: Risk-averse, emphasizes loss prevention
- **Balanced Prompt**: Standard approach (baseline)
- **Liberal Prompt**: Growth-oriented, emphasizes inclusion
- **Detailed Prompt**: Comprehensive analysis required
- **Concise Prompt**: Quick, efficient decisions

## 📈 Statistical Analysis

The framework provides comprehensive statistical analysis:

### Statistical Tests
- **Chi-Square Test**: Decision distribution differences
- **Two-Proportion Z-Tests**: Specific decision type comparisons
- **Independent T-Test**: Processing time differences
- **Effect Size Calculations**: Cohen's d, Cramér's V, Cohen's h

### Business Impact Analysis
- **Volume Impact**: Estimated monthly application changes
- **Loss Ratio Impact**: Risk exposure changes
- **Processing Cost Impact**: Manual review cost changes
- **Market Share Impact**: Competitive positioning
- **Risk Assessment**: Automated risk level evaluation

## 🛠️ Command Line Interface

### Basic Commands

```bash
# Rule comparisons
python ab_test_runner.py --rule-comparison standard conservative
python ab_test_runner.py --rule-comparison standard liberal
python ab_test_runner.py --rule-comparison conservative liberal

# Prompt comparisons
python ab_test_runner.py --prompt-comparison balanced conservative
python ab_test_runner.py --prompt-comparison balanced liberal
python ab_test_runner.py --prompt-comparison detailed concise

# Single variant analysis
python ab_test_runner.py --single-variant conservative
python ab_test_runner.py --single-variant prompt_liberal

# Comprehensive testing
python ab_test_runner.py --comprehensive
```

### Advanced Options

```bash
# Custom confidence level
python ab_test_runner.py --rule-comparison standard liberal --confidence-level 0.99

# Custom business parameters
python ab_test_runner.py --comprehensive --monthly-applications 50000

# Export results
python ab_test_runner.py --comprehensive --export comprehensive_results.json
```

## 📋 Sample Test Results

### Example: Conservative vs Liberal Rules

```
A/B TEST COMPARISON REPORT
================================================================================
Variant A: CONSERVATIVE
Variant B: LIBERAL
Total Tests: 6
Agreement Rate: 33.3%

--------------------------------------------------
DECISION DISTRIBUTION
--------------------------------------------------
Decision     Variant A    Variant B    Difference
--------------------------------------------------
Accept       16.7%        66.7%        +50.0%
Deny         66.7%        16.7%        -50.0%
Adjudicate   16.7%        16.7%        +0.0%

BUSINESS IMPACT ANALYSIS
--------------------------------------------------
Monthly Application Volume: 10,000
Risk Level: High

Decision Rate Changes:
  Accept Rate: +50.0% (+5,000 monthly)
  Deny Rate: -50.0% (-5,000 monthly)
  Adjudicate Rate: +0.0% (+0 monthly)

Estimated Business Impact:
  Loss Ratio Change: +0.250
  Processing Cost Change: $0/month
  Market Share Impact: +5.00%

Risk Factors:
  • Significant increase in acceptance rate may increase loss exposure
  • Low agreement rate indicates significant rule differences

Recommendations:
  • Consider gradual rollout due to significant acceptance rate increase
  • Review disagreement cases to understand rule impact
  • Continue monitoring key metrics post-implementation
```

## 🔧 Configuration Files

### Rule Configuration Files
- `underwriting_rules.json` - Standard balanced rules
- `underwriting_rules_conservative.json` - Stricter criteria
- `underwriting_rules_liberal.json` - More accepting criteria

### Key Differences Between Rule Sets

| Criteria | Conservative | Standard | Liberal |
|----------|-------------|----------|---------|
| DUI Threshold | 1+ (7 years) | 2+ (5 years) | 3+ (3 years) |
| Claims Threshold | 2+ at-fault | 3+ at-fault | 5+ at-fault |
| Coverage Lapse | 60+ days | 90+ days | 180+ days |
| Credit Score Min | 500 | 450 | No minimum |
| Young Driver Age | 23 | 21 | 21 |

## 📊 Sample Applicants

The framework includes 6 carefully designed test cases:

| ID | Profile | Expected Result |
|----|---------|----------------|
| APP001 | Clean record mature driver | Accept |
| APP002 | Good driver, minimal issues | Accept |
| APP003 | Multiple DUI violations | Deny |
| APP004 | Extended lapse + excessive claims | Deny |
| APP005 | Young driver with violations | Adjudicate |
| APP006 | Single major violation | Adjudicate |

## 🎯 Use Cases

### 1. Rule Optimization
Test different underwriting thresholds to optimize the balance between risk and market share:

```bash
# Test impact of relaxing DUI rules
python ab_test_runner.py --rule-comparison standard liberal

# Test impact of tightening claims criteria  
python ab_test_runner.py --rule-comparison standard conservative
```

### 2. Prompt Engineering
Optimize LLM instructions for consistent decision-making:

```bash
# Test detailed vs concise instructions
python ab_test_runner.py --prompt-comparison detailed concise

# Test risk-averse vs growth-oriented approaches
python ab_test_runner.py --prompt-comparison conservative liberal
```

### 3. Business Impact Assessment
Understand the business implications of rule changes:

```bash
# Get comprehensive business impact analysis
python ab_test_runner.py --comprehensive --monthly-applications 25000 --export business_impact.json
```

### 4. Regulatory Compliance Testing
Ensure new rules maintain compliance while optimizing performance:

```bash
# Test conservative approach for regulatory review
python ab_test_runner.py --single-variant conservative

# Compare against current standards
python ab_test_runner.py --rule-comparison standard conservative
```

## 📈 Interpreting Results

### Statistical Significance
- **p < 0.05**: Statistically significant difference
- **Effect Size**: Small (0.2), Medium (0.5), Large (0.8)
- **Agreement Rate**: % of cases where both variants agree

### Business Metrics
- **Accept Rate Change**: Impact on policy issuance
- **Loss Ratio Change**: Impact on profitability
- **Processing Cost**: Impact on operational efficiency
- **Risk Level**: Overall risk assessment (Low/Medium/High)

### Decision Guidelines
- **High Agreement (>85%)**: Safe to implement changes
- **Medium Agreement (70-85%)**: Monitor closely during rollout
- **Low Agreement (<70%)**: Investigate disagreements before implementation

## 🔄 Extending the Framework

### Adding New Rule Sets
1. Create new JSON file following the existing structure
2. Register in `ABTestRunner._register_default_configurations()`
3. Test with existing sample applicants

### Adding New Prompt Templates
1. Add new variant to `PromptVariant` enum
2. Create template in `PromptTemplateFactory`
3. Update descriptions and configurations

### Custom Sample Applicants
1. Modify `sample_applicants.py`
2. Add new test cases with known expected outcomes
3. Update validation logic in test runner

## 🚨 Best Practices

### Testing Strategy
1. **Start Small**: Test with sample applicants first
2. **Gradual Rollout**: Implement changes incrementally
3. **Monitor Closely**: Track key metrics post-implementation
4. **Document Changes**: Keep detailed records of rule modifications

### Statistical Considerations
1. **Sample Size**: Ensure adequate sample size for reliable results
2. **Multiple Testing**: Consider Bonferroni correction for multiple comparisons
3. **Effect Size**: Focus on practical significance, not just statistical significance
4. **Confidence Intervals**: Use confidence intervals for rate estimates

### Business Considerations
1. **Risk Management**: Balance growth with risk exposure
2. **Regulatory Compliance**: Ensure changes meet regulatory requirements
3. **Competitive Position**: Consider market impact of rule changes
4. **Customer Experience**: Balance automation with service quality

## 🔍 Troubleshooting

### Common Issues

**OpenAI API Key Error**
```bash
ERROR: OPENAI_API_KEY not found in environment variables.
```
Solution: Set your API key in environment or .env file

**Rule File Not Found**
```bash
FileNotFoundError: Rules file not found: underwriting_rules_custom.json
```
Solution: Ensure rule files exist in the project directory

**Statistical Analysis Errors**
```bash
Insufficient data for analysis
```
Solution: Ensure adequate sample size (minimum 2 cases per variant)

### Performance Optimization
- Use smaller sample sizes for initial testing
- Implement caching for repeated rule evaluations
- Consider parallel processing for large test suites

## 📚 Technical Architecture

### Core Components
- **ABTestEngine**: Manages test execution and comparison
- **StatisticalAnalyzer**: Performs statistical tests and analysis
- **BusinessImpactCalculator**: Estimates business metrics
- **PromptTemplateFactory**: Creates LLM instruction variations
- **UnderwritingEngine**: Core evaluation logic with A/B support

### Data Flow
1. **Configuration**: Load rules and prompt templates
2. **Execution**: Run applicants through variants
3. **Analysis**: Calculate metrics and statistical tests
4. **Reporting**: Generate comprehensive reports
5. **Export**: Save results for further analysis

This framework provides a robust foundation for data-driven underwriting optimization while maintaining statistical rigor and business relevance.


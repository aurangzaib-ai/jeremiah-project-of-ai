import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
#from scipy import stats
#import numpy as np
from .ab_engine import ComparisonMetrics, TestResult

@dataclass
class StatisticalTest:
    """Results from a statistical significance test."""
    test_name: str
    statistic: float
    p_value: float
    is_significant: bool
    confidence_level: float
    effect_size: Optional[float] = None
    interpretation: str = ""

@dataclass
class BusinessImpactAnalysis:
    """Business impact analysis for A/B test results."""
    variant_a_id: str
    variant_b_id: str
    
    # Volume estimates
    estimated_monthly_applications: int
    
    # Decision impact
    accept_rate_change: float
    deny_rate_change: float
    adjudicate_rate_change: float
    
    # Estimated volume changes
    additional_accepts_monthly: int
    additional_denies_monthly: int
    additional_adjudications_monthly: int
    
    # Business metrics
    estimated_loss_ratio_change: float
    estimated_processing_cost_change: float
    estimated_market_share_impact: float
    
    # Risk assessment
    risk_level: str  # "Low", "Medium", "High"
    risk_factors: List[str]
    recommendations: List[str]

class StatisticalAnalyzer:
    """Statistical analysis for A/B testing results."""
    
    def __init__(self, confidence_level: float = 0.95):
        """Initialize with confidence level (default 95%)."""
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level
    
    def chi_square_test(self, results_a: List[TestResult], results_b: List[TestResult]) -> StatisticalTest:
        """Perform chi-square test for decision distribution differences."""
        
        # Count decisions for each variant
        def count_decisions(results):
            counts = {'accept': 0, 'deny': 0, 'adjudicate': 0}
            for result in results:
                counts[result.decision.value] += 1
            return counts
        
        counts_a = count_decisions(results_a)
        counts_b = count_decisions(results_b)
        
        # Create contingency table
        observed = np.array([
            [counts_a['accept'], counts_a['deny'], counts_a['adjudicate']],
            [counts_b['accept'], counts_b['deny'], counts_b['adjudicate']]
        ])
        
        # Perform chi-square test
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(observed)
        
        is_significant = p_value < self.alpha
        
        # Calculate Cramér's V (effect size)
        n = observed.sum()
        cramers_v = math.sqrt(chi2_stat / (n * (min(observed.shape) - 1)))
        
        interpretation = self._interpret_chi_square(p_value, cramers_v, is_significant)
        
        return StatisticalTest(
            test_name="Chi-Square Test (Decision Distribution)",
            statistic=chi2_stat,
            p_value=p_value,
            is_significant=is_significant,
            confidence_level=self.confidence_level,
            effect_size=cramers_v,
            interpretation=interpretation
        )
    
    def proportion_z_test(self, results_a: List[TestResult], results_b: List[TestResult], 
                         decision_type: str) -> StatisticalTest:
        """Perform two-proportion z-test for specific decision type."""
        
        # Count specific decision type
        count_a = sum(1 for r in results_a if r.decision.value == decision_type)
        count_b = sum(1 for r in results_b if r.decision.value == decision_type)
        
        n_a = len(results_a)
        n_b = len(results_b)
        
        if n_a == 0 or n_b == 0:
            return StatisticalTest(
                test_name=f"Two-Proportion Z-Test ({decision_type})",
                statistic=0.0,
                p_value=1.0,
                is_significant=False,
                confidence_level=self.confidence_level,
                interpretation="Insufficient data for analysis"
            )
        
        p_a = count_a / n_a
        p_b = count_b / n_b
        
        # Pooled proportion
        p_pool = (count_a + count_b) / (n_a + n_b)
        
        # Standard error
        se = math.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        
        if se == 0:
            z_stat = 0
            p_value = 1.0
        else:
            z_stat = (p_a - p_b) / se
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        is_significant = p_value < self.alpha
        
        # Effect size (Cohen's h)
        cohens_h = 2 * (math.asin(math.sqrt(p_a)) - math.asin(math.sqrt(p_b)))
        
        interpretation = self._interpret_proportion_test(p_a, p_b, p_value, cohens_h, is_significant, decision_type)
        
        return StatisticalTest(
            test_name=f"Two-Proportion Z-Test ({decision_type})",
            statistic=z_stat,
            p_value=p_value,
            is_significant=is_significant,
            confidence_level=self.confidence_level,
            effect_size=abs(cohens_h),
            interpretation=interpretation
        )
    
    def t_test_processing_time(self, results_a: List[TestResult], results_b: List[TestResult]) -> StatisticalTest:
        """Perform t-test for processing time differences."""
        
        times_a = [r.processing_time_ms for r in results_a if r.error is None]
        times_b = [r.processing_time_ms for r in results_b if r.error is None]
        
        if len(times_a) < 2 or len(times_b) < 2:
            return StatisticalTest(
                test_name="Independent T-Test (Processing Time)",
                statistic=0.0,
                p_value=1.0,
                is_significant=False,
                confidence_level=self.confidence_level,
                interpretation="Insufficient data for analysis"
            )
        
        # Perform independent t-test
        t_stat, p_value = stats.ttest_ind(times_a, times_b)
        
        is_significant = p_value < self.alpha
        
        # Effect size (Cohen's d)
        mean_a = np.mean(times_a)
        mean_b = np.mean(times_b)
        pooled_std = math.sqrt(((len(times_a) - 1) * np.var(times_a, ddof=1) + 
                               (len(times_b) - 1) * np.var(times_b, ddof=1)) / 
                              (len(times_a) + len(times_b) - 2))
        
        cohens_d = (mean_a - mean_b) / pooled_std if pooled_std > 0 else 0
        
        interpretation = self._interpret_t_test(mean_a, mean_b, p_value, cohens_d, is_significant)
        
        return StatisticalTest(
            test_name="Independent T-Test (Processing Time)",
            statistic=t_stat,
            p_value=p_value,
            is_significant=is_significant,
            confidence_level=self.confidence_level,
            effect_size=abs(cohens_d),
            interpretation=interpretation
        )
    
    def confidence_interval_proportion(self, results: List[TestResult], decision_type: str) -> Tuple[float, float]:
        """Calculate confidence interval for a proportion."""
        
        count = sum(1 for r in results if r.decision.value == decision_type)
        n = len(results)
        
        if n == 0:
            return 0.0, 0.0
        
        p = count / n
        
        # Wilson score interval (more robust than normal approximation)
        z = stats.norm.ppf(1 - self.alpha/2)
        denominator = 1 + z**2/n
        centre_adjusted_probability = (p + z**2/(2*n)) / denominator
        adjusted_standard_deviation = math.sqrt((p*(1-p) + z**2/(4*n)) / n) / denominator
        
        lower_bound = centre_adjusted_probability - z * adjusted_standard_deviation
        upper_bound = centre_adjusted_probability + z * adjusted_standard_deviation
        
        return max(0, lower_bound), min(1, upper_bound)
    
    def power_analysis(self, effect_size: float, alpha: float = None, power: float = 0.8) -> int:
        """Calculate required sample size for given effect size and power."""
        
        if alpha is None:
            alpha = self.alpha
        
        # For two-proportion test
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        # Approximate sample size calculation
        n = 2 * ((z_alpha + z_beta) / effect_size)**2
        
        return math.ceil(n)
    
    def _interpret_chi_square(self, p_value: float, cramers_v: float, is_significant: bool) -> str:
        """Interpret chi-square test results."""
        
        significance_text = "statistically significant" if is_significant else "not statistically significant"
        
        if cramers_v < 0.1:
            effect_text = "negligible"
        elif cramers_v < 0.3:
            effect_text = "small"
        elif cramers_v < 0.5:
            effect_text = "medium"
        else:
            effect_text = "large"
        
        return f"The difference in decision distributions is {significance_text} (p={p_value:.4f}) with a {effect_text} effect size (Cramér's V={cramers_v:.3f})."
    
    def _interpret_proportion_test(self, p_a: float, p_b: float, p_value: float, 
                                  cohens_h: float, is_significant: bool, decision_type: str) -> str:
        """Interpret proportion test results."""
        
        significance_text = "statistically significant" if is_significant else "not statistically significant"
        direction = "higher" if p_b > p_a else "lower"
        
        effect_size_text = "negligible"
        if abs(cohens_h) > 0.2:
            effect_size_text = "small"
        if abs(cohens_h) > 0.5:
            effect_size_text = "medium"
        if abs(cohens_h) > 0.8:
            effect_size_text = "large"
        
        return f"Variant B has a {significance_text} {direction} {decision_type} rate ({p_b:.1%} vs {p_a:.1%}, p={p_value:.4f}) with a {effect_size_text} effect size."
    
    def _interpret_t_test(self, mean_a: float, mean_b: float, p_value: float, 
                         cohens_d: float, is_significant: bool) -> str:
        """Interpret t-test results."""
        
        significance_text = "statistically significant" if is_significant else "not statistically significant"
        direction = "slower" if mean_b > mean_a else "faster"
        
        effect_size_text = "negligible"
        if abs(cohens_d) > 0.2:
            effect_size_text = "small"
        if abs(cohens_d) > 0.5:
            effect_size_text = "medium"
        if abs(cohens_d) > 0.8:
            effect_size_text = "large"
        
        return f"Variant B is {significance_text} {direction} ({mean_b:.1f}ms vs {mean_a:.1f}ms, p={p_value:.4f}) with a {effect_size_text} effect size."

class BusinessImpactCalculator:
    """Calculate business impact of A/B test results."""
    
    def __init__(self, monthly_applications: int = 10000):
        """Initialize with estimated monthly application volume."""
        self.monthly_applications = monthly_applications
    
    def calculate_impact(self, metrics: ComparisonMetrics) -> BusinessImpactAnalysis:
        """Calculate comprehensive business impact analysis."""
        
        # Calculate rate changes
        accept_rate_change = metrics.accept_rate_b - metrics.accept_rate_a
        deny_rate_change = metrics.deny_rate_b - metrics.deny_rate_a
        adjudicate_rate_change = metrics.adjudicate_rate_b - metrics.adjudicate_rate_a
        
        # Calculate volume changes
        additional_accepts = int(self.monthly_applications * accept_rate_change / 100)
        additional_denies = int(self.monthly_applications * deny_rate_change / 100)
        additional_adjudications = int(self.monthly_applications * adjudicate_rate_change / 100)
        
        # Estimate business metrics
        loss_ratio_change = self._estimate_loss_ratio_change(accept_rate_change, deny_rate_change)
        processing_cost_change = self._estimate_processing_cost_change(adjudicate_rate_change)
        market_share_impact = self._estimate_market_share_impact(accept_rate_change, deny_rate_change)
        
        # Risk assessment
        risk_level, risk_factors = self._assess_risk(metrics, accept_rate_change, deny_rate_change)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, accept_rate_change, deny_rate_change, adjudicate_rate_change)
        
        return BusinessImpactAnalysis(
            variant_a_id=metrics.variant_a_id,
            variant_b_id=metrics.variant_b_id,
            estimated_monthly_applications=self.monthly_applications,
            accept_rate_change=accept_rate_change,
            deny_rate_change=deny_rate_change,
            adjudicate_rate_change=adjudicate_rate_change,
            additional_accepts_monthly=additional_accepts,
            additional_denies_monthly=additional_denies,
            additional_adjudications_monthly=additional_adjudications,
            estimated_loss_ratio_change=loss_ratio_change,
            estimated_processing_cost_change=processing_cost_change,
            estimated_market_share_impact=market_share_impact,
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommendations=recommendations
        )
    
    def _estimate_loss_ratio_change(self, accept_rate_change: float, deny_rate_change: float) -> float:
        """Estimate change in loss ratio based on acceptance/denial rate changes."""
        
        # Simplified model: higher acceptance rate typically increases loss ratio
        # This would need to be calibrated with actual loss data
        base_loss_ratio = 0.65  # Typical auto insurance loss ratio
        
        # Assume each 1% increase in acceptance rate increases loss ratio by 0.5%
        loss_ratio_impact = accept_rate_change * 0.005
        
        return loss_ratio_impact
    
    def _estimate_processing_cost_change(self, adjudicate_rate_change: float) -> float:
        """Estimate change in processing costs based on adjudication rate changes."""
        
        # Assume manual adjudication costs $50 per case vs $5 for automated
        cost_per_adjudication = 45  # Additional cost
        monthly_cost_change = (self.monthly_applications * adjudicate_rate_change / 100) * cost_per_adjudication
        
        return monthly_cost_change
    
    def _estimate_market_share_impact(self, accept_rate_change: float, deny_rate_change: float) -> float:
        """Estimate market share impact based on acceptance/denial changes."""
        
        # Higher acceptance rate generally improves market share
        # This is a simplified model
        market_share_impact = accept_rate_change * 0.1  # 1% acceptance increase = 0.1% market share increase
        
        return market_share_impact
    
    def _assess_risk(self, metrics: ComparisonMetrics, accept_rate_change: float, deny_rate_change: float) -> Tuple[str, List[str]]:
        """Assess risk level and identify risk factors."""
        
        risk_factors = []
        risk_score = 0
        
        # High acceptance rate increase
        if accept_rate_change > 10:
            risk_factors.append("Significant increase in acceptance rate may increase loss exposure")
            risk_score += 2
        elif accept_rate_change > 5:
            risk_factors.append("Moderate increase in acceptance rate")
            risk_score += 1
        
        # Low agreement rate
        if metrics.agreement_rate < 70:
            risk_factors.append("Low agreement rate indicates significant rule differences")
            risk_score += 2
        elif metrics.agreement_rate < 85:
            risk_factors.append("Moderate agreement rate")
            risk_score += 1
        
        # Processing time increase
        time_increase = metrics.avg_processing_time_b - metrics.avg_processing_time_a
        if time_increase > 1000:  # More than 1 second
            risk_factors.append("Significant processing time increase")
            risk_score += 1
        
        # Error rate increase
        if metrics.error_rate_b > metrics.error_rate_a:
            risk_factors.append("Increased error rate in variant B")
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 4:
            risk_level = "High"
        elif risk_score >= 2:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return risk_level, risk_factors
    
    def _generate_recommendations(self, metrics: ComparisonMetrics, accept_rate_change: float, 
                                deny_rate_change: float, adjudicate_rate_change: float) -> List[str]:
        """Generate business recommendations based on test results."""
        
        recommendations = []
        
        # Acceptance rate recommendations
        if accept_rate_change > 15:
            recommendations.append("Consider gradual rollout due to significant acceptance rate increase")
        elif accept_rate_change > 5:
            recommendations.append("Monitor loss ratios closely if implementing variant B")
        elif accept_rate_change < -10:
            recommendations.append("Variant B may be too restrictive, potentially losing market share")
        
        # Adjudication rate recommendations
        if adjudicate_rate_change > 10:
            recommendations.append("Ensure adequate underwriting staff for increased manual reviews")
        elif adjudicate_rate_change < -10:
            recommendations.append("Validate that automated decisions maintain quality standards")
        
        # Agreement rate recommendations
        if metrics.agreement_rate < 70:
            recommendations.append("Review disagreement cases to understand rule impact")
            recommendations.append("Consider A/B testing with smaller population first")
        
        # Performance recommendations
        time_increase = metrics.avg_processing_time_b - metrics.avg_processing_time_a
        if time_increase > 500:
            recommendations.append("Optimize variant B for better performance")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Results show minimal impact - safe to proceed with implementation")
        
        recommendations.append("Continue monitoring key metrics post-implementation")
        
        return recommendations


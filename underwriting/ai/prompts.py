from langchain.prompts import PromptTemplate
from typing import Dict, Any, List, Tuple
from enum import Enum

class PromptVariant(str, Enum):
    """Prompt template variants for A/B testing."""
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    LIBERAL = "liberal"
    DETAILED = "detailed"
    CONCISE = "concise"

class PromptTemplateFactory:
    """Factory for creating different prompt template variations."""
    
    @staticmethod
    def create_conservative_prompt() -> PromptTemplate:
        """Create a conservative prompt that emphasizes risk aversion."""
        
        template = """You are a conservative automobile insurance underwriter with a strong focus on risk management and loss prevention. Your primary objective is to protect the company from high-risk exposures while maintaining regulatory compliance.

UNDERWRITING RULES:
{rules}

APPLICANT INFORMATION:
{applicant_data}

CONSERVATIVE EVALUATION APPROACH:
1. Apply a strict interpretation of all underwriting rules
2. When in doubt, err on the side of caution (DENY or ADJUDICATE)
3. Give extra weight to recent violations and claims
4. Be particularly cautious with young drivers, high-performance vehicles, and poor credit scores
5. Consider cumulative risk factors - multiple minor issues may warrant denial
6. Prioritize long-term profitability over market share

DECISION CRITERIA (CONSERVATIVE):
- DENY: Apply hard stops strictly and consider borderline cases for denial
- ADJUDICATE: Use liberally for any case with multiple risk factors or uncertainty
- ACCEPT: Reserve for clearly low-risk applicants with excellent records

RISK ASSESSMENT PRIORITIES:
1. Claims history (highest weight)
2. Violation history 
3. Credit score and financial stability
4. Vehicle type and value
5. Driver age and experience
6. Coverage history

RESPONSE FORMAT:
Decision: [ACCEPT/DENY/ADJUDICATE]
Primary Reason: [Conservative risk-focused explanation]
Triggered Rules: [List specific rule IDs]
Risk Factors: [Comprehensive list of all identified risks]
Conservative Notes: [Additional risk considerations and concerns]

Evaluate this applicant with a conservative, risk-averse approach:"""

        return PromptTemplate(
            input_variables=["rules", "applicant_data"],
            template=template
        )
    
    @staticmethod
    def create_balanced_prompt() -> PromptTemplate:
        """Create the standard balanced prompt (original)."""
        
        template = """You are an expert automobile insurance underwriter. Your task is to evaluate an insurance applicant based on established underwriting rules and make one of three decisions: ACCEPT, DENY, or ADJUDICATE.

UNDERWRITING RULES:
{rules}

APPLICANT INFORMATION:
{applicant_data}

EVALUATION INSTRUCTIONS:
1. Carefully review the applicant's information against the underwriting rules
2. Check for any HARD STOPS that would result in automatic DENIAL
3. Check for any conditions that require ADJUDICATION (manual review)
4. If no hard stops or adjudication triggers apply, evaluate for ACCEPTANCE
5. Provide your decision with clear reasoning

DECISION CRITERIA:
- DENY: If any hard stop criteria are met (invalid license, multiple DUI, excessive claims, fraud history, extended coverage lapse)
- ADJUDICATE: If moderate risk factors require manual review (moderate violations, single major violation, young driver with violations, high-performance vehicle, poor credit, short coverage lapse)
- ACCEPT: If applicant meets acceptance criteria (clean record, minimal issues within acceptable limits)

RESPONSE FORMAT:
Decision: [ACCEPT/DENY/ADJUDICATE]
Primary Reason: [Brief explanation of the main factor driving the decision]
Triggered Rules: [List specific rule IDs that influenced the decision]
Risk Factors: [List key risk factors identified]
Additional Notes: [Any other relevant observations]

Please evaluate the applicant now:"""

        return PromptTemplate(
            input_variables=["rules", "applicant_data"],
            template=template
        )
    
    @staticmethod
    def create_liberal_prompt() -> PromptTemplate:
        """Create a liberal prompt that emphasizes market growth and inclusion."""
        
        template = """You are a growth-oriented automobile insurance underwriter focused on market expansion and customer inclusion. Your goal is to maximize policy issuance while maintaining acceptable risk levels and regulatory compliance.

UNDERWRITING RULES:
{rules}

APPLICANT INFORMATION:
{applicant_data}

LIBERAL EVALUATION APPROACH:
1. Apply underwriting rules with flexibility and consideration for individual circumstances
2. Look for reasons to ACCEPT rather than reasons to DENY
3. Consider positive factors that may offset negative ones
4. Give weight to recent improvements in driving behavior or credit
5. Recognize that past issues may not predict future performance
6. Balance risk management with business growth objectives

DECISION CRITERIA (LIBERAL):
- DENY: Only for clear hard stops that cannot be mitigated
- ADJUDICATE: For cases that need human review but have potential for acceptance
- ACCEPT: For applicants who meet basic safety standards, even with minor issues

POSITIVE FACTORS TO CONSIDER:
1. Length of time since last violation or claim
2. Overall driving experience and maturity
3. Stable employment and residence
4. Willingness to accept higher deductibles
5. Multiple vehicles or policies (loyalty indicators)
6. Completion of driver education or safety courses

RESPONSE FORMAT:
Decision: [ACCEPT/DENY/ADJUDICATE]
Primary Reason: [Growth-focused explanation emphasizing positive aspects]
Triggered Rules: [List specific rule IDs]
Risk Factors: [Balanced view of risks and mitigating factors]
Liberal Notes: [Opportunities for acceptance and risk mitigation]

Evaluate this applicant with a growth-oriented, inclusive approach:"""

        return PromptTemplate(
            input_variables=["rules", "applicant_data"],
            template=template
        )
    
    @staticmethod
    def create_detailed_prompt() -> PromptTemplate:
        """Create a detailed prompt that requires comprehensive analysis."""
        
        template = """You are a senior automobile insurance underwriter with extensive experience in complex risk assessment. You are known for your thorough, methodical approach to underwriting decisions and comprehensive documentation.

UNDERWRITING RULES:
{rules}

APPLICANT INFORMATION:
{applicant_data}

DETAILED EVALUATION REQUIREMENTS:
1. Conduct a comprehensive analysis of all risk factors
2. Examine the interplay between different risk elements
3. Consider both quantitative metrics and qualitative factors
4. Evaluate trends and patterns in the applicant's history
5. Assess the credibility and completeness of provided information
6. Consider regulatory and competitive implications

COMPREHENSIVE ANALYSIS FRAMEWORK:
A. DRIVER RISK ASSESSMENT:
   - Age and experience correlation
   - Violation pattern analysis
   - Claims frequency and severity trends
   - License history and status

B. VEHICLE RISK ASSESSMENT:
   - Safety ratings and features
   - Theft susceptibility
   - Repair costs and availability
   - Usage patterns and mileage

C. FINANCIAL RISK ASSESSMENT:
   - Credit score implications
   - Payment history indicators
   - Employment stability
   - Coverage history and lapses

D. ENVIRONMENTAL RISK FACTORS:
   - Geographic territory risks
   - Seasonal considerations
   - Local traffic patterns
   - Crime statistics

DECISION CRITERIA (DETAILED):
- DENY: Comprehensive risk analysis indicates unacceptable exposure
- ADJUDICATE: Complex risk profile requires specialized underwriter review
- ACCEPT: Thorough analysis confirms acceptable risk within guidelines

RESPONSE FORMAT:
Decision: [ACCEPT/DENY/ADJUDICATE]
Primary Reason: [Detailed explanation with supporting analysis]
Triggered Rules: [Complete list of applicable rules with explanations]
Risk Factors: [Comprehensive risk factor analysis with severity ratings]
Detailed Analysis: [In-depth discussion of risk interactions and considerations]
Recommendations: [Specific suggestions for risk mitigation or monitoring]

Provide a comprehensive, detailed evaluation of this applicant:"""

        return PromptTemplate(
            input_variables=["rules", "applicant_data"],
            template=template
        )
    
    @staticmethod
    def create_concise_prompt() -> PromptTemplate:
        """Create a concise prompt focused on efficiency and speed."""
        
        template = """You are an efficient automobile insurance underwriter focused on quick, accurate decisions. Make clear determinations based on key risk factors.

RULES: {rules}

APPLICANT: {applicant_data}

QUICK EVALUATION:
1. Check hard stops → DENY if found
2. Check adjudication triggers → ADJUDICATE if found  
3. Otherwise → ACCEPT

DECISION CRITERIA:
- DENY: Hard stop violations (DUI, fraud, excessive claims, invalid license, long lapse)
- ADJUDICATE: Moderate risks needing review (young driver violations, poor credit, recent claims)
- ACCEPT: Clean or minimal risk profile

FORMAT:
Decision: [ACCEPT/DENY/ADJUDICATE]
Reason: [Brief, specific explanation]
Rules: [Key rule IDs]
Factors: [Main risk factors]

Evaluate quickly and decisively:"""

        return PromptTemplate(
            input_variables=["rules", "applicant_data"],
            template=template
        )
    
    @staticmethod
    def get_prompt_template(variant: PromptVariant) -> PromptTemplate:
        """Get a prompt template by variant type."""
        
        factory_methods = {
            PromptVariant.CONSERVATIVE: PromptTemplateFactory.create_conservative_prompt,
            PromptVariant.BALANCED: PromptTemplateFactory.create_balanced_prompt,
            PromptVariant.LIBERAL: PromptTemplateFactory.create_liberal_prompt,
            PromptVariant.DETAILED: PromptTemplateFactory.create_detailed_prompt,
            PromptVariant.CONCISE: PromptTemplateFactory.create_concise_prompt
        }
        
        if variant not in factory_methods:
            raise ValueError(f"Unknown prompt variant: {variant}")
        
        return factory_methods[variant]()
    
    @staticmethod
    def get_all_variants() -> Dict[str, PromptTemplate]:
        """Get all prompt template variants."""
        
        return {
            variant.value: PromptTemplateFactory.get_prompt_template(variant)
            for variant in PromptVariant
        }
    
    @staticmethod
    def get_variant_descriptions() -> Dict[str, str]:
        """Get descriptions of each prompt variant."""
        
        return {
            PromptVariant.CONSERVATIVE.value: "Risk-averse approach emphasizing loss prevention and strict rule interpretation",
            PromptVariant.BALANCED.value: "Standard balanced approach following established guidelines",
            PromptVariant.LIBERAL.value: "Growth-oriented approach emphasizing market expansion and inclusion",
            PromptVariant.DETAILED.value: "Comprehensive analysis requiring thorough documentation and consideration",
            PromptVariant.CONCISE.value: "Efficient approach focused on quick, clear decisions"
        }

class PromptTestConfiguration:
    """Configuration for prompt template A/B testing."""
    
    def __init__(self, base_rules_file: str = "underwriting_rules.json"):
        """Initialize with base rules file."""
        self.base_rules_file = base_rules_file
        self.configurations = {}
        self._create_configurations()
    
    def _create_configurations(self):
        """Create test configurations for each prompt variant."""
        
        descriptions = PromptTemplateFactory.get_variant_descriptions()
        
        for variant in PromptVariant:
            self.configurations[variant.value] = {
                'variant_id': variant.value,
                'name': f"Prompt Template - {variant.value.title()}",
                'description': descriptions[variant.value],
                'rules_file': self.base_rules_file,
                'prompt_template': PromptTemplateFactory.get_prompt_template(variant),
                'parameters': {
                    'prompt_variant': variant.value,
                    'focus': self._get_variant_focus(variant)
                }
            }
    
    def _get_variant_focus(self, variant: PromptVariant) -> str:
        """Get the primary focus of each variant."""
        
        focus_map = {
            PromptVariant.CONSERVATIVE: "risk_aversion",
            PromptVariant.BALANCED: "balanced_assessment", 
            PromptVariant.LIBERAL: "market_growth",
            PromptVariant.DETAILED: "comprehensive_analysis",
            PromptVariant.CONCISE: "efficiency"
        }
        
        return focus_map.get(variant, "unknown")
    
    def get_configuration(self, variant: str) -> Dict[str, Any]:
        """Get configuration for a specific variant."""
        
        if variant not in self.configurations:
            raise ValueError(f"Unknown variant: {variant}")
        
        return self.configurations[variant]
    
    def get_all_configurations(self) -> Dict[str, Dict[str, Any]]:
        """Get all prompt template configurations."""
        
        return self.configurations.copy()
    
    def get_comparison_pairs(self) -> List[Tuple[str, str]]:
        """Get recommended comparison pairs for A/B testing."""
        
        return [
            (PromptVariant.CONSERVATIVE.value, PromptVariant.LIBERAL.value),
            (PromptVariant.BALANCED.value, PromptVariant.CONSERVATIVE.value),
            (PromptVariant.BALANCED.value, PromptVariant.LIBERAL.value),
            (PromptVariant.DETAILED.value, PromptVariant.CONCISE.value),
            (PromptVariant.BALANCED.value, PromptVariant.DETAILED.value)
        ]


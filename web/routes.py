"""
Flask routes for the underwriting web interface.
"""

import json
import os
from datetime import datetime
from flask import (
    Blueprint, render_template, request, jsonify, 
    flash, redirect, url_for, current_app
)

from underwriting.core.engine import UnderwritingEngine
from underwriting.core.models import (
    Applicant, Driver, Vehicle, Violation, Claim,
    LicenseStatus, ViolationType, ClaimType, VehicleCategory
)
from underwriting.data.sample_generator import create_sample_applicants
from underwriting.testing.ab_engine import ABTestEngine
from underwriting.testing.statistical_analysis import StatisticalAnalyzer

from .forms import ApplicantForm, ABTestForm, QuickTestForm

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)


@main_bp.route('/')
def index():
    """Home page with system overview."""
    return render_template('index.html')


@main_bp.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    """Applicant evaluation page."""
    form = ApplicantForm()
    
    if form.validate_on_submit():
        try:
            # Create applicant from form data
            applicant = create_applicant_from_form(form)
            
            # Initialize engine with selected rules
            engine = UnderwritingEngine(rules_file=form.rules_file.data)
            
            # Evaluate applicant
            result = engine.evaluate_applicant(applicant)
            
            # Render results
            return render_template('results.html', 
                                 applicant=applicant, 
                                 result=result,
                                 form_data=form.data)
            
        except Exception as e:
            flash(f'Error evaluating applicant: {str(e)}', 'error')
            current_app.logger.error(f'Evaluation error: {e}')
    
    return render_template('evaluate.html', form=form)


@main_bp.route('/quick-test', methods=['GET', 'POST'])
def quick_test():
    """Quick testing with sample applicants."""
    form = QuickTestForm()
    
    if form.validate_on_submit():
        try:
            # Get sample applicants
            sample_applicants = create_sample_applicants()
            
            # Filter based on test type
            if form.test_type.data == 'sample_accept':
                applicants = sample_applicants[:2]  # First 2 are accept cases
            elif form.test_type.data == 'sample_deny':
                applicants = sample_applicants[2:4]  # Next 2 are deny cases
            elif form.test_type.data == 'sample_adjudicate':
                applicants = sample_applicants[4:6]  # Last 2 are adjudicate cases
            else:
                applicants = sample_applicants  # All applicants
            
            # Initialize engine
            engine = UnderwritingEngine(rules_file=form.rules_file.data)
            
            # Evaluate all applicants
            results = []
            for applicant in applicants:
                result = engine.evaluate_applicant(applicant)
                results.append({
                    'applicant': applicant,
                    'result': result
                })
            
            return render_template('quick_test_results.html', 
                                 results=results,
                                 test_type=form.test_type.data,
                                 rules_file=form.rules_file.data)
            
        except Exception as e:
            flash(f'Error running quick test: {str(e)}', 'error')
            current_app.logger.error(f'Quick test error: {e}')
    
    return render_template('quick_test.html', form=form)


@main_bp.route('/ab-test', methods=['GET', 'POST'])
def ab_test():
    """A/B testing interface."""
    form = ABTestForm()
    
    if form.validate_on_submit():
        try:
            # Initialize A/B test engine
            ab_engine = ABTestEngine()
            
            # Get sample applicants for testing
            applicants = create_sample_applicants()
            
            # Run A/B test based on type
            if form.test_type.data == 'rule_comparison':
                results = run_rule_comparison(
                    ab_engine, applicants,
                    form.variant_a.data, form.variant_b.data,
                    form.confidence_level.data, form.monthly_applications.data
                )
            elif form.test_type.data == 'prompt_comparison':
                results = run_prompt_comparison(
                    ab_engine, applicants,
                    form.variant_a.data, form.variant_b.data,
                    form.confidence_level.data, form.monthly_applications.data
                )
            else:  # comprehensive
                results = run_comprehensive_test(
                    ab_engine, applicants,
                    form.confidence_level.data, form.monthly_applications.data
                )
            
            return render_template('ab_test_results.html', 
                                 results=results,
                                 form_data=form.data)
            
        except Exception as e:
            flash(f'Error running A/B test: {str(e)}', 'error')
            current_app.logger.error(f'A/B test error: {e}')
    
    return render_template('ab_test.html', form=form)


@main_bp.route('/documentation')
def documentation():
    """Documentation and help page."""
    return render_template('documentation.html')


@main_bp.route('/configuration')
def configuration():
    """Configuration and rules viewer."""
    try:
        # Load all rule configurations
        rules_configs = {}
        rule_files = [
            ('Standard', 'config/rules/underwriting_rules.json'),
            ('Conservative', 'config/rules/underwriting_rules_conservative.json'),
            ('Liberal', 'config/rules/underwriting_rules_liberal.json')
        ]
        
        for name, file_path in rule_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    rules_configs[name] = json.load(f)
        
        return render_template('configuration.html', rules_configs=rules_configs)
        
    except Exception as e:
        flash(f'Error loading configurations: {str(e)}', 'error')
        return render_template('configuration.html', rules_configs={})


# API Routes
@api_bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@api_bp.route('/evaluate', methods=['POST'])
def api_evaluate():
    """API endpoint for applicant evaluation."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['applicant_id', 'driver', 'credit_score', 'territory']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create applicant from JSON data
        applicant = create_applicant_from_json(data)
        
        # Initialize engine
        rules_file = data.get('rules_file', 'config/rules/underwriting_rules.json')
        engine = UnderwritingEngine(rules_file=rules_file)
        
        # Evaluate applicant
        result = engine.evaluate_applicant(applicant)
        
        # Return result as JSON
        return jsonify({
            'applicant_id': result.applicant_id,
            'decision': result.decision.value,
            'reason': result.reason,
            'triggered_rules': result.triggered_rules,
            'risk_factors': result.risk_factors,
            'timestamp': result.timestamp.isoformat()
        })
        
    except Exception as e:
        current_app.logger.error(f'API evaluation error: {e}')
        return jsonify({'error': str(e)}), 500


@api_bp.route('/sample-applicants')
def api_sample_applicants():
    """API endpoint to get sample applicants."""
    try:
        applicants = create_sample_applicants()
        
        # Convert to JSON-serializable format
        applicants_data = []
        for applicant in applicants:
            applicants_data.append({
                'applicant_id': applicant.applicant_id,
                'driver': {
                    'first_name': applicant.primary_driver.first_name,
                    'last_name': applicant.primary_driver.last_name,
                    'age': applicant.primary_driver.age,
                    'license_status': applicant.primary_driver.license_status.value,
                    'years_licensed': applicant.primary_driver.years_licensed
                },
                'credit_score': applicant.credit_score,
                'prior_insurance_lapse_days': applicant.prior_insurance_lapse_days,
                'territory': applicant.territory,
                'violations_count': len(applicant.primary_driver.violations),
                'claims_count': len(applicant.primary_driver.claims),
                'vehicles_count': len(applicant.vehicles)
            })
        
        return jsonify({'applicants': applicants_data})
        
    except Exception as e:
        current_app.logger.error(f'API sample applicants error: {e}')
        return jsonify({'error': str(e)}), 500


# Helper functions
def create_applicant_from_form(form):
    """Create an Applicant object from form data."""
    
    # Create driver
    driver = Driver(
        first_name=form.driver.first_name.data,
        last_name=form.driver.last_name.data,
        age=form.driver.age.data,
        license_status=LicenseStatus(form.driver.license_status.data),
        license_state=form.driver.license_state.data.upper(),
        years_licensed=form.driver.years_licensed.data,
        violations=[],  # Would be populated from dynamic form fields
        claims=[]  # Would be populated from dynamic form fields
    )
    
    # Create basic vehicle (would be expanded for multiple vehicles)
    vehicles = [
        Vehicle(
            year=2020,
            make="Toyota",
            model="Camry",
            vehicle_type=VehicleCategory.SEDAN,
            vin=""
        )
    ]
    
    # Create applicant
    applicant = Applicant(
        applicant_id=form.applicant_id.data,
        primary_driver=driver,
        vehicles=vehicles,
        credit_score=form.credit_score.data,
        prior_insurance_lapse_days=form.coverage_lapse_days.data,
        territory=form.territory.data,
        coverage_requested=form.requested_coverage.data
    )
    
    return applicant


def create_applicant_from_json(data):
    """Create an Applicant object from JSON data."""
    # Implementation would parse JSON and create Applicant object
    # This is a simplified version
    pass


def run_rule_comparison(ab_engine, applicants, variant_a, variant_b, confidence_level, monthly_apps):
    """Run rule comparison A/B test."""
    # Implementation would use the A/B testing engine
    # This is a placeholder for the actual implementation
    return {
        'test_type': 'rule_comparison',
        'variant_a': variant_a,
        'variant_b': variant_b,
        'results': 'Placeholder results'
    }


def run_prompt_comparison(ab_engine, applicants, variant_a, variant_b, confidence_level, monthly_apps):
    """Run prompt comparison A/B test."""
    # Implementation would use the A/B testing engine
    return {
        'test_type': 'prompt_comparison',
        'variant_a': variant_a,
        'variant_b': variant_b,
        'results': 'Placeholder results'
    }


def run_comprehensive_test(ab_engine, applicants, confidence_level, monthly_apps):
    """Run comprehensive A/B test suite."""
    # Implementation would run multiple tests
    return {
        'test_type': 'comprehensive',
        'results': 'Placeholder comprehensive results'
    }


"""
Web forms for the underwriting system using Flask-WTF.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField, DateField, 
    FloatField, FieldList, FormField, SubmitField,
    TextAreaField, BooleanField
)
from wtforms.validators import (
    DataRequired, NumberRange, Length, Optional,
    ValidationError
)
from datetime import date, timedelta

from underwriting.core.models import (
    LicenseStatus, ViolationType, ClaimType, VehicleCategory
)


class ViolationForm(FlaskForm):
    """Form for individual violation entry."""
    
    violation_type = SelectField(
        'Violation Type',
        choices=[(v.value, v.value.replace('_', ' ').title()) for v in ViolationType],
        validators=[DataRequired()]
    )
    
    date = DateField(
        'Date',
        validators=[DataRequired()],
        default=date.today() - timedelta(days=365)
    )
    
    description = StringField(
        'Description',
        validators=[Length(max=200)],
        render_kw={"placeholder": "Optional description"}
    )


class ClaimForm(FlaskForm):
    """Form for individual claim entry."""
    
    claim_type = SelectField(
        'Claim Type',
        choices=[(c.value, c.value.replace('_', ' ').title()) for c in ClaimType],
        validators=[DataRequired()]
    )
    
    date = DateField(
        'Date',
        validators=[DataRequired()],
        default=date.today() - timedelta(days=365)
    )
    
    amount = FloatField(
        'Amount ($)',
        validators=[DataRequired(), NumberRange(min=0, max=1000000)],
        render_kw={"placeholder": "0.00"}
    )
    
    at_fault = BooleanField(
        'At Fault',
        default=False
    )


class VehicleForm(FlaskForm):
    """Form for individual vehicle entry."""
    
    year = IntegerField(
        'Year',
        validators=[DataRequired(), NumberRange(min=1990, max=date.today().year + 1)],
        default=2020
    )
    
    make = StringField(
        'Make',
        validators=[DataRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "Toyota, Honda, Ford, etc."}
    )
    
    model = StringField(
        'Model',
        validators=[DataRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "Camry, Civic, F-150, etc."}
    )
    
    vehicle_type = SelectField(
        'Vehicle Category',
        choices=[(v.value, v.value.replace('_', ' ').title()) for v in VehicleCategory],
        validators=[DataRequired()]
    )
    
    vin = StringField(
        'VIN',
        validators=[Optional(), Length(min=17, max=17)],
        render_kw={"placeholder": "17-character VIN (optional)"}
    )


class DriverForm(FlaskForm):
    """Form for driver information."""
    
    first_name = StringField(
        'First Name',
        validators=[DataRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "John"}
    )
    
    last_name = StringField(
        'Last Name', 
        validators=[DataRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "Smith"}
    )
    
    age = IntegerField(
        'Age',
        validators=[DataRequired(), NumberRange(min=16, max=100)],
        default=35
    )
    
    license_status = SelectField(
        'License Status',
        choices=[(s.value, s.value.replace('_', ' ').title()) for s in LicenseStatus],
        validators=[DataRequired()]
    )
    
    license_state = StringField(
        'License State',
        validators=[DataRequired(), Length(min=2, max=2)],
        render_kw={"placeholder": "TX, CA, NY, etc."}
    )
    
    years_licensed = IntegerField(
        'Years Licensed',
        validators=[DataRequired(), NumberRange(min=0, max=80)],
        default=10
    )


class ApplicantForm(FlaskForm):
    """Main form for applicant information."""
    
    applicant_id = StringField(
        'Applicant ID',
        validators=[DataRequired(), Length(min=3, max=20)],
        render_kw={"placeholder": "APP001"}
    )
    
    # Driver information
    driver = FormField(DriverForm, label="Primary Driver")
    
    # Credit score
    credit_score = IntegerField(
        'Credit Score',
        validators=[DataRequired(), NumberRange(min=300, max=850)],
        default=700
    )
    
    # Coverage lapse
    coverage_lapse_days = IntegerField(
        'Coverage Lapse (Days)',
        validators=[DataRequired(), NumberRange(min=0, max=3650)],
        default=0,
        render_kw={"placeholder": "0 for continuous coverage"}
    )
    
    # Territory
    territory = StringField(
        'Territory/ZIP Code',
        validators=[DataRequired(), Length(min=5, max=10)],
        render_kw={"placeholder": "75001 or URBAN_TX"}
    )
    
    # Requested coverage
    requested_coverage = SelectField(
        'Requested Coverage',
        choices=[
            ('LIABILITY_ONLY', 'Liability Only'),
            ('BASIC', 'Basic Coverage'),
            ('STANDARD', 'Standard Coverage'),
            ('COMPREHENSIVE', 'Comprehensive Coverage'),
            ('PREMIUM', 'Premium Coverage')
        ],
        validators=[DataRequired()],
        default='STANDARD'
    )
    
    # Rules file selection
    rules_file = SelectField(
        'Underwriting Rules',
        choices=[
            ('config/rules/underwriting_rules.json', 'Standard Rules'),
            ('config/rules/underwriting_rules_conservative.json', 'Conservative Rules'),
            ('config/rules/underwriting_rules_liberal.json', 'Liberal Rules')
        ],
        validators=[DataRequired()],
        default='config/rules/underwriting_rules.json'
    )
    
    submit = SubmitField('Evaluate Applicant')
    
    def validate_coverage_lapse_days(self, field):
        """Custom validation for coverage lapse."""
        if field.data > 365:
            raise ValidationError('Coverage lapse over 1 year may result in automatic denial.')


class ABTestForm(FlaskForm):
    """Form for A/B testing configuration."""
    
    test_type = SelectField(
        'Test Type',
        choices=[
            ('rule_comparison', 'Rule Comparison'),
            ('prompt_comparison', 'Prompt Comparison'),
            ('comprehensive', 'Comprehensive Test Suite')
        ],
        validators=[DataRequired()],
        default='rule_comparison'
    )
    
    variant_a = SelectField(
        'Variant A',
        choices=[
            ('standard', 'Standard'),
            ('conservative', 'Conservative'),
            ('liberal', 'Liberal'),
            ('balanced', 'Balanced Prompt'),
            ('detailed', 'Detailed Prompt'),
            ('concise', 'Concise Prompt')
        ],
        validators=[DataRequired()],
        default='standard'
    )
    
    variant_b = SelectField(
        'Variant B',
        choices=[
            ('standard', 'Standard'),
            ('conservative', 'Conservative'),
            ('liberal', 'Liberal'),
            ('balanced', 'Balanced Prompt'),
            ('detailed', 'Detailed Prompt'),
            ('concise', 'Concise Prompt')
        ],
        validators=[DataRequired()],
        default='liberal'
    )
    
    confidence_level = FloatField(
        'Confidence Level',
        validators=[DataRequired(), NumberRange(min=0.8, max=0.99)],
        default=0.95,
        render_kw={"step": "0.01", "placeholder": "0.95"}
    )
    
    monthly_applications = IntegerField(
        'Monthly Applications',
        validators=[DataRequired(), NumberRange(min=1000, max=1000000)],
        default=10000,
        render_kw={"placeholder": "10000"}
    )
    
    submit = SubmitField('Run A/B Test')


class QuickTestForm(FlaskForm):
    """Form for quick testing with sample applicants."""
    
    test_type = SelectField(
        'Test Type',
        choices=[
            ('sample_all', 'Test All Sample Applicants'),
            ('sample_accept', 'Test Accept Cases Only'),
            ('sample_deny', 'Test Deny Cases Only'),
            ('sample_adjudicate', 'Test Adjudicate Cases Only')
        ],
        validators=[DataRequired()],
        default='sample_all'
    )
    
    rules_file = SelectField(
        'Underwriting Rules',
        choices=[
            ('config/rules/underwriting_rules.json', 'Standard Rules'),
            ('config/rules/underwriting_rules_conservative.json', 'Conservative Rules'),
            ('config/rules/underwriting_rules_liberal.json', 'Liberal Rules')
        ],
        validators=[DataRequired()],
        default='config/rules/underwriting_rules.json'
    )
    
    submit = SubmitField('Run Quick Test')


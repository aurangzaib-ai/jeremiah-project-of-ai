from datetime import date, timedelta
from underwriting.core.models import (
    Applicant, Driver, Vehicle, Violation, Claim,
    LicenseStatus, ViolationType, ClaimType, VehicleCategory
)

def create_sample_applicants():
    """Create 6 sample applicants for testing: 2 accept, 2 deny, 2 adjudicate."""
    
    applicants = []
    
    # APPLICANT 1 - SHOULD BE ACCEPTED
    applicant1 = Applicant(
        applicant_id="APP001",
        primary_driver=Driver(
            driver_id="DRV001",
            first_name="Sarah",
            last_name="Johnson",
            date_of_birth=date(1985, 3, 15),
            license_number="D123456789",
            license_state="CA",
            license_status=LicenseStatus.VALID,
            license_issue_date=date(2003, 3, 15),
            license_expiration_date=date(2027, 3, 15),
            violations=[],
            claims=[]
        ),
        vehicles=[
            Vehicle(
                vin="1HGBH41JXMN109186",
                year=2020,
                make="Honda",
                model="Accord",
                category=VehicleCategory.SEDAN,
                value=25000.0,
                vehicle_type=VehicleCategory.SEDAN
            )
        ],
        credit_score=750,
        prior_insurance_lapse_days=0,
        fraud_history=False,
        territory="Urban",
        coverage_requested=["Liability", "Collision", "Comprehensive"]
    )
    applicants.append(applicant1)
    
    # APPLICANT 2 - SHOULD BE ACCEPTED
    applicant2 = Applicant(
        applicant_id="APP002",
        primary_driver=Driver(
            driver_id="DRV002",
            first_name="Michael",
            last_name="Chen",
            date_of_birth=date(1978, 8, 22),
            license_number="D987654321",
            license_state="TX",
            license_status=LicenseStatus.VALID,
            license_issue_date=date(1996, 8, 22),
            license_expiration_date=date(2026, 8, 22),
            violations=[
                Violation(
                    violation_type=ViolationType.SPEEDING_10_UNDER,
                    violation_date=date(2021, 6, 10),
                    description="Speeding 8 mph over limit"
                )
            ],
            claims=[
                Claim(
                    claim_type=ClaimType.NOT_AT_FAULT,
                    claim_date=date(2020, 11, 5),
                    claim_amount=3500.0,
                    description="Rear-ended at traffic light"
                )
            ]
        ),
        vehicles=[
            Vehicle(
                vin="5NPE34AF4HH012345",
                year=2019,
                make="Hyundai",
                model="Elantra",
                category=VehicleCategory.SEDAN,
                value=18000.0,
                vehicle_type=VehicleCategory.SEDAN
            )
        ],
        credit_score=680,
        prior_insurance_lapse_days=15,
        fraud_history=False,
        territory="Urban",
        coverage_requested=["Liability", "Collision", "Comprehensive"]
    )
    applicants.append(applicant2)
    
    # APPLICANT 3 - SHOULD BE DENIED
    applicant3 = Applicant(
        applicant_id="APP003",
        primary_driver=Driver(
            driver_id="DRV003",
            first_name="Robert",
            last_name="Williams",
            date_of_birth=date(1990, 12, 3),
            license_number="D555666777",
            license_state="FL",
            license_status=LicenseStatus.VALID,
            license_issue_date=date(2008, 12, 3),
            license_expiration_date=date(2025, 12, 3),
            violations=[
                Violation(
                    violation_type=ViolationType.DUI,
                    violation_date=date(2022, 4, 18),
                    conviction_date=date(2022, 8, 15),
                    description="DUI - BAC 0.12"
                ),
                Violation(
                    violation_type=ViolationType.DUI,
                    violation_date=date(2020, 9, 22),
                    conviction_date=date(2021, 1, 10),
                    description="DUI - BAC 0.15"
                )
            ],
            claims=[
                Claim(
                    claim_type=ClaimType.AT_FAULT,
                    claim_date=date(2022, 4, 18),
                    claim_amount=15000.0,
                    description="Single vehicle accident - DUI related"
                )
            ]
        ),
        vehicles=[
            Vehicle(
                vin="1G1ZT53806F123456",
                year=2018,
                make="Chevrolet",
                model="Malibu",
                category=VehicleCategory.SEDAN,
                value=16000.0,
                vehicle_type=VehicleCategory.SEDAN
            )
        ],
        credit_score=520,
        prior_insurance_lapse_days=45,
        fraud_history=False,
        territory="Urban",
        coverage_requested=["Liability", "Collision", "Comprehensive"]
    )
    applicants.append(applicant3)
    
    # APPLICANT 4 - SHOULD BE DENIED
    applicant4 = Applicant(
        applicant_id="APP004",
        primary_driver=Driver(
            driver_id="DRV004",
            first_name="Jennifer",
            last_name="Davis",
            date_of_birth=date(1995, 5, 8),
            license_number="D111222333",
            license_state="NY",
            license_status=LicenseStatus.VALID,
            license_issue_date=date(2013, 5, 8),
            license_expiration_date=date(2025, 5, 8),
            violations=[
                Violation(
                    violation_type=ViolationType.SPEEDING_15_OVER,
                    violation_date=date(2023, 2, 14),
                    description="Speeding 18 mph over limit"
                )
            ],
            claims=[
                Claim(
                    claim_type=ClaimType.AT_FAULT,
                    claim_date=date(2022, 7, 30),
                    claim_amount=8500.0,
                    description="Collision with parked car"
                ),
                Claim(
                    claim_type=ClaimType.AT_FAULT,
                    claim_date=date(2021, 11, 12),
                    claim_amount=12000.0,
                    description="Intersection collision"
                ),
                Claim(
                    claim_type=ClaimType.AT_FAULT,
                    claim_date=date(2020, 3, 25),
                    claim_amount=6500.0,
                    description="Backing into another vehicle"
                )
            ]
        ),
        vehicles=[
            Vehicle(
                vin="WBAVA37598NJ12345",
                year=2017,
                make="BMW",
                model="328i",
                category=VehicleCategory.LUXURY_SEDAN,
                value=22000.0,
                vehicle_type=VehicleCategory.SEDAN
            )
        ],
        credit_score=580,
        prior_insurance_lapse_days=120,
        fraud_history=False,
        territory="Urban",
        coverage_requested=["Liability", "Collision", "Comprehensive"]
    )
    applicants.append(applicant4)
    
    # APPLICANT 5 - SHOULD REQUIRE ADJUDICATION
    applicant5 = Applicant(
        applicant_id="APP005",
        primary_driver=Driver(
            driver_id="DRV005",
            first_name="Tyler",
            last_name="Martinez",
            date_of_birth=date(2003, 9, 12),
            license_number="D444555666",
            license_state="AZ",
            license_status=LicenseStatus.VALID,
            license_issue_date=date(2021, 9, 12),
            license_expiration_date=date(2029, 9, 12),
            violations=[
                Violation(
                    violation_type=ViolationType.SPEEDING_15_OVER,
                    violation_date=date(2023, 8, 5),
                    description="Speeding 20 mph over limit"
                ),
                Violation(
                    violation_type=ViolationType.IMPROPER_PASSING,
                    violation_date=date(2023, 3, 18),
                    description="Unsafe passing on highway"
                )
            ],
            claims=[]
        ),
        vehicles=[
            Vehicle(
                vin="JH4KA8260MC123456",
                year=2015,
                make="Acura",
                model="TLX",
                category=VehicleCategory.SPORTS_CAR,
                value=19000.0,
                vehicle_type=VehicleCategory.SPORTS_CAR
            )
        ],
        credit_score=620,
        prior_insurance_lapse_days=0,
        fraud_history=False,
        territory="Urban",
        coverage_requested=["Liability", "Collision", "Comprehensive"]
    )
    applicants.append(applicant5)
    
    # APPLICANT 6 - FIXED: Now SHOULD BE ACCEPTED
    applicant6 = Applicant(
        applicant_id="APP006",
        primary_driver=Driver(
            driver_id="DRV006",
            first_name="Amanda",
            last_name="Thompson",
            date_of_birth=date(1988, 11, 30),
            license_number="D777888999",
            license_state="WA",
            license_status=LicenseStatus.VALID,
            license_issue_date=date(2006, 11, 30),
            license_expiration_date=date(2026, 11, 30),
            violations=[
                Violation(
                    violation_type=ViolationType.SPEEDING_10_UNDER,
                    violation_date=date(2020, 1, 1),
                    description="Speeding 8 mph over limit"
                )
            ],
            claims=[]
        ),
        vehicles=[
            Vehicle(
                vin="1FTFW1ET5DFC12345",
                year=2021,
                make="Ford",
                model="F-150",
                category=VehicleCategory.PICKUP,
                value=35000.0,
                vehicle_type=VehicleCategory.PICKUP
            )
        ],
        credit_score=710,
        prior_insurance_lapse_days=0,
        fraud_history=False,
        territory="Urban",
        coverage_requested=["Liability", "Collision", "Comprehensive"]
    )
    applicants.append(applicant6)
    
    return applicants

def print_applicant_summary(applicant: Applicant):
    driver = applicant.primary_driver
    print(f"\n=== {applicant.applicant_id}: {driver.first_name} {driver.last_name} ===")
    print(f"Age: {driver.age}")
    print(f"License Status: {driver.license_status.value}")
    print(f"Violations: {len(driver.violations)}")
    for v in driver.violations:
        years_ago = (date.today() - v.violation_date).days // 365
        print(f"  - {v.violation_type.value} ({years_ago} years ago)")
    print(f"Claims: {len(driver.claims)}")
    for c in driver.claims:
        years_ago = (date.today() - c.claim_date).days // 365
        print(f"  - {c.claim_type.value}: ${c.claim_amount:,.0f} ({years_ago} years ago)")
    print(f"Credit Score: {applicant.credit_score}")
    print(f"Coverage Lapse: {applicant.prior_insurance_lapse_days} days")
    print(f"Vehicles: {len(applicant.vehicles)}")
    for v in applicant.vehicles:
        print(f"  - {v.year} {v.make} {v.model} ({v.category.value})")

if __name__ == "__main__":
    applicants = create_sample_applicants()
    print("SAMPLE APPLICANTS FOR TESTING")
    print("=" * 50)
    for applicant in applicants:
        print_applicant_summary(applicant)

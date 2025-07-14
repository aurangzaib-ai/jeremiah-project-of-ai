from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum

class LicenseStatus(str, Enum):
    VALID = "valid"
    SUSPENDED = "suspended" 
    REVOKED = "revoked"
    EXPIRED = "expired"
    INVALID = "invalid"

class ViolationType(str, Enum):
    DUI = "DUI"
    RECKLESS_DRIVING = "reckless_driving"
    HIT_AND_RUN = "hit_and_run"
    VEHICULAR_HOMICIDE = "vehicular_homicide"
    SPEEDING_15_OVER = "speeding_15_over"
    SPEEDING_10_UNDER = "speeding_10_under"
    IMPROPER_PASSING = "improper_passing"
    FOLLOWING_TOO_CLOSE = "following_too_close"
    IMPROPER_TURN = "improper_turn"
    PARKING_VIOLATION = "parking_violation"

class ClaimType(str, Enum):
    AT_FAULT = "at_fault"
    NOT_AT_FAULT = "not_at_fault"
    COMPREHENSIVE = "comprehensive"

class VehicleCategory(str, Enum):
    SEDAN = "sedan"
    SUV = "suv"
    MINIVAN = "minivan"
    PICKUP = "pickup"
    SPORTS_CAR = "sports_car"
    CONVERTIBLE = "convertible"
    PERFORMANCE = "performance"
    LUXURY_SEDAN = "luxury_sedan"
    LUXURY_SUV = "luxury_suv"
    SUPERCAR = "supercar"
    RACING = "racing"
    MODIFIED = "modified"

class UnderwritingDecision(str, Enum):
    ACCEPT = "accept"
    DENY = "deny"
    ADJUDICATE = "adjudicate"

class Violation(BaseModel):
    violation_type: ViolationType
    violation_date: date
    conviction_date: Optional[date] = None
    description: str = ""

class Claim(BaseModel):
    claim_type: ClaimType
    claim_date: date
    claim_amount: float
    description: str = ""

class Vehicle(BaseModel):
    vin: str
    year: int
    make: str
    model: str
    category: VehicleCategory
    vehicle_type: VehicleCategory

class Driver(BaseModel):
    driver_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    license_number: str
    license_state: str
    license_status: LicenseStatus
    license_issue_date: date
    license_expiration_date: date
    violations: List[Violation] = Field(default_factory=list)
    claims: List[Claim] = Field(default_factory=list)
    
    @property
    def years_licensed_calc(self) -> int:
        today = date.today()
        return today.year - self.license_issue_date.year - ((today.month, today.day) < (self.license_issue_date.month, self.license_issue_date.day))
    
    years_licensed: int = years_licensed_calc

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Applicant(BaseModel):
    applicant_id: str
    primary_driver: Driver
    additional_drivers: List[Driver] = Field(default_factory=list)
    vehicles: List[Vehicle] = Field(default_factory=list)
    credit_score: Optional[int] = None
    prior_insurance_lapse_days: int = 0
    fraud_history: bool = False
    territory: str
    coverage_requested: List[str] = Field(default_factory=list)
    
    @property
    def all_drivers(self) -> List[Driver]:
        return [self.primary_driver] + self.additional_drivers

class UnderwritingResult(BaseModel):
    applicant_id: str
    decision: UnderwritingDecision
    reason: str
    triggered_rules: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


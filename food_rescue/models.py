"""
Data models representing the core entities in the Food Rescue System.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Donation:
    id: Optional[int]
    donor_name: str
    donor_type: str  # Restaurant, Hostel, Wedding/Event, Supermarket
    food_item: str
    food_category: str  # Cooked Meal, Bakery, Raw Produce, Packaged
    quantity_servings: int
    quantity_kg: float
    location_zone: str
    contact_phone: str
    created_at: str
    expires_in_hours: float
    status: str = "Available"  # Available, Matched, Collected, Expired

    @property
    def is_urgent(self) -> bool:
        """Donations expiring in less than 4 hours are marked urgent."""
        return self.expires_in_hours <= 4.0 and self.status == "Available"


@dataclass
class NGORequest:
    id: Optional[int]
    ngo_name: str
    beneficiary_type: str  # Orphanage, Old Age Home, Slum Community, Night Shelter
    required_servings: int
    location_zone: str
    contact_person: str
    contact_phone: str
    created_at: str
    status: str = "Pending"  # Pending, Fulfilled, Partially Fulfilled


@dataclass
class MatchResult:
    donation_id: int
    ngo_id: int
    donor_name: str
    ngo_name: str
    food_item: str
    servings_matched: int
    location_zone: str
    urgency_level: str
    matched_at: str

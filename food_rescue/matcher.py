"""
Smart Matching Engine:
Implements expiration-urgency and zone-proximity algorithms to pair donors with NGOs.
"""

from datetime import datetime
from typing import List, Tuple
from food_rescue.models import Donation, NGORequest, MatchResult


class SmartMatchingEngine:
    @staticmethod
    def calculate_urgency_score(donation: Donation) -> float:
        """
        Higher score means higher priority to rescue.
        Donations expiring within 3 hours get exponential urgency boost.
        """
        if donation.expires_in_hours <= 0:
            return -1.0  # Expired
        if donation.expires_in_hours <= 3.0:
            return 100.0 / donation.expires_in_hours
        return 50.0 / donation.expires_in_hours

    @classmethod
    def match_donations_to_ngos(
        cls, donations: List[Donation], ngo_requests: List[NGORequest]
    ) -> List[MatchResult]:
        """
        Matching Strategy:
        1. Filter out expired food items.
        2. Sort donations by urgency (earliest expiry first).
        3. Prioritize NGOs in the exact same location zone to minimize transit time.
        4. Match based on quantity requirement suitability.
        """
        matches: List[MatchResult] = []
        unmatched_ngos = list(ngo_requests)

        # Sort available donations by expiration urgency (lowest hours remaining first)
        active_donations = [d for d in donations if d.expires_in_hours > 0 and d.status == "Available"]
        active_donations.sort(key=lambda d: d.expires_in_hours)

        for donation in active_donations:
            best_ngo = None
            best_index = -1

            # Pass 1: Same zone match (ideal to prevent food spoilage during travel)
            for idx, ngo in enumerate(unmatched_ngos):
                if ngo.status == "Pending" and ngo.location_zone == donation.location_zone:
                    best_ngo = ngo
                    best_index = idx
                    break

            # Pass 2: If no same-zone NGO, pick any available NGO if time permits (>3 hours expiry)
            if best_ngo is None and donation.expires_in_hours >= 3.0:
                for idx, ngo in enumerate(unmatched_ngos):
                    if ngo.status == "Pending":
                        best_ngo = ngo
                        best_index = idx
                        break

            if best_ngo and best_index >= 0:
                servings_matched = min(donation.quantity_servings, best_ngo.required_servings)
                urgency_tag = "CRITICAL (<3 hrs)" if donation.expires_in_hours <= 3.0 else (
                    "HIGH (<6 hrs)" if donation.expires_in_hours <= 6.0 else "NORMAL"
                )

                match = MatchResult(
                    donation_id=donation.id,
                    ngo_id=best_ngo.id,
                    donor_name=donation.donor_name,
                    ngo_name=best_ngo.ngo_name,
                    food_item=donation.food_item,
                    servings_matched=servings_matched,
                    location_zone=f"{donation.location_zone} -> {best_ngo.location_zone}",
                    urgency_level=urgency_tag,
                    matched_at=datetime.now().strftime("%Y-%m-%d %H:%M")
                )
                matches.append(match)
                unmatched_ngos.pop(best_index)

        return matches

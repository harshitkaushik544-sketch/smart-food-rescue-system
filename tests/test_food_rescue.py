"""
Unit tests for the Food Rescue & Waste Reduction System.
Can be run with: python -m unittest discover tests
"""

import unittest
import os
from food_rescue.models import Donation, NGORequest
from food_rescue.database import DatabaseManager
from food_rescue.matcher import SmartMatchingEngine
from food_rescue.analytics import ImpactAnalytics


class TestFoodRescueSystem(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_food_rescue.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.db = DatabaseManager(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_donation_urgency(self):
        urgent_donation = Donation(
            id=1, donor_name="Test Cafe", donor_type="Cafe", food_item="Sandwiches",
            food_category="Bakery", quantity_servings=20, quantity_kg=7.0,
            location_zone="North", contact_phone="123", created_at="2026-11-05 10:00",
            expires_in_hours=2.5, status="Available"
        )
        non_urgent_donation = Donation(
            id=2, donor_name="Test Store", donor_type="Store", food_item="Rice Bags",
            food_category="Packaged", quantity_servings=50, quantity_kg=25.0,
            location_zone="North", contact_phone="123", created_at="2026-11-05 10:00",
            expires_in_hours=12.0, status="Available"
        )
        self.assertTrue(urgent_donation.is_urgent)
        self.assertFalse(non_urgent_donation.is_urgent)

    def test_smart_matching_same_zone(self):
        donations = [
            Donation(1, "Hotel Grand", "Hotel", "Buffet Leftover", "Cooked", 50, 15.0, "Zone-A", "111", "today", 3.0, "Available"),
            Donation(2, "Hostel Mess", "Hostel", "Curry & Rice", "Cooked", 100, 30.0, "Zone-B", "222", "today", 6.0, "Available"),
        ]
        ngos = [
            NGORequest(1, "Shelter B", "Shelter", 80, "Zone-B", "Contact B", "333", "today", "Pending"),
            NGORequest(2, "Shelter A", "Shelter", 40, "Zone-A", "Contact A", "444", "today", "Pending"),
        ]

        matches = SmartMatchingEngine.match_donations_to_ngos(donations, ngos)
        self.assertEqual(len(matches), 2)
        # Zone-A urgent donation should match Zone-A NGO
        first_match = matches[0]
        self.assertEqual(first_match.donor_name, "Hotel Grand")
        self.assertEqual(first_match.ngo_name, "Shelter A")

    def test_database_persistence_and_analytics(self):
        self.db.seed_sample_data()
        donations = self.db.get_available_donations()
        ngos = self.db.get_pending_ngo_requests()

        self.assertGreater(len(donations), 0)
        self.assertGreater(len(ngos), 0)

        matches = SmartMatchingEngine.match_donations_to_ngos(donations, ngos)
        for m in matches:
            self.db.record_match(m)

        all_matches = self.db.get_all_matches()
        self.assertGreater(len(all_matches), 0)

        summary = ImpactAnalytics.generate_summary(self.test_db)
        self.assertGreater(summary["total_servings_rescued"], 0)
        self.assertGreater(summary["co2_emissions_averted_kg"], 0)


if __name__ == "__main__":
    unittest.main()

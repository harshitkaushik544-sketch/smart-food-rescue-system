"""
SQLite Database management for persisting donations, NGO requests, and matches.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional
from food_rescue.models import Donation, NGORequest, MatchResult


class DatabaseManager:
    def __init__(self, db_path: str = "food_rescue.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Donations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS donations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    donor_name TEXT NOT NULL,
                    donor_type TEXT NOT NULL,
                    food_item TEXT NOT NULL,
                    food_category TEXT NOT NULL,
                    quantity_servings INTEGER NOT NULL,
                    quantity_kg REAL NOT NULL,
                    location_zone TEXT NOT NULL,
                    contact_phone TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_in_hours REAL NOT NULL,
                    status TEXT DEFAULT 'Available'
                )
            """)

            # NGO Requests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ngo_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ngo_name TEXT NOT NULL,
                    beneficiary_type TEXT NOT NULL,
                    required_servings INTEGER NOT NULL,
                    location_zone TEXT NOT NULL,
                    contact_person TEXT NOT NULL,
                    contact_phone TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    status TEXT DEFAULT 'Pending'
                )
            """)

            # Matches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    donation_id INTEGER NOT NULL,
                    ngo_id INTEGER NOT NULL,
                    donor_name TEXT NOT NULL,
                    ngo_name TEXT NOT NULL,
                    food_item TEXT NOT NULL,
                    servings_matched INTEGER NOT NULL,
                    location_zone TEXT NOT NULL,
                    urgency_level TEXT NOT NULL,
                    matched_at TEXT NOT NULL,
                    FOREIGN KEY (donation_id) REFERENCES donations (id),
                    FOREIGN KEY (ngo_id) REFERENCES ngo_requests (id)
                )
            """)
            conn.commit()

    def add_donation(self, donation: Donation) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO donations (
                    donor_name, donor_type, food_item, food_category,
                    quantity_servings, quantity_kg, location_zone,
                    contact_phone, created_at, expires_in_hours, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                donation.donor_name, donation.donor_type, donation.food_item,
                donation.food_category, donation.quantity_servings,
                donation.quantity_kg, donation.location_zone, donation.contact_phone,
                donation.created_at, donation.expires_in_hours, donation.status
            ))
            conn.commit()
            return cursor.lastrowid

    def add_ngo_request(self, request: NGORequest) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ngo_requests (
                    ngo_name, beneficiary_type, required_servings,
                    location_zone, contact_person, contact_phone,
                    created_at, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request.ngo_name, request.beneficiary_type,
                request.required_servings, request.location_zone,
                request.contact_person, request.contact_phone,
                request.created_at, request.status
            ))
            conn.commit()
            return cursor.lastrowid

    def get_available_donations(self) -> List[Donation]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM donations
                WHERE status = 'Available'
                ORDER BY expires_in_hours ASC
            """)
            rows = cursor.fetchall()
            return [
                Donation(
                    id=row["id"],
                    donor_name=row["donor_name"],
                    donor_type=row["donor_type"],
                    food_item=row["food_item"],
                    food_category=row["food_category"],
                    quantity_servings=row["quantity_servings"],
                    quantity_kg=row["quantity_kg"],
                    location_zone=row["location_zone"],
                    contact_phone=row["contact_phone"],
                    created_at=row["created_at"],
                    expires_in_hours=row["expires_in_hours"],
                    status=row["status"]
                ) for row in rows
            ]

    def get_pending_ngo_requests(self) -> List[NGORequest]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM ngo_requests
                WHERE status = 'Pending'
                ORDER BY id ASC
            """)
            rows = cursor.fetchall()
            return [
                NGORequest(
                    id=row["id"],
                    ngo_name=row["ngo_name"],
                    beneficiary_type=row["beneficiary_type"],
                    required_servings=row["required_servings"],
                    location_zone=row["location_zone"],
                    contact_person=row["contact_person"],
                    contact_phone=row["contact_phone"],
                    created_at=row["created_at"],
                    status=row["status"]
                ) for row in rows
            ]

    def record_match(self, match: MatchResult):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO matches (
                    donation_id, ngo_id, donor_name, ngo_name,
                    food_item, servings_matched, location_zone,
                    urgency_level, matched_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                match.donation_id, match.ngo_id, match.donor_name,
                match.ngo_name, match.food_item, match.servings_matched,
                match.location_zone, match.urgency_level, match.matched_at
            ))
            cursor.execute("UPDATE donations SET status = 'Matched' WHERE id = ?", (match.donation_id,))
            cursor.execute("UPDATE ngo_requests SET status = 'Fulfilled' WHERE id = ?", (match.ngo_id,))
            conn.commit()

    def get_all_matches(self) -> List[dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matches ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]

    def seed_sample_data(self):
        """Seeds realistic sample data for demo and evaluation."""
        sample_donations = [
            Donation(None, "Taj Gateway Hotel", "Hotel/Restaurant", "Assorted Biryani & Dal Makhani", "Cooked Meal", 80, 28.0, "North Zone", "+91 98765 43210", datetime.now().strftime("%Y-%m-%d %H:%M"), 3.5, "Available"),
            Donation(None, "Campus Central Mess", "Hostel/Cafeteria", "Steamed Rice, Roti & Mix Sabzi", "Cooked Meal", 120, 42.0, "East Zone", "+91 98220 11223", datetime.now().strftime("%Y-%m-%d %H:%M"), 5.0, "Available"),
            Donation(None, "Daily Bread Bakery", "Bakery", "Fresh Whole Wheat Breads & Buns", "Bakery", 45, 12.5, "North Zone", "+91 99112 33445", datetime.now().strftime("%Y-%m-%d %H:%M"), 18.0, "Available"),
            Donation(None, "Metro Convention Hall", "Wedding/Event", "Paneer Gravy & Jeera Rice", "Cooked Meal", 150, 55.0, "South Zone", "+91 97654 32198", datetime.now().strftime("%Y-%m-%d %H:%M"), 2.5, "Available"),
            Donation(None, "GreenFresh Mart", "Supermarket", "Seasonal Fruits & Veggie Crates", "Raw Produce", 60, 30.0, "West Zone", "+91 98450 76543", datetime.now().strftime("%Y-%m-%d %H:%M"), 24.0, "Available"),
        ]

        sample_ngos = [
            NGORequest(None, "Hope Orphanage & Care", "Orphanage", 75, "North Zone", "Sister Anita", "+91 94230 45678", datetime.now().strftime("%Y-%m-%d %H:%M"), "Pending"),
            NGORequest(None, "Aashray Night Shelter", "Night Shelter", 110, "East Zone", "Ramesh Verma", "+91 98234 56789", datetime.now().strftime("%Y-%m-%d %H:%M"), "Pending"),
            NGORequest(None, "Vridhashram Elders Home", "Old Age Home", 50, "North Zone", "Dr. Meera Joshi", "+91 97651 23456", datetime.now().strftime("%Y-%m-%d %H:%M"), "Pending"),
            NGORequest(None, "Robin Food Warriors", "Slum Community", 140, "South Zone", "Kabir Khan", "+91 98901 23456", datetime.now().strftime("%Y-%m-%d %H:%M"), "Pending"),
        ]

        for donation in sample_donations:
            self.add_donation(donation)
        for ngo in sample_ngos:
            self.add_ngo_request(ngo)

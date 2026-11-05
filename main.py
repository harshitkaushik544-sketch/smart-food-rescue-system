#!/usr/bin/env python3
"""
Main Interactive CLI for Smart Food Rescue & Waste Reduction Network.
Designed for college viva demonstrations, practical testing, and real-world simulation.
"""

import sys
from datetime import datetime
from food_rescue.models import Donation, NGORequest
from food_rescue.database import DatabaseManager
from food_rescue.matcher import SmartMatchingEngine
from food_rescue.analytics import ImpactAnalytics

# Try importing tabulate for pretty tables, else fallback to built-in formatting
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


def print_table(headers, rows):
    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
    else:
        # Fallback formatting without external dependencies
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))
        
        header_str = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
        separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
        print(header_str)
        print(separator)
        for row in rows:
            print(" | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row)))


def display_header():
    print("\n" + "=" * 70)
    print("  🍲 SMART FOOD RESCUE & SURPLUS REDISTRIBUTION SYSTEM 🍲")
    print("       A Real-Life Python Project for Zero Hunger (SDG 2)")
    print("=" * 70)


def display_menu():
    print("""
[1] 📦 Register Surplus Food Donation (Donors / Caterers / Mess)
[2] 🏢 Register Food Requirement (NGO / Shelter / Orphanage)
[3] 📋 View Available Food Donations (Sorted by Urgency)
[4] 🤝 View Pending NGO Requests
[5] ⚡ Run Smart Matching Algorithm (Auto-Distribute Urgently)
[6] 📜 View Confirmed Matches & Distribution History
[7] 📊 View Impact Analytics (Meals Rescued, CO2 & Water Saved)
[8] 🧪 Load Realistic Sample / Seed Data (One-Click Demo)
[0] 🚪 Exit System
""")


def handle_add_donation(db: DatabaseManager):
    print("\n--- [Register Food Donation] ---")
    try:
        donor_name = input("Donor / Organization Name: ").strip()
        print("Donor Type: [1] Restaurant  [2] College Mess/Hostel  [3] Event/Wedding  [4] Supermarket")
        dtype_choice = input("Select type (1-4): ").strip()
        dtype_map = {"1": "Restaurant", "2": "Hostel/Mess", "3": "Event/Wedding", "4": "Supermarket"}
        donor_type = dtype_map.get(dtype_choice, "Other")

        food_item = input("Food Description (e.g. Rice & Dal, Assorted Curry): ").strip()
        servings = int(input("Approximate Servings (persons): ").strip())
        kg = float(input("Estimated Weight in Kilograms (kg): ").strip())
        
        print("Zones: [1] North Zone  [2] South Zone  [3] East Zone  [4] West Zone  [5] Central Zone")
        zone_choice = input("Select Zone (1-5): ").strip()
        zone_map = {"1": "North Zone", "2": "South Zone", "3": "East Zone", "4": "West Zone", "5": "Central Zone"}
        zone = zone_map.get(zone_choice, "Central Zone")

        phone = input("Donor Contact Phone: ").strip()
        expiry_hours = float(input("Shelf-life remaining before spoilage (Hours, e.g. 3.5): ").strip())

        donation = Donation(
            id=None,
            donor_name=donor_name,
            donor_type=donor_type,
            food_item=food_item,
            food_category="Cooked Meal",
            quantity_servings=servings,
            quantity_kg=kg,
            location_zone=zone,
            contact_phone=phone,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
            expires_in_hours=expiry_hours
        )

        d_id = db.add_donation(donation)
        print(f"\n✅ Success: Food Donation logged with ID #{d_id}!")
        if donation.is_urgent:
            print("⚠️ ALERT: High Urgency! This donation expires in under 4 hours.")
    except Exception as e:
        print(f"\n❌ Error adding donation: {e}")


def handle_add_ngo(db: DatabaseManager):
    print("\n--- [Register NGO Food Request] ---")
    try:
        ngo_name = input("NGO / Shelter Name: ").strip()
        print("Beneficiary Type: [1] Orphanage  [2] Night Shelter  [3] Old Age Home  [4] Slum Community")
        b_choice = input("Select Type (1-4): ").strip()
        b_map = {"1": "Orphanage", "2": "Night Shelter", "3": "Old Age Home", "4": "Slum Community"}
        beneficiary_type = b_map.get(b_choice, "Community")

        needed_servings = int(input("Number of Meals / Servings Needed: ").strip())
        
        print("Zones: [1] North Zone  [2] South Zone  [3] East Zone  [4] West Zone  [5] Central Zone")
        zone_choice = input("Select Zone (1-5): ").strip()
        zone_map = {"1": "North Zone", "2": "South Zone", "3": "East Zone", "4": "West Zone", "5": "Central Zone"}
        zone = zone_map.get(zone_choice, "Central Zone")

        contact_person = input("Coordinator Name: ").strip()
        phone = input("Emergency Contact Phone: ").strip()

        request = NGORequest(
            id=None,
            ngo_name=ngo_name,
            beneficiary_type=beneficiary_type,
            required_servings=needed_servings,
            location_zone=zone,
            contact_person=contact_person,
            contact_phone=phone,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        r_id = db.add_ngo_request(request)
        print(f"\n✅ Success: NGO Request registered with ID #{r_id}!")
    except Exception as e:
        print(f"\n❌ Error adding NGO request: {e}")


def handle_view_donations(db: DatabaseManager):
    donations = db.get_available_donations()
    if not donations:
        print("\nℹ️ No available food donations right now. Add one or seed demo data!")
        return

    headers = ["ID", "Donor", "Item", "Servings", "Weight (kg)", "Zone", "Expires In", "Urgency"]
    rows = []
    for d in donations:
        urgency = "🔥 CRITICAL" if d.expires_in_hours <= 3.0 else ("⚠️ URGENT" if d.expires_in_hours <= 5.0 else "NORMAL")
        rows.append([
            d.id, d.donor_name, d.food_item, d.quantity_servings,
            f"{d.quantity_kg} kg", d.location_zone, f"{d.expires_in_hours} hrs", urgency
        ])

    print("\n--- AVAILABLE SURPLUS FOOD INVENTORY ---")
    print_table(headers, rows)


def handle_view_ngos(db: DatabaseManager):
    requests = db.get_pending_ngo_requests()
    if not requests:
        print("\nℹ️ No pending requests from NGOs at this time.")
        return

    headers = ["ID", "NGO / Organization", "Beneficiaries", "Needed Servings", "Zone", "Contact"]
    rows = [
        [r.id, r.ngo_name, r.beneficiary_type, r.required_servings, r.location_zone, f"{r.contact_person} ({r.contact_phone})"]
        for r in requests
    ]
    print("\n--- PENDING NGO FOOD REQUESTS ---")
    print_table(headers, rows)


def handle_run_matching(db: DatabaseManager):
    donations = db.get_available_donations()
    requests = db.get_pending_ngo_requests()

    if not donations:
        print("\n❌ Cannot run match: No available donations in system.")
        return
    if not requests:
        print("\n❌ Cannot run match: No pending NGO requests in system.")
        return

    print(f"\nRunning AI-inspired urgency & proximity matcher...")
    matches = SmartMatchingEngine.match_donations_to_ngos(donations, requests)

    if not matches:
        print("\n⚠️ No optimal matches could be formed with current constraints.")
        return

    headers = ["Match", "Donor", "Matched NGO", "Food Item", "Servings", "Route / Zone", "Urgency Level"]
    rows = [
        [f"#{idx+1}", m.donor_name, m.ngo_name, m.food_item, m.servings_matched, m.location_zone, m.urgency_level]
        for idx, m in enumerate(matches)
    ]
    print("\n🎉 OPTIMAL MATCHES COMPUTED:")
    print_table(headers, rows)

    confirm = input("\nConfirm and commit these matches to database? (y/n): ").strip().lower()
    if confirm == "y":
        for m in matches:
            db.record_match(m)
        print("✅ Matches successfully executed! Donors & NGOs notified.")
    else:
        print("Matching canceled.")


def handle_view_matches(db: DatabaseManager):
    matches = db.get_all_matches()
    if not matches:
        print("\nℹ️ No matches have been executed yet.")
        return

    headers = ["ID", "Donor", "Recipient NGO", "Food Item", "Servings", "Urgency", "Timestamp"]
    rows = [
        [m["id"], m["donor_name"], m["ngo_name"], m["food_item"], m["servings_matched"], m["urgency_level"], m["matched_at"]]
        for m in matches
    ]
    print("\n--- DISTRIBUTION & RESCUE HISTORY ---")
    print_table(headers, rows)


def handle_analytics(db: DatabaseManager):
    summary = ImpactAnalytics.generate_summary(db.db_path)
    print("\n" + "=" * 55)
    print("      🌱 REAL-WORLD IMPACT & SUSTAINABILITY REPORT 🌱")
    print("=" * 55)
    print(f" • Total Donations Recorded:   {summary['total_donations_logged']}")
    print(f" • Successful Rescues/Matches: {summary['total_matches_completed']}")
    print(f" • Total Meals Distributed:    {summary['total_servings_rescued']} meals")
    print(f" • Food Waste Diverted:        {summary['food_waste_prevented_kg']} kg")
    print(f" • CO2 Emissions Avoided:      {summary['co2_emissions_averted_kg']} kg CO2e")
    print(f" • Embedded Water Conserved:   {summary['water_saved_liters']} Liters")
    print("-" * 55)
    print(" Beneficiary Distribution Breakdown:")
    for b_type, count in summary["beneficiary_distribution"].items():
        print(f"   - {b_type}: {count} deliveries")
    print("=" * 55)


def main():
    db = DatabaseManager()
    display_header()

    while True:
        display_menu()
        choice = input("Enter your option (0-8): ").strip()

        if choice == "1":
            handle_add_donation(db)
        elif choice == "2":
            handle_add_ngo(db)
        elif choice == "3":
            handle_view_donations(db)
        elif choice == "4":
            handle_view_ngos(db)
        elif choice == "5":
            handle_run_matching(db)
        elif choice == "6":
            handle_view_matches(db)
        elif choice == "7":
            handle_analytics(db)
        elif choice == "8":
            db.seed_sample_data()
            print("\n✅ Realistic sample dataset loaded into database successfully!")
        elif choice == "0":
            print("\nThank you for supporting Zero Hunger and Food Waste Reduction. Goodbye!\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice! Please select 0 to 8.")


if __name__ == "__main__":
    main()

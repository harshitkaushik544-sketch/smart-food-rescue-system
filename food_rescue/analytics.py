"""
Impact & Environmental Analytics:
Calculates meals rescued, waste prevented, CO2 emissions averted, and water saved.
"""

from typing import List, Dict, Any
import sqlite3


class ImpactAnalytics:
    KG_PER_SERVING = 0.35  # Average meal serving is ~350g
    CO2_KG_PER_FOOD_KG = 2.5  # Landfill decay & lifecycle emission factor
    WATER_LITERS_PER_FOOD_KG = 1000.0  # Embedded agricultural water footprint

    @classmethod
    def generate_summary(cls, db_path: str = "food_rescue.db") -> Dict[str, Any]:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Total donations
            cursor.execute("SELECT COUNT(*), COALESCE(SUM(quantity_servings), 0), COALESCE(SUM(quantity_kg), 0) FROM donations")
            total_donations, total_servings_donated, total_kg_donated = cursor.fetchone()

            # Total matches successfully executed
            cursor.execute("SELECT COUNT(*), COALESCE(SUM(servings_matched), 0) FROM matches")
            total_matches, total_servings_matched = cursor.fetchone()

            # Fulfilled weight approximation
            kg_saved = total_servings_matched * cls.KG_PER_SERVING
            co2_averted_kg = kg_saved * cls.CO2_KG_PER_FOOD_KG
            water_saved_liters = kg_saved * cls.WATER_LITERS_PER_FOOD_KG

            # Beneficiary category breakdown
            cursor.execute("""
                SELECT n.beneficiary_type, COUNT(m.id)
                FROM matches m
                JOIN ngo_requests n ON m.ngo_id = n.id
                GROUP BY n.beneficiary_type
            """)
            beneficiary_distribution = dict(cursor.fetchall())

            return {
                "total_donations_logged": total_donations,
                "total_matches_completed": total_matches,
                "total_servings_rescued": total_servings_matched,
                "food_waste_prevented_kg": round(kg_saved, 2),
                "co2_emissions_averted_kg": round(co2_averted_kg, 2),
                "water_saved_liters": round(water_saved_liters, 2),
                "beneficiary_distribution": beneficiary_distribution,
            }

# 🍲 Smart Food Rescue & Surplus Redistribution Network
> **A Real-Life Python Project Addressing Community Food Waste and Hunger Alleviation**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![UN SDG Alignment](https://img.shields.io/badge/UN%20SDGs-SDG%202%20%7C%20SDG%2012-orange.svg)](https://sdgs.un.org/goals)

---

## 📌 Problem Statement & Real-Life Relevance

In urban areas, college cafeterias, convention centers, and wedding banquet halls, huge quantities of prepared, edible food are thrown away every single day. Simultaneously, orphanages, old age homes, night shelters, and low-income communities nearby suffer from acute food insecurity.

### The Real-World Bottleneck:
1. **Time Sensitivity (Perishability):** Cooked food spoils rapidly (within 4–6 hours). Traditional charity processes are too slow to coordinate pickups before food spoils.
2. **Logistical Disconnect:** Donors lack direct communication channels with verified nearby charities.
3. **Lack of Metrics:** Organizations have no transparent data on meals saved, greenhouse gas emissions prevented, or waste diverted.

**Smart Food Rescue Network** is a software solution designed to bridge this gap through urgency-weighted matching, zone-based routing, and real-time environmental impact calculations.

---

## 🎯 UN Sustainable Development Goals (SDG) Alignment
- **SDG 2: Zero Hunger** — Ensuring surplus nutritious meals reach vulnerable populations.
- **SDG 12: Responsible Consumption & Production** — Diverting food waste from city landfills.
- **SDG 13: Climate Action** — Reducing methane and greenhouse emissions caused by decomposing organic waste in landfills.

---

## ⚙️ Key Features

- **Donor Registration Portal:** Cafeterias, hotels, and event organizers can quickly register surplus food (servings, weight in kg, expiration window in hours, contact details, and location zone).
- **Charity / NGO Needs Registry:** Orphanages, shelters, and community kitchens register current meal shortfalls and beneficiary demographics.
- **Smart Urgency-Priority Matching Engine:**
  - Evaluates remaining shelf life using an exponential urgency function.
  - Prioritizes same-zone donor-recipient pairing to minimize transit latency.
  - Automatically flags items with critical urgency (< 3 hours shelf-life).
- **Impact & Sustainability Analytics:**
  - Computes total servings distributed.
  - Calculates food waste diverted (in kg).
  - Estimates carbon emissions prevented ($1\text{ kg food waste} \approx 2.5\text{ kg }\text{CO}_2\text{e}$).
  - Computes embedded water footprint saved ($1000\text{ Liters / kg}$).
- **Data Persistence:** Built on relational SQLite (`food_rescue.db`) with zero external database server requirements.
- **Built-in Demo Generator:** Single-click sample data seeding for effortless viva demonstrations.

---

## 📂 Project Architecture

```
smart-food-rescue-system/
│
├── main.py                  # Interactive CLI Dashboard & Entry Point
├── requirements.txt         # Project dependencies (tabulate)
├── .gitignore               # Ignored build and database artifacts
├── README.md                # Project documentation & presentation guide
│
├── food_rescue/             # Core application package
│   ├── __init__.py          # Package initialization & version metadata
│   ├── models.py            # OOP dataclasses: Donation, NGORequest, MatchResult
│   ├── database.py          # SQLite database connection & CRUD methods
│   ├── matcher.py           # Urgency & proximity matching algorithm
│   └── analytics.py         # Environmental impact & sustainability calculations
│
└── tests/                   # Automated unit test suite
    └── test_food_rescue.py  # Unittest assertions for core logic & database
```

---

## 🚀 Installation & How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/harshitkaushik544-sketch/smart-food-rescue-system.git
cd smart-food-rescue-system
```

### 2. (Optional) Install Dependencies
The project runs seamlessly on standard Python library. For enhanced table formatting, install `tabulate`:
```bash
pip install -r requirements.txt
```

### 3. Run the Interactive Application
```bash
python main.py
```

### 4. Run Automated Unit Tests
```bash
python -m unittest discover tests
```

---

## 🧪 Demonstration Walkthrough (For Evaluation / Viva)

1. Launch `python main.py`.
2. Choose **Option `[8]`** to populate the system with realistic community sample data (Taj Gateway Hotel, Campus Mess, Hope Orphanage, Aashray Shelter, etc.).
3. Choose **Option `[3]`** to inspect active donations and note the urgency indicators (`🔥 CRITICAL` for items expiring under 3 hours).
4. Choose **Option `[5]`** to run the **Smart Matching Algorithm**. The engine pairs donors with closest matching NGOs and asks for confirmation.
5. Choose **Option `[7]`** to view the **Impact & Sustainability Analytics**, displaying carbon offsets and water saved in real-time.

---

## 🎓 College Viva & Interview Q&A Guide

**Q1: What real-world problem does this project address?**
> *Answer:* It tackles urban food wastage and hunger by providing a fast, automated coordination mechanism that matches perishable surplus food from commercial kitchens to verified charities before the food spoils.

**Q2: How does the matching algorithm work?**
> *Answer:* The algorithm ranks donations by expiry urgency using an urgency scoring function. It performs a two-pass match: first pairing same-zone entities to minimize transit time, and then matching based on required capacity and food volume.

**Q3: How are the environmental metrics calculated?**
> *Answer:* According to global environmental studies, every kilogram of food diverted from municipal landfills prevents approximately $2.5\text{ kg}$ of greenhouse gas emissions ($\text{CO}_2\text{ equivalent}$) and conserves approximately $1,000\text{ Liters}$ of agricultural water footprint embedded in the food supply chain.

**Q4: Which Python design patterns and paradigms are utilized?**
> *Answer:* The project follows Object-Oriented Programming (OOP) with Python `dataclasses`, the Repository pattern for SQLite data access separation, modular architecture, and automated test-driven validation via `unittest`.

---

## 🔮 Future Scope
- Integration with OpenStreetMap / Google Maps API for automated route optimization.
- SMS / WhatsApp API notifications via Twilio for emergency volunteer alerts.
- IoT integration with smart temperature sensors to verify cold-chain food safety before delivery.

---

## 👨‍💻 Author
**HARSHIT SURENDER KAUSHIK**

import csv
import random
from datetime import date, timedelta

random.seed(42)

def generate_logs(start_date, start_weight, periods):
    """
    periods: list of (weeks, slope_kg_per_week)
    Returns list of (date, weight) tuples, one entry per week
    """
    logs = []
    current_weight = start_weight
    current_date = start_date

    for weeks, slope in periods:
        for _ in range(weeks):
            month = current_date.month
            # summer holiday spike (July) and christmas spike (December)
            if month == 7:
                seasonal = random.uniform(0.8, 1.8)
            elif month == 12:
                seasonal = random.uniform(1.0, 2.2)
            else:
                seasonal = 0.0
            # occasional spike up (water retention, heavy meal etc)
            if random.random() < 0.15:
                noise = random.uniform(0.5, 1.4)
            else:
                noise = random.uniform(-0.6, 0.5)
            logs.append((current_date.isoformat(), round(current_weight + noise + seasonal, 1)))
            current_weight += slope
            current_date += timedelta(days=7)

    return logs


# --- User A: Wegovy, 12 months, reaches target ---
# Doses: 0.25mg (6wk), 0.5mg (10wk), 1.0mg (16wk), 1.7mg (20wk)
user_a_periods = [
    (6,  -0.85),   # 0.25mg: strong initial response
    (10, -0.50),   # 0.5mg: settling
    (16, -0.45),   # 1.0mg: steady
    (12, -0.38),   # 1.7mg: consistent
    (8,  -0.30),   # 2.4mg: final phase, reaches target
]
user_a_logs = generate_logs(date(2025, 1, 8), 92.0, user_a_periods)

with open("user-a-wegovy/weight_log.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "weight_kg"])
    w.writerows(user_a_logs)

with open("user-a-wegovy/medication_doses.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["medication_name", "dose", "unit", "date_changed"])
    w.writerow(["Wegovy", 0.25, "mg", "2025-01-08"])
    w.writerow(["Wegovy", 0.5,  "mg", "2025-02-19"])
    w.writerow(["Wegovy", 1.0,  "mg", "2025-04-29"])
    w.writerow(["Wegovy", 1.7,  "mg", "2025-08-26"])
    w.writerow(["Wegovy", 2.4,  "mg", "2025-11-18"])


# --- User B: Wegovy plateau → Mounjaro ---
# Wegovy 0.25mg (8wk): near flat
# Wegovy 0.5mg (8wk): near flat
# Mounjaro 2.5mg (4wk), 5mg (4wk), 7.5mg (4wk), 10mg (4wk), 12.5mg (24wk)
user_b_periods = [
    (8,  -0.12),   # Wegovy 0.25mg: minimal response
    (8,  -0.10),   # Wegovy 0.5mg: still barely moving
    (4,  -0.70),   # Mounjaro 2.5mg: noticeable response
    (4,  -0.95),   # Mounjaro 5mg: strong response
    (4,  -1.05),   # Mounjaro 7.5mg: peak response
    (4,  -0.95),   # Mounjaro 10mg: sustained
    (24, -0.75),   # Mounjaro 12.5mg: steady, approaches target
]
user_b_logs = generate_logs(date(2025, 3, 4), 127.0, user_b_periods)

with open("user-b-mounjaro-switch/weight_log.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "weight_kg"])
    w.writerows(user_b_logs)

with open("user-b-mounjaro-switch/medication_doses.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["medication_name", "dose", "unit", "date_changed"])
    w.writerow(["Wegovy",   0.25, "mg", "2025-03-04"])
    w.writerow(["Wegovy",   0.5,  "mg", "2025-04-29"])
    w.writerow(["Mounjaro", 2.5,  "mg", "2025-06-24"])
    w.writerow(["Mounjaro", 5.0,  "mg", "2025-07-22"])
    w.writerow(["Mounjaro", 7.5,  "mg", "2025-08-19"])
    w.writerow(["Mounjaro", 10.0, "mg", "2025-09-16"])
    w.writerow(["Mounjaro", 12.5, "mg", "2025-10-14"])

print("Done.")
print(f"User A: {len(user_a_logs)} entries, final weight: {user_a_logs[-1][1]}kg")
print(f"User B: {len(user_b_logs)} entries, final weight: {user_b_logs[-1][1]}kg")

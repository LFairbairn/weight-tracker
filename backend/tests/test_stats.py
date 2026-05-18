from datetime import date, timedelta


def create_test_user(client):
    client.post("/users", json={
        "name": "Test User",
        "height": 170.0,
        "target_weight": 70.0,
        "weight_unit": "kg",
        "measurement_unit": "cm",
    })


def seed_linear_logs(client, start_date, start_weight, slope_per_week, weeks):
    """Seed perfectly linear weekly weight data so regression results are predictable."""
    for i in range(weeks):
        d = start_date + timedelta(weeks=i)
        weight = round(start_weight + slope_per_week * i, 2)
        client.post("/weight-logs", json={"date": d.isoformat(), "weight_kg": weight})


def add_dose(client, med_id, dose, date_changed):
    client.post(f"/medications/{med_id}/doses", json={
        "dose": dose, "unit": "mg", "date_changed": date_changed,
    })


def test_stats_no_user(client):
    response = client.get("/stats")
    assert response.status_code == 404


def test_stats_basic_regression(client):
    create_test_user(client)

    # 4 weekly logs at exactly -0.5 kg/week — slope and R² are perfectly predictable
    seed_linear_logs(client, date(2025, 1, 1), 80.0, -0.5, 4)

    med_id = client.post("/medications", json={"name": "Wegovy", "start_date": "2025-01-01"}).json()["id"]
    add_dose(client, med_id, 0.25, "2025-01-01")

    response = client.get("/stats")
    assert response.status_code == 200

    period = response.json()["dose_periods"][0]
    assert period["dose"] == 0.25
    assert period["entries"] == 4
    assert period["slope_kg_per_week"] == -0.5
    assert period["r_squared"] == 1.0


def test_stats_overall_trend(client):
    create_test_user(client)
    seed_linear_logs(client, date(2025, 1, 1), 80.0, -0.5, 4)

    med_id = client.post("/medications", json={"name": "Wegovy", "start_date": "2025-01-01"}).json()["id"]
    add_dose(client, med_id, 0.25, "2025-01-01")

    overall = client.get("/stats").json()["overall"]
    assert overall["slope_kg_per_week"] == -0.5
    assert overall["r_squared"] == 1.0


def test_stats_multiple_dose_periods(client):
    create_test_user(client)

    # 8 weekly logs — first 4 in dose period 1, last 4 in dose period 2
    # Dose 2 starts Jan 29 (week 4), so period 1 ends Jan 28
    seed_linear_logs(client, date(2025, 1, 1), 80.0, -0.5, 8)

    med_id = client.post("/medications", json={"name": "Wegovy", "start_date": "2025-01-01"}).json()["id"]
    add_dose(client, med_id, 0.25, "2025-01-01")
    add_dose(client, med_id, 0.5,  "2025-01-29")

    response = client.get("/stats")
    assert response.status_code == 200

    periods = response.json()["dose_periods"]
    assert len(periods) == 2
    assert periods[0]["dose"] == 0.25
    assert periods[0]["entries"] == 4
    assert periods[1]["dose"] == 0.5
    assert periods[1]["entries"] == 4


def test_stats_period_with_insufficient_data(client):
    """A period with fewer than 2 logs should return null for slope and r_squared."""
    create_test_user(client)

    # Three weekly logs starting Jan 1
    client.post("/weight-logs", json={"date": "2025-01-01", "weight_kg": 80.0})
    client.post("/weight-logs", json={"date": "2025-01-08", "weight_kg": 79.5})
    client.post("/weight-logs", json={"date": "2025-01-15", "weight_kg": 79.0})

    med_id = client.post("/medications", json={"name": "Wegovy", "start_date": "2025-01-01"}).json()["id"]
    # Period 1: Jan 1–7 — only the Jan 1 log falls in this range (1 entry, not enough)
    add_dose(client, med_id, 0.25, "2025-01-01")
    # Period 2: Jan 8 onwards — Jan 8 and Jan 15 logs (2 entries, enough)
    add_dose(client, med_id, 0.5,  "2025-01-08")

    periods = client.get("/stats").json()["dose_periods"]
    assert periods[0]["slope_kg_per_week"] is None
    assert periods[0]["r_squared"] is None
    assert periods[1]["slope_kg_per_week"] is not None

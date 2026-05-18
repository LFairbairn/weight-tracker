def create_test_user(client):
    client.post("/users", json={
        "name": "Test User",
        "height": 170.0,
        "target_weight": 70.0,
        "weight_unit": "kg",
        "measurement_unit": "cm",
    })


def create_test_medication(client):
    return client.post("/medications", json={"name": "Wegovy", "start_date": "2025-01-08"})


# --- Medications ---

def test_create_medication(client):
    create_test_user(client)
    response = create_test_medication(client)
    assert response.status_code == 201
    assert response.json()["name"] == "Wegovy"


def test_list_medications(client):
    create_test_user(client)
    create_test_medication(client)
    client.post("/medications", json={"name": "Mounjaro", "start_date": "2025-06-24"})

    response = client.get("/medications")
    assert response.status_code == 200
    names = [m["name"] for m in response.json()]
    assert "Wegovy" in names
    assert "Mounjaro" in names


def test_get_medication(client):
    create_test_user(client)
    med_id = create_test_medication(client).json()["id"]

    response = client.get(f"/medications/{med_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Wegovy"


def test_get_medication_not_found(client):
    create_test_user(client)
    response = client.get("/medications/999")
    assert response.status_code == 404


def test_update_medication(client):
    create_test_user(client)
    med_id = create_test_medication(client).json()["id"]

    response = client.patch(f"/medications/{med_id}", json={"name": "Wegovy (updated)"})
    assert response.status_code == 200
    assert response.json()["name"] == "Wegovy (updated)"


# --- Doses (nested under a medication) ---

def test_create_dose(client):
    create_test_user(client)
    med_id = create_test_medication(client).json()["id"]

    response = client.post(f"/medications/{med_id}/doses", json={
        "dose": 0.25,
        "unit": "mg",
        "date_changed": "2025-01-08",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["dose"] == 0.25
    assert data["unit"] == "mg"


def test_list_doses_ordered_by_date(client):
    create_test_user(client)
    med_id = create_test_medication(client).json()["id"]

    client.post(f"/medications/{med_id}/doses", json={"dose": 0.5, "unit": "mg", "date_changed": "2025-03-01"})
    client.post(f"/medications/{med_id}/doses", json={"dose": 0.25, "unit": "mg", "date_changed": "2025-01-01"})

    response = client.get(f"/medications/{med_id}/doses")
    assert response.status_code == 200
    doses = response.json()
    assert len(doses) == 2
    assert doses[0]["date_changed"] == "2025-01-01"
    assert doses[1]["date_changed"] == "2025-03-01"


def test_list_doses_medication_not_found(client):
    create_test_user(client)
    response = client.get("/medications/999/doses")
    assert response.status_code == 404


def test_update_dose(client):
    create_test_user(client)
    med_id = create_test_medication(client).json()["id"]
    dose_id = client.post(f"/medications/{med_id}/doses", json={
        "dose": 0.25, "unit": "mg", "date_changed": "2025-01-08",
    }).json()["id"]

    response = client.patch(f"/medications/{med_id}/doses/{dose_id}", json={"dose": 0.5})
    assert response.status_code == 200
    assert response.json()["dose"] == 0.5


def test_delete_dose(client):
    create_test_user(client)
    med_id = create_test_medication(client).json()["id"]
    dose_id = client.post(f"/medications/{med_id}/doses", json={
        "dose": 0.25, "unit": "mg", "date_changed": "2025-01-08",
    }).json()["id"]

    response = client.delete(f"/medications/{med_id}/doses/{dose_id}")
    assert response.status_code == 204

    doses = client.get(f"/medications/{med_id}/doses").json()
    assert len(doses) == 0

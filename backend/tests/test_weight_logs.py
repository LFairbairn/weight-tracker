def create_test_user(client):
    """Helper: every weight log needs a user (foreign key)."""
    client.post("/users", json={
        "name": "Test User",
        "height": 165.0,
        "target_weight": 65.0,
        "weight_unit": "kg",
        "measurement_unit": "cm",
    })


def test_create_weight_log(client):
    create_test_user(client)
    response = client.post("/weight-logs", json={
        "date": "2026-01-01",
        "weight_kg": 80.0,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["weight_kg"] == 80.0
    assert data["date"] == "2026-01-01"
    assert data["user_id"] == 1


def test_list_weight_logs(client):
    create_test_user(client)
    client.post("/weight-logs", json={"date": "2026-01-01", "weight_kg": 80.0})
    client.post("/weight-logs", json={"date": "2026-01-02", "weight_kg": 79.5})

    response = client.get("/weight-logs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Should come back in date order
    assert data[0]["date"] == "2026-01-01"
    assert data[1]["date"] == "2026-01-02"


def test_get_single_weight_log(client):
    create_test_user(client)
    client.post("/weight-logs", json={"date": "2026-01-01", "weight_kg": 80.0})

    response = client.get("/weight-logs/1")
    assert response.status_code == 200
    assert response.json()["weight_kg"] == 80.0


def test_get_weight_log_not_found(client):
    create_test_user(client)
    response = client.get("/weight-logs/999")
    assert response.status_code == 404


def test_update_weight_log(client):
    create_test_user(client)
    client.post("/weight-logs", json={"date": "2026-01-01", "weight_kg": 80.0})

    response = client.patch("/weight-logs/1", json={"weight_kg": 79.0})
    assert response.status_code == 200
    assert response.json()["weight_kg"] == 79.0


def test_delete_weight_log(client):
    create_test_user(client)
    client.post("/weight-logs", json={"date": "2026-01-01", "weight_kg": 80.0})

    response = client.delete("/weight-logs/1")
    assert response.status_code == 204

    response = client.get("/weight-logs/1")
    assert response.status_code == 404

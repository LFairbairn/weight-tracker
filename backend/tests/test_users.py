def create_test_user(client):
    return client.post("/users", json={
        "name": "Test User",
        "height": 170.0,
        "target_weight": 70.0,
        "weight_unit": "kg",
        "measurement_unit": "cm",
    })


def test_get_user(client):
    create_test_user(client)
    response = client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["height"] == 170.0
    assert data["target_weight"] == 70.0


def test_get_user_not_found(client):
    response = client.get("/users/me")
    assert response.status_code == 404


def test_update_user(client):
    create_test_user(client)
    response = client.patch("/users/me", json={"target_weight": 65.0})
    assert response.status_code == 200
    assert response.json()["target_weight"] == 65.0


def test_update_user_partial(client):
    create_test_user(client)
    response = client.patch("/users/me", json={"height": 175.0})
    assert response.status_code == 200
    data = response.json()
    assert data["height"] == 175.0
    assert data["name"] == "Test User"  # unchanged fields stay the same


def test_create_duplicate_user(client):
    create_test_user(client)
    response = create_test_user(client)
    assert response.status_code == 400

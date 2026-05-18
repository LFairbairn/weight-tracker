def upload(client, endpoint, filename, content):
    return client.post(
        f"/upload/{endpoint}",
        files={"file": (filename, content.encode(), "text/csv")},
    )


USER_CSV = "name,height_cm,target_weight_kg\nAlex,168,68"

WEIGHT_CSV = "date,weight_kg\n2025-01-01,80.0\n2025-01-08,79.5\n2025-01-15,79.0"

DOSES_CSV = (
    "medication_name,dose,unit,date_changed\n"
    "Wegovy,0.25,mg,2025-01-01\n"
    "Wegovy,0.5,mg,2025-02-19"
)


# --- User upload ---

def test_upload_user_creates_user(client):
    response = upload(client, "user", "user.csv", USER_CSV)
    assert response.status_code == 200
    assert response.json()["created"] == "Alex"

    user = client.get("/users/me").json()
    assert user["name"] == "Alex"
    assert user["height"] == 168.0
    assert user["target_weight"] == 68.0


def test_upload_user_replaces_existing_user(client):
    upload(client, "user", "user.csv", USER_CSV)

    response = upload(client, "user", "user.csv", "name,height_cm,target_weight_kg\nSam,172,90")
    assert response.json()["created"] == "Sam"
    assert client.get("/users/me").json()["name"] == "Sam"


def test_upload_user_empty_file(client):
    response = upload(client, "user", "user.csv", "name,height_cm,target_weight_kg")
    assert response.status_code == 200
    assert "error" in response.json()


# --- Weight log upload ---

def test_upload_weight_logs(client):
    upload(client, "user", "user.csv", USER_CSV)

    response = upload(client, "weight-logs", "weight_log.csv", WEIGHT_CSV)
    assert response.status_code == 200
    assert response.json()["inserted"] == 3

    logs = client.get("/weight-logs").json()
    assert len(logs) == 3
    assert logs[0]["weight_kg"] == 80.0


def test_upload_weight_logs_replaces_existing(client):
    upload(client, "user", "user.csv", USER_CSV)
    upload(client, "weight-logs", "weight_log.csv", WEIGHT_CSV)  # 3 logs

    response = upload(client, "weight-logs", "weight_log.csv", "date,weight_kg\n2025-03-01,78.0")
    assert response.json()["inserted"] == 1
    assert len(client.get("/weight-logs").json()) == 1


def test_upload_weight_logs_skips_rows_with_missing_fields(client):
    upload(client, "user", "user.csv", USER_CSV)

    csv = "date,weight_kg\n2025-01-01,80.0\n2025-01-08,\n,79.0\n2025-01-15,79.0"
    response = upload(client, "weight-logs", "weight_log.csv", csv)
    assert response.json()["inserted"] == 2  # 2 rows skipped (missing date or weight)


# --- Medication doses upload ---

def test_upload_medication_doses(client):
    upload(client, "user", "user.csv", USER_CSV)

    response = upload(client, "medication-doses", "medication_doses.csv", DOSES_CSV)
    assert response.status_code == 200
    assert response.json()["inserted"] == 2

    medications = client.get("/medications").json()
    assert len(medications) == 1  # both doses belong to Wegovy — only one Medication record
    assert medications[0]["name"] == "Wegovy"

    doses = client.get(f"/medications/{medications[0]['id']}/doses").json()
    assert len(doses) == 2


def test_upload_medication_doses_multiple_medications(client):
    upload(client, "user", "user.csv", USER_CSV)

    csv = (
        "medication_name,dose,unit,date_changed\n"
        "Wegovy,0.25,mg,2025-01-01\n"
        "Mounjaro,2.5,mg,2025-06-01"
    )
    upload(client, "medication-doses", "medication_doses.csv", csv)

    assert len(client.get("/medications").json()) == 2


def test_upload_medication_doses_replaces_existing(client):
    upload(client, "user", "user.csv", USER_CSV)
    upload(client, "medication-doses", "medication_doses.csv", DOSES_CSV)  # Wegovy

    new_csv = "medication_name,dose,unit,date_changed\nMounjaro,2.5,mg,2025-06-01"
    upload(client, "medication-doses", "medication_doses.csv", new_csv)

    medications = client.get("/medications").json()
    assert len(medications) == 1
    assert medications[0]["name"] == "Mounjaro"


def test_upload_medication_doses_empty_file(client):
    upload(client, "user", "user.csv", USER_CSV)
    response = upload(client, "medication-doses", "medication_doses.csv", "medication_name,dose,unit,date_changed")
    assert response.json()["inserted"] == 0


# --- Reset ---

def test_reset_clears_all_data(client):
    upload(client, "user", "user.csv", USER_CSV)
    upload(client, "weight-logs", "weight_log.csv", WEIGHT_CSV)

    response = client.post("/upload/reset")
    assert response.status_code == 200
    assert response.json()["reset"] is True
    assert client.get("/users/me").status_code == 404


def test_reset_with_no_data_succeeds(client):
    response = client.post("/upload/reset")
    assert response.status_code == 200
    assert response.json()["reset"] is True

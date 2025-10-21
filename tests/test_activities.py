from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_contains_expected_keys():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Sanity check: activities is a dict and contains the sample keys
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_student@mergington.edu"

    # Ensure not already signed up
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    if email in participants:
        # Remove if present to start clean
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json()["message"]

    # Confirm participant present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # Unregister
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert f"Unregistered {email}" in resp.json()["message"]

    # Confirm removed
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants

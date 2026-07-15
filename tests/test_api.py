def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload


def test_signup_adds_new_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    before = client.get("/activities").json()[activity_name]["participants"]
    assert email not in before

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    after = client.get("/activities").json()[activity_name]["participants"]
    assert email in after
    assert len(after) == len(before) + 1


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant(client):
    activity_name = "Chess Club"
    participant = "daniel@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{participant}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {participant} from {activity_name}"

    updated_participants = client.get("/activities").json()[activity_name]["participants"]
    assert participant not in updated_participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown Club/participants/student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_unknown_participant_returns_404(client):
    activity_name = "Chess Club"

    response = client.delete(
        f"/activities/{activity_name}/participants/not-registered@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_is_case_insensitive(client):
    activity_name = "Chess Club"
    mixed_case_email = "MICHAEL@MERGINGTON.EDU"

    response = client.delete(
        f"/activities/{activity_name}/participants/{mixed_case_email}"
    )

    assert response.status_code == 200

    updated_participants = client.get("/activities").json()[activity_name]["participants"]
    assert "michael@mergington.edu" not in updated_participants

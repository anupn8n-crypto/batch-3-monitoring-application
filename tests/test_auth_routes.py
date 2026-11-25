"""Unit tests for login, logout, and protected routes."""

import pytest

from app import create_app


@pytest.fixture
def app():
    application = create_app()
    application.config.update(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "ADMIN_USERNAME": "admin",
        }
    )
    # Ensure a known hash for the demo password used in tests.
    from app.auth_utils import hash_password

    application.config["ADMIN_PASSWORD_HASH"] = hash_password("admin123")
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Sign in" in body
    assert "admin" in body


def test_login_success_redirects_home(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_login_failure_generic_error(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "wrong-password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Invalid credentials" in body
    # Security: never leak stack traces or submitted password.
    assert "Traceback" not in body
    assert "wrong-password" not in body
    assert "werkzeug" not in body.lower()


def test_protected_home_redirects_when_logged_out(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logout_clears_session(client):
    client.post("/login", data={"username": "admin", "password": "admin123"})
    home = client.get("/")
    assert home.status_code == 200

    logout = client.post("/logout", follow_redirects=False)
    assert logout.status_code == 302
    assert "/login" in logout.headers["Location"]

    blocked = client.get("/", follow_redirects=False)
    assert blocked.status_code == 302
    assert "/login" in blocked.headers["Location"]

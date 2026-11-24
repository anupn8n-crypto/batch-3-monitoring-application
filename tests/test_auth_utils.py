"""Unit tests for password hashing helpers."""

from app.auth_utils import hash_password, verify_password


def test_hash_is_not_plaintext():
    password = "admin123"
    hashed = hash_password(password)
    assert hashed != password
    assert password not in hashed


def test_correct_password_verifies():
    password = "correct-horse-battery"
    hashed = hash_password(password)
    assert verify_password(hashed, password) is True


def test_wrong_password_fails():
    hashed = hash_password("right-password")
    assert verify_password(hashed, "wrong-password") is False


def test_empty_inputs_fail_verification():
    hashed = hash_password("something")
    assert verify_password("", "something") is False
    assert verify_password(hashed, "") is False
    assert verify_password("", "") is False

import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("first@mail.com", "1111", 200),
    ("first@mail.com", "1111", 400),
    ("secondt@mail.com", "1111", 200),
    ("third", "1111", 422),
    ("fourth@dgfg", "1111", 422),
])
async def test_auth_flow(ac, email: str, password: str, status_code: int):
    # /register
    response_register = await ac.post(
        "auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    assert response_register.status_code == status_code
    if status_code != 200:
        return
    res = response_register.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"

    # /login
    response_login = await ac.post(
        "auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert response_login.status_code == status_code
    res = response_login.json()
    assert isinstance(res, dict)
    assert ac.cookies["access_token"]
    assert "access_token" in response_login.json()

    # /me
    response_me = await ac.get("auth/me")
    assert response_me.status_code == status_code
    user = response_me.json()
    assert response_me.status_code == status_code
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    response_logout = await ac.post("auth/logout")
    assert response_logout.status_code == status_code
    res = response_logout.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "access_token" not in ac.cookies

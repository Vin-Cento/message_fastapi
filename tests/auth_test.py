import requests


def signup(username, password):
    ENDPOINT = "http://localhost:8004/signup"
    payload = {"username": username, "password": password}
    res = requests.post(f"{ENDPOINT}", json=payload)
    return res


def login(username, password):
    ENDPOINT = "http://localhost:8004/login"
    payload = {"username": username, "password": password}
    res = requests.post(f"{ENDPOINT}", data=payload)
    return res


def changeusername(username, password, new_username):
    ENDPOINT = "http://localhost:8004/reset_username"
    payload = {"username": username, "password": password, "username_new": new_username}
    res = requests.put(f"{ENDPOINT}", json=payload)
    return res


def changepassword(username, password, new_password):
    ENDPOINT = "http://localhost:8004/reset_username"
    payload = {"username": username, "password": password, "password_new": new_password}
    res = requests.put(f"{ENDPOINT}", json=payload)
    return res


def delete_account(username, password, token):
    ENDPOINT = "http://localhost:8004/delete_account"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"username": username, "password": password}
    res = requests.delete(f"{ENDPOINT}", data=payload, headers=headers)
    return res

user, wrong_user, password, wrong_password = "new_user", "wrong_user", "password", "pas"

print("test signing")
assert signup(user, password).status_code == 200
assert signup(user, password).status_code == 406

print("testing login")
assert login(user, wrong_password).status_code == 404
assert login(wrong_user, password).status_code == 404
assert login(wrong_user, wrong_password).status_code == 404

# login correctly and get token
res = login(user, password)
token = eval(res.content.decode("utf-8"))["access_token"]
wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2ODQ2MjkyMDR9.JN_dHRt88wiJmphGZt37wLxc6gFNf6BnjZyGQ6sakL0"
assert res.status_code == 200

print("testing delete")
assert delete_account(wrong_user, password, token).status_code == 404
assert delete_account(user, wrong_password, token).status_code == 404
assert delete_account(user, wrong_password, wrong_token).status_code == 401

print("delete new account")
assert delete_account(user, password, token).status_code == 204
assert delete_account(user, password, token).status_code == 404

assert login(user, password).status_code == 404

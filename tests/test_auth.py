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


# sign up with new user
user, wrong_user, password, wrong_password = "new_user", "wrong_user", "password", "pas"
assert signup(user, password).status_code == 200
# sign up with existing user
assert signup(user, password).status_code == 406

# login with wrong credential
assert login(user, wrong_password).status_code == 404
assert login(wrong_user, password).status_code == 404
assert login(wrong_user, wrong_password).status_code == 404

# login correctly and get token
res = login(user, password)
token = eval(res.content.decode("utf-8"))["token"]
wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2ODQ2MjkyMDR9.JN_dHRt88wiJmphGZt37wLxc6gFNf6BnjZyGQ6sakL0"
assert res.status_code == 200

# delete empty account
assert delete_account(wrong_user, password, token).status_code == 404
# delete bad password
assert delete_account(user, wrong_password, token).status_code == 404
# delete bad token
assert delete_account(user, wrong_password, wrong_token).status_code == 404

# delete created account
assert delete_account(user, password, token).status_code == 204
# delete deleted acount
assert delete_account(user, password, token).status_code == 404

# login with deleted acount
assert login(user, password).status_code == 404

import requests

def signup(username, password):
    ENDPOINT = "http://localhost:8004/signup"
    payload = {"username": username, "password": password}
    res = requests.post(f"{ENDPOINT}", json=payload)
    return res

def login(username, password):
    ENDPOINT = "http://localhost:8004/login"
    payload = {"username": username, "password": password}
    res = requests.post(f"{ENDPOINT}", json=payload)
    return res

# sign up with new user
assert signup("new_user", "password").status_code == 200
assert login("new_user", "password").status_code == 200

# sign up with username already taken
assert signup("vinny1", "vinny1").status_code == 406

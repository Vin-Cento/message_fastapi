import requests

def signup(username, password):
    ENDPOINT = "http://localhost:8004/signup"
    payload = {"username": username, "password": password}
    res = requests.post(f"{ENDPOINT}", json=payload)
    return res

assert signup("vinny2", "vinny2").status_code == 406
assert signup("vinny1", "vinny1").status_code == 406

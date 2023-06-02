import requests

ENDPOINT = "http://localhost:8004/messages"

def login(username, password):
    ENDPOINT = "http://localhost:8004/login"
    payload = {"username": username, "password": password}
    res = requests.post(f"{ENDPOINT}", data=payload)
    return res

def get_message():
    ENDPOINT = "http://localhost:8004/api/v1/messages"
    pass

def post_message():
    ENDPOINT = "http://localhost:8004/api/v1/messages"
    pass

def delete_message():
    ENDPOINT = "http://localhost:8004/api/v1/messages"
    pass

def edit_message():
    ENDPOINT = "http://localhost:8004/api/v1/messages"
    pass

def test_message():
    user, wrong_user, password, wrong_password = "new_user", "wrong_user", "password", "pas"
    assert signup(user, password).status_code == 200
    get_message()
    post_message()
    edit_message()
    pass

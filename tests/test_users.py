import requests

ENDPOINT = "http://localhost:8004/users"

def create_user():
    payload = {"username": "vinny", "password": "12345"}
    print(f"testing {ENDPOINT}")

    print(f"post {ENDPOINT}")
    print(f"payload {payload}")
    res = requests.post(f"{ENDPOINT}/", json=payload)
    assert res.status_code == 200
    content_post = res.json()
    ID = content_post["user_id"]
    print(f"return {content_post}")

    ENDPOINT_ID = ENDPOINT + "/" + str(ID)

    print(f"delete {ENDPOINT_ID}")
    res = requests.delete(ENDPOINT_ID)
    status_code = res.status_code
    assert status_code == 204

    res = requests.get(ENDPOINT_ID)
    status_code = res.status_code
    assert status_code == 404

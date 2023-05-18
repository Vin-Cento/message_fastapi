import requests

ENDPOINT = "http://localhost:8004/messages"


def test_message():
    payload = {"message": "test message"}
    print(f"testing {ENDPOINT}")

    print(f"post {ENDPOINT}")
    print(f"payload {payload}")
    res = requests.post(f"{ENDPOINT}/", json=payload)
    assert res.status_code == 200
    content_post = res.json()
    ID = content_post["message_id"]
    print(f"return {content_post}")

    ENDPOINT_ID = ENDPOINT + "/" + str(ID)

    print(f"get {ENDPOINT_ID}")
    test_endpoint = ENDPOINT_ID
    res = requests.get(test_endpoint)
    content_get = res.json()
    status_code = res.status_code
    assert content_get == content_post
    assert status_code == 200
    print(f"return {content_get}")

    payload_new = {"message": "changed"}
    print(f"put {ENDPOINT_ID}")
    print(f"payload {payload_new}")
    res = requests.put(ENDPOINT_ID, json=payload_new)
    status_code = res.status_code
    assert status_code == 204

    res = requests.get(ENDPOINT_ID)
    status_code = res.status_code
    content = res.json()
    assert content == {"message_id": ID, "message": "changed"}
    assert status_code == 200

    print(f"delete {ENDPOINT_ID}")
    res = requests.delete(ENDPOINT_ID)
    status_code = res.status_code
    assert status_code == 204

    res = requests.get(ENDPOINT_ID)
    status_code = res.status_code
    assert status_code == 404

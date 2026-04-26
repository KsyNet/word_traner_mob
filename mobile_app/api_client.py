import requests

BASE_URL = "http://192.168.0.13:8000"  # Для телефона заменить на IP ПК
USER_ID = None
USERNAME = None

TIMEOUT = 5


def safe(r):
    try:
        return r.json()
    except:
        print("SERVER ERROR:", r.text)
        return {"ok": False, "error": "Invalid server response"}


def register(username, password):
    try:
        r = requests.post(
            f"{BASE_URL}/register",
            params={"username": username, "password": password},
            timeout=TIMEOUT
        )
        data = safe(r)

        if data.get("ok"):
            global USER_ID, USERNAME
            USER_ID = data["user_id"]
            USERNAME = username

        return data

    except Exception as e:
        return {"ok": False, "error": str(e)}


def login(username, password):
    try:
        r = requests.post(
            f"{BASE_URL}/login",
            params={"username": username, "password": password},
            timeout=TIMEOUT
        )
        data = safe(r)

        if data.get("ok"):
            global USER_ID, USERNAME
            USER_ID = data["user_id"]
            USERNAME = username

        return data

    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_username():
    return USERNAME


def get_words():
    if not USER_ID:
        return {"error": "Not logged in"}

    try:
        r = requests.get(
            f"{BASE_URL}/words",
            params={"user_id": USER_ID},
            timeout=TIMEOUT
        )
        return safe(r)
    except Exception as e:
        return {"error": str(e)}


def add_word(word, translation, level="easy"):
    if not USER_ID:
        return {"error": "Not logged in"}

    try:
        r = requests.post(
            f"{BASE_URL}/add_word",
            params={
                "user_id": USER_ID,
                "word": word,
                "translation": translation,
                "level": level
            },
            timeout=TIMEOUT
        )
        return safe(r)
    except Exception as e:
        return {"error": str(e)}


def delete_word(word_id):
    if not USER_ID:
        return {"error": "Not logged in"}

    try:
        r = requests.post(
            f"{BASE_URL}/delete_word",
            params={"user_id": USER_ID, "word_id": word_id},
            timeout=TIMEOUT
        )
        return safe(r)
    except Exception as e:
        return {"error": str(e)}


def quiz():
    if not USER_ID:
        return {"error": "Not logged in"}

    try:
        r = requests.get(
            f"{BASE_URL}/quiz",
            params={"user_id": USER_ID},
            timeout=TIMEOUT
        )
        return safe(r)
    except Exception as e:
        return {"error": str(e)}


def submit_answer(selected, correct):
    if not USER_ID:
        return {"error": "Not logged in"}

    try:
        r = requests.post(
            f"{BASE_URL}/quiz/answer",
            params={
                "user_id": USER_ID,
                "selected": selected,
                "correct": correct
            },
            timeout=TIMEOUT
        )
        return safe(r)
    except Exception as e:
        return {"error": str(e)}


def stats():
    if not USER_ID:
        return {"error": "Not logged in"}

    try:
        r = requests.get(
            f"{BASE_URL}/stats",
            params={"user_id": USER_ID},
            timeout=TIMEOUT
        )
        data = safe(r)

        if isinstance(data, dict) and "error" not in data:
            data["username"] = USERNAME

        return data

    except Exception as e:
        return {"error": str(e)}
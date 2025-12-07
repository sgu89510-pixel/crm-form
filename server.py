from flask import Flask, request, jsonify
import requests
import random
import string

app = Flask(__name__)

TRACKBOX_URL = "https://track.fintechgurus.org/api/signup/procform"

AI = "2958294"
CI = "1"
GI = "292"
FUNNEL = "Education 365"
LANG = "RU"


def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    firstname = data.get("firstname")
    lastname = data.get("lastname")
    email = data.get("email")
    phone = data.get("phone")
    ip = data.get("ip")

    if not all([firstname, lastname, email, phone, ip]):
        return jsonify({"error": "missing_fields"}), 400

    password = generate_password()

    payload = {
        "ai": AI,
        "ci": CI,
        "gi": GI,
        "userip": ip,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "password": password,
        "phone": phone,
        "so": FUNNEL,
        "sub": "",
        "lg": LANG,
        # domain для Trackbox обязателен
        "domain": "track.fintechgurus.org"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(TRACKBOX_URL, json=payload, headers=headers)
        return jsonify({
            "sent_payload": payload,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Trackbox lead receiver is running."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
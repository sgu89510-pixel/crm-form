from flask import Flask, request, send_file, jsonify
import requests

app = Flask(__name__)

# ================= НАСТРОЙКИ =================
API_KEY = "c6Fp4FgkIUVvgDEgogTYfaAZM6fT8oBA"

ADD_LEAD_URL = "https://elvioncrm636.pro/api/add_lead"
LEADS_INFO_URL = "https://elvioncrm636.pro/api/leads_info"

COUNTRY = "KZ"
LANGUAGE = "RU"
SOURCE = "kaz_chrome"
SOURCE_URL = "https://kaz_chrome.com"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# ================= ROUTES =================
@app.route("/", methods=["GET"])
def index():
    return send_file("lead_form.html")


@app.route("/submit", methods=["POST"])
def submit():
    payload = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "country": COUNTRY,
        "language": LANGUAGE,
        "source": SOURCE,
        "source_url": SOURCE_URL,
        "comment": "Lead from landing"
    }

    try:
        response = requests.post(
            ADD_LEAD_URL,
            json=payload,
            headers=HEADERS,
            timeout=15
        )

        return jsonify({
            "status_code": response.status_code,
            "request": payload,
            "response": response.json()
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "request": payload
        }), 500


# ===== OPTIONAL: получение инфо по лидам =====
@app.route("/leads_info", methods=["POST"])
def leads_info():
    payload = {
        "limit": request.json.get("limit", 200),
        "offset": request.json.get("offset", 0),
        "registration_date_from": request.json.get("registration_date_from"),
        "registration_date_to": request.json.get("registration_date_to"),
        "ftd_date_from": request.json.get("ftd_date_from"),
        "ftd_date_to": request.json.get("ftd_date_to")
    }

    try:
        response = requests.post(
            LEADS_INFO_URL,
            json=payload,
            headers=HEADERS,
            timeout=15
        )
        return jsonify(response.json())

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
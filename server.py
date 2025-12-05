from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


@app.route("/send_lead", methods=["POST"])
def send_lead():
    try:
        data = request.json

        # Получаем IP
        forwarded = request.headers.get("X-Forwarded-For", "")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        # CRM endpoint
        API_TOKEN = "HwLfFkRaUV2RFC8j0ugPf0uhsppU1MRRcrzvhEfzVSzSVSmUaXUnhXO0So7D"
        CRM_URL = f"https://tracking.rivabrookes12.com/api/v3/integration?api_token={API_TOKEN}"

        # Формируем payload в формате "x-www-form-urlencoded"
        payload = {
            "link_id": 92,
            "fname": data.get("firstName", ""),
            "lname": data.get("lastName", ""),
            "email": data.get("email", ""),
            "fullphone": data.get("phone", ""),
            "ip": ip,
            "country": "RU",
            "language": "ru",
            "funnel": "Deepseek",
            "domain": "form-landing.site",  # подмена домена
            "description": data.get("source", "facebook")  # facebook / google
        }

        # Отправка
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(CRM_URL, data=payload, headers=headers, timeout=20)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text,
            "sent_payload": payload
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
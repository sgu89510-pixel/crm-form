from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form.to_dict()

        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        # Получаем IP клиента
        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.remote_addr

        # Формируем payload
        payload = {
            "token": "HwLfFkRaUV2RFC8j0ugPf0uhsppU1MRRcrzvhEfzVSzSVSmUaXUnhXO0So7D",
            "firstname": data.get("firstName", ""),
            "lastname": data.get("lastName", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", "").replace("+", ""),
            "country": "EU",
            "language": "en",
            "funnel": "Deepseek",
            "comment": "",
            "descriptions": data.get("source", ""),   # facebook / google
            "link_id": 92,
            "ip": ip
        }

        CRM_URL = "https://tracking.rivabrookes12.com/api/v1/lead"

        headers = {"Content-Type": "application/json"}

        response = requests.post(CRM_URL, json=payload, headers=headers, timeout=20)

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
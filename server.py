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

        # Получаем корректный IP клиента
        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.remote_addr

        # Определяем источник трафика (FB/Google)
        source = request.args.get("utm_source", "").lower()
        if source in ["facebook", "fb"]:
            traffic_source = "facebook"
        elif source in ["google", "g"]:
            traffic_source = "google"
        else:
            traffic_source = "unknown"

        # Формируем описание (description)
        description = f"Traffic source: {traffic_source}"

        # Формируем payload
        payload = {
            "token": "HwLfFkRaUV2RFC8j0ugPf0uhsppU1MRRcrzvhEfzVSzSVSmUaXUnhXO0So7D",
            "link_id": 92,
            "firstname": data.get("firstname", ""),
            "lastname": data.get("lastname", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", "").replace("+", ""),
            "country": "EU",
            "language": "en",
            "funnel": "Deepseek",
            "comment": "",
            "description": description,
            "ip": ip
        }

        CRM_URL = "https://tracking.rivabrookes12.com/api/v1/lead"

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(CRM_URL, json=payload, headers=headers)

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
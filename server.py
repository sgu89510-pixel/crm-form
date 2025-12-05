from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# ---------------------------
#  FORM RENDER
# ---------------------------
@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")

# ---------------------------
#  LEAD SENDER
# ---------------------------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form.to_dict()

        # Проверяем что данные пришли
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        # IP пользователя
        forwarded = request.headers.get("X-Forwarded-For", "")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        # Сбор payload
        payload = {
            "token": "HwLfFkRaUV2RFC8j0ugPf0uhsppU1MRRcrzvhEfzVSzSVSmUaXUnhXO0So7D",
            "firstname": data.get("firstName", ""),
            "lastname": data.get("lastName", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", "").replace("+", ""),
            "country": "EU",
            "funnel": "Deepseek",
            "description": data.get("traffic_source", ""),   # Facebook или Google
            "link_id": 92,
            "ip": ip
        }

        CRM_URL = "https://tracking.rivabrookes12.com/api/v2/lead/add"

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

# ---------------------------
#  RUN SERVER
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
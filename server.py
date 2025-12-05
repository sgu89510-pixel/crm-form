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
        # принимаем form-data и JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        if not data:
            return jsonify({"success": False, "error": "Empty data"}), 400

        # IP пользователя
        forwarded = request.headers.get("X-Forwarded-For")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        # source (facebook / google)
        source = data.get("source", "").lower()
        if source not in ["facebook", "google"]:
            source = "facebook"  # дефолт

        # ПЛАТФОРМА ТРЕБУЕТ ТАКИЕ ПОЛЯ:
        payload = {
            "token": "HwLfFkRaUV2RFC8j0ugPf0uhsppU1MRRcrzvhEfzVSzSVSmUaXUnhXO0So7D",
            "firstname": data.get("firstname", ""),
            "lastname": data.get("lastname", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", "").replace("+", ""),
            "country": "EU",
            "language": "en",
            "funnel": "Deepseek",
            "descriptions": source,
            "link_id": 92,
            "ip": ip
        }

        CRM_URL = "https://tracking.rivabrookes12.com/api/lead/add"

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
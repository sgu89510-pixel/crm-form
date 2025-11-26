from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")   # твоя форма

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form.to_dict()

        if not data:
            return jsonify({"success": False, "error": "Нет данных"}), 400

        # IP корректно (Render → X-Forwarded-For)
        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.remote_addr

        payload = {
            "affc": "AFF-74J7Q3VWER",
            "bxc": "BX-2FIXYD4ZPIXOW",
            "vtc": "VT-HP8XSRMKVS6E7",

            "profile": {
                "firstName": data.get("firstName", ""),
                "lastName": data.get("lastName", ""),
                "email": data.get("email", ""),
                "password": "Temp12345!",
                "phone": data.get("phone", "").replace("+", "").replace(" ", "")
            },

            "ip": ip,
            "funnel": "Cryptomind",
            "landingURL": "https://walloram.onrender.com",
            "geo": "RU",
            "lang": "ru",
            "landingLang": "ru",
            "userAgent": request.headers.get("User-Agent"),
            "comment": None
        }

        CRM_URL = "https://golden-vault.hn-crm.com/api/lead/create"

        headers = {
            "Content-Type": "application/json",
            "Api-Key": "573d022a-83fd-4ea9-879f-0e6dee76374f"
        }

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
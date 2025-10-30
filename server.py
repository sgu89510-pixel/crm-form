from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="")
CORS(app)

# === СТАТИЧЕСКИЕ ФАЙЛЫ (HTML) ===
@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'lead_form.html')

# === ОТПРАВКА ЛИДА В CRM ===
@app.route('/send_lead', methods=["POST"])
def send_lead():
    data = request.json

    crm_url = "https://golden-vault.hn-crm.com/api/external/integration/lead"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "573d022a-83fd-4ea9-879f-0e6dee76374f"
    }

    payload = {
        "affc": "AFF-74J7Q3VWER",
        "bxc": "BX-2FIXYD4ZPIXOW",
        "vtc": "VT-HP8XSRMKVS6E7",
        "funnel": "cryptoedu",
        "landingURL": "https://walloram.onrender.com",
        "geo": "RU",
        "lang": "ru",
        "landingLang": "ru",
        "profile": {
            "firstName": data.get("name", ""),
            "lastName": "",
            "email": data.get("email", ""),
            "password": "AutoGen123!",
            "phone": data.get("phone", "").replace("+", "")
        },
        "ip": request.remote_addr or "127.0.0.1"
    }

    try:
        response = requests.post(crm_url, headers=headers, json=payload, timeout=30)
        return jsonify({
            "crm_response": response.text,
            "crm_status": response.status_code,
            "success": response.ok
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False})
# === Запуск сервера ===
if  __name__  == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Starting server on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

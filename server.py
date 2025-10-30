from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="")
CORS(app)
import random, re

def random_ru_ip():
    return f"95.108.{random.randint(0,255)}.{random.randint(1,254)}"

def get_valid_ip():
    ip_header = request.headers.get("X-Forwarded-For", request.remote_addr)
    ip = ip_header.split(",")[0].strip() if ip_header else None
    pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
    return ip if ip and re.match(pattern, ip) else random_ru_ip()

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
           "lastName": data.get("name", ""),
            "email": data.get("email", ""),
            "password": "AutoGen123!",
            "phone": data.get("phone", "").replace("+", "")
        },
       "ip": get_valid_ip(),
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

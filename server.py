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

    # Проверяем, чтобы были переданы нужные поля
    if not all(k in data for k in ("name", "email", "phone")):
        return jsonify({"error": "Missing required fields"}), 400

    # Добавляем идентификаторы CRM
    data["affc"] = "AFF-74J7Q3VWER"
    data["bxc"] = "BX-2FIXYD4ZPIXOW"
    data["vtc"] = "VT-HP8XSRMKVS6E7"

    # Правильный URL API
    crm_url = "https://golden-vault.hn-crm.com/api/v2/leads/create"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": "573d022a-83fd-4ea9-879f-0e6dee76374f"
    }

    try:
        response = requests.post(crm_url, json=data, headers=headers, timeout=30)
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

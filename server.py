from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='')

# === СТАТИЧЕСКИЕ ФАЙЛЫ (HTML) ===
@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'lead_form.html')

# === ОТПРАВКА ЛИДА В CRM ===
@app.route('/send_lead', methods=['POST'])
def send_lead():
    data = request.json

    # добавляем воронку по умолчанию
    data["funnel"] = "cryptoedu"

    crm_url = "https://golden-vault.hn-crm.com/api/leads/create"

    try:
        response = requests.post(crm_url, json=data, timeout=30)
        return jsonify({
            "crm_response": response.text,
            "crm_status": response.status_code,
            "success": response.ok
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False})
    data = request.json
    crm_url = "https://golden-vault.hn-crm.com/api/leads/create"

    try:
        response = requests.post(crm_url, json=data, timeout=30)
        return jsonify({
            "crm_response": response.text,
            "crm_status": response.status_code,
            "success": response.ok
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False})

import os

if  __name__  == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

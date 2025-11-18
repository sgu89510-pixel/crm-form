from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="")
CORS(app)

# === ОТОБРАЖЕНИЕ HTML-ФОРМЫ ===
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "lead_form.html")


# === ОТПРАВКА ЛИДА В CRM stormchg.biz ===
@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    # Получаем реальный IP (Render передает его в X-Forwarded-For)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip:
        ip = ip.split(",")[0]  # если несколько IP — берем первый

    crm_url = "https://stormchg.biz/api/external/integration/lead"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "a9e96a13-9d82-465c-a111-085b94756b81"
    }

    payload = {
        "affc": "AFF-7HXBU5456B",
        "bxc": "BX-6MWDHF8F519II",
        "vtc": "VT-HP8XSRMKVS6E7",

        "profile": {
            "firstName": data.get("name", ""),
            "lastName": "Testov",
            "email": data.get("email", ""),
            "password": "AutoGen123!",
            "phone": data.get("phone", "")
                .replace("+", "")
                .replace("-", "")
                .replace(" ", "")
        },

        "ip": ip if ip else "127.0.0.1",
        "funnel": "kaz_atom",   # ← ВАЖНО! ТВОЯ ВОРОНКА
        "landingURL": "https://walloram.onrender.com/",
        "geo": "KZ",
        "lang": "ru",
        "landingLang": "ru",

        # OPTIONAL
        "userAgent": request.headers.get("User-Agent"),
        "comment": None,
        "utmSource": None,
        "utmMedium": None,
        "utmCampaign": None,
        "utmId": None,
        "subId": None,
        "subId_a": None,
        "subId_b": None,
        "subId_c": None,
        "subId_d": None,
        "subId_e": None,
        "subId_f": None
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


# === ЗАПУСК НА RENDER ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
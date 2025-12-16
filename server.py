from flask import Flask, request
import requests
import random
import string
import json

app = Flask(__name__)

def generate_password():
    return "A@" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@app.route("/")
def index():
    return open("lead_form.html", encoding="utf-8").read()

@app.route("/submit", methods=["POST"])
def submit():

    # ДАННЫЕ, КОТОРЫЕ УХОДЯТ В CRM
    fields = {
        "api_key": "8ed304133d586ba2b9649d6c60f2a18e",
        "map_id": 4240,
        "email": request.form.get("email"),
        "first_name": request.form.get("first_name"),
        "second_name": request.form.get("second_name"),
        "phone": request.form.get("phone"),
        "country": "RU",
        "language": "ru",
        "campaign": "Evropaprigon",
        "description": "Лид с лендинга",
        "password": generate_password()
    }

    try:
        response = requests.post(
            "https://bestcliq.tech/api/v1/AddLead",
            data=fields,
            timeout=15
        )
        crm_response_text = response.text
        try:
            crm_response_json = response.json()
        except:
            crm_response_json = crm_response_text

    except Exception as e:
        return f"<pre>Request error:\n{str(e)}</pre>", 500

    # 🔍 МАСКИРУЕМ API KEY ДЛЯ ОТОБРАЖЕНИЯ
    safe_fields = fields.copy()
    safe_fields["api_key"] = "********"

    # ✅ HTML ОТВЕТ С REQUEST + RESPONSE
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>CRM Debug</title>
        <style>
            body {{ font-family: monospace; background:#111; color:#0f0; padding:20px; }}
            pre {{ background:#000; padding:15px; border:1px solid #0f0; }}
            h2 {{ color:#00ffff; }}
        </style>
    </head>
    <body>

    <h2>📤 REQUEST TO CRM</h2>
    <pre>{json.dumps(safe_fields, indent=2, ensure_ascii=False)}</pre>

    <h2>📥 CRM RESPONSE</h2>
    <pre>{json.dumps(crm_response_json, indent=2, ensure_ascii=False)}</pre>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
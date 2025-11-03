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
@app.route('/send_lead', methods=['POST'])
def send_lead():
    data = request.json

    # Данные формы
    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    ip = request.remote_addr or "127.0.0.1"

    # Разделяем имя на имя и фамилию
    first_name = name.split(" ")[0] if name else ""
    last_name = " ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else "User"

    # URL CRM
    crm_url = "https://crm.my-crm.social/api/leads"

    # Заголовки запроса
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1IiwianRpIjoiZjFhZjA4ZGQ3ODRmNjBlODEzNzc0ZTIyYjQ3NmYwODYyNGJjODg3NGYxNWYyNmFlZTAxODlhOWY1NTlhZDYxODEzMDZmYmFjNTIwYjg0NGEiLCJpYXQiOjE3NjIxNzkwNjQuNjI5ODc0LCJuYmYiOjE3NjIxNzkwNjQuNjI5ODc3LCJleHAiOjE3OTM3MTUwNjQuNjI1MzU2LCJzdWIiOiIyMSIsInNjb3BlcyI6W119.r2MafjbmghoD6JfVkv5uWbzsleChZMHZV6K-eX5gngfLgEbQlv5hLAcisJuSUC3o01yz8FsVVxOn6vHxOR7_SL_n7uxFRYN2-ozU_CF0IcpEWf8Bws0Y_HQi4o1SV2rniXLQN8F5XRpZWAfMYeBTne-x8sETO7zdUzXlBs0qp_4fwKKLEwDtUSE5686ZgUQgL-eruPd_0QFzB2KiPXxnUkoz0SLOdzrsurYdMsREyvQ-cicVVNObKo2hbJJoEsHJkF1u28J4iqEmnxCDNqkwWqj7vJAqDx-00oew3X_wlt4fQ5C0zvR4Z4P3fr1o-1pfgtcUwMFi_O4E-ab3w0ng4KxjLWjeMVgGv7l12PKAFD5zh1xlqZQKb914NFMOvyzSQ9CiAVJzAlsYEcn30bHo3zMoI9JUbXGj9uHmgFMIrqMDWzudCQCsz2ArlFxdqaW8QRiBtcx9O_x2NQxU-2YxNwJNixPZLnHgPPn6Q64Dl2nEOxuMrs1cM4Skr9AuiUtsqgLP7GrUubSGD_mtGFDo_QRjmiqJ1WuUUY0Vxycosqh1aAXCTezSUkzDVYdZM4ZQ_Dw2A0V7jkrW016F0ggQFS8rmZaPfAb9IxnxhWc4YrH6efJFZrYqYZz2_sSAU72jcl6dkY14xoaqDbNQ9efwgSHruJQb9UJgaUprEASKPYw"
    }

    # Формирование тела запроса
    payload = {
        "full_name": f"{first_name} {last_name}",
        "country": "KZ",
        "email": email,
        "landing": "https://kaz_atom.onrender.com/",
        "phone": phone,
        "user_id": "21",
        "ip": ip,
        "source": "MediaSnipers",
        "landing_name": "kaz_atom"
    }

    try:
        response = requests.post(crm_url, headers=headers, data=payload, timeout=30)
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

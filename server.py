from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


@app.route("/send_lead", methods=["POST"])
def send_lead():
    try:
        data = request.json

        # Получаем IP пользователя
        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.remote_addr

        # --- CRM SETTINGS ---
        API_TOKEN = "HwLfFkRaUV2RFC8j0ugPf0uhsppU1MRRcrzvhEfzVSzSVSmUaXUnhXO0So7D"
        LINK_ID = 92
        FUNNEL = "Deepseek"

        # Формируем payload строго по их API (form-urlencoded)
        payload = {
            "link_id": LINK_ID,
            "fname": data.get("firstName"),
            "lname": data.get("lastName"),
            "email": data.get("email"),
            "fullphone": data.get("phone"),
            "ip": ip,
            "country": "EU",                 # ты сказал GEO = Европа
            "language": "en",
            "source": data.get("source"),    # FB or Google
            "funnel": FUNNEL,
            "domain": "form",                # можем скрыть домен
            "description": data.get("source"),  # передаём source
        }

        # URL вида /api/v3/integration?api_token=TOKEN
        url = f"https://tracking.rivabrookes12.com/api/v3/integration?api_token={API_TOKEN}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=payload, headers=headers)

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
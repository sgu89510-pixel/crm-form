from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

API_TOKEN = "HwLfFkRaUV2RFC8j0ugPf0uhsppU1MRRcrzvhEfzVSzSVSmUaXUnhXO0So7D"
LINK_ID = 92

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


@app.route("/send_lead", methods=["POST"])
def send_lead():
    try:
        data = request.json

        # Lead IP
        forwarded = request.headers.get("X-Forwarded-For", "")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        # Required POST fields (urlencoded!)
        payload = {
            "link_id": LINK_ID,
            "fname": data.get("firstName", ""),
            "lname": data.get("lastName", ""),
            "email": data.get("email", ""),
            "fullphone": data.get("phone", ""),
            "ip": ip,
            "country": "EU",
            "language": "en",
            "funnel": "Deepseek",
            "source": data.get("source"),
            "domain": "landing.com",  # можно скрыть любой домен
            "description": f"source={data.get('source')}"
        }

        url = f"https://tracking.rivabrookes12.com/api/v3/integration?api_token={API_TOKEN}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, data=payload, headers=headers)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
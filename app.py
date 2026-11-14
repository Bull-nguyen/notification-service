```python
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELNYX_API_KEY = os.getenv("TELNYX_API_KEY", "")
TELNYX_API_URL = "https://api.telnyx.com/v2"

HEADERS = {
    "Authorization": f"Bearer {TELNYX_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/webhooks/telnyx", methods=["POST"])
def handle_telnyx_webhook():
    """Receive and process inbound call events from Telnyx."""
    payload = request.json or {}
    event_data = payload.get("data", {})
    event_type = event_data.get("event_type")
    call_control_id = event_data.get("payload", {}).get("call_control_id")

    if event_type == "call.initiated" and call_control_id:
        # Automatically answer incoming call
        answer_url = f"{TELNYX_API_URL}/calls/{call_control_id}/actions/answer"
        requests.post(answer_url, headers=HEADERS, timeout=10)

    elif event_type == "call.answered" and call_control_id:
        # Play an automated greeting message using Text-to-Speech
        speak_url = f"{TELNYX_API_URL}/calls/{call_control_id}/actions/speak"
        body = {
            "payload": "Hello. Thank you for calling our automated support line.",
            "voice": "female",
            "language": "en-US"
        }
        requests.post(speak_url, json=body, headers=HEADERS, timeout=10)

    return jsonify({"status": "received"}), 200


def send_voice_notification(to_number: str, from_number: str, connection_id: str):
    """Trigger an outbound transactional reminder call via Telnyx REST API."""
    url = f"{TELNYX_API_URL}/calls"
    payload = {
        "connection_id": connection_id,
        "to": to_number,
        "from": from_number
    }
    response = requests.post(url, json=payload, headers=HEADERS, timeout=10)
    return response.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import requests

def send_to_slack(message: str):
    WEBHOOK_URL = "https://hooks.slack.com/services/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"
    
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }
    
    response = requests.post(WEBHOOK_URL, json=payload)
    
    try:
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        print("Message sent to Slack successfully.")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to send message to Slack: {e}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

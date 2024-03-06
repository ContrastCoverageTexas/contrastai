import os
import requests

# Use an environment variable for the webhook URL
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_to_slack(message: str):
    """
    Sends a message to Slack.
    """
    if not WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL environment variable not set.")
        return None

    response = requests.post(
        WEBHOOK_URL,
        json={
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
    )
    try:
        response.raise_for_status()  # Raises an error for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return response

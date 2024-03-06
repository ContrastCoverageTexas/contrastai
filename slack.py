import requests

WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_to_slack(message: str):
    """
    Sends a message to Slack
    """
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
    # Log response for debugging
    print(f"Response code: {response.status_code}")
    print(f"Response body: {response.text}")
    return response

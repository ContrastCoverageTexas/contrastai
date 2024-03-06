import requests

def send_to_slack(message: str):
    """
    Sends a simple text message to Slack
    """
    WEBHOOK_URL= "https://hooks.slack.com/services/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"
    
    return requests.post(
      WEBHOOK_URL,
      json={"text": message}
    )

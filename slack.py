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

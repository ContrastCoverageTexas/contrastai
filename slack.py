import requests

WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_to_slack(message: str):
  """
  Sends a message to Slack
  """
  return requests.post(
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

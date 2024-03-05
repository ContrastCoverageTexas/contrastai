import os
import requests

WEBHOOK_URL = database_password = os.getenv('WEBHOOK_URL')

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

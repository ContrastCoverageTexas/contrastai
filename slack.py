import requests

def send_to_slack(message: str):
  """
  Sends a message to Slack
  """
  WEBHOOK_URL= "https://hooks.slack.com/services/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"
  
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

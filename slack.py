import requests
import logging

# Configure basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_to_slack(message: str):
    """
    Sends a simple text message to Slack
    """
    WEBHOOK_URL = "https://hooks.slack.com/services/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"
    
    logging.info(f"Sending message to Slack: {message}")
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={"text": message}
        )
        # Log the response from Slack
        if response.status_code == 200:
            logging.info("Message sent successfully.")
        else:
            logging.error(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        logging.exception("Failed to send message due to an exception.")
        raise SystemExit(e)

if __name__ == "__main__":
    send_to_slack("Emergency Yall")

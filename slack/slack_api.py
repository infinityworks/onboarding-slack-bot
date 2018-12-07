import requests
import json
import logging
import os

logger = logging.getLogger()

class SlackAPI:

    def send_to_slack(self, slack_data):
        webhook_url = 'https://hooks.slack.com/services/T0330CH2P/BEM1RCU2W/' + str(os.environ.get('SLACK_MESSAGE_API_KEY'))

        try:
            response = requests.post(
                webhook_url, data=json.dumps(slack_data),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as error:
            logger.error("Error sending message to Slack. Error: " + str(error))
            return False
        print(response.status_code)

        if response.status_code != 200:
            logger.error('Could not message Slack. Response code recieved: ' + str(response.status_code))
            return False
        logging.info("Sent message to Slack asking for the new starters location")
        return True




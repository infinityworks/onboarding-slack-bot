import logging
from bambooHRappy.bambooHRappy import bambooHrApi
from slack.slack_api import SlackAPI
import os
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bamboo = bambooHrApi(os.environ.get('BAMBOO_TOKEN'), 'infinityworks')


def process_request_for_location(event, context):
    bamboo_request = json.loads(event['body'])
    try:
        employee_id = bamboo_request['employees'][0]['id']
    except:
        logger.critical("No ID was sent with the request.")
        exit(2)

    try:
        employee_details = bamboo.get_employee(employee_id, 'firstName', 'lastName')
    except Exception as error:
        logger.error('Error whilst communicating with Bamboo: ' + str(error))

    full_name = employee_details['firstName'] + " " + employee_details['lastName']

    slack_data = {
        "text": "Which office does " + full_name + " work in?",
        "attachments": [
            {
                "text": "",
                "color": "#3AA3E3",
                "callback_id": "office_picker",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "leeds",
                        "text": "Leeds",
                        "style": "danger",
                        "type": "button",
                        "value": employee_id
                    },
                    {
                        "name": "london",
                        "text": "London",
                        "style": "danger",
                        "type": "button",
                        "value": employee_id
                    },
                    {
                        "name": "manchester",
                        "text": "Manchester",
                        "style": "danger",
                        "type": "button",
                        "value": employee_id
                    }
                ]

            }
        ]
    }

    slack = SlackAPI()
    slack.send_to_slack(slack_data)

    response = {
        "statusCode": 200,
        "body": json.dumps("Message Received")
    }

    return response
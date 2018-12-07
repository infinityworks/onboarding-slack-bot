import json
import urllib
import requests
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def process_event(event):
    params = urllib.parse.unquote_plus(urllib.parse.unquote_plus(event['body']))
    params = json.dumps(params)[9:][:-1].replace("\\", "")
    params = json.loads(params)

    return params

def process_slack_response(event, context):
    try:
        params = process_event(event)
    except Exception as error:
        logger.critical('Could not process the request. Malformed form data was returned: ' + error)
        exit(2)

    office = params['actions'][0]['name']
    employee_id = params['actions'][0]['value']

    onboarding_response = call_onboarding_script(office, employee_id)

    if onboarding_response == False:
        response = {
            "statusCode": 200,
            "body": json.dumps("Dang, that didn't work. Please check the logs.")
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps("Successfully added the employee to: " + office)
        }

    return response


def call_onboarding_script(office, employee_id):
    try:
        requests.post("URLWHENLIVE", headers={"super_secret_key": os.getenv('SLACK_TO_ONBOARDING_API_KEY')}, body={"employee_id": employee_id, "office": office})
    except Exception as error:
        logger.critical("Could not post to the onboarding script: " + str(error))
        return False

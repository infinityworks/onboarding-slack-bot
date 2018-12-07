from slack.send_buttons_to_slack import process_request_for_location
from slack.recieve_from_slack import process_slack_response


def init_process_request_for_location(event, context):
    return process_request_for_location(event, context)

def init_process_slack_response(event, context):
    return process_slack_response(event, context)

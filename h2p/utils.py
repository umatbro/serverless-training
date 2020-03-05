import base64
import json

def get_url_from_lambda_event(event) -> str:
    is_base64 = event.get('isBase64Encoded', False)
    body = event.get('body', None)
    if not body:
        sqs_event = get_first_event_from_sqs_Records(event)
        return get_url_from_lambda_event(sqs_event)
    if is_base64:
        body = base64.b64decode(body)
    body = json.loads(body)
    return body.get('url', None)


def error_response(body):
    return {
        'statusCode': 400,
        'body': body,
        'headers': { 'Content-Type': 'application/json' },
        'isBase64Encoded': False,
    }


def get_first_event_from_sqs_Records(event):
    """
    If the lambda trigger is SQS, the event contains "Records" list.
    This function will get first item from records - this item can be used as regular event.
    """
    records = event.get('Records')
    if records:
        return records[0]

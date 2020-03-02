import base64
import json

def get_url_from_lambda_event(event) -> str:
    is_base64 = event.get('isBase64Encoded', False)
    body = event.get('body', None)
    if not body:
        return None
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

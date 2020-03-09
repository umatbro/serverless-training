import json
import os
import boto3

def get_body_from_event(event):
    return json.loads(event.get('body'))


def response(body, status=None):
    return {
        'isBase64Encoded': False,
        'statusCode': status or 200,
        'body': json.dumps(body),
    }

def main(event, context):
    print('event', event)
    body = get_body_from_event(event)
    print('body', body)

    credentials = {
        'aws_access_key_id': os.environ['ACCESS_KEY'],
        'aws_secret_access_key': os.environ['SECRET_KEY'],
    }

    ses = boto3.client('ses', **credentials)
    message = body.get('message')
    email = body.get('send_to')

    if not (email and message):
        return response({'message': 'This field is required', 'send_to': 'This field is required'}, status=400)
    
    try:
        res = ses.send_email(
            Source=os.environ['EMAIL_FROM'],
            Destination={
                'ToAddresses': [
                    email,
                ],
            },
            Message={
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Test email',
                },
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': message,
                    },
                },
            },
        )
    except ses.exceptions.MessageRejected as e:
        return response({
            'message': f'Could not send message to {email}',
            'traceback': str(e),
        }, 403)
    
    return response({
        'message': message,
        'send_to': email,
    })

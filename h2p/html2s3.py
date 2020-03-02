import os
import json
import datetime as dt

import boto3
import weasyprint

from utils import get_url_from_lambda_event, error_response

def main(event, context):
    url = get_url_from_lambda_event(event)
    if not url:
        return error_response({
            'url': 'This field is required',
        })

    html = weasyprint.HTML(url)
    pdf = html.write_pdf()

    client = boto3.resource(
        's3',
        aws_access_key_id=os.environ['ACCESS_KEY'],
        aws_secret_access_key=os.environ['SECRET_KEY'],
    )
    bucket_name = os.environ['BUCKET_NAME']
    now_str = dt.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
    file_name = f'{now_str}.pdf'
    # s3 = boto3.resource('s3')
    client.Bucket(bucket_name).put_object(Key=file_name, Body=pdf, ACL='public-read')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'url': os.path.join(os.environ['BUCKET_URL'], file_name),
        }),
        'headers': { 'Content-Type': 'application/json' },
        'isBase64Encoded': False,
    }

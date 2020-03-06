import os
import json
import datetime as dt

import boto3
import weasyprint

from utils import get_url_from_lambda_event


def main(event, context):
    print(event)
    url = get_url_from_lambda_event(event)
    if not url:
        raise ValueError('Url not found')

    html = weasyprint.HTML(url)
    pdf = html.write_pdf()

    credentials = {
        'aws_access_key_id': os.environ['ACCESS_KEY'],
        'aws_secret_access_key': os.environ['SECRET_KEY'],
    }

    client = boto3.resource(
        's3', **credentials,
    )
    bucket_name = os.environ['BUCKET_NAME']
    now_str = dt.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
    file_name = f'{now_str}.pdf'

    client.Bucket(bucket_name).put_object(Key=file_name, Body=pdf, ACL='public-read')

    cloudwatch = boto3.resource('cloudwatch', **credentials)
    metric = cloudwatch.Metric('custom', 'pdf-size')
    metric.put_data(MetricData=[
        {
            'MetricName': 'pdf-size',
            'Value': len(pdf),
            'Unit': 'Bytes',
        },
    ])

    return {
        'statusCode': 200,
        'body': json.dumps({
            'url': os.path.join(os.environ['BUCKET_URL'], file_name),
        }),
        'headers': { 'Content-Type': 'application/json' },
        'isBase64Encoded': False,
    }

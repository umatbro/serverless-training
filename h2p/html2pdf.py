from weasyprint import HTML
import json
import base64

from utils import get_url_from_lambda_event

def html_to_pdf(html):
    generator = HTML(string=html)
    pdf = generator.write_pdf()
    return pdf


def webpage_to_pdf(address):
    generator = HTML(address)
    pdf = generator.write_pdf()
    return pdf

def response_file(content):
    return {
        'isBase64Encoded'   : True,
        'statusCode'        : 200,
        'headers'           : { 'Content-Type': 'application/pdf' },
        'body'              : content
    }

def error_response(body):
    return {
        'statusCode': 400,
        'body': body,
        'headers': { 'Content-Type': 'application/json' },
        'isBase64Encoded': False,
    }


def main(event, context):
    print(event)
    url = get_url_from_lambda_event(event)
    if not url:
        return error_response({
            'url': 'This field is required'
        })
    pdf = webpage_to_pdf(url)
    
    # convert bytes to base64
    encoded = base64.b64encode(pdf)
    encoded = encoded.decode('utf-8')
    return response_file(encoded)

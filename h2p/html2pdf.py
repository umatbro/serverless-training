from weasyprint import HTML
import json
import base64

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
    }


def main(event, context):
    print(event)
    # body = json.loads(event['body']) or {}
    # html = body.get('html', None)
    body = event.get('body', None)
    if body:
        decoded_body = base64.b64decode(body)
        body = json.loads(decoded_body)
    else:
        return error_response({
            'url': 'This field is required',
        })
    address = body.get('url', '')
    if not address:
        return error_response({
            'url': 'This field is required'
        })
    pdf = webpage_to_pdf(address)
    # convert bytes to base64
    encoded = base64.b64encode(pdf)
    encoded = encoded.decode('utf-8')
    return response_file(encoded)

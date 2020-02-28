from weasyprint import HTML
import json
import base64

def html_to_pdf(html):
    generator = HTML(string=html)
    pdf = generator.write_pdf()
    return pdf


def response(content):
    return {
        'isBase64Encoded'   : True,
        'statusCode'        : 200,
        'headers'           : { 'Content-Type': 'application/pdf' },
        'body'              : content
    }


def main(event, context):
    print(event)
    # body = json.loads(event['body']) or {}
    # html = body.get('html', None)
    html = '''
    <h1>The title</h1>
    <p>Content goes here</p>
    '''
    if not html:
        return "html: this field is required"
    pdf = html_to_pdf(html)
    # convert bytes to base64
    encoded = base64.b64encode(pdf)
    encoded = encoded.decode('utf-8')
    return response(encoded)

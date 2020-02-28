import json
# import pandas as pd

def hello(event, context):
    # df = pd.DataFrame({'a': [1, 2, 3], 'b':[2,3,4]})
    df = {'hej':2}
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        # "input": event
        'df': df,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

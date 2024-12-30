import json
import helper

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    ticker = event['ticker']
    #txt = helper.fetch_latest_filing(ticker)
    helper.display_float_data(ticker = ticker)
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    helper.display_filings_data(ticker = ticker)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{ticker}",
            # "location": ip.text.replace("\n", "")
        }),
    }

# https://yzeh8m0ah5.execute-api.us-east-1.amazonaws.com/Prod/hello/
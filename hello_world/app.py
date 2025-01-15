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
    historical_data = helper.get_ticker_historical_data(ticker = ticker)

    float_data = helper.get_float(ticker = ticker)

    dates_of_interest = helper.get_wick_days(historical_data = historical_data)
    dates_df = helper.add_metadata_to_ticker_df(dates_of_interest = dates_of_interest)

    dates_json = json.loads(dates_df.to_json())

    gap_days_df = helper.identify_gap_days(historical_data = historical_data)
    gaps_json = json.loads(gap_days_df.to_json())

    helper.display_float_data(ticker = ticker)
    print("------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
    offerings = helper.display_filings_data(ticker = ticker)
    offerings_json = json.loads(offerings.to_json())
    print("------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
    helper.display_price_data(ticker = ticker)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{ticker}",
            "float_data": float_data,
            "offerings": offerings_json,
            "wick_days": dates_json,
            "gap_days": gaps_json
            # "location": ip.text.replace("\n", "")
        }),
    }

# https://yzeh8m0ah5.execute-api.us-east-1.amazonaws.com/Prod/hello/
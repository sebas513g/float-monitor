import requests
import constants as const
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
from dateutil.relativedelta import relativedelta
import json

# This function will fetch a JSON object from a .json file    
def fetch_json_settings(filename):
    with open("./" + filename) as json_file:
        json_data = json.load(json_file)

    return json_data

"""
    The FILING_SUBMISSIONS_BASE_URL expects a 10 digit CIK. However, the JSON and text files provided by the sec.gov website don't provide
    the leading zeroes. Say company XYZ's CIK number is 112233. When we query the FILING_SUBMISSIONS_BASE_URL, if we pass in the number 112233,
    it will return an error because instead it is expecting 0000112233 (leading zeroes that pad the number to 10 digits). 

    This function adds the leading zeroes to the provided CIK number and returns that value.

    Since we need this value for a URL, we return a string format of the CIK number because an integer would lose the leading zeroes.

    Parameters
    ----------
    cik_number: int, required
        Central Index Key that identifies individuals or companies that have filed disclosures with the SEC. 

    Returns
    -------
    A leading zero-padding, 10-digit string version of the cik_number parameter. 
"""
def prepare_cik(cik_number):
    while len(cik_number) < 10:
        cik_number = "0" + cik_number
    return cik_number

"""
    Searches tickers_json and retrieves the relevant metadata for the given ticker.

    Parameters
    ----------
    ticker: str, required

    tickers_json: str, required

    Returns
    -------
    Returns the metadata for the given ticker. 
"""
def get_ticker_metadata(ticker, tickers_json):
    return list(filter(lambda x: x["ticker"] == ticker, tickers_json.values()))[0]

"""
    Parameters
    ----------
    ticker: str, required

    tickers_json: str, required

    is_padding_necessary: boolean, required, default = True
        If is_padding_necessary = True, then the cik_number returned will be in the 10 digit format. 

    Returns
    -------
    Returns the cik_number of the given ticker. The returned value is a string.
"""
def get_cik_number(ticker, tickers_json, is_padding_necessary = True):
    metadata = get_ticker_metadata(ticker, tickers_json)
    cik_number = str(metadata['cik_str'])

    if is_padding_necessary:
        cik_number = prepare_cik(str(metadata['cik_str']))

    return cik_number

"""
    To retrieve the sec filings data for a given company, we need a url in the following format:
    const.FILING_SUBMISSIONS_BASE_URL + <company_cik_number> + .json

    Here the <company_cik_number> must be in the format outlined in the description of the prepare_cik() function.

    Parameters
    ----------
    cik_number: str, required

    Returns
    -------
    URL for all SEC filing submissions for a given company, the company is identified by the CIK Number.
"""
def set_filing_metadata_url(cik_number):
    return const.FILING_SUBMISSIONS_BASE_URL + cik_number + ".json"

"""
    Parameters
    ----------
    ticker: str, required
        The ticker symbol of the stock to be analyzed. This parameter represents the unique identifier for the stock on the exchange, typically consisting
        of a short string of letters (e.g., 'AAPL' for Apple). The ticker is used to fetch relevant data and perform analysis on the corresponding stock.

    ticker_json: dict, required
        A dictionary that maps stock tickers to their respective CIK number and company name.
        This parameter is used to retrieve the CIK number of a stock based on the provided ticker.
    
    Returns
    -------
    Returns the URL where we can access historical SEC filing data for the given ticker.
"""
def get_filings_metadata_url(ticker, tickers_json):
    #metadata = list(filter(lambda x: x["ticker"] == ticker, tickers_json.values()))[0]
    metadata = get_ticker_metadata(ticker = ticker, tickers_json = tickers_json)
    cik_number = metadata['padded_cik_str']

    return set_filing_metadata_url(cik_number=cik_number)

"""
    Retrieves all SEC filing submissions from the SEC API.

    Parameters
    ----------
    ticker: str, required

    tickers_json: str, required

    Returns
    -------
    A dataframe containing all SEC filing submissions
"""
def get_all_filing_submissions(ticker, tickers_json):
    sec_filings_metadata_url = get_filings_metadata_url(ticker=ticker.upper(), tickers_json=tickers_json)

    # Connecting to SEC API
    response = requests.get(sec_filings_metadata_url, headers=const.HTTP_REQUEST_USER_AGENT).json()

    metadata = response['filings']['recent']

    # Dataframe must be transposed to get data to be displayed correctly
    filings_df = pd.DataFrame(metadata.values()).T
    filings_df.columns = metadata.keys()
    
    return filings_df

"""
    Parameters
    ----------
    filings_df: Dataframe, required
        Dataframe of all SEC filing submissions. 

    filed_after_date: date, optional, default = None
        This parameter allows the user to determine how far back they want to look at the SEC filings. Although the filed_after_date parameter is defaulted to None,
        the true default value will be today() - 1 year.

    Returns
    -------
    All SEC filing submissions filed after the filed_after_date parameter.
"""
def get_latest_filings(filings_df, filed_after_date = None):
    if filed_after_date is None:
        filed_after_date = str(date.today() + relativedelta(years = -1))

    #print(filings_df[(filings_df['reportDate'] >= filed_after_date) & filings_df["form"].isin(const.FORMS_OF_INTEREST)])

    return filings_df[(filings_df['filingDate'] >= filed_after_date) & filings_df['form'].isin(const.FORMS_OF_INTEREST)]


def get_single_filing_url(item, cik_number):
    return const.SINGLE_FILING_BASE_URL + str(cik_number) + "/" + item["accessionNumber"].replace("-", "") + "/" + item["primaryDocument"]

"""
    Defines the tags that we want to extract text from in an html document.
"""
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True

"""
    Used for extracting text from html.
"""
def extract_text(content):
    soup = BeautifulSoup(content, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


"""
    Retrieves company facts from SEC API
"""
def get_company_facts(ticker, tickers_json):
    company_facts_url = const.COMPANY_FACTS_BASE_URL + get_cik_number(ticker = ticker.upper(), tickers_json = tickers_json) + ".json"
    print(company_facts_url)

    cf_url_response = requests.get(company_facts_url, headers = const.HTTP_REQUEST_USER_AGENT).json()

    print(cf_url_response['facts']['dei']['EntityPublicFloat']['units'])
    return

"""
    Parameters
    ----------
    ticker: str, required

    Returns
    -------
    A dictionary containing the source and float number for 4 different sources. 
    Here is an example of an item from the dict output: {"source": "Yahoo! Finance", "float": 14,250,000}
"""
def get_float(ticker):
    url = const.FLOAT_TRACKING_BASE_URL + ticker.upper()
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    float_dict = const.FLOAT_DICT
    iteration = 0

    for item in soup.find_all("div", class_="card-body flex-grow-1"):

        float_str = item.find("p").text
        if float_str:
            float_str = float_str.replace("M", "")
            float_dict[iteration]['float'] = float(float_str) * const.FLOAT_CALCULATION_MULTIPLIER
      
        iteration += 1

    return float_dict

"""

"""
def calculate_avg_float(float_dict):
    num_sources = 0
    float_sum = 0.0

    for item in float_dict:
        item_float = float_dict[item]['float']
        if item_float is not None:
            float_sum += item_float
            num_sources += 1
        
    return int(float_sum / num_sources)


def display_float_data(ticker):
    float_dict = get_float(ticker)

    float_df = pd.DataFrame(float_dict.values()).T
    print("Here are the the public float figures for {} gathered from various sources for your reference\n".format(ticker.upper()))
    print(float_df)
    avg_float = calculate_avg_float(float_dict)

    print("\nThe average calculated float for {}, calculated from the figures gathered from all the sources above, is: {:,}".format(ticker.upper(), avg_float))

    return


def display_filings_data(ticker):
    tickers_json = fetch_json_settings(filename = const.FULL_TICKER_DATA_JSON_FILE)
    filings_df = get_all_filing_submissions(ticker, tickers_json)

    latest = get_latest_filings(filings_df = filings_df)
    offerings = latest[latest['form'].isin(["S-1", "S-3"])]

    if offerings.empty:
        print("{} has not filed for any offerings in the past year.".format(ticker))
    else:
        print("Here is a list of the latest offerings by {} with the most recent {} being filed on {}\n".format(ticker.upper(), offerings.iloc[0]['form'], offerings.iloc[0]['filingDate']))
        print(offerings)
        
    return
    

def fetch_latest_filing(ticker):

    tickers_json = fetch_json_settings(filename = const.FULL_TICKER_DATA_JSON_FILE)

    #print("Enter ticker symbol: ")
    # ticker = input()

    sec_filings_metadata_url = get_filings_metadata_url(ticker=ticker.upper(), tickers_json=tickers_json)

    print(sec_filings_metadata_url)

    response = requests.get(sec_filings_metadata_url, headers=const.HTTP_REQUEST_USER_AGENT).json()

    metadata = response['filings']['recent']

    filings_df = pd.DataFrame(metadata.values()).T
    filings_df.columns = metadata.keys()

    filing_url = get_single_filing_url(
        item = filings_df.iloc[0],
        cik_number = get_cik_number(ticker = ticker.upper(), tickers_json = tickers_json, is_padding_necessary = False)
    )

    print(filing_url)

    filing_response = requests.get(filing_url, headers = const.HTTP_REQUEST_USER_AGENT)

    extracted_txt = extract_text(filing_response.content)

    return extract_text(filing_response.content)

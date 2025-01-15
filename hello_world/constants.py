FILING_SUBMISSIONS_BASE_URL = "https://data.sec.gov/submissions/CIK"        # This URL gives us access to all the submitted SEC Filing Submissions for a given company
SINGLE_FILING_BASE_URL = "https://www.sec.gov/Archives/edgar/data/"
FLOAT_TRACKING_BASE_URL = "https://knowthefloat.com/ticker/"
TICKER_DATA_JSON_FILE = "ticker_data.json"
FULL_TICKER_DATA_JSON_FILE = "full_ticker_data.json"
CIK_STR_LENGTH = 10
HTTP_REQUEST_USER_AGENT = {
    'Accept': "application/json",
    #'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    'Cookie': "nmstat=34a0ee2f-92e9-fb6e-9650-c99fbb5b06a0; __utma=27389246.49364516.1722341368.1723550889.1723552957.2; __utmz=27389246.1723552957.2.2.utmcsr=sec.gov|utmccn=(referral)|utmcmd=referral|utmcct=/; _ga_ZC7E8DWE3S=GS1.1.1723552957.2.0.1723552963.0.0.0; _ga_DKBJ584YLP=GS1.1.1723552957.2.0.1723552963.0.0.0; _gid=GA1.2.1606794089.1734348922; _ga=GA1.1.49364516.1722341368; bm_mi=C798211F45E1121FB0F863D8A43ACB19~YAAQEvzaF7wlNruTAQAAWGz20Bo4vzt099jHKiQc7YLFUpfrGI3oEC503vOnQRI5EgY9yRqhVdMyiNL9WaRLntCHMSXPGcl/ruLkMcsDuPlW/bCi1bkp+lmpuDGUxHC1OHg46a19nk7nYM5eEEUp5yoY8Wkrs8ozwmdd2fFSA/gL8FySJ0tzDuHNbYE8lASZrfhKv9ymJTI1ZY4bOBTHWsf+8wn8LKmip+VxDPz/UiykVHXffXjoJ+Hdk8IxTj9C2JoWKHX8URJ88gy8+W21bonD4mkIyxBJohzlczq6WB3fxTLR/SbZqTK8Qe++kmNPsYAlU1mllYy3~1; ak_bmsc=067E0594DCB5C5942370325C8A468154~000000000000000000000000000000~YAAQEvzaF8knNruTAQAA+G/20Br2283g46xlMYgHaJf8f0BBvekdTwREmEiOA7VXxibMslBNvVfQ2CR/gcpkU72CYMf1I4Nt3N3vHcTCu2bw1yr/vglPcjOZNRI19DlhxURrMDHR79QwTTWuCMY4Lwj+0GNvg0zOvVJJG4IjOJXvPQYVTfcIIAFivhmlu6/3LIz4TnRnnTBc8QN5AvIlsWbyCRp4WpZxz0pXTNDzuVOvj9I3nFHrGI0CmVECo7cwbBo3CukCtHE6yKWY+acwRMA7t8QGnY69HAxt3gHOTZHcaBWFASl6dB6138/a9SI1ES+HcrYLmrpv5aNO8WhdQIwpEc2yIzzaGSl0HukTADB+EpgRDcbqhf44FXrGfeqcZFBUKBxS9JXgVxm+n24gwqQLWjAITAk7Wr8A3B+cTTIrr48BikSnVe9wre9M5iwQBzCTcORagbspR2mSFsseMwIoo0vmtQijg5pLQAT0hWMgW68qYBNFkQ3r1A==; _ga_CSLL4ZEK4L=GS1.1.1734377631.55.1.1734377635.0.0.0; _4c_=%7B%22_4c_s_%22%3A%22jZJbj9sgEIX%2FSsRzcMDgC3mrUqnqQ1u16uUxcmBso01sC9jQbZT%2F3iHxZrepKtUvNud8c2YMnEjsYSBrXgkpqqoUFS%2FYkjzAkyfrE3HWpNeRrIkqSwWiBGpaJqnc5YrWWhla7jRjNdStyCuyJD9TlmR5JVVRSinPS2KG5wwHBrzthhvHGSsqiVyNnJ3CDOI0Is8VOoVidywqiX2ObO6zrr6Lt6jZqCtV%2F4kmBdHJ3Xf9J6qnGT0RPRrA9lxlvM4YbT3OEX6hQgVjJKWO5lGHbXiaEhdht%2FDmAQ0DR6thG60JfQooRPmi9mC7Plx2O4WYNBvJswK%2Fox3MGO%2FrZvVWV%2BeJ3bkxeki1m96NB1hwwVEe8UzJj0tFGtdBC85dsD6Eya9Xqxhj5kFn3XhceWic7mlr93boEu9tSL8y%2B7OAN%2BWq0av23SbVbL9uvqD%2B8ZXyefPpwyw9uv1%2FNV2B6RpHm2naW90EOw4U97VzzeGANrVDANc2GvxLm8VfjRevGr97s%2F32%2Fi0upBKlLHiZ8SrPheSirMl5PnMh8UYygS7eghBw1BrX6Tmfz78B%22%7D; _ga_300V1CHKH1=GS1.1.1734377631.53.1.1734377793.0.0.0; bm_sv=D1ED9E4B8A66E85E4D806300E1FDF3B6~YAAQFfwxFxZwp7aTAQAAm2j80BrmA9bhMDWEs8TrCqz0tv3KKTXspF1FnuRYOIxNn0nY7BKwNhnu6AzMvGcz/5c8lEou765fu30q+3nCHr44YHdzOnUGiaFg2TpPOFB8FitJYaADHQu2Cz8rJVItMHIKFYu/TPh/SfEV/cWw9TTGUYpq+8ZXyeheQrlqFpJfSvKdAj1K1FtW4Jq6dh1ZfZJzKb3NtQLoFwhe4BVnKO8H/NX9voEi50fMjXvUOQ==~1",
    'Cache-Control': "max-age=0",
    'Accept-Encoding': "gzip, deflate, br, zstd",
    'Accept-Language': "en-US,en;q=0.9",
    'Sec-Fetch-Dest': "document",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-Site': "none",
    'Sec-Fetch-User': "?1",
    'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Ch-Ua-Mobile': "?0",
    'Upgrade-Insecure-Requests': "1",
    'Priority': "u=0, i"
}
FLOAT_DICT = {
    0: {
        "source": "Yahoo! Finance",
        "float": None,
    },
    1: {
        "source": "Finviz",
        "float": None,
    },
    2: {
        "source": "WSJ",
        "float": None,
    },
    3: {
        "source": "Dilution Tracker",
        "float": None,
    }
}
FORMS_OF_INTEREST = ["S-3", "424B", "8-K", "10-Q", "10-K", "S-1", "3", "4", "5"]
COMPANY_FACTS_BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK"
FLOAT_CALCULATION_MULTIPLIER = 1000000

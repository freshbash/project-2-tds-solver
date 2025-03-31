import json                   # to convert API to json format
from urllib.parse import urlencode, urljoin
import requests               # to get the webpage
from bs4 import BeautifulSoup # to parse the webpage
import pandas as pd
import re                     # regular expression operators
from datetime import datetime
from geopy.geocoders import Nominatim
import os
import tabula

def q4(required_city):
    location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
    'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
    's': required_city,
    'stack': 'aws',
    'locale': 'en',
    'filter': 'international',
    'place-types': 'settlement,airport,district',
    'order': 'importance',
    'a': 'true',
    'format': 'json'
    })

    result = requests.get(location_url).json()

    url = 'https://www.bbc.com/weather/'+result['response']['results']['results'][0]['id']
    response = requests.get(url)

    html = BeautifulSoup(response.content, "html.parser")

    json_response = html.find_all("script", attrs={"type": "application/json"})
    json_data = json.loads(json_response[0].string)

    result = dict()
    for sample in json_data["data"]["forecasts"]:
        issue_date = sample["summary"]["report"]["localDate"]
        ewd = sample["summary"]["report"]["enhancedWeatherDescription"]
        result[issue_date] = ewd

    return json.dumps(result, indent=4)


def q5(location):
    locator = Nominatim(user_agent="myGeocoder")

    # type any address text
    location = locator.geocode(location)
    return max(float(location.raw["boundingbox"][0]), float(location.raw["boundingbox"][1]))

def q9(subject, filter_subject, filter_score, group, file):
    group_range = list(map(int, group.split("-")))
    pages = list(range(group_range[0], group_range[1] + 1))
    dataframes = tabula.read_pdf(file, pages=pages, multiple_tables=True)

    all_data = pd.concat(dataframes, ignore_index=True)

    filtered_students = all_data[all_data[filter_subject] >= int(filter_score)]

    total_subject_marks = int(filtered_students[subject].sum())

    return total_subject_marks

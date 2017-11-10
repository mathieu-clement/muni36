#!/usr/bin/env python3

from bs4 import BeautifulSoup
import datetime
import requests
import sys
import time

def get_html(stop):
    stop=stop[1:]
    url='https://www.nextbus.com/predictor/adaPrediction.jsp?a=sf-muni&r=36&d=36___I_F00&s=' + stop
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Cannot download data from ' + url)
    return r.text


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    minutes = [
                int(td.get_text()) 
                for td in soup.find_all(class_='adapredictMinTD') 
                if 'minutes' not in td.get_text()
              ]
    time_str = [
                    p.get_text()
                    for p in soup.find_all('p')
                    if 'Valid as of' in p.get_text()
                 ][0]
    # "Valid as of 1:12 PM Thursday, November 9"
    base_dt = datetime.datetime.strptime(time_str, 'Valid as of %I:%M %p %A, %B %d')
    base_dt = base_dt.replace(time.localtime().tm_year) # set it to this year
    return (base_dt, minutes)


def to_datetimes(parsed):
    base_dt, minutes = parsed
    return [base_dt + datetime.timedelta(minutes=m) for m in minutes]

minutes = parse(get_html(sys.argv[1]))
print(minutes)
dts = to_datetimes(minutes)
print(dts)

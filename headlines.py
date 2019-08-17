# -*- coding: utf-8 -*-

# openweather: 
# http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=8ce7fcc052d37bc543e82202cd5f47f5
import datetime
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import request
import feedparser
import requests
import json
import urllib.parse

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640',
}

DEFAULTS = {
    'publication': 'bbc',
    'city': 'London,UK',
    'currency_from': 'GBP',
    'currency_to': 'USD',

}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=8ce7fcc052d37bc543e82202cd5f47f5"
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?app_id=a223c611cc7a46508e75de2b70272fe3"


def get_rate(frm, to):
    currencies = ['USD', 'GBP', 'EUR', 'ZAR']
    return 0.9, currencies

@app.route("/bin/<bin>")
def get_bin(bin):
    return dict(code=0, message='Vietcombank') if bin == '123456' else jsonify(dict(code=1, message='BIN not found'))


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

@app.route("/")
def home():
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather (city)

    # get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)
    response = make_response(render_template("home.html",
                                articles=articles,
                                weather=weather,
                                currency_from=currency_from,
                                currency_to=currency_to,
                                rate=rate,
                                currencies=sorted(currencies))
    )
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

    # return render_template("home.html", articles=articles, 
    #                         weather=weather, currency_from=currency_from, 
    #                         currency_to=currency_to, rate=rate)

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

@app.route("/read")
def read_new():
    url = request.args.get('url')
    if url:
        r = requests.get(url)
        return r.content
    else:
        return jsonify({'code': 1, 'message': 'not found'})

@app.route("/testme/<city>")
def get_weather(city):
    api_url = 'http://.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
    city = urllib.parse.quote(city)
    api = api_url.format(city)
    # r = requests.get(api)
    # return r.content
    # parsed = json.loads(data)
    # weather = None 
    # if parsed.get('weather'):
    #     weather = {
    #         "description": parsed['weather'][0]['description'],
    #         "temperature": parsed['main']['temp'],
    #         "city": parsed['name'],
    #     }

    #     return weather
    # else:
    #     return {
    #         "description": "",
    #         "temperature": "",
    #         "city": "",
    #     }
    return {
        "description": "clear sky",
        "temperature": "37",
        "city": "Sai Gon",
        "country": "Vietnam"
    }

if __name__ == "__main__":
    app.run(port=5000, debug=True)

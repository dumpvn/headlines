# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import feedparser
import requests

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640',
}

@app.route("/bin/<bin>")
def get_bin(bin):
    return dict(code=0, message='Vietcombank') if bin == '123456' else jsonify(dict(code=1, message='BIN not found'))

@app.route("/", methods=['GET', 'POST'])
def get_news():
    # query = request.args.get('publication')
    query = request.form.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()

    url = RSS_FEEDS[publication]
    feed = feedparser.parse(url)
    return render_template('home.html', articles=feed['entries'])

@app.route("/read")
def read_new():
    url = request.args.get('url')
    if url:
        r = requests.get(url)
        return r.content
    else:
        return jsonify({'code': 1, 'message': 'not found'})

if __name__ == "__main__":
    app.run(port=5000, debug=True)

# -*- coding: utf-8 -*-

from flask import Flask
import feedparser

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640',
}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_job = feed['entries'][0]
    return """<html>
        <body>
            <h1> Headlines </h1>
            <b>{0}</b> <br/>
            <i>{1}</i> <br/>
            <p>{2}</p> <br/>
        </body>
    </html>""".format(first_job.get("title"), first_job.get("published"),
    first_job.get("summary"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)

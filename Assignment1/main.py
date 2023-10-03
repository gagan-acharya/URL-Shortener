import random
import string
import json
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_urls = {}

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET","POST"])
def short():
    if request.method == "POST":
        long_url = request.form['long_url']
        if long_url in shortened_urls.values():
            print('yes')
            short_url = list(shortened_urls.keys())[list(shortened_urls.values()).index(long_url)]
        else:
            short_url = generate_short_url()
            while short_url in shortened_urls:
                short_url = generate_short_url()
            shortened_urls[short_url] = long_url
        with open("urls.json","w") as file:
            json.dump(shortened_urls, file)
        short_res=f"Shortened URL: {request.url_root}{short_url}"
        return render_template("index.html",res=short_res)
        # return f"Shortened URL: {request.url_root}{short_url}"
    return render_template("index.html")

@app.route("/long", methods=["GET","POST"])
def long():
    if request.method == "POST":
        short_url = request.form['short_url']
        if short_url in shortened_urls.keys():
            print('yes')
            long_url = shortened_urls[short_url]
        else:
            long_url = "URL not found"
        long_res=f"Expanded URL: {long_url}"
        # return f"Expanded URL: {request.url_root}{long_url}"
    return render_template("index.html",res=long_res)


@app.route("/<short_url>/")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404
    
    
if __name__ == "__main__":
    with open("urls.json", "r") as file:
         shortened_urls = json.load(file)     
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from urllib.parse import urlparse
import requests

app = Flask(__name__)

msgs = {
  "success": "Your url has been accepted, thank you!",
  "no_netloc": "It seems this is not a valid url. If this is an error, please contact BD103.",
  "bad_status_code": "The website returned a bad status code (not 200). Please confirm that you can access it.",
  "timeout_error": "The request timed out. Please make sure that this is a valid website. Contact BD103 if this is a mistake.",
  "connection_error": "Could not connect to the server. Please make sure that this is a valid website. Contact BD103 if this is a mistake."
}

@app.route("/")
def index():
  global msgs
  return render_template("index.html", msgs=msgs)

@app.route("/submit", methods=["POST"])
def submit():

  suggested_url = request.form["url"]
  o = urlparse(suggested_url)

  if o.netloc:
    try:
      r = requests.get("https://" + o.netloc)
    except requests.exceptions.Timeout:
      return redirect(url_for("index", msg="timeout_error"))
    except requests.exceptions.ConnectionError:
      return redirect(url_for("index", msg="connection_error"))

    if r.status_code == 200:
      with open(f"suggested/{date.today()}.txt", "at") as f:
        print("https://" + o.netloc, file=f)
      return redirect(url_for("index", msg="success"))
    else:
      return redirect(url_for("index", msg="bad_status_code"))
  else:
    with open("log.txt", "at") as f:
      print(o, file=f)
    return redirect(url_for("index", msg="no_netloc"))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)

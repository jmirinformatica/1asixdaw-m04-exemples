# pip3 install Flask
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # current date and time
    now = datetime.now()
    return render_template("index.html", data=now)

# Necessari per iniciar un servidor de proves
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

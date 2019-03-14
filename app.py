from flask import Flask, redirect, render_template, request, url_for
from scrape import Status

app = Flask(__name__)


@app.route('/')
def index():
    st = Status()
    st.update()
    return render_template("index.html", responses=st.responses)


if __name__ == '__main__':
    app.run()

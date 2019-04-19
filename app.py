from flask import Flask, redirect, render_template, request, url_for
from main import Status
import asyncio

app = Flask(__name__)


@app.route('/')
def index():
    st = Status()
    asyncio.run(st.upd())
    return render_template("index.html", RESPONSES=st.responses)


if __name__ == '__main__':
    app.run()

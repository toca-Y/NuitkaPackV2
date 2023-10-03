import werkzeug

from flask import Flask
import http.server, asyncio

app = Flask(__name__)

import importlib.metadata

print(f"Werkzeug/{importlib.metadata.version('werkzeug')}")


@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'


if __name__ == '__main__':
    """
    Main run
    """
    app.run()

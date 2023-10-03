import requests
import http.cookies
import six

res = requests.get('https://www.baidu.com/')
print(res.status_code, )
print(res.content)
import jinja2.defaults

from flask import Flask
import http.server, asyncio
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'



# import cv2
#
# print(cv2)
# print(cv2.__dir__())
# print(cv2.imread)
# import numpy
#
# a = numpy.array([1, 2, 3])
# print(a)
#
#
# import pandas
#
# a = pandas.Series([1, 2, 3])
#
# print(a)
#

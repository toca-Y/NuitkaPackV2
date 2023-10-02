
import requests
import http.cookies
import six

res = requests.get('https://www.baidu.com/')
print(res.status_code, )
print(res.content)

import numpy

a = numpy.array([1, 2, 3])
print(a)


import pandas

a = pandas.Series([1, 2, 3])

print(a)


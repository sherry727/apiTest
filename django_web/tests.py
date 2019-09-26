# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
#from urllib import request
# import cookielib
#from http import cookiejar

from django.test import TestCase
import requests
url = 'http://192.168.1.235:786/www/index.php?m=bug&f=browse&productID=50&browseType=bySearch&queryID=myQueryID'
cookies = {'sid': 'sid=9gc3ied2beuoa7go45khjk9bfh'}
wb_data = requests.get(url, cookies=cookies)
soup = BeautifulSoup(wb_data.text, 'lxml')
print(soup)
# -*- coding: utf-8 -*-
import requests
import json,csv
import codecs
import pymysql
import logging
import sys;
reload(sys);
sys.setdefaultencoding('utf8')


def execute(url, heads, params, method='POST', cookies=None, files=None):
    r =''
    if method=='POST':
        r=requests.request('post', url=url, headers=heads, json=params, cookies=cookies, files=files)
    elif method=='GET':
        r=requests.request('get', url=url, headers=heads, json=params, cookies=cookies, files=files)
    return r

def _load_json_from_response(self, response):
    try:
        re = json.loads(response)
    except Exception as e:
        raise ValueError('Not a valid JSON\n' + e.message)
    return re

def get_value_from_response(self, response, json_path=''):
    """get value
    """
    if isinstance(response, (str)):
        response = self._load_json_from_response(response)

    if json_path.find('.') > -1:
        key = json_path[0: json_path.index('.')]
        #print(key)
        if isinstance(response, list) and key.isdigit():
            dict1 = response[int(key)]
        elif isinstance(response, dict):
            dict1 = response.get(key)
            #print(dict1)
        else:
            return response
        key1 = json_path[json_path.index('.') + 1:]
        if key1.find('.') > -1:
            return self.get_value_from_response(dict1, key1)
        else:
            if isinstance(dict1, list) and key1.isdigit():
                return dict1[int(key1)]
            elif isinstance(dict1, dict):
                return dict1.get(key1)
            else:
                return dict1
    else:
        if isinstance(response, list) and json_path.isdigit():
            return response[int(json_path)]
        elif isinstance(response, dict):
            return response.get(json_path)
        else:
            return response


def write_csv_file(path, head, data):
    try:
        with open(path, 'wb') as csv_file:
            csv_file.write(codecs.BOM_UTF8)
            writer = csv.writer(csv_file, dialect='excel')
            if head is not None:
                writer.writerow(head)
            for row in data:
                writer.writerow(row)
            csv_file.close()
            print("Write a CSV file to path %s Successful." % path)
            logging.info("Write a CSV file to path %s Successful." % path)
    except Exception as e:
        logging.info("Write an CSV file to path: %s, Case: %s" % (path, e))


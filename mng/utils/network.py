# coding=utf-8
import urllib.request
import requests
import json

import time

from mng.utils.sync import run_in_background


def post_json(json_dict, post_url):
    req = urllib.request.Request(post_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    json_data = json.dumps(json_dict)
    json_byte = json_data.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(json_byte))
    ret = urllib.request.urlopen(req, json_byte)
    ret_str = ret.read().decode()
    print(ret_str)
    return json.loads(ret_str)


def get(url):
    r = requests.get(url)
    print(r.text)


def post(url, json_dict):
    r = requests.post(url, params=json_dict)
    print(r.text)

if __name__ == '__main__':
    # save_record('某活动', '申请人', '10086', 'zuzhi', 2016, 1, 1, 2016, 1, 2, 1, 2, 3, 4)
    # modify_record('某活动', '申请人', '10086', 'zuzhi', 2016, 1, 1, 2016, 1, 3, 1, 2, 3, 4)
    # remove_record('某活动', '10086')
    # get('http://114.215.146.135:8080/oa/record/getRecordByPage.do')
    run_in_background(save_record, 'huod', 'shenqingren', '39380123', 'xgb', 2016, 11, 12, 2016, 11, 13, 2, 3, 4, 5)
    time.sleep(1)

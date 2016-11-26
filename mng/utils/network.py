# coding=utf-8
import urllib.request
import requests
import json


def post_json(json_dict, post_url):
    json_dict = json_dict
    post_url = post_url
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


def save_record(event_name, applicant, phone, org, start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, exhibition):
    start_date = "%d-%02d-%02d" % (start_year, start_month, start_day)
    end_date = "%d-%02d-%02d" % (end_year, end_month, end_day)
    print(start_date)
    print(end_date)
    post('http://114.215.146.135:8080/oa/record/saveRecord.do', {
            "eventName": event_name,
            "header": applicant,
            "phone": phone,
            "Unit": org,
            "startDate": start_date,
            "endDate": end_date,
            "materials": str(desk_num) + "," + str(tent_num) + "," + str(umbrella_num) + "," + str(exhibition)
        })


def remove_record(event_name, phone):
    post('http://114.215.146.135:8080/oa/record/deleteRecord.do', {
        "eventName": event_name,
        "phone": phone
    })


def modify_record(event_name, applicant, phone, org, start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, exhibition):
    remove_record(event_name, phone)
    save_record(event_name, applicant, phone, org, start_year, start_month, start_day, end_year, end_month, end_day, desk_num, tent_num, umbrella_num, exhibition)

if __name__ == '__main__':
    # save_record('某活动', '申请人', '10086', 'zuzhi', 2016, 1, 1, 2016, 1, 2, 1, 2, 3, 4)
    modify_record('某活动', '申请人', '10086', 'zuzhi', 2016, 1, 1, 2016, 1, 3, 1, 2, 3, 4)
    # remove_record('某活动', '10086')
    # get('http://114.215.146.135:8080/oa/record/getRecordByPage.do')

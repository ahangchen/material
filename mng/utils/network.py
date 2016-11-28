import urllib.request
import json


def post_json(json_dict, post_url):
    req = urllib.request.Request(post_url)
    if json_dict != None:
        json_dict = json_dict
        post_url = post_url
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        json_data = json.dumps(json_dict)
        json_byte = json_data.encode('utf-8')  # needs to be bytes
        req.add_header('Content-Length', len(json_byte))
    else:
        ret = urllib.request.urlopen(post_url).read().decode()
    print(ret)
    return json.loads(ret)

if __name__ == '__main__':
    # print(post_json('', 'http://110.64.69.101:8081/team/info/?tid=1'))
    print(post_json(None, 'http://114.215.146.135:8080/oa/record/getRecordByPage.do'))


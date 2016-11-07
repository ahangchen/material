import urllib.request
import json


def post_json(json_dict, post_url):
    json_dict = json_dict
    post_url = post_url
    req = urllib.request.Request(post_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    json_data = json.dumps(json_dict)
    json_byte = json_data.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(json_byte))
    return json.loads(urllib.request.urlopen(req, json_byte).read().decode())

if __name__ == '__main__':
    print(post_json('', 'http://110.64.69.101:8081/team/info/?tid=1'))

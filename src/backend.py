#!/usr/bin/env python3

import json, pip._vendor.requests 

def api_call(classes):
    '''
    input: a list of classes
    output: python data structure from the json
    https://api.umd.io/v1/courses/CMSC421,CMSC422
    '''
    http_request = 'https://api.umd.io/v1/courses/' + ",".join(classes)
    response = pip._vendor.requests.get(http_request)
    json_data = json.loads(response.text)
    # print(json_data)
    return json_data


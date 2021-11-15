#!/usr/bin/env python3

import json, requests 

def api_call(classes):
    '''
    Return the json dump from the api call to umd.io
    Parameters:
    classes (list of strings): list of course ids
    Returns:
    A python data structure representing the json
    '''
    http_request = 'https://api.umd.io/v1/courses/' + ",".join(classes)
    response = requests.get(http_request)
    json_data = json.loads(response.text)
    # print(json_data)
    return json_data



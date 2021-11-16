#!/usr/bin/env python3

import json, requests 

def get_courses(course_list):
    '''
    Return the json dump from the api call to umd.io
    Parameters:
    classes (list of strings): list of course ids
    Returns:
    A python data structure representing the json
    '''
    http_request = 'https://api.umd.io/v1/courses/' + ",".join(course_list)
    response = requests.get(http_request)
    json_data = json.loads(response.text)
    # print(json_data)
    return json_data

def get_sections(course):
    '''
    Return the json dump from the api call to umd.io
    Parameters:
    classes (string): string of course_id
    Returns:
    A python data structure representing the json
    '''
    http_request = 'https://api.umd.io/v1/courses/' + course + '/sections'
    response = requests.get(http_request)
    json_data = json.loads(response.text)
    # print(json_data)
    return json_data

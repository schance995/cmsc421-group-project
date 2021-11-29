#!/usr/bin/env python3

import json
import requests
import requests_cache
from dataclasses import dataclass, field
from typing import List

requests_cache.install_cache('cmsc421_cache')


def get_courses(course_list):
    """
    Return the json dump from the api call to umd.io
    Parameters:
    classes (list of strings): list of course ids
    Returns:
    A python data structure representing the json
    """
    http_request = "https://api.umd.io/v1/courses/" + ",".join(course_list)
    response = requests.get(http_request)
    json_data = json.loads(response.text)
    # print(json_data)

    # Parsing json into class definition
    course_info = list()
    for data in json_data:
        course = CourseItem()
        course.course_id = data["course_id"]
        course.name = data["name"]
        course.dept_id = data["dept_id"]
        course.credits = int(data["credits"])

        section_data = get_sections(data["course_id"])

        for each_section in section_data:
            section = SectionItem()
            section.section_id = each_section["section_id"]
            section.open_seats = each_section["open_seats"]

            section.meetings = list()
            for each_meeting in each_section["meetings"]:
                meeting = Meeting()
                meeting.days = each_meeting["days"]
                meeting.start_time = convert_str_to_int(
                    each_meeting["start_time"])
                meeting.end_time = convert_str_to_int(each_meeting["end_time"])
                section.meetings.append(meeting)

            course.sections.append(section)

        course_info.append(course)

    # replaced return statement
    return course_info


def get_sections(course):
    """
    Return the json dump from the api call to umd.io
    Parameters:
    classes (string): string of course_id
    Returns:
    A python data structure representing the json
    """
    http_request = "https://api.umd.io/v1/courses/" + course + "/sections"
    response = requests.get(http_request)
    json_data = json.loads(response.text)
    # print(json_data)
    return json_data

# def get_course_by_sections
# https://api.umd.io/v1/courses/{course_ids}/sections/{section_ids}


def convert_str_to_int(str):
    # convert string time to int time so that we can sort the schedule by time

    time = 0
    idx_colon = str.find(":")
    hours = int(str[:idx_colon])
    idx_m = str.find("m")
    minutes = int(str[idx_colon+1: idx_m-1])

    if hours == 12:
        hours = 0
    if "pm" in str:
        hours += 12

    time += hours*60
    time += minutes

    return time

# class for meeting info of a section


@dataclass
class Meeting:
    days: str = ""
    start_time: int = 0
    end_time: int = 0

# class for section info of a course


@dataclass
class SectionItem:
    section_id: str = ""
    open_seats: str = ""
    meetings: List[Meeting] = field(default_factory=list)

# class for course info


@dataclass
class CourseItem:
    course_id: str = ""
    name: str = ""
    dept_id: str = ""
    credits: int = 0
    sections: List[SectionItem] = field(default_factory=list)

    def __repr__(self):
        return '{} ({}) [{}]'.format(self.course_id, self.name, ', '.join([s.section_id.split('-')[1] for s in self.sections]))

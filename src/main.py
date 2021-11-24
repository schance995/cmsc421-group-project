#!/usr/bin/env python3

import sys
import re
from backend import get_courses

def find_indices(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]

def main():
    print('Type up to 7 classes (space or newline separated) (optionally with section number) and press Ctrl-D when you are done)')
    classes = []
    classes_with_section = {}

    # regex match
    p = re.compile(r'(?P<course>[A-Z]{4}[0-9]{3}[A-Z]?)(?P<section>-[0-9]{4})?')
    for s in sys.stdin.read().split():
        match = p.match(s.upper())
        if match:
            if match.group('section'):
                classes_with_section.setdefault(match.group('course'), []).append(match.group('section'))
            classes.append(match.group('course'))
        else:
            print(s, 'did not match format, skipping')

    if len(classes) > 7:
        print('Enter 7 or fewer classes')
        exit(1)
    elif len(classes) == 0:
        print('Enter at least 1 class')
        exit(1)

    schedule = get_courses(classes)
    for course_id, sections in classes_with_section.items():
        # collect all sections as a set
        sections = set(s[1:] for s in sections)
        # find where the course is located in the schedule
        course_id_index = find_indices(schedule, lambda course_item: course_item.course_id == course_id)[0]
        # select sections that the user specified
        schedule[course_id_index].sections = [i for i in schedule[course_id_index].sections if i.section_id.split('-')[1] in sections]
    # TODO: run GA
    print('Your schedule is:')
    print(*schedule, sep='\n')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys
import re
from backend import get_courses
from ga import sga
from dateutil import parser

def find_indices(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]

# MTuWThF(8:00AM-12:00AM)

def main():
    print('Type up to 7 classes (space or newline separated) (optionally with section number) and press Ctrl-D when you are done)')
    print('You can also type in times to exclude following this format: MTuWThF@11AM-12PM')
    # the date format can be flexible because of dateutil parser
    print('Classes are not case sensitive, time exclusions are.')
    classes = []
    classes_with_section = {}
    days_dict = dict()
    days_dict["M"] = []
    days_dict["Tu"] = []
    days_dict["W"] = []
    days_dict["Th"] = []
    days_dict["F"] = []

    # regex match
    p = re.compile(r'(?P<course>[A-Z]{4}[0-9]{3}[A-Z]?)(?P<section>-[0-9]{4})?')
    timepattern = re.compile('(?P<days>(M|Tu|W|Th|F)+)@(?P<start>.+)-(?P<end>.+)')
    for s in sys.stdin.read().split():
        match = p.match(s.upper())
        if match:
            if match.group('section'):
                classes_with_section.setdefault(match.group('course'), []).append(match.group('section'))
            classes.append(match.group('course'))
        else:
            match = timepattern.match(s)
            if match:
                # regex handles days correctly, just split by uppercase letter
                days = set(re.findall('[A-Z][^A-Z]*', match.group('days')))
                start = parser.parse(match.group('start')).time()
                t = str(start).split(':')
                # convert start time into minutes
                start_total_minutes = int(t[0])*60+int(t[1])*1 
                end = parser.parse(match.group('end')).time()
                t = str(end).split(':')
                # convert end time into minutes
                end_total_minutes = int(t[0])*60+int(t[1])*1 
                if end < start:
                    print('End time should be after start time')
                    exit(1)
                for day in days:
                    days_dict[day].append([start_total_minutes, end_total_minutes])
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

    # print(schedule, days_dict)
    # runs genetic_algorithm
    genetic_algorithm = sga(schedule, days_dict)
    best_score, best_batch_schedule,best_batch_schedule_decoded = genetic_algorithm.runGA()

    print('--------------------')
#    print(f'Overall best fitness score is: {best_score}')
#    print(f'Your schedules are:\n {best_batch_schedule}')
#    print(f'Your schedules are (with section_id):\n {best_batch_schedule_decoded}')
    print('Your schedules are (with section_id):')
    for schedule in best_batch_schedule_decoded:
        #  for s in schedule:
            #  parts = s.split('-')
            #  print(f'{parts[0]}({parts[1]})', end=' ')
        print(*[s.split('-')[0] + '(' + s.split('-')[1] + ')' for s in schedule])

if __name__ == '__main__':
    main()

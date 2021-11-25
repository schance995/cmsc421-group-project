#!/usr/bin/env python3

import sys
from backend import get_courses
from ga import sga

def main():
    print('Type up to 7 classes (space or newline separated) and press Ctrl-D when you are done)')
    classes = [s.upper() for s in sys.stdin.read().split()]
    if len(classes) > 7:
        print('Enter 7 or fewer classes')
        exit(1)
    print('Your classes are')
    print(*classes)
    schedule = get_courses(classes)
    # print(f'Your schedule is:{schedule}')
    genetic_algorithm = sga(schedule)
    best_score, best_batch_schedule = genetic_algorithm.runGA()
    print('--------------------')
    print(f'Overall best fitness score is: {best_score}')
    print(f'Your schedules are:\n {best_batch_schedule}')


if __name__ == '__main__':
    main()

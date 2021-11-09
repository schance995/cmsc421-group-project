#!/usr/bin/env python3

import sys
from backend import api_call
from ga import runGA

def main():
    print('Type up to 7 classes (space or newline separated) and press Ctrl-D when you are done)')
    classes = [s.upper() for s in sys.stdin.read().split()]
    if len(classes) > 7:
        print('Enter 7 or fewer classes')
        exit(1)
    print('Your classes are')
    print(*classes)
    schedule = runGA(api_call(classes))
    print('Your schedule is:')
    print(schedule)

if __name__ == '__main__':
    main()

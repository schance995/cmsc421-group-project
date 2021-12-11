# cmsc421-group-project

A genetic algorithm to create class schedules.

## Running the program

Type in classes in the format as described in `src/test_input.txt`

To exclude times at certain days (eg avoid classes from 8 to 9 am), type in:

MTuWThF@8am-9am

You can also feed classes through standard input:

`python3 main.py < test_input.txt`

Or run the script

`sh src/test.sh`

A graph of the fitness function is generated in `src/graphs`.

## IMPORTANT

The requests-cache dependency is used to avoid hammering umd.io excessively.

Make sure you run the program from the same directory every time to take advantage of the cache.

## Read the fantastic manuals!

in the `docs` folder

## Read the fantastic source code!

in the `src` folder


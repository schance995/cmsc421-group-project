# Documentation 

## Backend 

1. The `inputs` will be a list of course names that the user wants to make a schedule for 
2. The `output` will be a json dump https://docs.python.org/3/library/json.html containing all the sections for each of the courses selected by the user. 

## Algorithm 

1. The `input` will be json dump from backend 
2. The `output` will be json string representing different schedules that are produced at the end of GA
3. In the init function:
    * create the initial population of chromosome 
        * A `chromosome` is represented using whole numbers. The length of chromosome is the number of courses that the user wants to take. The numbers in chromosome present section number. For ex: If the user wants to take CMSC421, CMSC424, ENGL393 then a chromosome would be like [1 2 5] where element at index 0 is representing CMSC421 section 1, element at index 1 is representing CMSC424 section 2, and element at index 2 is representing ENGL393 section 5. The information about the section numbers will be present in json dump from backend. 
4. Fitness function
* The fitness function will be decided later on. 
5. Crossover 
* To do a `crossover`, we take two chromosomes and randomly find the crossover point. We switch the section numbers to the left of the crossover point. For ex, chromosome A = [1 2 5] and chromosome B = [2 1 3] and crossover point is 1 (there are two options since length is 3), we get A = [2 2 5] and B = [1 1 3] 
6. Mutation 
* To do a `mutation`, randomly pick a course to mutate on and change it's section number if it has more than 1 sections. For ex, A = [1 2 5] and we randomly pick to mutate on CMSC424 (there are three options to mutate on since three courses), let's say there are 3 different sections of CMSC424 then we will randomly pick either section 1 or section 3. So, A = [1 3 5] 
7. Monitor the average fitness like we did with the ant project 





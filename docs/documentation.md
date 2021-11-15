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
* To do a `mutation`, randomly pick a section out of all the possible sections of each course to mutate on. For ex, A = [1, 2], where there are two courses selected by the user CMSC421 and CMSC422. If CMSC421 and CMSC422 have 2 sections each, we pick one section out of total 4 sections to mutate on. 
7. Monitor the average fitness like we did with the ant project 





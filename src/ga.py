# Simple Genetic Algorithm
# source: https://www.cs.umd.edu/~reggia/cmsc421/papers/SGA.py

from numpy.core.fromnumeric import shape
import matplotlib.pyplot as plt
import numpy as np
from config import config as cfg
import pathlib

class sga:

    # note:   Population > Group > Chromosome
    def __init__(self, course_list, graph_dir="graph"):
        # stringLength: int, popSize: int, nGens: int,
        # prob. mutation pm: float; prob. crossover pc: float

        # the size of population, group
        self.pop_size = cfg['population_size']
        self.group_size = cfg["group_size"]
        # pop_size must be even
        if np.mod(self.pop_size, 2) == 0:           
            self.pop_size = self.pop_size
        else:
            self.pop_size = self.pop_size+1
        # probability of mutation
        self.pm = cfg['prob_mutation']
        # probability of crossover                      
        self.pc = cfg['prob_crossover']
        # max number of generations                       
        self.num_gens = cfg['num_gens']
        # get the course list    
        self.course_list = course_list
        # set the length of each string
        self.string_length = len(self.course_list) 
        # get the size of each section
        self.section_length = self.get_all_section_length()
        # get the output directory of graph and if it doesn't exist, create one.
        self.graph_output = pathlib.Path(graph_dir)
        self.graph_output.mkdir(parents=True, exist_ok=True)

        # population initialization
        self.pop = self.init_population()


    # compute population fitness values
    # TODO
    def fitness_function(self, pop):          
        # fitness is currently the sum of chromosome
        fitness = np.sum(np.sum(pop, axis = -1), -1)
        return fitness

    # extract section information from course list
    def get_all_sections(self):
        section_list = [course.sections for course in self.course_list]
        return section_list

    # get the length of all courses
    def get_all_section_length(self):
        sections = self.get_all_sections()
        return [len(course) for course in sections]

    # initialize the a chromosome by randomly select sections from section list
    def init_chrom(self):
        return [np.random.randint(section) for section in self.section_length]

    # initialize the population by repeatedly call init_chrom to the size of population
    def init_population(self):
        init_pop = [[self.init_chrom() for chrom in range(self.group_size)] for group in range(self.pop_size)]
        # initialize records
        # fitness values for initial population
        fitness = self.fitness_function(init_pop)
        # current best fitness of the first group
        self.best_fit_group_score = max(fitness)
        best_loc = np.argwhere(fitness == self.best_fit_group_score)[0][0]
        # group with the best fitness      
        self.best_fit_group = init_pop[best_loc]   
        # array of max fitness vals each generation
        self.bestfitarray = np.zeros(self.num_gens + 1)
        self.bestfitarray[0] = self.best_fit_group_score  # (+ 1 for init pop plus nGens)
        # array of mean fitness vals each generation
        self.meanfitarray = np.zeros(self.num_gens + 1)
        self.meanfitarray[0] = fitness.mean()
        
        self.overall_best_score = self.best_fit_group_score
        self.overall_best_group = self.best_fit_group
        return init_pop

    # conduct tournaments to select two offspring
    def tournament(self, pop, fitness, popsize):  # fitness array, pop size
        # select first parent par1
        cand1 = np.random.randint(popsize)      # candidate 1, 1st tourn., int
        cand2 = cand1                           # candidate 2, 1st tourn., int
        while cand2 == cand1:                   # until cand2 differs
            cand2 = np.random.randint(popsize)  # identify a second candidate
        if fitness[cand1] > fitness[cand2]:     # if cand1 more fit than cand2
            par1 = cand1  # then first parent is cand1
        else:  # else first parent is cand2
            par1 = cand2
        # select second parent par2
        cand1 = np.random.randint(popsize)      # candidate 1, 2nd tourn., int
        cand2 = cand1                           # candidate 2, 2nd tourn., int
        while cand2 == cand1:                   # until cand2 differs
            cand2 = np.random.randint(popsize)  # identify a second candidate
        if fitness[cand1] > fitness[cand2]:     # if cand1 more fit than cand2
            par2 = cand1  # then 2nd parent par2 is cand1
        else:  # else 2nd parent par2 is cand2
            par2 = cand2
        return par1, par2

    # single point crossover: we consider each group as a large "chromosome". i.e. Apply crossover on group.
    def xover(self, group1, group2):
        group1, group2 = (np.array(group1),np.array(group2))  
        shape_of_group = group1.shape
        group1, group2 = group1.flatten(), group2.flatten()
        # cut locn to right of position (hence subtract 1)
        locn = np.random.randint(0, len(group1) - 1)
        tmp = np.copy(group1)       # save child1 copy, then do crossover
        # crossover the segment before the point
        group1[:locn+1] = group2[:locn+1]
        group2[:locn+1] = tmp[:locn+1]
        group1, group2 = np.reshape(group1, shape_of_group), np.reshape(group2, shape_of_group)
        return group1, group2
    
    # Consider all chromosome in a group as a huge chromosome. i.e. Apply bitwise mutation on group.
    def mutate(self, pop, section_list):            
        mutate_rand_map = np.random.rand(*pop.shape)
        mutate_location = np.where(mutate_rand_map < self.pm)
        for x, y, z in zip(mutate_location[0], mutate_location[1], mutate_location[2]):
            my_list = list(range(section_list[z]))
            my_list.remove(pop[x, y, z])
            if len(my_list) != 0:
                pop[x, y, z] = np.random.choice(my_list)
        return pop

    # program driver: runs the genetic algorithm
    def runGA(self):    
        # process generation by generation
        for gen in range(self.num_gens):  
            # Compute fitness of the pop
            fitness = self.fitness_function(self.pop)  # measure fitness
            # initialize new population
            newPop = np.zeros((self.pop_size, self.group_size, self.string_length), dtype='int64')
            # create new population newPop via selection and crossovers with prob pc
            # create popSize/2 pairs of offspring
            for pair in range(0, self.pop_size, 2):
                # tournament selection of two parent indices
                p1, p2 = self.tournament(self.pop, fitness, self.pop_size)  # p1, p2 integers
                group1 = np.copy(self.pop[p1])       
                group2 = np.copy(self.pop[p2])      
                if np.random.rand() < self.pc:               
                    group1, group2 = self.xover(group1, group2)  
                # add offspring to newPop
                newPop[pair, :] = group1
                newPop[pair + 1, :] = group2
            # mutations to population with probability pm
            new_pop = self.mutate(newPop, self.section_length)
            self.pop = new_pop
            new_fitness = self.fitness_function(self.pop)    # fitness values for new population
            self.best_fit_group_score = max(new_fitness)
            best_loc = np.argwhere(new_fitness == self.best_fit_group_score)[0][0]
            # save best fitness for plotting
            self.bestfitarray[gen + 1] = self.best_fit_group_score
            # save mean fitness for plotting
            self.meanfitarray[gen + 1] = fitness.mean()

            if self.best_fit_group_score > self.overall_best_score:
                self.overall_best_score = self.best_fit_group_score 
                self.overall_best_group = self.best_fit_group
            if (np.mod(gen, 10) == 0):            # print epoch, max fitness
                print("generation: ", gen+1, "max fitness: ", self.best_fit_group_score)
        # save graph
        print(f'Saving Graph')
        x = np.arange(self.num_gens + 1)
        # print(f'shape of x: {x.shape}')
        # print(f'shape of best array: {self.bestfitarray.shape}')
        # print(f'shape of average array:{self.meanfitarray.shape}')
        plt.title(f'Best Fitness and Mean Fitness Score VS Epochs ')
        plt.plot(x, self.bestfitarray, label = 'Best Fitness Score')
        plt.plot(x, self.meanfitarray, label = 'Average Fitness Score')
        plt.xlabel('Epoch Number')
        plt.ylabel('Fitness Score')
        plt.legend()
        plt.savefig(self.graph_output/(f'pop-size={self.pop_size}_group-size={self.group_size}_pm={self.pm}_pc={self.pc}.jpg'))
        return self.overall_best_score, self.overall_best_group


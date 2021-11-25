# Simple Genetic Algorithm
# source: https://www.cs.umd.edu/~reggia/cmsc421/papers/SGA.py

import pylab as pl
import numpy as np
from config import config as cfg

class sga:

    def __init__(self):
        # stringLength: int, popSize: int, nGens: int,
        # prob. mutation pm: float; prob. crossover pc: float

        # open, initialize output file
        fid = open("results.txt", "w")        
        self.fid = fid
        # number of bits in a chromosome
        self.stringLength = cfg['string_length']   
        self.pop_size = cfg['population_size']
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
        self.pop = np.random.rand(self.popSize, self.stringLength)
        # create initial pop
        self.pop = np.where(self.pop < 0.5, 1, 0)  
        # fitness values for initial population
        fitness = self.fitFcn(self.pop)
        self.bestfit = fitness.max()       # fitness of (first) most fit chromosome
        self.bestloc = np.where(fitness == self.bestfit)[
            0][0]  # most fit chromosome locn
        self.bestchrome = self.pop[self.bestloc,
                                   :]              # most fit chromosome
        # array of max fitness vals each generation
        self.bestfitarray = np.zeros(self.nGens + 1)
        self.bestfitarray[0] = self.bestfit  # (+ 1 for init pop plus nGens)
        # array of mean fitness vals each generation
        self.meanfitarray = np.zeros(self.nGens + 1)
        self.meanfitarray[0] = fitness.mean()
        fid.write("popSize: {}  nGens: {}  pm: {}  pc: {}\n".format(
            self.pop_size, self.num_gens, self.pm, self.pc))
        fid.write("initial population, fitnesses: (up to 1st 100 chromosomes)\n")
        for c in range(min(100, self.pop_size)):   # for each of first 100 chromosomes
            fid.write("  {}  {}\n".format(self.pop[c, :], fitness[c]))
        fid.write("Best initially:\n  {} at locn {}, fitness = {}\n".format(
            self.bestchrome, self.bestloc, self.bestfit))

    # example fitness function   *** Must be modified for an application problem ***
    def fitFcn(self, pop):          # compute population fitness values
        # fitness is currently the number of 1's in chromosome
        fitness = sum(pop.T)
        return fitness

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

    def xover(self, child1, child2):    # single point crossover
        # cut locn to right of position (hence subtract 1)
        locn = np.random.randint(0, self.stringLength - 1)
        tmp = np.copy(child1)       # save child1 copy, then do crossover
        # crossover the segment before the point
        child1[:locn+1] = child2[:locn+1]
        child2[:locn+1] = tmp[:locn+1]
        return child1, child2

    def mutate(self, pop, section_list):            # bitwise point mutations
        whereMutate = np.random.rand(np.shape(pop)[0], np.shape(pop)[1])
        whereMutate = np.where(whereMutate < self.pm)
        for x, y in zip(whereMutate[0], whereMutate[1]):
            my_list = list(range(1,section_list[y]+1))
            my_list.remove(pop[x, y])
            pop[x, y] = np.random.choice(my_list)
        return pop

    def runGA(self):     # run simple genetic algorithme
        fid = self.fid   # output file
        for gen in range(self.nGens):  # for each generation gen
            # Compute fitness of the pop
            fitness = self.fitFcn(self.pop)  # measure fitness
            # initialize new population
            newPop = np.zeros((self.popSize, self.stringLength), dtype='int64')
            # create new population newPop via selection and crossovers with prob pc
            # create popSize/2 pairs of offspring
            for pair in range(0, self.popSize, 2):
                # tournament selection of two parent indices
                p1, p2 = self.tournament(
                    self.pop, fitness, self.popSize)  # p1, p2 integers
                child1 = np.copy(self.pop[p1, :])       # child1 for newPop
                child2 = np.copy(self.pop[p2, :])       # child2 for newPop
                if np.random.rand() < self.pc:                 # with prob self.pc
                    child1, child2 = self.xover(child1, child2)  # do crossover
                # add offspring to newPop
                newPop[pair, :] = child1
                newPop[pair + 1, :] = child2
            # mutations to population with probability pm
            newPop = self.mutate(newPop)
            self.pop = newPop
            fitness = self.fitFcn(self.pop)    # fitness values for population
            self.bestfit = fitness.max()       # fitness of (first) most fit chromosome
            # save best fitness for plotting
            self.bestfitarray[gen + 1] = self.bestfit
            # save mean fitness for plotting
            self.meanfitarray[gen + 1] = fitness.mean()
            self.bestloc = np.where(fitness == self.bestfit)[
                0][0]  # most fit chromosome locn
            self.bestchrome = self.pop[self.bestloc,
                                       :]              # most fit chromosome
            if (np.mod(gen, 10) == 0):            # print epoch, max fitness
                print("generation: ", gen+1, "max fitness: ", self.bestfit)
        fid.write("\nfinal population, fitnesses: (up to 1st 100 chromosomes)\n")
        fitness = self.fitFcn(self.pop)         # compute population fitnesses
        self.bestfit = fitness.max()            # fitness of (first) most fit chromosome
        self.bestloc = np.where(fitness == self.bestfit)[
            0][0]  # most fit chromosome locn
        self.bestchrome = self.pop[self.bestloc,
                                   :]              # most fit chromosome
        for c in range(min(100, self.popSize)):  # for each of first 100 chromosomes
            fid.write("  {}  {}\n".format(self.pop[c, :], fitness[c]))
        fid.write("Best:\n  {} at locn {}, fitness: {}\n\n".format(
            self.bestchrome, self.bestloc, self.bestfit))
        fid.close()
        pl.ion()      # activate interactive plotting
        pl.xlabel("Generation")
        pl.ylabel("Fitness of Best, Mean Chromosome")
        pl.plot(self.bestfitarray, 'kx-', self.meanfitarray, 'kx--')
        pl.show()
        pl.pause(0)

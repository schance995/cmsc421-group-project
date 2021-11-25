import numpy as np
from numpy.lib.function_base import _parse_input_dimensions

pop = np.array([
        [1,3,5,1,2],
        [1,1,1,1,1]])
section_list =[2,3,5,3,4]
child1 = [1,2,3,4,5]
child2 = [4,5,6,7,8]



def mutate_single_chrom(pop, section_list):
    whereMutate = np.random.rand(np.shape(pop)[0], np.shape(pop)[1])
    whereMutate = np.where(whereMutate < 0.5)
    for x, y in zip(whereMutate[0], whereMutate[1]):
        my_list = list(range(1,section_list[y]+1))
        my_list.remove(pop[x, y])
        pop[x, y] = np.random.choice(my_list)
    return pop

def xover(child1, child2):    # single point crossover
    # cut locn to right of position (hence subtract 1)
    locn = 5#np.random.randint(0, 5 - 1)
    print(f'random loc:{locn}')
    tmp = np.copy(child1)       # save child1 copy, then do crossover
    # crossover the segment before the point
    child1[:locn+1] = child2[:locn+1]
    child2[:locn+1] = tmp[:locn+1]
    return child1, child2


if __name__ == "__main__":
    print(mutate_single_chrom(pop, section_list))
    print(xover(child1, child2))
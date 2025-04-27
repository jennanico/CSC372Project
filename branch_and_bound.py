import sys
from copy import copy
from bisect import insort
import math

class BinPackSolver():
    def __init__(self, weight_limit: int, items: list):
        self.weight_limit = weight_limit
        self.items = items

    ## might be able to do a better initial bound
    def get_root(self):
        bins = [[0]]
        return BinPackTN(bins,1,1,len(self.items),self)
    
    ##updated
    def find_solution(self):
        PQ: list[BinPackTN] = [self.get_root()]
        best_node = PQ[0]

        while PQ != []:
            most_promising = PQ.pop()
            for child in most_promising.get_children():
                if child.has_better_value(best_node):
                    cp_bins = child.bins.copy()
                    cp_item_to_add = child.item_to_add
                    cp_bins_used = child.bins_used
                    cp_bound = child.bound
                    best_node = BinPackTN(cp_bins,
                                          cp_item_to_add,
                                          cp_bins_used,
                                          cp_bound,
                                          child.solver)
                if child.might_be_better_than(best_node):
                    insort(PQ, child)
        return best_node

class BinPackTN():
    def __init__(self,
                 bins: list,
                 item_to_add: int,
                 bins_used: int,
                 bound: int,
                 solver: BinPackSolver):
        self.bins = bins
        self.item_to_add = item_to_add
        self.bins_used = bins_used
        self.bound = bound
        self.solver = solver
    ##
    def compute_bound(self):
        bins = 0
        ##greedyly fill remaining bins and return final number of bins
        return math.ceil(bins / 1.5)
    
    ## updated
    def might_be_better_than(self, other):
        return self.bound >= other.bins_used
    
    ## updated
    def has_better_value(self, other):
        return (self.bound <= other.bound and 
                self.item_to_add == len(self.solver.items))
    
    ## updated
    def __lt__(self, other):
        return self.might_be_better_than(other)
    
    ## updated
    def get_children(self):
        if self.item_to_add == len(self.solver.items):
            return []
        children = []
        for bin in range(len(self.bins)):
            ##if item fits add to bin - stops us from creating invalid nodes
            if (self.solver.item[self.item_to_add]) + self.bin_capasity(bin) <= self.solver.weight_limit:
                new_bins = self.bins.copy()
                new_bins[bin].append(self.item_to_add)
                child = BinPackTN(new_bins,
                                  self.item_to_add + 1,
                                  self.bins_used,
                                  0,
                                  self.solver)
                child.bound = child.compute_bound()
                children.append(child)
        new_bins = self.bins.copy()
        new_bins.append([])
        new_bins[len(self.bins)].append(self.item_to_add)
        child = BinPackTN(new_bins,
                          self.item_to_add + 1,
                          self.bins_used + 1,
                          0,
                          self.solver)
        child.bound = child.compute_bound()
        children.append(child)
        return children
    
    ##might not need this - just depends on how we want to represent the bins
    def bin_capasity(self, bin):
        total_weight = 0
        for item in self.bins[bin]:
            total_weight = total_weight + self.solver.items[item]
        return total_weight
##
def main():
    input_values = sys.argv[1]
    file_input = open(input_values,'r')
    with open(input_values, 'r') as file:
        input_lines = file.readlines()
    weight_limit = input_lines[0]
    items = input_lines[2:]
    file_input.close()
    BinPack = BinPackSolver(weight_limit, items)
    best_sol = BinPack.find_solution()

    print(best_sol.bins_used)
    for bin in best_sol.bins:
        print (bin)
          
if __name__ == "__main__":
    main()
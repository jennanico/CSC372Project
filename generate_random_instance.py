'''
Creates a random instance file for the bin packing problem.

Usage:
    generate_random_instance.py [amount_items] [max_weight] [output_file] [method]

    [method] options:
       - uniform --> generates uniformly weighted items in range (1, max_weight)
       - likelihood --> generates with weighted likelihoods:
          -  likelihood_heavy : items on heavier side 25% more likely
          -  likelihood_light : items on lighter side 25% more likely
          -  likelihood_average : items toward the mean weight 25% more likely
    
    Example usage:
        python generate_random_instance.py 20 50 output.txt likelihood_average

'''

# Imports
import argparse
import numpy
import random
import math


'''
Uniform random generation of amount_items.
'''
def uniform_random(amount_items, max_weight, output_file):
    random_weights = numpy.random.randint(1, max_weight+1, amount_items) # randint() method is uniform
    numpy.savetxt(output_file, random_weights, fmt='%d')


'''
Weighted random generation; either likelihood_heavy, likelihood_light or likelihood_average.
'''
def likelihood_random(amount_items, max_weight, output_file, method):

    if (method == "likelihood_heavy") or (method == "likelihood_light"): # Method likelihood_heavy
                                                                         # or likelihood_light
        range_1 = (1, math.floor(max_weight / 2))
        range_2 = (math.floor(max_weight / 2) + 1, max_weight)

        ranges = [1, 2]
        weights = []

        if method == "likelihood_heavy":
            weights = [0.25, 0.75]
        elif method == "likelihood_light":
            weights = [0.75, 0.25]

        random_weights = []
        for i in range(0, amount_items):
            selection = random.choices(ranges, weights=weights, k=1)    # Determine range to select from,
            if selection == [1]:                                        # then generate from range
                random_weight = numpy.random.randint(range_1[0], range_1[1]+1)
            else:
                random_weight = numpy.random.randint(range_2[0], range_2[1]+1)
            
            random_weights.append(random_weight)

        numpy.savetxt(output_file, random_weights, fmt='%d')
    
    else:   # Method likelihood_average

        mean_weight = math.floor(max_weight / 2)

        mean_range = (math.floor(mean_weight - mean_weight / 4), math.floor(mean_weight + mean_weight / 4))

        ranges = [1, 2, 3]
        weights = [0.25, 0.50, 0.25]

        random_weights = []
        for i in range(0, amount_items):
            selection = random.choices(ranges, weights=weights, k=1)    # Determine range to select from,
            if selection == [1]:                                        # then generate from range
                random_weight = numpy.random.randint(1, mean_range[0]-1)
            elif selection == [2]:
                random_weight = numpy.random.randint(mean_range[0], mean_range[1]+1)
            else:
                random_weight = numpy.random.randint(mean_range[1]+1, max_weight)

            random_weights.append(random_weight)

        numpy.savetxt(output_file, random_weights, fmt='%d')    # Write to file


'''
Main; arguments, checks and setup.
'''
def main():
    # Accept arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("amount_items")
    parser.add_argument("max_weight")
    parser.add_argument("output_file")
    parser.add_argument("method")
    args = parser.parse_args()

    valid_methods = ["uniform", "likelihood_heavy", "likelihood_light", "likelihood_average"]

    # Check valid arguments
    if int(args.amount_items) < 0:
        print("Invalid Argument -- amount_items must be more than 0.")
        return
    if int(args.max_weight) < 0:
        print("Invalid Argument -- max_weight must be more than 0.")
        return
    if args.method not in valid_methods:
        print("Invalid Argument -- method must be uniform, likelihood_heavy, likelihood_light, or likelihood_average.")
        return
    
    amount_items = int(args.amount_items)
    max_weight = int(args.max_weight)
    output_file = args.output_file
    method = args.method

    if method == "uniform":
        uniform_random(amount_items, max_weight, output_file)
    else:
        likelihood_random(amount_items, max_weight, output_file, method)


if __name__ == "__main__":
    main()
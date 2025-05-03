import time
import greedy
import branch_and_bound
import backtrack

def main():
    weight_limit = 100

    files = ["dummy_input2.txt"]

    greedy_times = []
    bnb_times = []
    back_times = []

    for file in files:
        #Greedy Run time
        items = greedy.read_file(file)

        start_time = time.perf_counter() #Start

        items.sort(reverse=True)
        bins = [[]]
        greedy.compute_greedy(bins, 0, items, weight_limit)

        end_time = time.perf_counter() #End

        execution_time = end_time - start_time
        greedy_times.append(execution_time)


        #Branch and Bound Run time
        items = greedy.read_file(file)

        start_time = time.perf_counter() #Start

        items.sort(reverse=True)
        BinPack = branch_and_bound.BinPackSolver(weight_limit, items)
        best_sol = BinPack.find_solution()

        end_time = time.perf_counter() #End

        execution_time = end_time - start_time
        bnb_times.append(execution_time)


        #Backtrack Run time
        items = greedy.read_file(file)

        start_time = time.perf_counter() #Start

        items.sort(reverse=True)
        BinPack = backtrack.BinPackSolver(weight_limit, items)
        best_sol = BinPack.find_solution()

        end_time = time.perf_counter() #End

        execution_time = end_time - start_time
        back_times.append(execution_time)


    print(greedy_times)
    print(bnb_times)
    print(back_times)


if __name__ == "__main__":
    main()
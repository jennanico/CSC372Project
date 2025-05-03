import time
import greedy
import branch_and_bound
import backtrack

def main():
    weight_limit = 100

    files = ["dummy_input2.txt"]

    bnb_times = []

    for file in files:
        #Branch and Bound Run time
        items = greedy.read_file(file)

        start_time = time.perf_counter() #Start

        items.sort(reverse=True)
        BinPack = branch_and_bound.BinPackSolver(weight_limit, items)
        best_sol = BinPack.find_solution()

        end_time = time.perf_counter() #End

        execution_time = end_time - start_time
        bnb_times.append(execution_time)
        print(execution_time)

    print(bnb_times)


if __name__ == "__main__":
    main()
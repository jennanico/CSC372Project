import sys


def compute_greedy(bins, start_index, items, weight_limit):
    
    for i in range(start_index, len(items)):
        was_packed = False
        for b in bins:
            if(get_bin_weight(b, items) + items[i] <= weight_limit):
                b.append(i)
                was_packed = True
                break
        if not was_packed:
            bins.append([i])

    return len(bins), bins          


'''
Calculates the current weight of the bin
'''
def get_bin_weight(b, items):
    s = 0
    for i in b:
        s += items[i]
    return s

'''
Takes a file and returns the item list
'''
def read_file(file_name):
    file = open(file_name, "r")
    items = file.readlines()
    file.close()
    return items


def main():
    #items = [20, 30, 34, 9, 3, 4, 34, 10, 39, 40] 

    weight_limit = int(sys.argv[1])
    items = read_file(sys.argv[2])
    bins = [[]]
    
    items.sort(reverse=True)
    num_bins, bins = compute_greedy(bins, 0, items, weight_limit)

    print(num_bins)
    print(bins)



if __name__ == "__main__":
    main()
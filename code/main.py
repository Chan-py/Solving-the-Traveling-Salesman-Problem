import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--algorithm", type=str, default="merge",
                    help="sorting algorithm")
parser.add_argument("--list", type=str, default="../dataset/real/100K_reverse_sorted.txt",
                    help="testcase file")
args = parser.parse_args()

data = read_list_from_txt(args.list)

# print("Original list:", data)

if args.algorithm == "stl":
    start_time = time.time()
    sorted_data = sorted(data[:])
    end_time = time.time()
    print(end_time - start_time)
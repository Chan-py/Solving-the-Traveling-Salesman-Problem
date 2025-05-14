import argparse
import time
from utils import read_tsp

parser = argparse.ArgumentParser()
parser.add_argument("--algorithm", type=str, default="heauristic",
                    help="tsp solver")
parser.add_argument("--list", type=str, default="../dataset/xql662.tsp",
                    help="testcase file")
args = parser.parse_args()

data = read_tsp(args.list)
print(data)

# print("Original list:", data)

if args.algorithm == "stl":
    start_time = time.time()
    sorted_data = sorted(data[:])
    end_time = time.time()
    print(end_time - start_time)
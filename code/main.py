import argparse
import time

from utils import read_tsp
import mst

parser = argparse.ArgumentParser()
parser.add_argument("--algorithm", type=str, default="mst",
                    help="tsp solver")
parser.add_argument("--list", type=str, default="../dataset/xql662.tsp",
                    help="testcase file")
args = parser.parse_args()

data = read_tsp(args.list)
print(len(data))

# print("Original list:", data)

if args.algorithm == "mst":
    start_time = time.time()
    _, ans = mst.run(data)
    end_time = time.time()
    print(ans)
    print(end_time - start_time)
import argparse
import time
import json

from utils import read_tsp, visualize_tour
import mst
import dp
import cluster_dp

parser = argparse.ArgumentParser()
parser.add_argument("--algorithm", type=str, default="new",
                    help="tsp solver")
parser.add_argument("--list", type=str, default="../dataset/mona-lisa100K.tsp",
                    help="testcase file")
args = parser.parse_args()

data = read_tsp(args.list)
print(len(data))

# print("Original list:", data)

if args.algorithm == "mst":
    total_time = 0
    for _ in range(1):
        start_time = time.time()
        _, ans = mst.run(data)
        end_time = time.time()
        total_time += end_time - start_time
    print(ans)
    print(total_time / 1)
    
if args.algorithm == "dp":
    start_time = time.time()
    tour, ans = dp.run(data)
    end_time = time.time()
    print(ans)
    print(end_time - start_time)
    visualize_tour(data, tour)

if args.algorithm == "new":
    iter_num = 5
    total_time = 0
    total_ans = 0
    for _ in range(iter_num):
        start_time = time.time()
        tour, ans = cluster_dp.run(data)
        end_time = time.time()
        total_ans += ans
        total_time += end_time - start_time
    print(total_ans / iter_num)
    print(total_time / iter_num)
    # with open("last_tour.json", "w") as fp:
    #     json.dump(tour, fp)

    # start_time = time.time()
    # tour, ans = cluster_dp.run(data)
    # end_time = time.time()
    # print(ans)
    # print(end_time - start_time)
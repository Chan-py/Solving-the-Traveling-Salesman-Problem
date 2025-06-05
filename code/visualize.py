import json

from utils import read_tsp, visualize_tour

# 나중에 (예: 다른 스크립트나 동일 스크립트 내에서)
# 1) data(노드 좌표 등) 는 이미 메모리에 로드돼 있다고 가정
# 2) "last_tour.json" 파일에 저장해둔 tour를 다시 불러옴

with open("mona_new_tour.json", "r") as fp:
    loaded_tour = json.load(fp)
data = read_tsp("../dataset/mona-lisa100K.tsp")
# 이제 visualize_tour 함수를 호출
visualize_tour(data, loaded_tour)
import gzip
import re

def read_tsp(path):
    """
    .tsp 또는 .tsp.gz 파일을 읽어서
    { idx: (x, y), ... } 형태의 dict로 반환합니다.
    """
    # 파일 열기: .gz면 gzip, 아니면 일반 open
    opener = gzip.open if path.endswith('.gz') else open
    with opener(path, 'rt') as f:
        lines = f.readlines()

    coords = {}
    in_coords = False
    for line in lines:
        line = line.strip()
        if line.startswith('NODE_COORD_SECTION'):
            in_coords = True
            continue
        if in_coords:
            if line == 'EOF' or line == '':  # 섹션 끝
                break
            # ex) "  1   37.619   55.755"
            parts = re.split(r'\s+', line)
            idx = int(parts[0])
            x, y = float(parts[1]), float(parts[2])
            coords[idx] = (x, y)
    return coords
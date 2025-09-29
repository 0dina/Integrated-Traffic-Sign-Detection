#!/usr/bin/env python3
from pathlib import Path
from collections import Counter

ROOT = Path("/Users/dina/Desktop/8cls_a_aug/dataset")
LAB = ROOT / "labels"

cnt = Counter()
bad = []
files = list(LAB.glob("*.txt"))
num_objs = 0
for p in files:
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s: 
                continue
            parts = s.split()
            try:
                cid = int(float(parts[0]))
            except:
                bad.append((p.name, line))
                continue
            if cid < 0 or cid > 7:
                bad.append((p.name, line))
            cnt[cid] += 1
            num_objs += 1

print("라벨 파일 수:", len(files))
print("총 객체 수  :", num_objs)
print("클래스 분포 :", dict(sorted(cnt.items())))
if bad:
    print("범위 밖/이상 라인 예시(최대 5개):")
    for x in bad[:5]:
        print(" ", x)
else:
    print("모든 클래스 인덱스가 0~7 범위에 있음.")

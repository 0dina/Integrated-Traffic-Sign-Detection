#!/usr/bin/env python3
import random, shutil
from pathlib import Path

random.seed(42)

SRC_ROOT = Path("/Users/dina/Desktop/8cls_a_aug/dataset_aug_all")
SRC_IMG, SRC_LAB = SRC_ROOT/"images", SRC_ROOT/"labels"
OUT_ROOT = Path("/Users/dina/Desktop/8cls_a_aug/dataset_aug_split")
splits = {"train":0.8, "val":0.1, "test":0.1}

for sp in splits:
    (OUT_ROOT/sp/"images").mkdir(parents=True, exist_ok=True)
    (OUT_ROOT/sp/"labels").mkdir(parents=True, exist_ok=True)

def has_label(img):
    return (SRC_LAB / (img.stem + ".txt")).exists()

samples = [(p, SRC_LAB/(p.stem+".txt")) for p in SRC_IMG.iterdir() if p.is_file() and has_label(p)]
random.shuffle(samples)

N = len(samples)
targets = {sp:int(round(N*r)) for sp,r in splits.items()}
bins = {sp:[] for sp in splits}

for img,lbl in samples:
    sp = min(bins, key=lambda k: len(bins[k]) / max(targets[k],1))
    if len(bins[sp]) >= targets[sp]:
        for alt in bins:
            if len(bins[alt]) < targets[alt]:
                sp = alt; break
    bins[sp].append((img,lbl))

for sp, items in bins.items():
    for img,lbl in items:
        shutil.copy2(img, OUT_ROOT/sp/"images"/img.name)
        shutil.copy2(lbl, OUT_ROOT/sp/"labels"/(img.stem+".txt"))

yaml = f"""# 8-class split dataset
path: {OUT_ROOT}
train: train/images
val: val/images
test: test/images

nc: 8
names:
  0: 30km_limit
  1: 50km_limit
  2: crosswalk
  3: kidprotectzone
  4: noparking
  5: stop
  6: oneway
  7: slow
"""
with (OUT_ROOT/"dataset.yaml").open("w", encoding="utf-8") as f:
    f.write(yaml)

print("DONE")
for sp in splits:
    print(sp, "샘플 수:", len(bins[sp]))
print("dataset.yaml:", OUT_ROOT/"dataset.yaml")

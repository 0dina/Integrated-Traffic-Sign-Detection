#!/usr/bin/env python3
import shutil
from pathlib import Path
from typing import List

# === 입력/출력 경로 ===
SRC_ROOT = Path("/Users/dina/Desktop/roadSign_detection_project/dataset/all")
SRC_IMG = SRC_ROOT / "images"
SRC_LAB = SRC_ROOT / "labels"

OUT_ROOT = Path("/Users/dina/Desktop/8cls_a_aug/dataset_aug")
OUT_IMG = OUT_ROOT / "images"
OUT_LAB = OUT_ROOT / "labels"
OUT_IMG.mkdir(parents=True, exist_ok=True)
OUT_LAB.mkdir(parents=True, exist_ok=True)

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

# === 규칙 ===
REMOVE = {5, 9}   # nouturn, uturn 제거
REMAP = {8: 5}    # stop(8) -> 5

def next_nonconflicting_path(dst_path: Path) -> Path:
    if not dst_path.exists():
        return dst_path
    stem, suffix = dst_path.stem, dst_path.suffix
    k = 1
    while True:
        cand = dst_path.with_name(f"{stem}_{k}{suffix}")
        if not cand.exists():
            return cand
        k += 1

def process_one_label(lbl_path: Path) -> List[str]:
    if not lbl_path.exists():
        return []
    out: List[str] = []
    with lbl_path.open("r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue
            parts = s.split()
            try:
                cid = int(float(parts[0]))
            except Exception:
                continue
            if cid in REMOVE:
                continue
            if cid in REMAP:
                cid = REMAP[cid]
            parts[0] = str(cid)
            out.append(" ".join(parts))
    return out

def label_path_for(img_path: Path) -> Path:
    return SRC_LAB / (img_path.stem + ".txt")

# 통계
kept_images = 0
removed_all_objects = 0
total_objects_before = 0
total_objects_after = 0

# 이미지 순회
for img_path in SRC_IMG.rglob("*"):
    if not img_path.is_file() or img_path.suffix.lower() not in IMG_EXTS:
        continue
    lbl_path = label_path_for(img_path)

    # before 카운트
    if lbl_path.exists():
        with lbl_path.open("r", encoding="utf-8") as f:
            for raw in f:
                if raw.strip():
                    total_objects_before += 1

    new_lines = process_one_label(lbl_path)
    total_objects_after += len(new_lines)

    if len(new_lines) == 0:
        removed_all_objects += 1
        continue  # 통째로 제외

    # 복사/저장
    dst_img = next_nonconflicting_path(OUT_IMG / img_path.name)
    dst_lab = OUT_LAB / (dst_img.stem + ".txt")

    shutil.copy2(img_path, dst_img)
    with dst_lab.open("w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    kept_images += 1

# dataset.yaml 작성
yaml_text = f"""# 8-class dataset (single-source filtered & remapped)
path: {OUT_ROOT}
train: images
val: images
test: images

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
with (OUT_ROOT / "dataset.yaml").open("w", encoding="utf-8") as f:
    f.write(yaml_text)

print("=== DONE ===")
print(f"출력 루트        : {OUT_ROOT}")
print(f"복사된 이미지 수 : {kept_images}")
print(f"제거(무라벨) 수  : {removed_all_objects}")
print(f"객체 수(before)  : {total_objects_before}")
print(f"객체 수(after)   : {total_objects_after}")
print(f"dataset.yaml     : {OUT_ROOT/'dataset.yaml'}")

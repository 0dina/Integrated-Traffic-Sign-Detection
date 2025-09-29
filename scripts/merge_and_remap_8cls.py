#!/usr/bin/env python3
import shutil, os, sys
from pathlib import Path
from typing import List  # <= 추가

# === 경로 설정 ===
SRC_DIRS = [
    Path("/Users/dina/Desktop/forModelTest/test_flat_dataset"),   # a 데이터셋
    Path("/Users/dina/Desktop/roadSign_detection_project/dataset/all"),  # 증강이미지셋
]
OUT_ROOT = Path("/Users/dina/Desktop/forModelTest/merged_8cls")
OUT_IMG = OUT_ROOT / "images"
OUT_LAB = OUT_ROOT / "labels"
OUT_ROOT.mkdir(parents=True, exist_ok=True)
OUT_IMG.mkdir(parents=True, exist_ok=True)
OUT_LAB.mkdir(parents=True, exist_ok=True)

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

# === 클래스 처리 규칙 ===
REMOVE = {5, 9}          # nouturn, uturn 제거
REMAP = {8: 5}           # stop(8) -> 5

def next_nonconflicting_path(dst_path: Path) -> Path:
    if not dst_path.exists():
        return dst_path
    stem, suffix = dst_path.stem, dst_path.suffix
    k = 1
    while True:
        candidate = dst_path.with_name(f"{stem}_{k}{suffix}")
        if not candidate.exists():
            return candidate
        k += 1

def process_one_label(lbl_path: Path) -> List[str]:  # <= 여기 수정
    """YOLO txt 라벨 한 파일을 읽어 필터/리맵 후 라인 리스트 반환. 전부 제거되면 빈 리스트."""
    if not lbl_path.exists():
        return []
    lines_out: List[str] = []
    with lbl_path.open("r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue
            parts = s.split()
            # YOLO 형식: class cx cy w h [etc...]
            try:
                cid = int(float(parts[0]))
            except Exception:
                continue
            if cid in REMOVE:
                continue
            if cid in REMAP:
                cid = REMAP[cid]
            parts[0] = str(cid)
            lines_out.append(" ".join(parts))
    return lines_out

def find_label_for_image(img_path: Path, labels_dir: Path) -> Path:
    return labels_dir / (img_path.stem + ".txt")

def collect_items(root: Path):
    img_dir = root / "images"
    lab_dir = root / "labels"
    if not img_dir.is_dir() or not lab_dir.is_dir():
        print(f"[WARN] {root} 에 images/labels 폴더가 없음. 스킵.")
        return []
    items = []
    for p in img_dir.rglob("*"):
        if p.suffix.lower() in IMG_EXTS and p.is_file():
            items.append((p, find_label_for_image(p, lab_dir)))
    return items

# 통계
kept_images = 0
removed_all_objects = 0
total_objects_before = 0
total_objects_after = 0

for src_root in SRC_DIRS:
    items = collect_items(src_root)
    for img_path, lbl_path in items:
        new_lines = process_one_label(lbl_path)

        # before
        if lbl_path.exists():
            with lbl_path.open("r", encoding="utf-8") as f:
                for raw in f:
                    if raw.strip():
                        total_objects_before += 1
        # after
        total_objects_after += len(new_lines)

        if len(new_lines) == 0:
            removed_all_objects += 1
            continue

        dst_img = next_nonconflicting_path(OUT_IMG / img_path.name)
        dst_lab = OUT_LAB / (dst_img.stem + ".txt")

        shutil.copy2(img_path, dst_img)
        with dst_lab.open("w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
        kept_images += 1

# dataset.yaml 작성
yaml_path = OUT_ROOT / "dataset.yaml"
yaml_content = f"""# merged and remapped to 8 classes (0~7)
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
with yaml_path.open("w", encoding="utf-8") as f:
    f.write(yaml_content)

print("=== DONE ===")
print(f"출력 루트        : {OUT_ROOT}")
print(f"복사된 이미지 수 : {kept_images}")
print(f"제거(무라벨) 수  : {removed_all_objects}")
print(f"객체 수(before)  : {total_objects_before}")
print(f"객체 수(after)   : {total_objects_after}")
print(f"dataset.yaml     : {yaml_path}")

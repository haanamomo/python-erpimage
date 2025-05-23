# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import os
from PIL import Image
from pathlib import Path
from collections import defaultdict
import re
import shutil
import hashlib

ALLOWED_FILE_TYPES = [
    '.jpg', '.jpeg', '.png', '.webp'
]

def generate_content_hash(file_path: Path, hash_len=10) -> str:
    """生成文件内容的 hash，用作唯一ID"""
    hasher = hashlib.md5()
    with file_path.open('rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()[:hash_len]


def process_file(file_path: Path, index: int, output_folder: Path):
    """将单张图片转为 webp 并输出到 output_folder 下"""
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
        file_id = generate_content_hash(file_path)

        new_path = output_folder / f"{file_id}.webp"

        with Image.open(file_path) as img:
            img.convert('RGB').save(new_path, 'webp', quality=80, method=6)
        print(f"  ✅ {file_path.name} → {new_path.name}")
    except Exception as e:
        print(f"  ❌ 转换失败：{file_path.name}，错误：{e}")


def process_folder(src_folder: Path, output_root):
    parts = src_folder.name.split('-')
    if len(parts) < 3:
        output_folder = output_root / src_folder.name
    else:
        middle = parts[1]
        output_folder = output_root / middle

    image_files = [
        f for f in src_folder.iterdir()
        if f.is_file() and f.suffix.lower() in ALLOWED_FILE_TYPES
    ]
    image_files.sort()

    print(f"📁 处理：{src_folder.name} → 输出：{output_folder.name}")
    for idx, file_path in enumerate(image_files, start=1):
        process_file(file_path, idx, output_folder)

flattened_pattern = re.compile(r'^([A-Z]{0,3}\d{3,6})')

def process_flattened(input_path: Path, output_root: Path):
    """
    扫描所有文件，按文件名前缀分组（例如 '1601 黑色 1.jpg' → '1601'）
    并把每组图放到 output_root/1601 里再转换为 webp
    """
    print("🔍 处理模式：摊平目录 ", input_path)

    grouped_files = defaultdict(list)

    for file in input_path.iterdir():
        if not file.is_file() or file.suffix.lower() not in ALLOWED_FILE_TYPES:
            continue

        # 匹配类似于 "1601 黑色 1.jpg" 的文件名，提取前缀
        match = flattened_pattern.match(file.stem)
        if match:
            prefix = match.group(1)
            grouped_files[prefix].append(file)
        else:
            print("not match: ", file.stem)

    for prefix, files in grouped_files.items():
        files.sort()
        print(f"📦 平铺组：{prefix}，共 {len(files)} 张")
        for idx, file in enumerate(files, start=1):
            process_file(file, idx, output_root / prefix)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("input_path", help='The path of the input file.')
    parser.add_argument("-f", "--flattened", action="store_true", help='是否处理摊平图片（统一目录中带编号）')

    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_root = input_path.parent / f"{input_path.name}_output"
    # 清空已有的输出目录（如果存在）
    if output_root.exists() and output_root.is_dir():
        shutil.rmtree(output_root)

    # 重建空目录
    output_root.mkdir(parents=True, exist_ok=True)

    if args.flattened:
        process_flattened(input_path, output_root)
    else:
        print("🔍 处理模式：标准目录结构")
        for folder in input_path.iterdir():
            if folder.is_dir():
                process_folder(folder, output_root)


if __name__ == "__main__":
    main()
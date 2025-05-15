# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import os
from PIL import Image
from pathlib import Path

ALLOWED_FILE_TYPES = [
    '.jpg', '.jpeg', '.png', '.webp'
]

def process_file(file_path: Path, index: int, output_folder: Path):
    """将单张图片转为 webp 并输出到 output_folder 下"""
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
        new_path = output_folder / f"{index}.webp"

        with Image.open(file_path) as img:
            img.convert('RGB').save(new_path, 'webp')
        print(f"  ✅ {file_path.name} → {new_path.name}")
    except Exception as e:
        print(f"  ❌ 转换失败：{file_path.name}，错误：{e}")


def process_folder(src_folder: Path, output_root):
    parts = src_folder.name.split('-')
    if len(parts) < 3:
        print(f"❌ 跳过不规范文件夹名：{src_folder.name}")
        return

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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("input_path", help='The path of the input file.')

    options = parser.parse_args()

    input_path = Path(options.input_path)
    output_root = input_path.parent / f"{input_path.name}_output"

    for folder in input_path.iterdir():
        if folder.is_dir():
            process_folder(folder, output_root)


if __name__ == "__main__":
    main()
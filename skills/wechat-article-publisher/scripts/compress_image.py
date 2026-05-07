#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow>=10.0.0",
# ]
# ///
"""
智能图片压缩工具 - 保持清晰度的前提下压缩图片

压缩策略：
1. 保持原始分辨率（不缩小尺寸）
2. 使用渐进式压缩（从高质量开始）
3. 目标大小：封面 800KB，配图 600KB
4. 最低质量：75（保证清晰度）

使用方法：
    python3 compress_image.py --input image.jpg --output compressed.jpg
    python3 compress_image.py --input image.jpg --output compressed.jpg --max-size 800
"""

import os
import sys
import argparse
from PIL import Image
import io


def get_file_size_kb(file_path: str) -> float:
    """获取文件大小（KB）"""
    return os.path.getsize(file_path) / 1024


def compress_image(
    input_path: str,
    output_path: str,
    max_size_kb: int = 800,
    min_quality: int = 75,
    initial_quality: int = 95
) -> dict:
    """
    智能压缩图片
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        max_size_kb: 目标大小（KB）
        min_quality: 最低质量（保证清晰度）
        initial_quality: 初始质量
        
    Returns:
        dict: 压缩结果信息
    """
    # 打开图片
    img = Image.open(input_path)
    original_size = get_file_size_kb(input_path)
    original_format = img.format
    width, height = img.size
    
    print(f"原始图片: {width}x{height}, {original_size:.1f}KB, 格式: {original_format}", file=sys.stderr)
    
    # 转换为 RGB（如果是 RGBA 或其他模式）
    if img.mode in ('RGBA', 'LA', 'P'):
        # 创建白色背景
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 如果原始图片已经小于目标大小，直接保存
    if original_size <= max_size_kb:
        img.save(output_path, 'JPEG', quality=95, optimize=True)
        final_size = get_file_size_kb(output_path)
        print(f"✅ 原始图片已满足要求，保存为高质量: {final_size:.1f}KB", file=sys.stderr)
        return {
            "success": True,
            "original_size_kb": original_size,
            "final_size_kb": final_size,
            "quality": 95,
            "compression_ratio": (1 - final_size / original_size) * 100,
            "message": "原始图片已满足要求"
        }
    
    # 渐进式压缩
    quality = initial_quality
    best_quality = quality
    best_size = float('inf')
    
    while quality >= min_quality:
        # 保存到内存缓冲区测试大小
        buffer = io.BytesIO()
        img.save(buffer, 'JPEG', quality=quality, optimize=True)
        size_kb = len(buffer.getvalue()) / 1024
        
        print(f"尝试质量 {quality}: {size_kb:.1f}KB", file=sys.stderr)
        
        # 如果大小合适，保存这个质量
        if size_kb <= max_size_kb:
            best_quality = quality
            best_size = size_kb
            # 保存到文件
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())
            break
        
        # 降低质量
        if size_kb > max_size_kb * 1.5:
            quality -= 10  # 大幅降低
        elif size_kb > max_size_kb * 1.2:
            quality -= 5   # 中等降低
        else:
            quality -= 2   # 小幅降低
    
    # 如果降到最低质量还是太大，使用最低质量保存
    if quality < min_quality:
        img.save(output_path, 'JPEG', quality=min_quality, optimize=True)
        best_quality = min_quality
        best_size = get_file_size_kb(output_path)
        print(f"⚠️  使用最低质量 {min_quality} 保存: {best_size:.1f}KB", file=sys.stderr)
    
    final_size = get_file_size_kb(output_path)
    compression_ratio = (1 - final_size / original_size) * 100
    
    print(f"✅ 压缩完成: {original_size:.1f}KB → {final_size:.1f}KB (质量: {best_quality}, 压缩率: {compression_ratio:.1f}%)", file=sys.stderr)
    
    return {
        "success": True,
        "original_size_kb": original_size,
        "final_size_kb": final_size,
        "quality": best_quality,
        "compression_ratio": compression_ratio,
        "width": width,
        "height": height,
        "message": f"压缩成功，质量 {best_quality}"
    }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="智能图片压缩工具 - 保持清晰度的前提下压缩图片",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="输入图片路径"
    )
    
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出图片路径"
    )
    
    parser.add_argument(
        "--max-size",
        type=int,
        default=800,
        help="目标大小（KB），默认: 800"
    )
    
    parser.add_argument(
        "--min-quality",
        type=int,
        default=75,
        help="最低质量（1-100），默认: 75（保证清晰度）"
    )
    
    parser.add_argument(
        "--initial-quality",
        type=int,
        default=95,
        help="初始质量（1-100），默认: 95"
    )
    
    args = parser.parse_args()
    
    try:
        # 检查输入文件
        if not os.path.exists(args.input):
            raise FileNotFoundError(f"输入文件不存在: {args.input}")
        
        # 压缩图片
        result = compress_image(
            args.input,
            args.output,
            args.max_size,
            args.min_quality,
            args.initial_quality
        )
        
        # 输出结果
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
微信公众号文章一键发布工具

功能：
1. 自动读取配置（公众号、API Key、排版样式）
2. Markdown 转 HTML（使用 doocs/md 排版）
3. 生成封面图（根据文章内容）
4. 上传到公众号草稿箱

使用方法：
    # 基础用法（自动生成封面）
    python3 publish_article.py --input article.md --title "文章标题"
    
    # 指定作者和摘要
    python3 publish_article.py --input article.md --title "文章标题" --author "作者名" --digest "文章摘要"
    
    # 使用已有封面
    python3 publish_article.py --input article.md --title "文章标题" --thumb_media_id "封面ID"
"""

import os
import sys
import argparse
import json
import subprocess
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config import get_wechat_config, get_doubao_api_key, get_markdown_config


def convert_markdown_to_html(input_file: str, output_file: str = None) -> str:
    """
    将 Markdown 转换为 HTML
    
    Args:
        input_file: Markdown 文件路径
        output_file: HTML 输出文件路径（可选）
        
    Returns:
        str: HTML 文件路径
    """
    # 获取排版配置
    markdown_config = get_markdown_config()
    converter = markdown_config['converter']
    theme = markdown_config['theme']
    
    # 如果没有指定输出文件，自动生成
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix('.html'))
    
    # 根据转换器选择脚本
    if converter == 'doocs':
        script = script_dir / 'markdown_to_wechat_doocs.py'
    else:
        script = script_dir / 'markdown_to_wechat_mdnice.py'
    
    # 执行转换
    cmd = [
        'python3', str(script),
        '--input', input_file,
        '--output', output_file,
        '--theme', theme
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Markdown 转换失败: {result.stderr}")
    
    print(f"✅ Markdown 转换成功: {output_file}")
    return output_file


def generate_cover_image(article_title: str, article_content: str = None) -> str:
    """
    生成封面图并上传到公众号
    
    Args:
        article_title: 文章标题
        article_content: 文章内容（可选，用于生成更精准的封面）
        
    Returns:
        str: 封面图的 thumb_media_id
    """
    # 获取豆包 API Key
    api_key = get_doubao_api_key()
    if not api_key:
        raise ValueError("缺少豆包 API Key，无法生成封面图")
    
    # 构建封面图提示词
    if article_content:
        # 提取文章前200字作为参考
        content_preview = article_content[:200].replace('\n', ' ')
        prompt = f"为文章《{article_title}》生成封面图。文章内容：{content_preview}。要求：温暖、有质感、适合公众号文章封面。"
    else:
        prompt = f"为文章《{article_title}》生成封面图。要求：温暖、有质感、适合公众号文章封面。"
    
    # 生成封面图
    script = script_dir / 'generate_cover.py'
    cmd = [
        'python3', str(script),
        '--prompt', prompt,
        '--output', 'cover.jpg'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"封面图生成失败: {result.stderr}")
    
    # 解析输出获取 thumb_media_id
    output = result.stdout
    try:
        # 查找 thumb_media_id
        for line in output.split('\n'):
            if 'thumb_media_id' in line.lower() or 'media_id' in line.lower():
                # 尝试提取 media_id
                if ':' in line:
                    media_id = line.split(':', 1)[1].strip()
                    print(f"✅ 封面图生成成功: {media_id}")
                    return media_id
    except:
        pass
    
    raise Exception("无法从输出中提取 thumb_media_id")


def upload_to_draft(title: str, html_file: str, thumb_media_id: str, author: str = None, digest: str = None) -> dict:
    """
    上传文章到公众号草稿箱
    
    Args:
        title: 文章标题
        html_file: HTML 文件路径
        thumb_media_id: 封面图 media_id
        author: 作者名（可选）
        digest: 文章摘要（可选）
        
    Returns:
        dict: 上传结果
    """
    # 读取 HTML 内容
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取公众号配置
    wechat_config = get_wechat_config()
    app_id = wechat_config['app_id']
    app_secret = wechat_config['app_secret']
    
    # 上传草稿
    script = script_dir / 'create_draft.py'
    cmd = [
        'python3', str(script),
        '--app_id', app_id,
        '--app_secret', app_secret,
        '--title', title,
        '--content', content,
        '--thumb_media_id', thumb_media_id
    ]
    
    if author:
        cmd.extend(['--author', author])
    if digest:
        cmd.extend(['--digest', digest])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"上传草稿失败: {result.stderr}")
    
    # 解析输出
    try:
        output = result.stdout
        # 查找 JSON 输出
        for line in output.split('\n'):
            if line.strip().startswith('{'):
                data = json.loads(line)
                if data.get('status') == 'success':
                    print(f"✅ 文章已上传到草稿箱")
                    print(f"   Media ID: {data.get('media_id')}")
                    return data
    except:
        pass
    
    raise Exception("无法解析上传结果")


def main():
    parser = argparse.ArgumentParser(description='微信公众号文章一键发布工具')
    parser.add_argument('--input', required=True, help='Markdown 文件路径')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--author', help='作者名称')
    parser.add_argument('--digest', help='文章摘要')
    parser.add_argument('--thumb_media_id', help='封面图 media_id（如果已有）')
    parser.add_argument('--no-cover', action='store_true', help='不生成封面图（需要提供 thumb_media_id）')
    
    args = parser.parse_args()
    
    try:
        print("=" * 60)
        print("微信公众号文章一键发布工具")
        print("=" * 60)
        
        # 步骤1：转换 Markdown 为 HTML
        print("\n[1/3] 转换 Markdown 为 HTML...")
        html_file = convert_markdown_to_html(args.input)
        
        # 步骤2：生成封面图（如果需要）
        thumb_media_id = args.thumb_media_id
        if not thumb_media_id and not args.no_cover:
            print("\n[2/3] 生成封面图...")
            # 读取文章内容
            with open(args.input, 'r', encoding='utf-8') as f:
                article_content = f.read()
            thumb_media_id = generate_cover_image(args.title, article_content)
        else:
            print("\n[2/3] 跳过封面图生成（使用已有封面）")
        
        # 步骤3：上传到草稿箱
        print("\n[3/3] 上传到公众号草稿箱...")
        result = upload_to_draft(
            title=args.title,
            html_file=html_file,
            thumb_media_id=thumb_media_id,
            author=args.author,
            digest=args.digest
        )
        
        print("\n" + "=" * 60)
        print("✅ 发布完成！")
        print("=" * 60)
        print(f"文章标题: {args.title}")
        if args.author:
            print(f"作者: {args.author}")
        print(f"Media ID: {result.get('media_id')}")
        print("\n请登录公众号后台查看草稿箱")
        
    except Exception as e:
        print(f"\n❌ 发布失败: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

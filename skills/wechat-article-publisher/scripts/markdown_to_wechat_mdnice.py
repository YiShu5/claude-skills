#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 转换器（Markdown Nice 风格）

基于 Markdown Nice 的经典主题设计，专业美观的排版。

使用方法：
    python3 markdown_to_wechat_mdnice.py --input article.md --output article.html --theme default
    
支持主题：
    - default: 默认主题（绿色清新）
    - orange: 橙心主题（橙色温暖）
    - purple: 紫色主题（优雅紫色）
    - blue: 蓝色主题（商务蓝色）
"""

import os
import sys
import argparse
import re


# Markdown Nice 风格的主题
THEMES = {
    "default": {
        "primary": "#3f9e4d",  # 绿色
        "secondary": "#e8f5e9",
        "text": "#2b2b2b",
        "text_light": "#595959",
        "border": "#e8f5e9",
        "code_bg": "#f6f8fa",
        "quote_bg": "#e8f5e9",
        "strong": "#3f9e4d",
    },
    "orange": {
        "primary": "#ff6800",  # 橙色
        "secondary": "#fff8f0",
        "text": "#2b2b2b",
        "text_light": "#595959",
        "border": "#ffe4cc",
        "code_bg": "#fff8f0",
        "quote_bg": "#fff8f0",
        "strong": "#ff6800",
    },
    "purple": {
        "primary": "#8e44ad",  # 紫色
        "secondary": "#f4ecf7",
        "text": "#2b2b2b",
        "text_light": "#595959",
        "border": "#e8daef",
        "code_bg": "#f4ecf7",
        "quote_bg": "#f4ecf7",
        "strong": "#8e44ad",
    },
    "blue": {
        "primary": "#1e88e5",  # 蓝色
        "secondary": "#e3f2fd",
        "text": "#2b2b2b",
        "text_light": "#595959",
        "border": "#bbdefb",
        "code_bg": "#e3f2fd",
        "quote_bg": "#e3f2fd",
        "strong": "#1e88e5",
    }
}


def get_theme_colors(theme_name):
    """获取主题颜色"""
    return THEMES.get(theme_name, THEMES["default"])


def markdown_to_html_mdnice(markdown_text, theme="default"):
    """
    将 Markdown 转换为 Markdown Nice 风格的 HTML
    """
    colors = get_theme_colors(theme)
    
    html_lines = []
    in_list = False
    in_ordered_list = False
    in_blockquote = False
    in_code_block = False
    code_block_lines = []
    list_counter = 0
    
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 代码块
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_lines = []
            else:
                in_code_block = False
                code_content = '\n'.join(code_block_lines)
                code_content = code_content.replace('<', '&lt;').replace('>', '&gt;')
                html_lines.append(f'''<pre style="margin: 10px 0; padding: 15px; background-color: {colors["code_bg"]}; border-radius: 5px; border: 1px solid {colors["border"]}; overflow-x: auto; font-size: 14px; line-height: 1.6;"><code style="font-family: Consolas, Monaco, 'Courier New', monospace; color: {colors["text"]};">{code_content}</code></pre>''')
                code_block_lines = []
            i += 1
            continue
        
        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue
        
        # 空行
        if not line.strip():
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
                list_counter = 0
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            i += 1
            continue
        
        # 标题
        if line.startswith('# '):
            content = process_inline(line[2:], colors)
            html_lines.append(f'''<h1 style="margin: 1.2em 0 1em; padding: 0; font-weight: bold; color: {colors["text"]}; font-size: 24px; text-align: center; line-height: 1.4;">{content}</h1>''')
        elif line.startswith('## '):
            content = process_inline(line[3:], colors)
            html_lines.append(f'''<h2 style="margin: 1.2em 0 0.8em; padding: 0 0 0.3em 0; font-weight: bold; color: {colors["text"]}; font-size: 20px; border-bottom: 2px solid {colors["primary"]}; line-height: 1.4;">{content}</h2>''')
        elif line.startswith('### '):
            content = process_inline(line[4:], colors)
            html_lines.append(f'''<h3 style="margin: 1em 0 0.6em; padding: 0 0 0 10px; font-weight: bold; color: {colors["text"]}; font-size: 18px; border-left: 4px solid {colors["primary"]}; line-height: 1.4;">{content}</h3>''')
        elif line.startswith('#### '):
            content = process_inline(line[5:], colors)
            html_lines.append(f'''<h4 style="margin: 1em 0 0.5em; padding: 0; font-weight: bold; color: {colors["text"]}; font-size: 16px; line-height: 1.4;">{content}</h4>''')
        # 分隔线
        elif line.strip() == '---' or line.strip() == '***':
            html_lines.append(f'''<hr style="margin: 20px 0; border: none; border-top: 1px solid {colors["border"]};" />''')
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append(f'''<ul style="margin: 10px 0; padding-left: 20px; list-style-type: none;">''')
                in_list = True
            content = process_inline(line[2:], colors)
            html_lines.append(f'''<li style="margin: 5px 0; padding-left: 0; position: relative; font-size: 15px; line-height: 1.8; color: {colors["text"]}; list-style-type: none;"><span style="position: absolute; left: -20px; color: {colors["primary"]}; font-weight: bold;">•</span>{content}</li>''')
        # 有序列表
        elif re.match(r'^\d+\.\s', line):
            if not in_ordered_list:
                html_lines.append(f'''<ol style="margin: 10px 0; padding-left: 20px; list-style-type: none; counter-reset: list-counter;">''')
                in_ordered_list = True
                list_counter = 0
            list_counter += 1
            content = re.sub(r'^\d+\.\s', '', line)
            content = process_inline(content, colors)
            html_lines.append(f'''<li style="margin: 5px 0; padding-left: 0; position: relative; font-size: 15px; line-height: 1.8; color: {colors["text"]}; list-style-type: none;"><span style="position: absolute; left: -20px; color: {colors["primary"]}; font-weight: bold;">{list_counter}.</span>{content}</li>''')
        # 引用
        elif line.startswith('> '):
            if not in_blockquote:
                html_lines.append(f'''<blockquote style="margin: 10px 0; padding: 10px 15px; background-color: {colors["quote_bg"]}; border-left: 4px solid {colors["primary"]}; border-radius: 0 5px 5px 0;">''')
                in_blockquote = True
            content = process_inline(line[2:], colors)
            html_lines.append(f'''<p style="margin: 5px 0; font-size: 14px; line-height: 1.8; color: {colors["text_light"]};">{content}</p>''')
        # 图片
        elif re.match(r'!\[.*?\]\(.*?\)', line):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt = match.group(1)
                src = match.group(2)
                html_lines.append(f'''<figure style="margin: 20px 0; text-align: center;"><img src="{src}" alt="{alt}" style="max-width: 100%; height: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />''')
                if alt:
                    html_lines.append(f'''<figcaption style="margin-top: 8px; font-size: 13px; color: {colors["text_light"]}; font-style: italic;">{alt}</figcaption>''')
                html_lines.append('</figure>')
        # 普通段落
        else:
            content = process_inline(line, colors)
            html_lines.append(f'''<p style="margin: 10px 0; font-size: 15px; line-height: 1.8; color: {colors["text"]}; text-align: justify; word-wrap: break-word;">{content}</p>''')
        
        i += 1
    
    # 关闭未关闭的标签
    if in_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    
    return '\n'.join(html_lines)


def process_inline(text, colors):
    """处理行内元素"""
    # 加粗
    text = re.sub(r'\*\*(.*?)\*\*', rf'<strong style="color: {colors["strong"]}; font-weight: bold;">\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.*?)\*', rf'<em style="font-style: italic;">\1</em>', text)
    # 行内代码
    text = re.sub(r'`(.*?)`', rf'<code style="padding: 2px 4px; background-color: {colors["code_bg"]}; border-radius: 3px; color: {colors["primary"]}; font-family: Consolas, Monaco, monospace; font-size: 14px;">\1</code>', text)
    # 链接
    text = re.sub(r'\[(.*?)\]\((.*?)\)', rf'<a href="\2" style="color: {colors["primary"]}; text-decoration: none; border-bottom: 1px solid {colors["primary"]};">\1</a>', text)
    return text


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Markdown 转微信公众号 HTML 转换器（Markdown Nice 风格）",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="输入 Markdown 文件路径"
    )
    
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出 HTML 文件路径"
    )
    
    parser.add_argument(
        "--theme", "-t",
        choices=["default", "orange", "purple", "blue"],
        default="default",
        help="主题: default(绿色), orange(橙色), purple(紫色), blue(蓝色)"
    )
    
    args = parser.parse_args()
    
    try:
        # 读取 Markdown 文件
        with open(args.input, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        # 转换为 HTML
        html_content = markdown_to_html_mdnice(markdown_text, args.theme)
        
        # 包装在 section 中
        final_html = f'<section style="padding: 10px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Ubuntu, \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei UI\', \'Microsoft YaHei\', \'Source Han Sans CN\', sans-serif;">\n{html_content}\n</section>'
        
        # 写入 HTML 文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"✅ 转换成功！")
        print(f"   输入: {args.input}")
        print(f"   输出: {args.output}")
        print(f"   主题: {args.theme}")
        print(f"   风格: Markdown Nice")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

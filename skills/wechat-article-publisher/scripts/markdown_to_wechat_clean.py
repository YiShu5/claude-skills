#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 转换器（简洁大气版）

特点：
- 去掉多余的背景色
- 优化列表显示
- 简洁大气的排版
- 所有样式使用内联方式

使用方法：
    python3 markdown_to_wechat_clean.py --input article.md --output article.html
"""

import os
import sys
import argparse
import re


def markdown_to_html_clean(markdown_text):
    """
    将 Markdown 转换为简洁大气的 HTML
    """
    html_lines = []
    in_list = False
    in_ordered_list = False
    in_blockquote = False
    in_code_block = False
    code_block_lines = []
    
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
                html_lines.append(f'<pre style="background-color: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; margin: 16px 0; border: 1px solid #e1e4e8;"><code style="font-family: Consolas, Monaco, monospace; font-size: 14px; color: #24292e;">{code_content}</code></pre>')
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
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            i += 1
            continue
        
        # 标题
        if line.startswith('# '):
            html_lines.append(f'<h1 style="font-size: 26px; font-weight: bold; color: #2c3e50; text-align: center; margin: 30px 0 20px 0; padding: 0; line-height: 1.4;">{process_inline(line[2:])}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2 style="font-size: 22px; font-weight: bold; color: #2c3e50; margin: 30px 0 15px 0; padding: 0 0 10px 0; border-bottom: 2px solid #3498db; line-height: 1.4;">{process_inline(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3 style="font-size: 18px; font-weight: bold; color: #34495e; margin: 25px 0 12px 0; padding: 0 0 0 12px; border-left: 4px solid #3498db; line-height: 1.4;">{process_inline(line[4:])}</h3>')
        # 分隔线
        elif line.strip() == '---' or line.strip() == '***':
            html_lines.append('<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 25px 0;" />')
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul style="margin: 12px 0; padding-left: 0; list-style: none;">')
                in_list = True
            content = process_inline(line[2:])
            html_lines.append(f'<li style="margin: 8px 0; padding-left: 24px; position: relative; font-size: 16px; line-height: 1.8; color: #333;"><span style="position: absolute; left: 0; color: #3498db; font-weight: bold;">•</span>{content}</li>')
        # 有序列表
        elif re.match(r'^\d+\.\s', line):
            if not in_ordered_list:
                html_lines.append('<ol style="margin: 12px 0; padding-left: 0; list-style: none; counter-reset: list-counter;">')
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s', '', line)
            content = process_inline(content)
            html_lines.append(f'<li style="margin: 8px 0; padding-left: 32px; position: relative; font-size: 16px; line-height: 1.8; color: #333; counter-increment: list-counter;"><span style="position: absolute; left: 0; color: #3498db; font-weight: bold;">{{counter(list-counter)}}.</span>{content}</li>')
        # 引用
        elif line.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote style="margin: 16px 0; padding: 12px 16px; background-color: #f8f9fa; border-left: 4px solid #3498db; border-radius: 4px;">')
                in_blockquote = True
            html_lines.append(f'<p style="margin: 8px 0; font-size: 15px; line-height: 1.8; color: #555;">{process_inline(line[2:])}</p>')
        # 图片
        elif re.match(r'!\[.*?\]\(.*?\)', line):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt = match.group(1)
                src = match.group(2)
                html_lines.append(f'<p style="text-align: center; margin: 20px 0;"><img src="{src}" alt="{alt}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1);" /></p>')
                if alt:
                    html_lines.append(f'<p style="text-align: center; margin: -10px 0 20px 0; font-size: 14px; color: #999; font-style: italic;">▲ {alt}</p>')
        # 普通段落
        else:
            html_lines.append(f'<p style="margin: 12px 0; font-size: 16px; line-height: 1.8; color: #333; text-align: justify;">{process_inline(line)}</p>')
        
        i += 1
    
    # 关闭未关闭的标签
    if in_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    
    return '\n'.join(html_lines)


def process_inline(text):
    """处理行内元素"""
    # 加粗
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #e74c3c; font-weight: bold;">\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.*?)\*', r'<em style="font-style: italic; color: #7f8c8d;">\1</em>', text)
    # 行内代码
    text = re.sub(r'`(.*?)`', r'<code style="background-color: #f1f2f6; padding: 2px 6px; border-radius: 3px; color: #e74c3c; font-family: Consolas, Monaco, monospace; font-size: 14px;">\1</code>', text)
    # 链接
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" style="color: #3498db; text-decoration: none; border-bottom: 1px solid #3498db;">\1</a>', text)
    return text


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Markdown 转微信公众号 HTML 转换器（简洁大气版）",
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
    
    args = parser.parse_args()
    
    try:
        # 读取 Markdown 文件
        with open(args.input, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        # 转换为 HTML
        html_content = markdown_to_html_clean(markdown_text)
        
        # 包装在 section 中
        final_html = f'<section style="padding: 20px; max-width: 100%; box-sizing: border-box;">\n{html_content}\n</section>'
        
        # 写入 HTML 文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"✅ 转换成功！")
        print(f"   输入: {args.input}")
        print(f"   输出: {args.output}")
        print(f"   样式: 简洁大气版")
        print(f"   特点: 优化列表显示，去掉多余背景色")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

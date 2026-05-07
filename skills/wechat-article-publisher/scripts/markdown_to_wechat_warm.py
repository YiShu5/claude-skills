#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 转换器（暖色风格）

专为春季、美食、生活类文章设计的暖色调排版。

使用方法：
    python3 markdown_to_wechat_warm.py --input article.md --output article.html
"""

import os
import sys
import argparse
import re


def markdown_to_html_warm(markdown_text):
    """
    将 Markdown 转换为暖色风格的微信公众号 HTML
    
    暖色配色方案：
    - 主色：珊瑚橙 #ff6b6b
    - 辅助色：温暖粉 #ffeaa7
    - 文字：深棕 #2d3436
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
                code_content = code_content.replace('<', '&lt;').replace('>', '&gt;')
                html_lines.append(f'<section style="margin: 16px 8px; padding: 16px; background-color: #fff5f5; border-radius: 8px; border: 1px solid #ffe0e0; overflow-x: auto;"><code style="display: block; font-family: Consolas, Monaco, \'Courier New\', monospace; font-size: 14px; line-height: 1.6; color: #2d3436; white-space: pre;">{code_content}</code></section>')
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
            content = process_inline(line[2:])
            html_lines.append(f'<h1 style="margin: 30px 8px 20px; padding: 0; font-size: 24px; font-weight: 600; line-height: 1.4; color: #ff6b6b; text-align: center;">{content}</h1>')
        elif line.startswith('## '):
            content = process_inline(line[3:])
            html_lines.append(f'<h2 style="margin: 28px 8px 16px; padding: 0 0 8px; font-size: 20px; font-weight: 600; line-height: 1.4; color: #ff6b6b; border-bottom: 2px solid #ffeaa7;">{content}</h2>')
        elif line.startswith('### '):
            content = process_inline(line[4:])
            html_lines.append(f'<h3 style="margin: 24px 8px 12px; padding: 0 0 0 12px; font-size: 18px; font-weight: 600; line-height: 1.4; color: #ff6b6b; border-left: 4px solid #ff6b6b;">{content}</h3>')
        elif line.startswith('#### '):
            content = process_inline(line[5:])
            html_lines.append(f'<h4 style="margin: 20px 8px 10px; padding: 0; font-size: 16px; font-weight: 600; line-height: 1.4; color: #ff6b6b;">{content}</h4>')
        # 分隔线
        elif line.strip() == '---' or line.strip() == '***':
            html_lines.append('<hr style="margin: 24px 8px; border: none; border-top: 1px solid #ffeaa7;" />')
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul style="margin: 12px 8px; padding-left: 28px; list-style-type: disc;">')
                in_list = True
            content = process_inline(line[2:])
            html_lines.append(f'<li style="margin: 6px 0; font-size: 15px; line-height: 1.8; color: #2d3436;">{content}</li>')
        # 有序列表
        elif re.match(r'^\d+\.\s', line):
            if not in_ordered_list:
                html_lines.append('<ol style="margin: 12px 8px; padding-left: 28px; list-style-type: decimal;">')
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s', '', line)
            content = process_inline(content)
            html_lines.append(f'<li style="margin: 6px 0; font-size: 15px; line-height: 1.8; color: #2d3436;">{content}</li>')
        # 引用
        elif line.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote style="margin: 16px 8px; padding: 12px 16px; background-color: #fff5f5; border-left: 4px solid #ff6b6b; border-radius: 0 8px 8px 0;">')
                in_blockquote = True
            content = process_inline(line[2:])
            html_lines.append(f'<p style="margin: 6px 0; font-size: 14px; line-height: 1.8; color: #636e72;">{content}</p>')
        # 图片
        elif re.match(r'!\[.*?\]\(.*?\)', line):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt = match.group(1)
                src = match.group(2)
                html_lines.append(f'<section style="margin: 24px 8px; text-align: center;"><img src="{src}" alt="{alt}" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(255,107,107,0.15);" />')
                if alt:
                    html_lines.append(f'<p style="margin: 10px 0 0; font-size: 13px; line-height: 1.6; color: #b2bec3; font-style: italic;">▲ {alt}</p>')
                html_lines.append('</section>')
        # 普通段落
        else:
            content = process_inline(line)
            html_lines.append(f'<p style="margin: 12px 8px; font-size: 15px; line-height: 1.8; color: #2d3436; text-align: justify; word-wrap: break-word;">{content}</p>')
        
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
    # 加粗 - 使用珊瑚橙强调
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #ff6b6b; font-weight: 600;">\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.*?)\*', r'<em style="font-style: italic; color: #636e72;">\1</em>', text)
    # 行内代码
    text = re.sub(r'`(.*?)`', r'<code style="padding: 2px 6px; background-color: #fff5f5; border-radius: 3px; color: #ff6b6b; font-family: Consolas, Monaco, monospace; font-size: 14px;">\1</code>', text)
    # 链接
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" style="color: #ff6b6b; text-decoration: none; border-bottom: 1px solid #ff6b6b;">\1</a>', text)
    return text


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Markdown 转微信公众号 HTML 转换器（暖色风格）",
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
        html_content = markdown_to_html_warm(markdown_text)
        
        # 包装在 section 中
        final_html = f'''<section style="padding: 16px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;">
{html_content}
</section>'''
        
        # 写入 HTML 文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"✅ 转换成功！")
        print(f"   输入: {args.input}")
        print(f"   输出: {args.output}")
        print(f"   风格: 暖色风格（珊瑚橙）")
        print(f"   适合: 春季、美食、生活类文章")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

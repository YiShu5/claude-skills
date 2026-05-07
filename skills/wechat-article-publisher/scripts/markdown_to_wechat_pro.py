#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 转换器（专业版）

基于 Markdown Nice 的设计理念：
- 极简设计，专业排版
- 完美的列表显示
- 合理的间距和层级
- 优雅的配色方案

使用方法：
    python3 markdown_to_wechat_pro.py --input article.md --output article.html
"""

import os
import sys
import argparse
import re


def markdown_to_html_pro(markdown_text):
    """
    将 Markdown 转换为专业的微信公众号 HTML
    
    设计原则：
    1. 使用微信原生列表样式，避免重复符号
    2. 极简配色，黑白灰为主，点缀色为辅
    3. 合理的间距，让内容呼吸
    4. 清晰的层级，一目了然
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
                html_lines.append(f'<section style="margin: 16px 8px; padding: 16px; background-color: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8; overflow-x: auto;"><code style="display: block; font-family: Consolas, Monaco, \'Courier New\', monospace; font-size: 14px; line-height: 1.6; color: #24292e; white-space: pre;">{code_content}</code></section>')
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
            html_lines.append(f'<h1 style="margin: 30px 8px 20px; padding: 0; font-size: 24px; font-weight: 600; line-height: 1.4; color: #1a1a1a; text-align: center;">{content}</h1>')
        elif line.startswith('## '):
            content = process_inline(line[3:])
            html_lines.append(f'<h2 style="margin: 28px 8px 16px; padding: 0 0 8px; font-size: 20px; font-weight: 600; line-height: 1.4; color: #1a1a1a; border-bottom: 2px solid #e8e8e8;">{content}</h2>')
        elif line.startswith('### '):
            content = process_inline(line[4:])
            html_lines.append(f'<h3 style="margin: 24px 8px 12px; padding: 0 0 0 12px; font-size: 18px; font-weight: 600; line-height: 1.4; color: #1a1a1a; border-left: 4px solid #3370ff;">{content}</h3>')
        elif line.startswith('#### '):
            content = process_inline(line[5:])
            html_lines.append(f'<h4 style="margin: 20px 8px 10px; padding: 0; font-size: 16px; font-weight: 600; line-height: 1.4; color: #1a1a1a;">{content}</h4>')
        # 分隔线
        elif line.strip() == '---' or line.strip() == '***':
            html_lines.append('<hr style="margin: 24px 8px; border: none; border-top: 1px solid #e8e8e8;" />')
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul style="margin: 12px 8px; padding-left: 28px; list-style-type: disc;">')
                in_list = True
            content = process_inline(line[2:])
            html_lines.append(f'<li style="margin: 6px 0; font-size: 15px; line-height: 1.8; color: #333333;">{content}</li>')
        # 有序列表
        elif re.match(r'^\d+\.\s', line):
            if not in_ordered_list:
                html_lines.append('<ol style="margin: 12px 8px; padding-left: 28px; list-style-type: decimal;">')
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s', '', line)
            content = process_inline(content)
            html_lines.append(f'<li style="margin: 6px 0; font-size: 15px; line-height: 1.8; color: #333333;">{content}</li>')
        # 引用
        elif line.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote style="margin: 16px 8px; padding: 12px 16px; background-color: #f8f9fa; border-left: 4px solid #3370ff; border-radius: 0 4px 4px 0;">')
                in_blockquote = True
            content = process_inline(line[2:])
            html_lines.append(f'<p style="margin: 6px 0; font-size: 14px; line-height: 1.8; color: #666666;">{content}</p>')
        # 图片
        elif re.match(r'!\[.*?\]\(.*?\)', line):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt = match.group(1)
                src = match.group(2)
                html_lines.append(f'<section style="margin: 24px 8px; text-align: center;"><img src="{src}" alt="{alt}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);" />')
                if alt:
                    html_lines.append(f'<p style="margin: 10px 0 0; font-size: 13px; line-height: 1.6; color: #999999; font-style: italic;">▲ {alt}</p>')
                html_lines.append('</section>')
        # 普通段落
        else:
            content = process_inline(line)
            html_lines.append(f'<p style="margin: 12px 8px; font-size: 15px; line-height: 1.8; color: #333333; text-align: justify; word-wrap: break-word;">{content}</p>')
        
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
    # 加粗 - 使用深色强调
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #1a1a1a; font-weight: 600;">\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.*?)\*', r'<em style="font-style: italic; color: #666666;">\1</em>', text)
    # 行内代码 - 使用浅灰背景
    text = re.sub(r'`(.*?)`', r'<code style="padding: 2px 6px; background-color: #f6f8fa; border-radius: 3px; color: #d73a49; font-family: Consolas, Monaco, monospace; font-size: 14px;">\1</code>', text)
    # 链接 - 使用蓝色
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" style="color: #3370ff; text-decoration: none; border-bottom: 1px solid #3370ff;">\1</a>', text)
    return text


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Markdown 转微信公众号 HTML 转换器（专业版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
设计理念：
  - 极简设计，专业排版
  - 黑白灰为主，蓝色点缀
  - 完美的列表显示
  - 合理的间距和层级
        """
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
        html_content = markdown_to_html_pro(markdown_text)
        
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
        print(f"   风格: 专业版（极简设计）")
        print(f"   特点: 完美列表、合理间距、清晰层级")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

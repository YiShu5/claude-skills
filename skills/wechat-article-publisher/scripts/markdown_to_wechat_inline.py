#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 转换器（内联样式版本）

微信公众号编辑器不支持 <style> 标签，必须使用内联样式。

使用方法：
    python3 markdown_to_wechat_inline.py --input article.md --style warm --output article.html
"""

import os
import sys
import argparse
import re
from html.parser import HTMLParser


class InlineStyler(HTMLParser):
    """HTML 解析器，添加内联样式"""
    
    def __init__(self, style_name="warm"):
        super().__init__()
        self.style_name = style_name
        self.output = []
        self.in_code = False
        self.in_pre = False
        
    def handle_starttag(self, tag, attrs):
        """处理开始标签"""
        attrs_dict = dict(attrs)
        style = self.get_style_for_tag(tag, attrs_dict)
        
        # 构建新的属性字符串
        new_attrs = []
        for key, value in attrs:
            if key != 'style':  # 移除原有的 style
                new_attrs.append(f'{key}="{value}"')
        
        if style:
            new_attrs.append(f'style="{style}"')
        
        attrs_str = ' '.join(new_attrs)
        if attrs_str:
            self.output.append(f'<{tag} {attrs_str}>')
        else:
            self.output.append(f'<{tag}>')
        
        if tag == 'code':
            self.in_code = True
        if tag == 'pre':
            self.in_pre = True
    
    def handle_endtag(self, tag):
        """处理结束标签"""
        self.output.append(f'</{tag}>')
        if tag == 'code':
            self.in_code = False
        if tag == 'pre':
            self.in_pre = False
    
    def handle_data(self, data):
        """处理文本数据"""
        self.output.append(data)
    
    def get_html(self):
        """获取处理后的 HTML"""
        return ''.join(self.output)
    
    def get_style_for_tag(self, tag, attrs):
        """根据标签获取内联样式"""
        if self.style_name == "warm":
            return self.get_warm_style(tag, attrs)
        elif self.style_name == "fresh":
            return self.get_fresh_style(tag, attrs)
        elif self.style_name == "business":
            return self.get_business_style(tag, attrs)
        elif self.style_name == "simple":
            return self.get_simple_style(tag, attrs)
        return ""
    
    def get_warm_style(self, tag, attrs):
        """温暖风格 - 橙红色系"""
        styles = {
            'p': 'font-size: 16px; padding: 19px; text-align: left; line-height: 1.75em; margin-bottom: 10px; background-color: rgb(255, 251, 244); box-sizing: border-box;',
            'h1': 'font-size: 24px; font-weight: bold; color: rgb(239, 112, 96); text-align: center; margin: 20px 0; padding: 0;',
            'h2': 'font-size: 20px; font-weight: bold; background: rgb(239, 112, 96); color: #ffffff; padding: 8px 15px; border-radius: 4px; margin: 30px 0 20px 0; display: inline-block;',
            'h3': 'font-size: 18px; font-weight: bold; color: rgb(239, 112, 96); margin: 20px 0 10px 0; padding: 0;',
            'ul': 'padding-left: 20px; margin: 10px 0;',
            'ol': 'padding-left: 20px; margin: 10px 0;',
            'li': 'font-size: 15px; line-height: 1.75em; padding: 5px 0; margin: 0;',
            'blockquote': 'border-left: 4px solid rgb(239, 112, 96); background: #fff9f9; padding: 10px 15px; margin: 10px 0;',
            'a': 'color: rgb(239, 112, 96); text-decoration: none; border-bottom: 1px solid rgb(239, 112, 96);',
            'strong': 'color: rgb(255, 79, 121); font-weight: bold;',
            'em': 'font-style: italic;',
            'hr': 'border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;',
            'img': 'max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: block; margin: 20px auto;',
            'code': 'background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; color: rgb(239, 112, 96); font-family: Courier New, monospace; font-size: 14px;',
            'pre': 'background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 10px 0;',
        }
        return styles.get(tag, '')
    
    def get_fresh_style(self, tag, attrs):
        """清新风格 - 绿色系"""
        styles = {
            'p': 'font-size: 16px; padding: 19px; text-align: left; line-height: 1.75em; margin-bottom: 10px; background-color: rgb(239, 251, 236); box-sizing: border-box;',
            'h1': 'font-size: 24px; font-weight: bold; color: rgb(37, 132, 181); text-align: center; margin: 20px 0; padding: 0 0 10px 0; border-bottom: 2px solid rgb(37, 132, 181);',
            'h2': 'font-size: 20px; font-weight: bold; color: rgb(37, 132, 181); padding: 8px 15px; margin: 30px 0 20px 0; border-bottom: 4px solid rgb(37, 132, 181); display: inline-block;',
            'h3': 'font-size: 18px; font-weight: bold; color: rgb(37, 132, 181); margin: 20px 0 10px 0; padding: 5px 10px; border-bottom: 2px solid rgb(37, 132, 181); display: inline-block;',
            'ul': 'padding-left: 20px; margin: 10px 0;',
            'ol': 'padding-left: 20px; margin: 10px 0;',
            'li': 'font-size: 16px; line-height: 1.75em; padding: 5px 0; margin: 0;',
            'blockquote': 'border: 1px dashed rgb(37, 132, 181); background: transparent; padding: 10px 15px; margin: 10px 0;',
            'a': 'color: rgb(37, 132, 181); text-decoration: none; border-bottom: 1px solid rgb(37, 132, 181);',
            'strong': 'color: rgb(37, 132, 181); font-weight: bold;',
            'em': 'color: rgb(37, 132, 181); font-style: italic;',
            'hr': 'border: none; border-top: 1px solid rgb(37, 132, 181); margin: 20px 0;',
            'img': 'max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: block; margin: 20px auto;',
            'code': 'background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; color: rgb(37, 132, 181); font-family: Courier New, monospace; font-size: 14px;',
            'pre': 'background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 10px 0;',
        }
        return styles.get(tag, '')
    
    def get_business_style(self, tag, attrs):
        """商务风格 - 蓝灰色系"""
        styles = {
            'p': 'font-size: 16px; padding: 19px; text-align: left; line-height: 1.75em; margin-bottom: 10px; background-color: rgba(72, 126, 252, 0.09); box-sizing: border-box;',
            'h1': 'font-size: 24px; font-weight: bold; color: rgb(160, 160, 160); text-align: center; margin: 20px 0; padding: 0 0 10px 0; border-bottom: 2px solid rgb(198, 196, 196);',
            'h2': 'font-size: 18px; font-weight: bold; background-color: rgb(33, 33, 34); color: rgb(255, 255, 255); padding: 10px 30px; margin: 30px 0 20px 0; border-radius: 0 50px 50px 0; display: inline-block;',
            'h3': 'font-size: 17px; font-weight: bold; color: rgb(33, 33, 34); margin: 20px 0 10px 0; padding: 6px 10px; border-top: 2px solid rgb(33, 33, 34); display: inline-block;',
            'ul': 'padding-left: 20px; margin: 10px 0;',
            'ol': 'padding-left: 20px; margin: 10px 0;',
            'li': 'font-size: 15px; line-height: 1.75em; padding: 5px 0; margin: 0;',
            'blockquote': 'border-left: 4px solid rgb(221, 221, 221); padding: 10px 15px; margin: 10px 0; color: rgb(119, 119, 119);',
            'a': 'color: rgb(239, 112, 96); text-decoration: none; border-bottom: 1px solid rgb(239, 112, 96);',
            'strong': 'color: rgb(255, 79, 121); font-weight: bold;',
            'em': 'font-style: italic;',
            'hr': 'border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;',
            'img': 'max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: block; margin: 20px auto;',
            'code': 'background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; color: rgb(239, 112, 96); font-family: Courier New, monospace; font-size: 14px;',
            'pre': 'background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 10px 0;',
        }
        return styles.get(tag, '')
    
    def get_simple_style(self, tag, attrs):
        """简约风格 - 黑白灰"""
        styles = {
            'p': 'font-size: 16px; padding: 10px 0; text-align: left; line-height: 1.75em; margin-bottom: 10px; color: #333;',
            'h1': 'font-size: 24px; font-weight: bold; color: #333; text-align: center; margin: 20px 0; padding: 0 0 10px 0; border-bottom: 2px solid #333;',
            'h2': 'font-size: 20px; font-weight: bold; color: #333; margin: 30px 0 15px 0; padding: 0 0 0 10px; border-left: 4px solid #333;',
            'h3': 'font-size: 18px; font-weight: bold; color: #666; margin: 20px 0 10px 0; padding: 0;',
            'ul': 'padding-left: 20px; margin: 10px 0;',
            'ol': 'padding-left: 20px; margin: 10px 0;',
            'li': 'font-size: 16px; line-height: 1.75em; padding: 5px 0; margin: 0;',
            'blockquote': 'border-left: 4px solid #ccc; background: #f9f9f9; padding: 10px 15px; margin: 10px 0; color: #666;',
            'a': 'color: #333; text-decoration: none; border-bottom: 1px solid #333;',
            'strong': 'color: #000; font-weight: bold;',
            'em': 'font-style: italic; color: #666;',
            'hr': 'border: none; border-top: 1px solid #ddd; margin: 20px 0;',
            'img': 'max-width: 100%; border-radius: 4px; display: block; margin: 20px auto;',
            'code': 'background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; color: #333; font-family: Courier New, monospace; font-size: 14px;',
            'pre': 'background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 10px 0; border: 1px solid #ddd;',
        }
        return styles.get(tag, '')


def markdown_to_html_basic(markdown_text):
    """
    简单的 Markdown 转 HTML（不依赖 markdown 库）
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
                html_lines.append('<pre><code>' + '\n'.join(code_block_lines) + '</code></pre>')
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
            html_lines.append(f'<h1>{process_inline(line[2:])}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{process_inline(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{process_inline(line[4:])}</h3>')
        # 分隔线
        elif line.strip() == '---' or line.strip() == '***':
            html_lines.append('<hr />')
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{process_inline(line[2:])}</li>')
        # 有序列表
        elif re.match(r'^\d+\.\s', line):
            if not in_ordered_list:
                html_lines.append('<ol>')
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s', '', line)
            html_lines.append(f'<li>{process_inline(content)}</li>')
        # 引用
        elif line.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            html_lines.append(f'<p>{process_inline(line[2:])}</p>')
        # 图片
        elif re.match(r'!\[.*?\]\(.*?\)', line):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt = match.group(1)
                src = match.group(2)
                html_lines.append(f'<p style="text-align: center;"><img src="{src}" alt="{alt}" /></p>')
        # 普通段落
        else:
            html_lines.append(f'<p>{process_inline(line)}</p>')
        
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
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # 行内代码
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # 链接
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    return text


def add_inline_styles(html_content, style_name="warm"):
    """为 HTML 添加内联样式"""
    styler = InlineStyler(style_name)
    styler.feed(html_content)
    return styler.get_html()


def markdown_to_wechat_html(markdown_text, style="warm"):
    """
    将 Markdown 转换为带内联样式的微信公众号 HTML
    
    Args:
        markdown_text: Markdown 文本
        style: 样式名称 (warm/fresh/business/simple)
        
    Returns:
        str: HTML 文本（带内联样式）
    """
    # 转换 Markdown 到基础 HTML
    html_content = markdown_to_html_basic(markdown_text)
    
    # 添加内联样式
    styled_html = add_inline_styles(html_content, style)
    
    # 包装在 section 中
    final_html = f'<section>\n{styled_html}\n</section>'
    
    return final_html


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Markdown 转微信公众号 HTML 转换器（内联样式版本）",
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
        "--style", "-s",
        choices=["warm", "fresh", "business", "simple"],
        default="warm",
        help="样式风格: warm(温暖橙红), fresh(清新绿色), business(商务蓝灰), simple(简约黑白)"
    )
    
    args = parser.parse_args()
    
    try:
        # 读取 Markdown 文件
        with open(args.input, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        # 转换为 HTML
        html_content = markdown_to_wechat_html(markdown_text, args.style)
        
        # 写入 HTML 文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 转换成功！")
        print(f"   输入: {args.input}")
        print(f"   输出: {args.output}")
        print(f"   样式: {args.style}")
        print(f"   使用内联样式，兼容微信公众号编辑器")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 转换器（doocs/md 风格）

参考 doocs/md 项目的优秀设计，提供多种专业主题。

使用方法：
    python3 markdown_to_wechat_doocs.py --input article.md --output article.html --theme default
    
支持主题：
    - default: 默认主题（简洁优雅）
    - green: 绿意主题（清新自然）
    - purple: 紫色主题（优雅高贵）
    - orange: 橙心主题（温暖活力）
    - cyan: 青色主题（清爽专业）
"""

import os
import sys
import argparse
import re


# doocs/md 风格的主题配置
THEMES = {
    "default": {
        "name": "默认主题",
        "primary": "#3f51b5",
        "text": "#2b2b2b",
        "text_light": "#595959",
        "bg_light": "#f8f9fa",
        "border": "#e0e0e0",
        "code_bg": "#f6f8fa",
        "quote_bg": "#f8f9fa",
        "quote_border": "#3f51b5",
    },
    "green": {
        "name": "绿意主题",
        "primary": "#3eaf7c",
        "text": "#2c3e50",
        "text_light": "#6c757d",
        "bg_light": "#f3f5f7",
        "border": "#eaecef",
        "code_bg": "#f3f5f7",
        "quote_bg": "#f3f5f7",
        "quote_border": "#3eaf7c",
    },
    "purple": {
        "name": "紫色主题",
        "primary": "#8e44ad",
        "text": "#2c3e50",
        "text_light": "#6c757d",
        "bg_light": "#f8f9fa",
        "border": "#e0e0e0",
        "code_bg": "#f8f9fa",
        "quote_bg": "#f8f9fa",
        "quote_border": "#8e44ad",
    },
    "orange": {
        "name": "橙心主题",
        "primary": "#ff6800",
        "text": "#2c3e50",
        "text_light": "#6c757d",
        "bg_light": "#fff8f0",
        "border": "#ffe4cc",
        "code_bg": "#fff8f0",
        "quote_bg": "#fff8f0",
        "quote_border": "#ff6800",
    },
    "cyan": {
        "name": "青色主题",
        "primary": "#00bcd4",
        "text": "#2c3e50",
        "text_light": "#6c757d",
        "bg_light": "#f0f9ff",
        "border": "#d1ecf1",
        "code_bg": "#f0f9ff",
        "quote_bg": "#f0f9ff",
        "quote_border": "#00bcd4",
    }
}


def get_theme(theme_name):
    """获取主题配置"""
    return THEMES.get(theme_name, THEMES["default"])


def markdown_to_html_doocs(markdown_text, theme_name="default"):
    """
    将 Markdown 转换为 doocs/md 风格的 HTML
    """
    theme = get_theme(theme_name)
    
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
                # 代码块内换行用 <br> 标签，确保微信公众号正确显示
                code_content = code_content.replace('\n', '<br>')
                html_lines.append(f'''<section style="margin: 16px 8px; padding: 16px; background-color: {theme["code_bg"]}; border-radius: 4px; border: 1px solid {theme["border"]}; overflow-x: auto;"><code style="display: block; font-family: 'Operator Mono', 'Fira Code', Consolas, Monaco, 'Courier New', monospace; font-size: 14px; line-height: 1.6; color: {theme["text"]};">{code_content}</code></section>''')
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
            content = process_inline(line[2:], theme)
            html_lines.append(f'''<h1 style="margin: 30px 8px 20px; padding: 0; font-size: 24px; font-weight: 600; line-height: 1.4; color: {theme["text"]}; text-align: center;">{content}</h1>''')
        elif line.startswith('## '):
            content = process_inline(line[3:], theme)
            html_lines.append(f'''<h2 style="margin: 28px 8px 16px; padding: 0 0 8px; font-size: 20px; font-weight: 600; line-height: 1.4; color: {theme["text"]}; border-bottom: 2px solid {theme["primary"]};">{content}</h2>''')
        elif line.startswith('### '):
            content = process_inline(line[4:], theme)
            html_lines.append(f'''<h3 style="margin: 24px 8px 12px; padding: 0 0 0 12px; font-size: 18px; font-weight: 600; line-height: 1.4; color: {theme["text"]}; border-left: 4px solid {theme["primary"]};">{content}</h3>''')
        elif line.startswith('#### '):
            content = process_inline(line[5:], theme)
            html_lines.append(f'''<h4 style="margin: 20px 8px 10px; padding: 0; font-size: 16px; font-weight: 600; line-height: 1.4; color: {theme["text"]};">{content}</h4>''')
        # 分隔线
        elif line.strip() == '---' or line.strip() == '***':
            html_lines.append(f'<hr style="margin: 24px 8px; border: none; border-top: 1px solid {theme["border"]};" />')
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append(f'<ul style="margin: 12px 8px; padding-left: 28px; list-style-type: disc;">')
                in_list = True
            content = process_inline(line[2:], theme)
            html_lines.append(f'''<li style="margin: 6px 0; font-size: 15px; line-height: 1.8; color: {theme["text"]};">{content}</li>''')
        # 有序列表
        elif re.match(r'^\d+\.\s', line):
            if not in_ordered_list:
                html_lines.append(f'<ol style="margin: 12px 8px; padding-left: 28px; list-style-type: decimal;">')
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s', '', line)
            content = process_inline(content, theme)
            html_lines.append(f'''<li style="margin: 6px 0; font-size: 15px; line-height: 1.8; color: {theme["text"]};">{content}</li>''')
        # 引用
        elif line.startswith('> '):
            if not in_blockquote:
                html_lines.append(f'''<blockquote style="margin: 16px 8px; padding: 12px 16px; background-color: {theme["quote_bg"]}; border-left: 4px solid {theme["quote_border"]}; border-radius: 0 4px 4px 0;">''')
                in_blockquote = True
            content = process_inline(line[2:], theme)
            html_lines.append(f'''<p style="margin: 6px 0; font-size: 14px; line-height: 1.8; color: {theme["text_light"]};">{content}</p>''')
        # 图片
        elif re.match(r'!\[.*?\]\(.*?\)', line):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt = match.group(1)
                src = match.group(2)
                html_lines.append(f'''<section style="margin: 24px 8px; text-align: center;"><img src="{src}" alt="{alt}" style="max-width: 100%; height: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />''')
                if alt:
                    html_lines.append(f'''<p style="margin: 10px 0 0; font-size: 13px; line-height: 1.6; color: {theme["text_light"]}; font-style: italic;">▲ {alt}</p>''')
                html_lines.append('</section>')
        # 普通段落
        else:
            content = process_inline(line, theme)
            html_lines.append(f'''<p style="margin: 12px 8px; font-size: 15px; line-height: 1.8; color: {theme["text"]}; text-align: justify; word-wrap: break-word;">{content}</p>''')
        
        i += 1
    
    # 关闭未关闭的标签
    if in_list:
        # 移除ul/li之间的换行符，避免微信公众号显示多余空行
        html_lines.append('</ul>')
    if in_ordered_list:
        # 移除ol/li之间的换行符，避免微信公众号显示多余空行
        html_lines.append('</ol>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    
    # 移除列表项之间的换行符，避免微信公众号渲染多余空行
    result = '\n'.join(html_lines)
    result = result.replace('</li>\n<li', '</li><li')
    result = result.replace('</li>\n</ol>', '</li></ol>')
    result = result.replace('</li>\n</ul>', '</li></ul>')
    
    # 修复微信公众号列表渲染问题：将ol/ul转换为段落格式
    result = fix_wechat_list_rendering(result, theme)
    
    return result


def process_inline(text, theme):
    """处理行内元素"""
    # 加粗
    text = re.sub(r'\*\*(.*?)\*\*', rf'<strong style="color: {theme["primary"]}; font-weight: 600;">\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.*?)\*', rf'<em style="font-style: italic;">\1</em>', text)
    # 行内代码
    text = re.sub(r'`(.*?)`', rf'<code style="padding: 2px 6px; background-color: {theme["code_bg"]}; border-radius: 3px; color: {theme["primary"]}; font-family: Consolas, Monaco, monospace; font-size: 14px;">\1</code>', text)
    # 链接
    text = re.sub(r'\[(.*?)\]\((.*?)\)', rf'<a href="\2" style="color: {theme["primary"]}; text-decoration: none; border-bottom: 1px solid {theme["primary"]};">\1</a>', text)
    return text


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Markdown 转微信公众号 HTML 转换器（doocs/md 风格）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持主题：
  default  - 默认主题（简洁优雅）
  green    - 绿意主题（清新自然）
  purple   - 紫色主题（优雅高贵）
  orange   - 橙心主题（温暖活力）
  cyan     - 青色主题（清爽专业）
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
    
    parser.add_argument(
        "--theme", "-t",
        choices=["default", "green", "purple", "orange", "cyan"],
        default="default",
        help="主题选择"
    )
    
    args = parser.parse_args()
    
    try:
        # 读取 Markdown 文件
        with open(args.input, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        # 自动读取 footer.md 并拼接到文章末尾
        footer_path = os.path.join(os.path.dirname(__file__), '..', 'footer.md')
        if os.path.exists(footer_path):
            with open(footer_path, 'r', encoding='utf-8') as f:
                footer_content = f.read()
            if footer_content:
                markdown_text = markdown_text.rstrip() + '\n\n' + footer_content
        
        # 转换为 HTML
        html_content = markdown_to_html_doocs(markdown_text, args.theme)
        
        # 获取主题信息
        theme = get_theme(args.theme)
        
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
        print(f"   主题: {theme['name']}")
        print(f"   风格: doocs/md")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def fix_wechat_list_rendering(html_content, theme):
    """
    修复微信公众号列表渲染问题
    微信公众号对ol/ul标签的渲染有问题，会有多余空行
    解决方案：使用div+span替代ol/ul
    """
    # 修复ol/ul标签前后的换行符（保持ol/ul标签名）
    html_content = re.sub(r'<ol([^>]*)>\n', r'<ol\g<1>>\n', html_content)
    html_content = re.sub(r'\n</ol>', r'\n</ol>', html_content)
    html_content = re.sub(r'<ul([^>]*)>\n', r'<ul\g<1>>\n', html_content)
    html_content = re.sub(r'\n</ul>', r'\n</ul>', html_content)
    
    # 修复代码块后的空行，确保代码块之间有适当间距
    html_content = re.sub(r'</code></section>\n+<p', r'</code></section><br><p', html_content)
    html_content = re.sub(r'</code></section>\n+<h', r'</code></section><br><h', html_content)
    html_content = re.sub(r'</code></section>\n+<ul', r'</code></section><br><ul', html_content)
    html_content = re.sub(r'</code></section>\n+<ol', r'</code></section><br><ol', html_content)
    html_content = re.sub(r'</code></section>\n+<section', r'</code></section><br><section', html_content)
    
    # 修复section之间的空行
    html_content = re.sub(r'</section>\n+<section', r'</section><br><section', html_content)
    
    # 将ol（有序列表）转换为段落格式
    def replace_ol(match):
        items = re.findall(r'<li[^>]*>(.*?)</li>', match.group(), re.DOTALL)
        result = []
        for i, item in enumerate(items, 1):
            result.append(f'<p style="margin: 4px 8px; font-size: 15px; line-height: 1.8; color: {theme["text"]}; text-align: justify; word-wrap: break-word;"><strong style="color: {theme["primary"]}; font-weight: 600;">{i}. </strong>{item}</p>')
        return '\n'.join(result)
    
    html_content = re.sub(r'<ol[^>]*>.*?</ol>', replace_ol, html_content, flags=re.DOTALL)
    
    # 将ul（无序列表）转换为段落格式
    def replace_ul(match):
        items = re.findall(r'<li[^>]*>(.*?)</li>', match.group(), re.DOTALL)
        result = []
        for item in items:
            result.append(f'<p style="margin: 4px 8px; font-size: 15px; line-height: 1.8; color: {theme["text"]}; text-align: justify; word-wrap: break-word;">• {item}</p>')
        return '\n'.join(result)
    
    html_content = re.sub(r'<ul[^>]*>.*?</ul>', replace_ul, html_content, flags=re.DOTALL)
    
    return html_content


if __name__ == "__main__":
    main()

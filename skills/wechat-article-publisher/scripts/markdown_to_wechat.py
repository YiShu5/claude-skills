#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 转换器

支持多种样式模板：
1. 清新风格 - 绿色系
2. 商务风格 - 蓝色系
3. 温暖风格 - 橙红色系
4. 简约风格 - 黑白灰

使用方法：
    python3 markdown_to_wechat.py --input article.md --style warm --output article.html
"""

import os
import sys
import argparse
import markdown
from markdown.extensions import tables, fenced_code, codehilite

# 样式模板
STYLES = {
    "warm": """
/* 温暖风格 - 橙红色系 */
#nice {
  padding: 20px;
}

#nice p {
  font-size: 16px;
  padding: 19px;
  text-align: left;
  display: inline-block;
  width: 100%;
  background-color: rgb(255, 251, 244);
  line-height: 1.75em;
  margin-bottom: 10px;
}

#nice h1 {
  text-align: center;
  margin-bottom: 20px;
}

#nice h1 {
  font-size: 24px;
  font-weight: bold;
  color: rgb(239, 112, 96);
}

#nice h2 {
  border-bottom: 2px solid rgb(239, 112, 96);
  font-size: 1.3em;
  margin-top: 30px;
  margin-bottom: 20px;
}

#nice h2 {
  display: inline-block;
  font-weight: bold;
  background: rgb(239, 112, 96);
  color: #ffffff;
  padding: 3px 10px 1px;
  border-top-right-radius: 3px;
  border-top-left-radius: 3px;
  margin-right: 3px;
  font-size: 18px;
}

#nice h2:after {
  display: inline-block;
  content: " ";
  vertical-align: bottom;
  border-bottom: 36px solid #efebe9;
  border-right: 20px solid transparent;
}

#nice h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: bold;
  color: rgb(239, 112, 96);
}

#nice ul, #nice ol {
  padding-left: 20px;
}

#nice li {
  font-size: 15px;
  line-height: 1.75em;
  background-color: transparent;
  padding: 5px 0;
}

#nice blockquote {
  border-left: 4px solid rgb(239, 112, 96);
  background: #fff9f9;
  padding: 10px 15px;
  margin: 10px 0;
}

#nice blockquote p {
  font-size: 15px;
  line-height: 1.75em;
  background-color: transparent;
  padding: 5px 0;
}

#nice a {
  color: rgb(239, 112, 96);
  border-bottom: 1px solid rgb(239, 112, 96);
  text-decoration: none;
}

#nice strong {
  color: rgb(255, 79, 121);
  font-weight: bold;
}

#nice em {
  font-style: italic;
}

#nice hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 20px 0;
}

#nice img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: block;
  margin: 20px auto;
}

#nice code {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  color: rgb(239, 112, 96);
  font-family: 'Courier New', monospace;
}

#nice pre {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
}

#nice pre code {
  background-color: transparent;
  padding: 0;
  color: #333;
}
""",
    
    "fresh": """
/* 清新风格 - 绿色系 */
#nice {
  padding: 20px;
}

#nice p {
  font-size: 16px;
  padding: 19px;
  text-align: left;
  display: inline-block;
  width: 100%;
  background-color: rgb(239, 251, 236);
  line-height: 1.75em;
  margin-bottom: 10px;
}

#nice h1 {
  line-height: 28px;
  border-bottom: 1px solid rgb(37,132,181);
  text-align: center;
  margin-bottom: 20px;
}

#nice h1 {
  color: rgb(37,132,181);
  font-size: 24px;
  font-weight: bold;
}

#nice h2 {
  margin-top: 30px;
  margin-bottom: 20px;
}

#nice h2 {
  font-size: 18px;
  border-bottom: 4px solid rgb(37,132,181);
  padding: 2px 4px;
  color: rgb(37,132,181);
  display: inline-block;
}

#nice h3 {
  margin-top: 20px;
  margin-bottom: 10px;
}

#nice h3 {
  font-size: 16px;
  border-bottom: 1px solid rgb(37,132,181);
  padding: 2px 10px;
  color: rgb(37,132,181);
  display: inline-block;
}

#nice ul, #nice ol {
  padding-left: 20px;
}

#nice li {
  font-size: 16px;
  line-height: 1.75em;
  padding: 5px 0;
}

#nice blockquote {
  border: 1px dashed rgb(37,132,181);
  background: transparent;
  padding: 10px 15px;
  margin: 10px 0;
}

#nice blockquote p {
  font-size: 15px;
  line-height: 1.75em;
  background-color: transparent;
  padding: 5px 0;
}

#nice a {
  color: rgb(37,132,181);
  border-bottom: 1px solid rgb(37,132,181);
  text-decoration: none;
}

#nice strong {
  color: rgb(37,132,181);
  font-weight: bold;
}

#nice em {
  color: rgb(37,132,181);
  font-style: italic;
}

#nice hr {
  border: none;
  border-top: 1px solid rgb(37,132,181);
  margin: 20px 0;
}

#nice img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: block;
  margin: 20px auto;
}

#nice code {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  color: rgb(37,132,181);
  font-family: 'Courier New', monospace;
}

#nice pre {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
}

#nice pre code {
  background-color: transparent;
  padding: 0;
  color: #333;
}
""",

    "business": """
/* 商务风格 - 蓝灰色系 */
#nice {
  padding: 20px;
}

#nice p {
  font-size: 16px;
  padding: 19px;
  text-align: left;
  display: inline-block;
  width: 100%;
  background-color: rgba(72, 126, 252, 0.09);
  line-height: 1.75em;
  margin-bottom: 10px;
}

#nice h1 {
  margin-top: -0.46em;
  margin-bottom: 0.1em;
  border-bottom: 2px solid rgb(198, 196, 196);
  text-align: center;
}

#nice h1 {
  padding-top: 5px;
  padding-bottom: 5px;
  color: rgb(160, 160, 160);
  font-size: 24px;
  line-height: 2;
}

#nice h2 {
  margin: 10px auto;
  height: 40px;
  background-color: rgb(251, 251, 251);
  border-bottom: 1px solid rgb(246, 246, 246);
  overflow: hidden;
}

#nice h2 {
  margin-left: -10px;
  display: inline-block;
  width: auto;
  height: 40px;
  background-color: rgb(33, 33, 34);
  border-bottom-right-radius: 100px;
  color: rgb(255, 255, 255);
  padding-right: 30px;
  padding-left: 30px;
  line-height: 40px;
  font-size: 16px;
}

#nice h3 {
  margin: 20px auto 5px;
  border-top: 1px solid rgb(221, 221, 221);
}

#nice h3 {
  margin-top: -1px;
  padding-top: 6px;
  padding-right: 5px;
  padding-left: 5px;
  font-size: 17px;
  border-top: 2px solid rgb(33, 33, 34);
  display: inline-block;
  line-height: 1.1;
}

#nice ul, #nice ol {
  padding-left: 20px;
}

#nice li {
  font-size: 15px;
  line-height: 1.75em;
  padding: 5px 0;
}

#nice blockquote {
  border-left: 4px solid rgb(221, 221, 221);
  margin-top: 1.2em;
  margin-bottom: 1.2em;
  padding-right: 1em;
  padding-left: 1em;
  color: rgb(119, 119, 119);
}

#nice blockquote p {
  font-size: 15px;
  color: rgb(119, 119, 119);
  line-height: 1.75em;
  background-color: transparent;
  padding: 5px 0;
}

#nice a {
  color: rgb(239, 112, 96);
  border-bottom: 1px solid rgb(239, 112, 96);
  text-decoration: none;
}

#nice strong {
  color: rgb(255, 79, 121);
  font-weight: bold;
}

#nice hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 20px 0;
}

#nice img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: block;
  margin: 20px auto;
}

#nice code {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  color: rgb(239, 112, 96);
  font-family: 'Courier New', monospace;
}

#nice pre {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
}

#nice pre code {
  background-color: transparent;
  padding: 0;
  color: #333;
}
""",

    "simple": """
/* 简约风格 - 黑白灰 */
#nice {
  padding: 20px;
}

#nice p {
  font-size: 16px;
  padding: 10px 0;
  text-align: left;
  line-height: 1.75em;
  margin-bottom: 10px;
}

#nice h1 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #333;
}

#nice h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-top: 30px;
  margin-bottom: 15px;
  padding-left: 10px;
  border-left: 4px solid #333;
}

#nice h3 {
  font-size: 18px;
  font-weight: bold;
  color: #666;
  margin-top: 20px;
  margin-bottom: 10px;
}

#nice ul, #nice ol {
  padding-left: 20px;
}

#nice li {
  font-size: 16px;
  line-height: 1.75em;
  padding: 5px 0;
}

#nice blockquote {
  border-left: 4px solid #ccc;
  background: #f9f9f9;
  padding: 10px 15px;
  margin: 10px 0;
  color: #666;
}

#nice blockquote p {
  font-size: 15px;
  line-height: 1.75em;
  padding: 5px 0;
}

#nice a {
  color: #333;
  border-bottom: 1px solid #333;
  text-decoration: none;
}

#nice strong {
  color: #000;
  font-weight: bold;
}

#nice em {
  font-style: italic;
  color: #666;
}

#nice hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 20px 0;
}

#nice img {
  max-width: 100%;
  border-radius: 4px;
  display: block;
  margin: 20px auto;
}

#nice code {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  color: #333;
  font-family: 'Courier New', monospace;
}

#nice pre {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
  border: 1px solid #ddd;
}

#nice pre code {
  background-color: transparent;
  padding: 0;
  color: #333;
}
"""
}


def markdown_to_html(markdown_text, style="warm"):
    """
    将 Markdown 转换为带样式的 HTML
    
    Args:
        markdown_text: Markdown 文本
        style: 样式名称 (warm/fresh/business/simple)
        
    Returns:
        str: HTML 文本
    """
    # 配置 Markdown 扩展
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
    ]
    
    # 转换 Markdown 到 HTML
    html_content = markdown.markdown(markdown_text, extensions=extensions)
    
    # 获取样式
    css_style = STYLES.get(style, STYLES["warm"])
    
    # 构建完整的 HTML
    full_html = f"""<section id="nice">
{html_content}

<style>
{css_style}
</style>

</section>"""
    
    return full_html


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Markdown 转微信公众号 HTML 转换器",
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
        html_content = markdown_to_html(markdown_text, args.style)
        
        # 写入 HTML 文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 转换成功！")
        print(f"   输入: {args.input}")
        print(f"   输出: {args.output}")
        print(f"   样式: {args.style}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
微信公众号文章提取工具（简化版）

使用 requests + BeautifulSoup 直接提取文章内容
"""

import sys
import json
import re
import requests
from bs4 import BeautifulSoup
import html2text


def extract_wechat_article(url):
    """提取微信公众号文章"""
    try:
        # 设置请求头，模拟浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        # 发送请求
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            raise Exception(f"请求失败，状态码: {response.status_code}")
        
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title_tag = soup.find('h1', class_='rich_media_title')
        title = title_tag.get_text(strip=True) if title_tag else "未知标题"
        
        # 提取作者
        author_tag = soup.find('a', class_='rich_media_meta_link')
        author = author_tag.get_text(strip=True) if author_tag else "未知作者"
        
        # 提取发布时间
        time_tag = soup.find('em', id='publish_time')
        publish_time = time_tag.get_text(strip=True) if time_tag else "未知时间"
        
        # 提取正文内容
        content_tag = soup.find('div', class_='rich_media_content')
        if not content_tag:
            raise Exception("未找到文章内容")
        
        # 转换为 Markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        h.body_width = 0  # 不自动换行
        
        markdown_content = h.handle(str(content_tag))
        
        # 清理多余的空行
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # 构建完整的 Markdown
        full_markdown = f"""# {title}

**作者**: {author}  
**发布时间**: {publish_time}

---

{markdown_content.strip()}

---

**原文链接**: {url}
"""
        
        return {
            "success": True,
            "title": title,
            "author": author,
            "publish_time": publish_time,
            "content": markdown_content.strip(),
            "full_markdown": full_markdown,
            "url": url
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }


def main():
    if len(sys.argv) < 2:
        print("用法: python3 extract_simple.py <微信文章URL>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    result = extract_wechat_article(url)
    
    if result["success"]:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"提取失败: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

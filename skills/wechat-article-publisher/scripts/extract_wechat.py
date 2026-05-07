#!/usr/bin/env python3
"""
微信公众号文章提取脚本
使用 requests 直接获取文章内容
"""

import requests
import re
import json
import sys
from bs4 import BeautifulSoup

def extract_wechat_article(url):
    """提取微信公众号文章"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.encoding = 'utf-8'
        html = response.text
        
        # 使用 BeautifulSoup 解析
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title = ''
        title_tag = soup.find('h1', id='activity-name') or soup.find('h1', class_='title')
        if not title_tag:
            title_tag = soup.find('meta', property='og:title')
            title = title_tag['content'] if title_tag else ''
        else:
            title = title_tag.get_text(strip=True)
        
        # 提取作者
        author = ''
        author_tag = soup.find('meta', property='og:article:author') or soup.find('a', id='js_name')
        if author_tag:
            author = author_tag.get_text(strip=True) if not author_tag.get('content') else author_tag['content']
        
        # 提取发布时间
        publish_time = ''
        time_tag = soup.find('em', id='publish_time') or soup.find('span', class_='publish_time')
        if time_tag:
            publish_time = time_tag.get_text(strip=True)
        
        # 提取文章内容
        content = ''
        content_tag = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if content_tag:
            # 移除脚本和样式
            for script in content_tag(['script', 'style']):
                script.decompose()
            content = content_tag.get_text(separator='\n', strip=True)
        
        # 提取封面图
        cover = ''
        cover_tag = soup.find('meta', property='og:image')
        if cover_tag:
            cover = cover_tag.get('content', '')
        
        # 提取摘要
        description = ''
        desc_tag = soup.find('meta', property='og:description')
        if desc_tag:
            description = desc_tag.get('content', '')
        
        if not title:
            return {
                'success': False,
                'error': '无法提取文章标题，可能需要微信验证'
            }
        
        return {
            'success': True,
            'title': title,
            'author': author,
            'publishTime': publish_time,
            'description': description,
            'cover': cover,
            'content': content,
            'link': url
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    if len(sys.argv) < 2:
        print("用法: python3 extract_wechat.py <微信文章URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = extract_wechat_article(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
配置管理工具

自动读取 .env 文件中的配置信息
"""

import os
from pathlib import Path


def load_config():
    """加载配置文件"""
    config = {}
    
    # 获取当前脚本所在目录的父目录
    skill_dir = Path(__file__).parent.parent
    env_file = skill_dir / '.env'
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
    
    return config


def get_wechat_config():
    """获取微信公众号配置"""
    config = load_config()
    return {
        'app_id': config.get('WECHAT_APP_ID', ''),
        'app_secret': config.get('WECHAT_APP_SECRET', '')
    }


def get_doubao_api_key():
    """获取豆包 API 密钥"""
    config = load_config()
    return config.get('DOUBAO_API_KEY', '')


def get_markdown_config():
    """获取 Markdown 排版配置"""
    config = load_config()
    return {
        'converter': config.get('MARKDOWN_CONVERTER', 'doocs'),
        'theme': config.get('MARKDOWN_THEME', None)  # None 表示由 Agent 动态选择
    }


def select_theme_by_content(title: str = "", content: str = "") -> str:
    """
    根据文章内容自动选择合适的主题
    
    Args:
        title: 文章标题
        content: 文章内容
        
    Returns:
        str: 主题名称（orange, blue, green, purple, red, cyan, black, pink）
    """
    text = (title + " " + content).lower()
    
    # 励志、鸡汤、女性相关 → orange
    if any(keyword in text for keyword in ['励志', '成长', '女人', '女性', '独立', '搞钱', '改变', '蜕变']):
        return 'orange'
    
    # 科技、商务、职场 → blue
    if any(keyword in text for keyword in ['科技', 'ai', '人工智能', '商务', '职场', '管理', '效率']):
        return 'blue'
    
    # 健康、养生、环保 → green
    if any(keyword in text for keyword in ['健康', '养生', '环保', '自然', '运动', '饮食']):
        return 'green'
    
    # 情感、浪漫 → pink
    if any(keyword in text for keyword in ['爱情', '恋爱', '浪漫', '情感', '甜蜜']):
        return 'pink'
    
    # 品牌、高端 → purple
    if any(keyword in text for keyword in ['品牌', '奢侈', '高端', '优雅', '艺术']):
        return 'purple'
    
    # 旅行、文艺 → cyan
    if any(keyword in text for keyword in ['旅行', '旅游', '游记', '文艺', '清新']):
        return 'cyan'
    
    # 节日、活动 → red
    if any(keyword in text for keyword in ['节日', '春节', '新年', '活动', '庆祝']):
        return 'red'
    
    # 默认使用 orange（温暖通用）
    return 'orange'



def get_article_config():
    """获取文章格式配置"""
    config = load_config()
    return {
        'show_title': config.get('ARTICLE_SHOW_TITLE', 'false').lower() == 'true',
        'image_count': int(config.get('ARTICLE_IMAGE_COUNT', '3')),
        'image_orientation': config.get('IMAGE_ORIENTATION', 'horizontal'),
        'image_prompt_suffix': config.get('IMAGE_PROMPT_SUFFIX', '，16:9横屏构图')
    }


if __name__ == '__main__':
    # 测试配置读取
    wechat = get_wechat_config()
    doubao_key = get_doubao_api_key()
    markdown = get_markdown_config()
    article = get_article_config()
    
    print("微信公众号配置:")
    print(f"  AppID: {wechat['app_id']}")
    print(f"  AppSecret: {wechat['app_secret'][:10]}...")
    print(f"\n豆包 API Key: {doubao_key[:20]}...")
    print(f"\nMarkdown 排版配置:")
    print(f"  转换器: {markdown['converter']}")
    print(f"  主题: {markdown['theme'] or '动态选择'}")
    print(f"\n文章格式配置:")
    print(f"  正文显示标题: {article['show_title']}")
    print(f"  配图数量: {article['image_count']}")
    print(f"  图片方向: {article['image_orientation']}")
    print(f"  图片提示词后缀: {article['image_prompt_suffix']}")
    
    # 测试主题选择
    print(f"\n主题选择测试:")
    test_cases = [
        ("当女人一门心思搞钱，她就开始长脑子", "励志 女性 独立"),
        ("2024年AI技术发展趋势分析", "科技 人工智能 商务"),
        ("春天来了，去这10个地方旅行吧", "旅行 清新 文艺"),
        ("如何保持健康的生活方式", "健康 养生 运动"),
        ("爱情里最重要的是什么", "爱情 情感 浪漫"),
    ]
    
    for title, content in test_cases:
        theme = select_theme_by_content(title, content)
        print(f"  '{title}' → {theme}")

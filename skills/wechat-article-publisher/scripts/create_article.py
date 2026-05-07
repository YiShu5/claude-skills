#!/usr/bin/env python3
"""
智能文章生成并发布到公众号草稿箱

支持多种模式：
1. 基于参考文章改写：提取 URL 内容 → 改写 → 生成封面 → 上传草稿
2. 基于标题创作：标题 → 搜索资料 → 生成文章 → 生成封面 → 上传草稿
3. 直接发布：提供完整内容 → 生成封面 → 上传草稿

使用方法：
    # 模式1：基于参考文章改写
    python3 create_article.py --mode rewrite --url "https://mp.weixin.qq.com/s/..." --app-id xxx --app-secret xxx
    
    # 模式2：基于标题创作
    python3 create_article.py --mode create --title "如何使用AI提升工作效率" --app-id xxx --app-secret xxx
    
    # 模式3：直接发布
    python3 create_article.py --mode direct --title "标题" --content "内容" --app-id xxx --app-secret xxx
    
    # 可选参数
    --provider doubao|qwen  # 选择图像生成引擎（默认：doubao）
    --author "作者名"       # 文章作者
    --digest "摘要"         # 文章摘要
    --no-cover             # 不生成封面
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def extract_article(url: str) -> dict:
    """提取文章内容"""
    print(f"📖 正在提取文章: {url}")
    
    script_dir = Path(__file__).parent
    extract_script = script_dir / "extract_to_markdown.py"
    
    result = subprocess.run(
        ["python3", str(extract_script), url, "--json"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        raise Exception(f"提取文章失败: {result.stderr}")
    
    data = json.loads(result.stdout)
    if data.get("error"):
        raise Exception(f"提取文章失败: {data.get('message')}")
    
    print(f"✅ 提取成功: {data['title']}")
    return data


def rewrite_article(original_content: str, original_title: str) -> dict:
    """
    改写文章（这里需要调用 AI 模型）
    实际使用时，你可以调用 OpenClaw 的 AI 能力或外部 API
    """
    print(f"✍️  正在改写文章: {original_title}")
    
    # TODO: 这里应该调用 AI 模型进行改写
    # 示例：可以使用 OpenClaw 的 sessions_send 或直接调用 AI API
    
    # 临时实现：返回原文（实际使用时需要替换为真正的改写逻辑）
    print("⚠️  警告: 改写功能需要集成 AI 模型，当前返回原文")
    
    return {
        "title": f"【改写】{original_title}",
        "content": original_content,
        "digest": f"基于原文改写的内容"
    }


def search_and_create_article(title: str) -> dict:
    """
    根据标题搜索资料并创作文章
    """
    print(f"🔍 正在搜索资料: {title}")
    
    # TODO: 这里应该：
    # 1. 使用 web_fetch 或搜索 API 查找相关资料
    # 2. 调用 AI 模型基于资料生成文章
    
    # 临时实现：返回模板（实际使用时需要替换为真正的创作逻辑）
    print("⚠️  警告: 创作功能需要集成搜索和 AI 模型，当前返回模板")
    
    return {
        "title": title,
        "content": f"<section><h2>{title}</h2><p>这是根据标题生成的文章内容...</p></section>",
        "digest": f"关于{title}的深度解析"
    }


def generate_cover(prompt: str, provider: str = "doubao") -> str:
    """生成封面图片"""
    print(f"🎨 正在生成封面 (使用 {provider})...")
    
    script_dir = Path(__file__).parent
    cover_script = script_dir / "generate_cover.py"
    
    result = subprocess.run(
        ["python3", str(cover_script), "--prompt", prompt, "--provider", provider],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        raise Exception(f"生成封面失败: {result.stderr}")
    
    data = json.loads(result.stdout)
    if not data.get("success"):
        raise Exception(f"生成封面失败: {data}")
    
    image_url = data["image_url"]
    print(f"✅ 封面生成成功: {image_url}")
    
    # 下载图片
    import requests
    print("📥 正在下载封面图片...")
    img_response = requests.get(image_url, timeout=30)
    img_response.raise_for_status()
    
    # 保存到临时文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_file.write(img_response.content)
    temp_file.close()
    
    print(f"✅ 封面已下载: {temp_file.name}")
    return temp_file.name


def upload_cover(image_path: str, app_id: str, app_secret: str) -> str:
    """上传封面到微信"""
    print("📤 正在上传封面到微信...")
    
    script_dir = Path(__file__).parent
    upload_script = script_dir / "upload_material.py"
    
    result = subprocess.run(
        [
            "python3", str(upload_script),
            "--app_id", app_id,
            "--app_secret", app_secret,
            "--image_path", image_path
        ],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        raise Exception(f"上传封面失败: {result.stderr}")
    
    data = json.loads(result.stdout)
    thumb_media_id = data.get("thumb_media_id")
    
    if not thumb_media_id:
        raise Exception(f"上传封面失败: 未获取到 thumb_media_id")
    
    print(f"✅ 封面上传成功: {thumb_media_id}")
    return thumb_media_id


def create_draft(title: str, content: str, app_id: str, app_secret: str, 
                 thumb_media_id: str = None, author: str = None, digest: str = None) -> str:
    """创建草稿"""
    print("📝 正在创建草稿...")
    
    script_dir = Path(__file__).parent
    draft_script = script_dir / "create_draft.py"
    
    cmd = [
        "python3", str(draft_script),
        "--app_id", app_id,
        "--app_secret", app_secret,
        "--title", title,
        "--content", content
    ]
    
    if thumb_media_id:
        cmd.extend(["--thumb_media_id", thumb_media_id])
    if author:
        cmd.extend(["--author", author])
    if digest:
        cmd.extend(["--digest", digest])
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        raise Exception(f"创建草稿失败: {result.stderr}")
    
    data = json.loads(result.stdout)
    media_id = data.get("media_id")
    
    if not media_id:
        raise Exception(f"创建草稿失败: 未获取到 media_id")
    
    print(f"✅ 草稿创建成功: {media_id}")
    return media_id


def main():
    parser = argparse.ArgumentParser(
        description="智能文章生成并发布到公众号草稿箱",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # 模式选择
    parser.add_argument(
        "--mode",
        choices=["rewrite", "create", "direct"],
        required=True,
        help="工作模式: rewrite (改写), create (创作), direct (直接发布)"
    )
    
    # 输入参数
    parser.add_argument("--url", help="参考文章 URL (rewrite 模式)")
    parser.add_argument("--title", help="文章标题 (create/direct 模式)")
    parser.add_argument("--content", help="文章内容 HTML (direct 模式)")
    
    # 微信凭证
    parser.add_argument("--app-id", required=True, help="微信公众号 AppID")
    parser.add_argument("--app-secret", required=True, help="微信公众号 AppSecret")
    
    # 可选参数
    parser.add_argument("--provider", choices=["doubao", "qwen"], default="doubao",
                        help="图像生成引擎 (默认: doubao)")
    parser.add_argument("--author", help="文章作者")
    parser.add_argument("--digest", help="文章摘要")
    parser.add_argument("--no-cover", action="store_true", help="不生成封面")
    
    args = parser.parse_args()
    
    try:
        # 根据模式处理
        if args.mode == "rewrite":
            if not args.url:
                print("错误: rewrite 模式需要提供 --url 参数", file=sys.stderr)
                sys.exit(1)
            
            # 提取原文
            original = extract_article(args.url)
            
            # 改写文章
            article = rewrite_article(original["content"], original["title"])
            title = article["title"]
            content = article["content"]
            digest = args.digest or article.get("digest")
            
        elif args.mode == "create":
            if not args.title:
                print("错误: create 模式需要提供 --title 参数", file=sys.stderr)
                sys.exit(1)
            
            # 搜索并创作
            article = search_and_create_article(args.title)
            title = article["title"]
            content = article["content"]
            digest = args.digest or article.get("digest")
            
        else:  # direct
            if not args.title or not args.content:
                print("错误: direct 模式需要提供 --title 和 --content 参数", file=sys.stderr)
                sys.exit(1)
            
            title = args.title
            content = args.content
            digest = args.digest
        
        # 生成封面
        thumb_media_id = None
        cover_path = None
        
        if not args.no_cover:
            cover_prompt = f"为文章《{title}》生成封面图片，风格专业、简洁、现代"
            cover_path = generate_cover(cover_prompt, args.provider)
            thumb_media_id = upload_cover(cover_path, args.app_id, args.app_secret)
        
        # 创建草稿
        media_id = create_draft(
            title=title,
            content=content,
            app_id=args.app_id,
            app_secret=args.app_secret,
            thumb_media_id=thumb_media_id,
            author=args.author,
            digest=digest
        )
        
        # 清理临时文件
        if cover_path and os.path.exists(cover_path):
            os.unlink(cover_path)
        
        # 输出结果
        result = {
            "success": True,
            "title": title,
            "media_id": media_id,
            "thumb_media_id": thumb_media_id
        }
        
        print("\n" + "="*50)
        print("🎉 文章已成功创建到草稿箱！")
        print("="*50)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

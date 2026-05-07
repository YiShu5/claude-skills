#!/usr/bin/env python3
"""
微信公众号文章提取并转换为 Markdown
调用 Node.js reader 提取文章并转换为 Markdown 格式
"""

import json
import subprocess
import sys
from pathlib import Path

def extract_to_markdown(url: str, save_path: str = None) -> dict:
    """
    提取微信公众号文章并转换为 Markdown
    
    Args:
        url: 文章链接 (mp.weixin.qq.com)
        save_path: 保存路径（可选，如果提供则保存 Markdown 文件）
    
    Returns:
        dict: 提取结果
            - title: 文章标题
            - author: 作者
            - publishTime: 发布时间
            - description: 摘要
            - cover: 封面图 URL
            - link: 原文链接
            - content: Markdown 内容
            - fullMarkdown: 完整 Markdown 文档（含元数据）
    """
    # 构建 Node.js 脚本路径
    script_dir = Path(__file__).parent.parent / "reader"
    extract_script = script_dir / "extract_and_convert.js"
    
    if not extract_script.exists():
        return {
            "error": True,
            "message": f"转换脚本不存在: {extract_script}"
        }
    
    try:
        # 执行 Node.js 脚本
        result = subprocess.run(
            ["node", str(extract_script), url],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            error_output = result.stderr
            return {
                "error": True,
                "message": f"提取失败: {error_output}"
            }
        
        # 解析返回结果
        output = json.loads(result.stdout)
        
        # 如果提供了保存路径，保存 Markdown 文件
        if save_path:
            save_file = Path(save_path)
            save_file.parent.mkdir(parents=True, exist_ok=True)
            save_file.write_text(output['fullMarkdown'], encoding='utf-8')
            output['saved_to'] = str(save_file)
        
        return output
        
    except subprocess.TimeoutExpired:
        return {
            "error": True,
            "message": "提取超时 (30秒)"
        }
    except json.JSONDecodeError as e:
        return {
            "error": True,
            "message": f"JSON 解析失败: {e}\n输出: {result.stdout}"
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"未知错误: {e}"
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="提取微信公众号文章并转换为 Markdown")
    parser.add_argument("url", help="文章链接 (mp.weixin.qq.com)")
    parser.add_argument("-o", "--output", help="保存 Markdown 文件路径（可选）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式（默认输出 Markdown）")
    
    args = parser.parse_args()
    
    result = extract_to_markdown(args.url, args.output)
    
    if result.get("error"):
        print(f"错误: {result['message']}", file=sys.stderr)
        sys.exit(1)
    
    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result['fullMarkdown'])
    
    if args.output:
        print(f"\n✅ 已保存到: {result['saved_to']}", file=sys.stderr)


if __name__ == "__main__":
    main()

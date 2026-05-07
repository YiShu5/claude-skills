#!/usr/bin/env python3
"""
创建微信公众号文章草稿

功能：
- 调用微信公众号API创建文章草稿
- 支持单篇图文消息
- 返回草稿media_id

使用说明：
- 脚本接收app_id和app_secret作为参数
- 内部自动获取access_token
- 然后创建文章草稿

注意：
- 公众号文章必须有封面图片
- 如果没有提供thumb_media_id，脚本会输出文章内容而不发送请求
"""

import sys
import argparse
import json
import requests


def get_access_token(app_id, app_secret):
    """
    获取微信公众号access_token

    Args:
        app_id: 微信公众号AppID
        app_secret: 微信公众号AppSecret

    Returns:
        str: access_token

    Raises:
        Exception: 获取access_token失败
    """
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        if response.status_code >= 400:
            raise Exception(f"获取access_token失败: HTTP {response.status_code}, {response.text}")

        data = response.json()

        errcode = data.get("errcode", 0)
        if errcode != 0:
            errmsg = data.get("errmsg", "未知错误")
            raise Exception(f"获取access_token失败: 微信错误[{errcode}] {errmsg}")

        access_token = data.get("access_token")
        if not access_token:
            raise Exception("获取access_token失败: 响应中未找到access_token")

        return access_token

    except requests.exceptions.RequestException as e:
        raise Exception(f"获取access_token失败: {str(e)}")


def create_draft(app_id=None, app_secret=None, title=None, content=None, digest=None, author=None, thumb_media_id=None, show_cover_pic=1):
    """
    创建微信公众号文章草稿

    Args:
        app_id: 微信公众号AppID（可选，从配置文件读取）
        app_secret: 微信公众号AppSecret（可选，从配置文件读取）
        title: 文章标题（必需）
        content: 文章HTML内容（必需）
        digest: 文章摘要（可选，不传则自动抓取）
        author: 作者名称（可选）
        thumb_media_id: 封面图片media_id（必需）
        show_cover_pic: 是否显示封面（可选，默认1）

    Returns:
        dict: 包含media_id的响应数据，或文章内容（如果无封面）

    Raises:
        Exception: API调用失败
    """
    # 从配置文件读取 app_id 和 app_secret（如果未提供）
    if not app_id or not app_secret:
        try:
            from config import get_wechat_config
            config = get_wechat_config()
            app_id = app_id or config.get('app_id')
            app_secret = app_secret or config.get('app_secret')
        except:
            pass
    
    if not app_id or not app_secret:
        raise ValueError("缺少微信公众号配置，请提供 app_id 和 app_secret 参数，或在 .env 文件中配置")
    
    # 检查是否提供了封面图片
    if not thumb_media_id:
        # 没有封面图片，输出文章内容而不发送请求
        return {
            "status": "no_cover",
            "message": "文章未发送：公众号文章必须有封面图片",
            "article": {
                "title": title,
                "content": content,
                "digest": digest,
                "author": author
            },
            "instruction": "请先生成封面图片，获取thumb_media_id后重新调用此脚本"
        }

    # 1. 获取access_token
    access_token = get_access_token(app_id, app_secret)

    # 2. 构建请求URL
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"

    # 3. 构建请求体数据结构
    articles = [{
        "title": title,
        "content": content,
        "thumb_media_id": thumb_media_id,
        "show_cover_pic": int(show_cover_pic)
    }]

    # 添加可选字段
    if digest:
        articles[0]["digest"] = digest
    if author:
        articles[0]["author"] = author

    request_data = {
        "articles": articles
    }

    # 4. 手动序列化JSON，确保使用UTF-8编码
    json_data = json.dumps(request_data, ensure_ascii=False)

    # 5. 设置请求头
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    # 6. 发起请求（使用data参数，传递UTF-8编码的字节）
    try:
        response = requests.post(
            url,
            data=json_data.encode('utf-8'),
            headers=headers,
            timeout=30
        )

        # 检查HTTP状态码
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")

        data = response.json()

        # 7. 微信API错误处理
        errcode = data.get("errcode", 0)
        if errcode != 0:
            errmsg = data.get("errmsg", "未知错误")
            error_msg = f"微信接口错误[{errcode}]: {errmsg}"
            # 常见错误码提示
            if errcode == 40001:
                error_msg += " (access_token无效或过期，请检查app_id和app_secret是否正确)"
            elif errcode == 40007:
                error_msg += " (无效的media_id)"
            elif errcode == 40008:
                error_msg += " (消息类型不支持)"
            elif errcode == 45001:
                error_msg += " (多媒体文件大小超过限制)"
            elif errcode == 40125:
                error_msg += " (无效的app_id或app_secret)"
            raise Exception(error_msg)

        # 8. 提取并返回结果
        media_id = data.get("media_id")
        if not media_id:
            raise Exception("创建草稿失败: 未获取到media_id")

        return {
            "status": "success",
            "errcode": 0,
            "errmsg": "ok",
            "media_id": media_id
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description="创建微信公众号文章草稿（必须有封面图片）",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 参数（app_id 和 app_secret 可选，从配置文件读取）
    parser.add_argument(
        "--app_id",
        help="微信公众号AppID（可选，从配置文件读取）"
    )
    parser.add_argument(
        "--app_secret",
        help="微信公众号AppSecret（可选，从配置文件读取）"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="文章标题"
    )
    parser.add_argument(
        "--content",
        required=True,
        help="文章HTML内容"
    )
    parser.add_argument(
        "--thumb_media_id",
        required=False,
        help="封面图片的media_id（必需，公众号文章必须有封面）"
    )

    # 可选参数
    parser.add_argument(
        "--digest",
        default=None,
        help="文章摘要（可选，不传则自动抓取正文前54个字）"
    )
    parser.add_argument(
        "--author",
        default=None,
        help="作者名称（可选）"
    )
    parser.add_argument(
        "--show_cover_pic",
        type=int,
        choices=[0, 1],
        default=1,
        help="是否显示封面（0=不显示，1=显示，默认1）"
    )

    args = parser.parse_args()

    try:
        result = create_draft(
            app_id=args.app_id,
            app_secret=args.app_secret,
            title=args.title,
            content=args.content,
            digest=args.digest,
            author=args.author,
            thumb_media_id=args.thumb_media_id,
            show_cover_pic=args.show_cover_pic
        )

        # 输出结果（JSON格式，便于程序解析）
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 根据状态返回不同的退出码
        if result.get("status") == "no_cover":
            # 没有封面，返回特殊状态码，但不是错误
            sys.exit(0)
        else:
            # 成功创建草稿
            sys.exit(0)

    except Exception as e:
        # 输出错误信息（stderr）
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

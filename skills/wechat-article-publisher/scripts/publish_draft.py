#!/usr/bin/env python3
"""
发布微信公众号草稿文章

功能：
- 调用微信公众号API发布草稿文章
- 支持发布单篇或多篇文章
- 返回publish_id用于查询发布状态

使用说明：
- 脚本接收app_id和app_secret作为参数
- 内部自动获取access_token
- 然后发布草稿文章
"""

import sys
import argparse
import json
from coze_workload_identity import requests


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


def publish_draft(app_id, app_secret, media_id):
    """
    发布微信公众号草稿文章

    Args:
        app_id: 微信公众号AppID（必需）
        app_secret: 微信公众号AppSecret（必需）
        media_id: 草稿的media_id（必需）

    Returns:
        dict: 包含publish_id的响应数据

    Raises:
        Exception: API调用失败
    """
    # 1. 获取access_token
    access_token = get_access_token(app_id, app_secret)

    # 2. 构建请求URL
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"

    # 3. 构建请求体
    request_data = {
        "media_id": media_id
    }

    # 4. 发起请求
    try:
        response = requests.post(
            url,
            json=request_data,
            timeout=30
        )

        # 检查HTTP状态码
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")

        data = response.json()

        # 5. 微信API错误处理
        errcode = data.get("errcode", 0)
        if errcode != 0:
            errmsg = data.get("errmsg", "未知错误")
            error_msg = f"微信接口错误[{errcode}]: {errmsg}"
            # 常见错误码提示
            if errcode == 40001:
                error_msg += " (access_token无效或过期，请检查app_id和app_secret是否正确)"
            elif errcode == 40007:
                error_msg += " (无效的media_id)"
            elif errcode == 45007:
                error_msg += " (发布时间冲突)"
            elif errcode == 64004:
                error_msg += " (该素材已被删除)"
            elif errcode == 40125:
                error_msg += " (无效的app_id或app_secret)"
            raise Exception(error_msg)

        # 6. 提取并返回结果
        publish_id = data.get("publish_id")
        if not publish_id:
            raise Exception("发布草稿失败: 未获取到publish_id")

        return {
            "errcode": 0,
            "errmsg": "ok",
            "publish_id": publish_id
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description="发布微信公众号草稿文章",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 必需参数
    parser.add_argument(
        "--app_id",
        required=True,
        help="微信公众号AppID"
    )
    parser.add_argument(
        "--app_secret",
        required=True,
        help="微信公众号AppSecret"
    )
    parser.add_argument(
        "--media_id",
        required=True,
        help="草稿的media_id（由create_draft.py创建草稿时返回）"
    )

    args = parser.parse_args()

    try:
        result = publish_draft(
            app_id=args.app_id,
            app_secret=args.app_secret,
            media_id=args.media_id
        )

        # 输出结果（JSON格式，便于程序解析）
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 返回成功状态码
        sys.exit(0)

    except Exception as e:
        # 输出错误信息（stderr）
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

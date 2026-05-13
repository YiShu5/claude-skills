#!/usr/bin/env python3
"""
上传图片素材到微信公众号

功能：
- 上传图片到微信服务器
- 返回thumb_media_id用于创建文章封面

授权方式: 使用app_id和app_secret获取access_token
"""

import os
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


def upload_material(app_id=None, app_secret=None, image_path=None):
    """
    上传图片素材到微信公众号

    Args:
        app_id: 微信公众号AppID（可选，从配置文件读取）
        app_secret: 微信公众号AppSecret（可选，从配置文件读取）
        image_path: 图片文件路径（必需）

    Returns:
        dict: 包含thumb_media_id的响应数据

    Raises:
        Exception: 上传失败
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
    
    # 1. 检查文件是否存在
    if not image_path:
        raise ValueError("缺少图片文件路径")
    
    if not os.path.exists(image_path):
        raise Exception(f"图片文件不存在: {image_path}")

    # 2. 获取access_token
    access_token = get_access_token(app_id, app_secret)

    # 3. 构建请求URL
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=thumb"

    # 4. 准备上传文件
    try:
        with open(image_path, 'rb') as f:
            files = {
                'media': (os.path.basename(image_path), f, 'image/jpeg')
            }

            # 5. 发起上传请求
            response = requests.post(url, files=files, timeout=60)

            # 检查HTTP状态码
            if response.status_code >= 400:
                raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")

            data = response.json()

            # 6. 微信API错误处理
            errcode = data.get("errcode", 0)
            if errcode != 0:
                errmsg = data.get("errmsg", "未知错误")
                error_msg = f"微信接口错误[{errcode}]: {errmsg}"
                # 常见错误码提示
                if errcode == 40001:
                    error_msg += " (access_token无效或过期，请检查app_id和app_secret是否正确)"
                elif errcode == 40004:
                    error_msg += " (无效的媒体文件类型)"
                elif errcode == 40005:
                    error_msg += " (无效的文件类型)"
                elif errcode == 40006:
                    error_msg += " (无效的图片大小，图片不能超过2MB)"
                elif errcode == 40125:
                    error_msg += " (无效的app_id或app_secret)"
                raise Exception(error_msg)

            # 7. 提取并返回结果
            thumb_media_id = data.get("media_id")
            if not thumb_media_id:
                raise Exception("上传图片失败: 未获取到thumb_media_id")

            return {
                "errcode": 0,
                "errmsg": "ok",
                "thumb_media_id": thumb_media_id,
                "url": data.get("url", "")
            }

    except IOError as e:
        raise Exception(f"读取图片文件失败: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"上传请求失败: {str(e)}")


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description="上传图片素材到微信公众号",
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
        "--image_path",
        required=True,
        help="图片文件路径"
    )

    args = parser.parse_args()

    try:
        result = upload_material(
            app_id=args.app_id,
            app_secret=args.app_secret,
            image_path=args.image_path
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

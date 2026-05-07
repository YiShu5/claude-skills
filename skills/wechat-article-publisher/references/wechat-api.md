# 微信公众号API接口说明

## 目录
1. [获取access_token接口](#获取access_token接口)
2. [创建草稿接口](#创建草稿接口)
3. [发布草稿接口](#发布草稿接口)
4. [常见错误码](#常见错误码)
5. [接口限制](#接口限制)

## 获取access_token接口

### 接口地址
```
GET https://api.weixin.qq.com/cgi-bin/token
```

### 请求参数
| 参数 | 是否必需 | 类型 | 说明 |
|------|---------|------|------|
| grant_type | 是 | String | 固定值：client_credential |
| appid | 是 | String | 微信公众号AppID |
| secret | 是 | String | 微信公众号AppSecret |

### 响应参数
```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

### 示例
```bash
curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=SECRET"
```

### 注意事项
- access_token有效期为7200秒（2小时）
- 建议在access_token过期前重新获取
- 同一AppID和AppSecret可以重复调用获取access_token

## 创建草稿接口

### 接口地址
```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN
```

### 请求参数
| 参数 | 是否必需 | 类型 | 说明 |
|------|---------|------|------|
| articles | 是 | Array | 图文消息数组，支持1-8篇文章 |

articles 数组中每个对象包含：

| 参数 | 是否必需 | 类型 | 说明 |
|------|---------|------|------|
| title | 是 | String | 标题 |
| author | 否 | String | 作者 |
| digest | 否 | String | 摘要（不传则自动抓取正文前54个字） |
| content | 是 | String | 图文消息的具体HTML内容 |
| content_source_url | 否 | String | 图文消息的原文地址 |
| thumb_media_id | 否 | String | 缩略图的media_id |
| show_cover_pic | 否 | Int | 是否显示封面，默认为1 |
| need_open_comment | 否 | Int | 是否打开评论，默认为0 |
| only_fans_can_comment | 否 | Int | 是否只有粉丝可以评论，默认为0 |

### 响应参数
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "media_id": "MEDIA_ID"
}
```

### 示例
```bash
curl -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [
      {
        "title": "文章标题",
        "author": "作者名称",
        "content": "<section><h2>正文内容</h2><p>段落内容...</p></section>",
        "digest": "文章摘要",
        "show_cover_pic": 1
      }
    ]
  }'
```

## 发布草稿接口

### 接口地址
```
POST https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=ACCESS_TOKEN
```

### 请求参数
| 参数 | 是否必需 | 类型 | 说明 |
|------|---------|------|------|
| media_id | 是 | String | 草稿的media_id |

### 响应参数
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "publish_id": "PUBLISH_ID"
}
```

### 示例
```bash
curl -X POST "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "media_id": "MEDIA_ID"
  }'
```

## 常见错误码

| 错误码 | 说明 |
|--------|------|
| 40001 | access_token无效或过期 |
| 40007 | 无效的media_id |
| 40008 | 消息类型不支持 |
| 40009 | 图片尺寸过大 |
| 40125 | 无效的app_id或app_secret |
| 44001 | 多媒体文件为空 |
| 44002 | POST的数据包为空 |
| 44003 | 图文消息内容为空 |
| 45001 | 多媒体文件大小超过限制 |
| 45007 | 发布时间冲突 |
| 64004 | 该素材已被删除 |

## 接口限制

### 调用频率限制
- 获取access_token接口：2000次/天
- 创建草稿接口：100次/天
- 发布草稿接口：100次/天

### 内容限制
- 标题：1-64字符
- 摘要：0-120字符
- 正文内容：支持HTML格式
- 封面图片：建议尺寸900*383，大小不超过2MB

### 注意事项
1. 发布操作不可逆，建议先创建草稿确认内容
2. 发布后文章进入审核队列，审核通过后正式发布
3. media_id有效期为3天
4. 同一草稿只能发布一次
5. 脚本会自动管理access_token，无需手动处理

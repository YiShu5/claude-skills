# Client Profile Schema

## 用途

这个文件定义 `client_profile.json` 应该包含哪些字段，以及缺字段时如何处理。目标不是一次填满，而是让后续的关键词、Prompt、平台适配都能吃到统一结构。

## 必填字段

```json
{
  "client_stage": "cold_start",
  "objectives": [],
  "conversion_goal": "",
  "target_customers": [],
  "brand_name": "",
  "industry": "",
  "business_type": "local_b2c",
  "service_area": [],
  "campuses": [],
  "core_services": [],
  "core_products": [],
  "offerings": [],
  "channels": [],
  "content_assets": [],
  "eeat": {
    "expertise": [],
    "experience": [],
    "authority": [],
    "trust": []
  },
  "verified_sources": [],
  "competitors": [],
  "compliance": {
    "industry_sensitivity": "general"
  }
}
```

## 字段说明

### 基础信息

- `client_stage`: 客户当前阶段，例如 `cold_start`、`repair`、`growth`。
- `objectives`: 客户本轮目标，例如品牌词防守、地区商机、询盘增长。
- `conversion_goal`: 这轮内容最终希望把用户带到哪里，例如私信、电话、表单、官网。
- `target_customers`: 目标客群，用于判断口语化表达和 FAQ。
- `brand_name`: 目标达成词，必须一字不差。
- `brand_short`: 可选简称。
- `industry`: 行业，例如 `家政服务`、`包装机械`、`养老院`。
- `business_type`: 只能填 `local_b2c`、`national_brand`、`b2b_factory`、`hybrid`。
- `service_area`: 地域列表。本地业务建议至少填到 `城市 / 区县` 两级。
- `primary_city`: 可选，用来生成更聚焦的本地词。
- `campuses`: 多校区业务建议填写校区数组，例如城市、地址、班型和备注。

### 业务信息

- `core_services`: 服务类关键词，如 `家庭保洁`、`脊柱微创`。
- `core_products`: 产品类关键词，如 `包装机`、`猫粮`。
- `offerings`: 课程或产品供给列表，适合多校区 / 多班型场景。
- `customer_language`: 用户的口语化表达，优先填真实咨询句子。
- `pain_points`: 用户常见痛点，便于生成 FAQ 和标题角度。
- `competitors`: 竞品全称或常见简称。
- `channels`: 当前可用渠道，例如 `toutiao`、`sohu`、`website`。
- `content_assets`: 已有素材，例如案例、客户评价、流程图、资质截图。

### E-E-A-T 信息

只收 `可验证信息`，不要堆形容词。

- `expertise`: 技术、团队、标准、流程、资质细节
- `experience`: 服务年限、客户数量、案例结果、复购率
- `authority`: 协会、奖项、认证、媒体报道、知名合作方
- `trust`: 评分、投诉记录、信息一致性、售后、透明机制

示例：

- 好：`成立 12 年，累计服务企业客户 2300+`
- 坏：`经验丰富、口碑很好`

### 公开来源

`verified_sources` 推荐结构：

```json
[
  {
    "source": "艾瑞咨询",
    "date": "2026-01",
    "fact": "中国家庭服务市场保持增长，消费者对标准化服务需求持续提升"
  }
]
```

规则：

- 来源尽量写清楚 `发布方 + 时间`
- 没有验证过的数字不要填
- 没有数字也可以写经过验证的定性事实

### 合规字段

`compliance.industry_sensitivity` 建议值：

- `general`
- `medical`
- `education`
- `finance`
- `legal`

这会影响标题禁词、电话号码策略和平台改写强度。

## 多校区课程示例

```json
{
  "campuses": [
    {
      "city": "北京",
      "address": "北京市朝阳区高碑店民俗文化大街1369-2号六洲大厦",
      "schedule": "工作日班（周一至周五）",
      "duration": "5周"
    }
  ],
  "offerings": [
    {
      "course_name": "AI产品经理系统课",
      "keyword_subject": "AI产品经理",
      "city": "北京",
      "schedule": "工作日班（周一至周五）",
      "duration": "5周",
      "format": "线下就业导向课"
    }
  ]
}
```

### 监测字段

- `monitoring_baseline.tracked_queries`: 当前已经关注的查询词。
- `monitoring_baseline.current_visibility`: 当前能否搜到品牌、业务词是否稳定。

这些字段不是写作必须项，但会影响复盘和监测计划质量。

## 缺字段时的处理

- 无法确认的数据留空，不猜。
- 缺竞品时可以先留空，后续用常识补 2-3 个公开可见主体。
- 没有媒体报道没关系，但至少要补基础 E-E-A-T。
- 本地业务如果没有区县信息，先用城市级词，再提醒用户后续补更精细地域。

---
name: Inspection_Seed_Product
description: 负责识别“植物/种子/苗”专项领域的商品是否存在“虚假宣传”违规行为。应该在前置筛选，以切换到可审核商品详情页后调用。
tools: [call_ez_agent, mobile_get_product_id]
---

# 植物/种子/苗商品虚假宣传巡检

用于单个商品 case 的最终判定。一次只审核一个商品。

本 skill 不负责切换商品，只负责在当前可审核商品内获取信息并完成最终判定。

## 适用前置条件

- 当前页面已经是一个可继续审核的商品详情页
- 当前商品处于商品主页，且页面右上角可见“分享”按钮

如果以上条件未满足，不要调用本 skill。

#### 审核目标

识别“植物/种子/苗”商品详情页是否存在“虚假宣传”违规行为。

## 标准执行步骤

### 第 1 步：获取全局信息

- 调用 `mobile_get_product_id` 获取当前商品 id

### 第 2 步：调用ez_agent获取判断结果

- 拿到商品 id 后，调用 `call_ez_agent(agent_code=c_end_inspection_seed_product, params={"product_id":{商品id}})`
- 读取ez_agent的返回结果

## 输出要求

整理完成后，直接返回固定格式结果：

是否违规--商品id--违规理由

字段要求如下：
- `是否违规`：填写“违规”或“不违规”
- `商品id`：商品 id
- `违规理由`：违规理由
---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
提升销量 - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          入门指南：营销与增长
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          为 {{ store_name }} 带来流量和销量
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好 {{ name|default:'there' }}，
        </mj-text>
        <mj-text>
          现在 {{ store_name }} 已初具规模，是时候专注于带来流量并提升销量了。以下是一些营销建议，帮助你入门。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          创建你的第一个折扣码
        </mj-text>
        <mj-text font-size="14px">
          提供一个开业折扣，吸引首批客户。前往 <strong>营销 > 折扣码</strong> 创建百分比或固定金额的折扣，可设置使用限制和过期日期。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          设置遗弃购物车恢复
        </mj-text>
        <mj-text font-size="14px">
          自动恢复流失的销售。在 <strong>营销 > 遗弃购物车</strong> 中启用遗弃购物车恢复邮件，提醒客户他们未完成的订单。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          连接你的社交媒体账号
        </mj-text>
        <mj-text font-size="14px">
          将你的社交媒体资料链接到店铺，让客户可以找到并关注你。在 <strong>设置 > 社交媒体</strong> 中添加链接，显示在店铺页脚。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          设置 Google Analytics 跟踪
        </mj-text>
        <mj-text font-size="14px">
          了解访客的来源以及他们如何与你的店铺互动。在 <strong>设置 > 分析</strong> 中添加你的 Google Analytics 跟踪 ID，开始收集数据。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          创建订阅邮件表单
        </mj-text>
        <mj-text font-size="14px">
          从第一天起建立你的邮件列表。在店铺中添加订阅邮件表单，收集访客的电子邮件。利用这些联系人进行促销、产品发布和客户互动。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
入门指南：营销与增长 - {{ store_name }}

你好 {{ name|default:'there' }}，

现在 {{ store_name }} 已初具规模，是时候专注于带来流量并提升销量了。以下是一些营销建议，帮助你入门。

1. 创建你的第一个折扣码
提供一个开业折扣，吸引首批客户。前往 营销 > 折扣码 创建折扣，可设置使用限制和过期日期。

2. 设置遗弃购物车恢复
自动恢复流失的销售。在 营销 > 遗弃购物车 中启用遗弃购物车恢复邮件。

3. 连接你的社交媒体账号
将你的社交媒体资料链接到店铺。在 设置 > 社交媒体 中添加链接。

4. 设置 Google Analytics 跟踪
了解访客的来源。在 设置 > 分析 中添加你的 Google Analytics 跟踪 ID。

5. 创建订阅邮件表单
从第一天起建立你的邮件列表。添加订阅邮件表单，收集访客的电子邮件用于促销和互动。

前往营销：{{ admin_url }}

需要帮助？联系 {{ support_email }}
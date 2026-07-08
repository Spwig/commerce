---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
更进一步 - {{ store_name }}

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
          入门指南：高级功能
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          充分发挥 {{ store_name }} 的潜力
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
          你已经运行 {{ store_name }} 有一两周了。以下是一些高级功能，帮助你将店铺提升到下一个层次。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          设置自动化电子邮件流程
        </mj-text>
        <mj-text font-size="14px">
          使用电子邮件流程自动化客户沟通。在 <strong>营销 > 电子邮件流程</strong> 中设置欢迎序列、购买后跟进和重新参与活动。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          为你的地区配置税规
        </mj-text>
        <mj-text font-size="14px">
          确保你收取正确的税率。前往 <strong>设置 > 税务</strong> 为每个销售地区配置税规。你可以设置含税或不含税的价格。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          探索 API 以进行集成
        </mj-text>
        <mj-text font-size="14px">
          如果你的计划包含 API 访问权限，你可以将店铺与外部工具和服务集成。前往 <strong>设置 > API</strong> 生成 API 密钥并查看文档。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          查看你的分析仪表板
        </mj-text>
        <mj-text font-size="14px">
          时刻关注店铺的表现。你的 <strong>仪表板</strong> 显示关键指标，包括收入、订单、热销产品和客户洞察，帮助你做出数据驱动的决策。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          考虑添加 POS 以进行店内销售
        </mj-text>
        <mj-text font-size="14px">
          也想进行线下销售吗？Spwig 的 POS 功能允许你处理线下交易，并与在线库存和订单管理同步。前往 <strong>设置 > POS</strong> 了解更多信息。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="探索你的仪表板" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
入门指南：高级功能 - {{ store_name }}

你好 {{ name|default:'there' }},

你已经运行 {{ store_name }} 有一两周了。以下是一些高级功能，帮助你将店铺提升到下一个层次。

1. 设置自动化电子邮件流程
使用欢迎序列、购买后跟进和重新参与活动自动化客户沟通。

2. 为你的地区配置税规
确保你收取正确的税率。前往 设置 > 税务 为每个地区配置税规。

3. 探索 API 以进行集成
如果计划包含 API 访问权限，可以将店铺与外部工具集成。前往 设置 > API 开始。

4. 查看你的分析仪表板
你的仪表板显示关键指标，包括收入、订单、热销产品和客户洞察。

5. 考虑添加 POS 以进行店内销售
也想进行线下销售吗？Spwig 的 POS 功能将线下交易与在线库存同步。

探索你的仪表板：{{ admin_url }}

需要帮助？联系 {{ support_email }}
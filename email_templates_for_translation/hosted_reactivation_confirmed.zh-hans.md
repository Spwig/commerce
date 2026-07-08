---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
欢迎回来！{{ store_name }} 已重新启用

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          欢迎回来！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} 已重新启用
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好，
        </mj-text>
        <mj-text>
          好消息！您的 <strong>{{ store_name }}</strong> 商店已重新激活。您的 <strong>{{ plan_name }}</strong> 订阅现已生效，商店即将重新上线。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          重新激活详情
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          计划：{{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          已处理付款：{{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          下次计费日期：{{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          您的商店现在正在重新上线。可能需要几分钟时间让所有内容完全恢复。一旦上线，您的商店将可以通过 {{ store_url }} 访问。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
欢迎回来！{{ store_name }} 已重新启用

你好，

好消息！您的 {{ store_name }} 商店已重新激活。您的 {{ plan_name }} 订阅现已生效，商店即将重新上线。

重新激活详情：
- 计划：{{ plan_name }}
- 已处理付款：{{ currency }}{{ amount }}
- 下次计费日期：{{ next_billing_date }}

您的商店现在正在重新上线。可能需要几分钟时间让所有内容完全恢复。一旦上线，您的商店将可以通过 {{ store_url }} 访问。

前往您的商店：{{ admin_url }}

需要帮助？请联系 {{ support_email }}
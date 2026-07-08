---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
訂閱確認 - {{ store_name }}

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
          訂閱確認！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          歡迎加入 Spwig
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          謝謝您的訂閱！您的 <strong>{{ plan_name }}</strong> 計畫已確認，適用於 <strong>{{ store_name }}</strong>。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          計畫詳情
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          計畫：{{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          計費週期：{{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          金額：{{ currency }}{{ amount }}{% if intro_period %} (試用價格){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          您的試用價格適用於 {{ intro_period }}。之後，您的計劃將以 {{ currency }}{{ full_amount }}/{{ billing_interval }} 重新續訂。
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          您的商店正在設置中，設置完成後您將收到另一封郵件。
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          下次計費日期：{{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
訂閱確認！

Hi {{ name|default:'there' }},

謝謝您的訂閱！您的 {{ plan_name }} 計畫已確認，適用於 {{ store_name }}。

計畫詳情：
- 計畫：{{ plan_name }}
- 計費週期：{{ billing_interval }}
- 金額：{{ currency }}{{ amount }}{% if intro_period %} (試用價格){% endif %}
{% if intro_period %}
這是您的試用價格，適用於 {{ intro_period }}。之後，您的計劃將以 {{ currency }}{{ full_amount }}/{{ billing_interval }} 重新續訂。
{% endif %}
您的商店正在設置中，設置完成後您將收到另一封郵件。

下次計費日期：{{ next_billing_date }}

需要幫助嗎？請聯繫 {{ support_email }}
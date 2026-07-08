---
template_type: subscription_canceled
category: Subscriptions
---

# Email Template: subscription_canceled

## Subject
❌ 您的 {{ plan_name }} 订阅已取消 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          我们很遗憾您离开了
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          您的订阅已取消
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Cancellation Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px" border="2px solid {{ theme.color.text_muted|default:'#6b7280' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
                取消摘要
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>计划:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>取消日期:</strong> {{ cancellation_date|date:"F d, Y" }}
              </mj-text>

              {% if access_until %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>使用权限截止日期:</strong> {{ access_until|date:"F d, Y" }}
              </mj-text>
              <mj-text font-size="13px" color="{{ theme.color.success|default:'#10b981' }}" padding="10px 0 5px 0">
                ✓ 您仍可在 {{ access_until|date:"F d, Y" }} 前继续使用您的权益
              </mj-text>
              {% else %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>状态:</strong> 立即取消
              </mj-text>
              {% endif %}
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What This Means Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          这意味着什么
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          您将不再被收费
        </mj-text>

        {% if access_until %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          您可在 {{ access_until|date:"F d, Y" }} 前继续使用您的权益
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          您的访问权限已立即结束
        </mj-text>
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          您可以随时重新激活订阅
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Feedback Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px 15px 20px" line-height="1.6" align="center">
          我们很乐意听到您的反馈，以帮助我们改进。
        </mj-text>
        <mj-button href="{{ feedback_url }}" background-color="{{ theme.color.text_muted|default:'#6b7280' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="14px" font-weight="600" border-radius="6px" padding="12px 28px">
          提交反馈
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Reactivate CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px 15px 20px" line-height="1.6" align="center">
          改变主意了吗？您可以随时重新激活您的订阅。
        </mj-text>
        <mj-button href="{{ reactivate_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          重新激活订阅
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          需要帮助？请联系 {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            由 Spwig 提供技术支持
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
我们很遗憾您离开了

您的订阅已取消

取消摘要：
计划：{{ plan_name }}
取消日期：{{ cancellation_date|date:"F d, Y" }}
{% if access_until %}使用权限截止日期：{{ access_until|date:"F d, Y" }}

✓ 您仍可在 {{ access_until|date:"F d, Y" }} 前继续使用您的权益
{% else %}状态：立即取消
{% endif %}

这意味着：
• 您将不再被收费
{% if access_until %}• 您可在 {{ access_until|date:"F d, Y" }} 前继续使用您的权益
{% else %}• 您的访问权限已立即结束
{% endif %}• 您可以随时重新激活

我们很乐意听到您的反馈，以帮助我们改进。
提交反馈：{{ feedback_url }}

改变主意了吗？您可以随时重新激活您的订阅。
重新激活订阅：{{ reactivate_url }}

需要帮助？请联系 {{ support_email }}

---
由 Spwig 提供技术支持 - https://spwig.com
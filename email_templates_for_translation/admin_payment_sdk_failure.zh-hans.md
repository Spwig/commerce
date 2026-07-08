---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
支付提供商问题 - {{ provider_name }} SDK 加载失败

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          支付提供商问题
        </mj-text>
        <mj-text>
          在结账过程中，客户无法加载 {{ provider_name }} 支付 SDK。这可能表示提供商出现了服务中断。
        </mj-text>
        <mj-text>
          <strong>提供商：</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>错误类型：</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>时间：</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>失败次数（最近一小时）：</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          此通知每小时每提供商限发一次。如果问题仍然存在，请检查提供商仪表板或联系其支持团队。
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          查看支付设置
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
支付提供商问题

在结账过程中，客户无法加载 {{ provider_name }} 支付 SDK。这可能表示提供商出现了服务中断。

提供商：{{ provider_name }}
错误类型：{{ error_type }}
时间：{{ timestamp }}
失败次数（最近一小时）：{{ failure_count }}

此通知每小时每提供商限发一次。如果问题仍然存在，请检查提供商仪表板或联系其支持团队。

查看支付设置：{{ admin_url }}
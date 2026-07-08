---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ 最后通知：您的订阅将在 {{ days_until_cancellation }} 天后取消

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ 最后通知
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          订阅即将取消
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          这是您的最后通知。我们无法处理您的 {{ plan_name }} 订阅付款。如果您在 {{ days_until_cancellation }} 天内未收到付款，您的订阅将被取消。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ 付款失败 - 需要采取行动
            </mj-text>
            <mj-text color="#991b1b">
              <strong>订阅:</strong> {{ plan_name }}<br/>
              <strong>应付金额:</strong> {{ amount_due }}<br/>
              <strong>失败尝试:</strong> {{ retry_count }}<br/>
              <strong>最后一次尝试:</strong> {{ last_retry_date }}<br/>
              <strong>取消日期:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          付款错误:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          会发生什么:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          如果在 {{ cancellation_date }} 前未收到付款：<br/>
          • 您的订阅将被取消<br/>
          • 您将无法访问所有订阅权益<br/>
          • 您的数据可能会被删除（请参阅保留策略）<br/>
          • 您需要重新订阅才能恢复访问
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          现在更新您的付款方式
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          更新付款方式
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          常见问题及解决方案:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>过期的信用卡:</strong> 使用当前信用卡更新<br/>
          • <strong>余额不足:</strong> 确保余额充足<br/>
          • <strong>信用卡被拒:</strong> 联系银行或使用其他信用卡<br/>
          • <strong>地址不匹配:</strong> 确认账单地址与信用卡一致
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              需要帮助吗？
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              如果您遇到付款问题或需要帮助，请立即联系我们的支持团队。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          联系支持
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          如果您想取消订阅，可以在您的账户设置中进行操作。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 最后通知

订阅即将取消

你好 {{ customer_name }}，

这是您的最后通知。我们无法处理您的 {{ plan_name }} 订阅付款。如果您在 {{ days_until_cancellation }} 天内未收到付款，您的订阅将被取消。

⚠️ 付款失败 - 需要采取行动：
- 订阅：{{ plan_name }}
- 应付金额：{{ amount_due }}
- 失败尝试：{{ retry_count }}
- 最后一次尝试：{{ last_retry_date }}
- 取消日期：{{ cancellation_date }}

付款错误：
{{ payment_error_message }}

会发生什么：
如果在 {{ cancellation_date }} 前未收到付款：
• 您的订阅将被取消
• 您将无法访问所有订阅权益
• 您的数据可能会被删除（请参阅保留策略）
• 您需要重新订阅才能恢复访问

现在更新您的付款方式

常见问题及解决方案：
• 过期的信用卡：使用当前信用卡更新
• 余额不足：确保余额充足
• 信用卡被拒：联系银行或使用其他信用卡
• 地址不匹配：确认账单地址与信用卡一致

需要帮助吗？
如果您遇到付款问题或需要帮助，请立即联系我们的支持团队。

更新付款方式：{{ update_payment_url }}
联系支持：{{ support_url }}

如果您想取消订阅，可以在您的账户设置中进行操作。
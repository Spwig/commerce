---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 您已达到最低付款门槛！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 您已达到最低付款门槛！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          好消息！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ affiliate_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          恭喜！您的联盟账户余额已达到最低付款门槛。现在您可以申请付款。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              您的余额：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>可用余额：</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>最低付款金额：</strong> {{ minimum_payout }}<br/>
              <strong>待结算佣金：</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下来该做什么：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 从您的联盟仪表板申请付款<br/>
          • 付款将在 {{ payout_schedule }} 处理<br/>
          • 资金将通过 {{ payment_method }} 发送
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          申请付款
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看仪表板
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 您已达到最低付款门槛！

好消息！

你好 {{ affiliate_name }}，

恭喜！您的联盟账户余额已达到最低付款门槛。现在您可以申请付款。

您的余额：
- 可用余额：{{ available_balance }}
- 最低付款金额：{{ minimum_payout }}
- 待结算佣金：{{ pending_balance }}

接下来该做什么：
• 从您的联盟仪表板申请付款
• 付款将在 {{ payout_schedule }} 处理
• 资金将通过 {{ payment_method }} 发送

申请付款：{{ request_payout_url }}
查看仪表板：{{ portal_url }}
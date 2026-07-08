---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ 检测到异常佣金活动 - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 高额佣金警报
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          检测到异常活动
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          附属会员 {{ affiliate_name }} 赚取了异常高额的佣金。为防止欺诈，需要进行审核。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              警报详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>附属会员：</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>佣金金额：</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>订单价值：</strong> {{ order_value }}<br/>
              <strong>订单编号：</strong> {{ order_number }}<br/>
              <strong>检测时间：</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          为何被标记：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 检查订单详情以确认其合法性<br/>
          • 检查附属会员的推荐历史记录<br/>
          • 确认客户与推荐人无关联<br/>
          • 在管理面板中批准或拒绝佣金
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          审核佣金
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看附属会员详情
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          该佣金有待审核，未经批准不会支付。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 高额佣金警报

检测到异常活动

附属会员 {{ affiliate_name }} 赚取了异常高额的佣金。为防止欺诈，需要进行审核。

警报详情：
- 附属会员：{{ affiliate_name }} ({{ affiliate_id }})
- 佣金金额：{{ commission_amount }}
- 订单价值：{{ order_value }}
- 订单编号：{{ order_number }}
- 检测时间：{{ detected_at }}

为何被标记：
{{ flag_reason }}

建议操作：
• 检查订单详情以确认其合法性
• 检查附属会员的推荐历史记录
• 确认客户与推荐人无关联
• 在管理面板中批准或拒绝佣金

审核佣金：{{ review_commission_url }}
查看附属会员详情：{{ affiliate_details_url }}

该佣金有待审核，未经批准不会支付。
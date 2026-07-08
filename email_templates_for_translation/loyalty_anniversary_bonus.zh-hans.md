---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} 年 - 感谢您！

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} 年庆祝！
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          今天标志着您加入我们忠诚度计划以来的 {{ years_as_member }} 年{{ years_as_member|pluralize }}。感谢您成为如此宝贵的一员！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              周年奖励
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} 积分
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              为庆祝 {{ years_as_member }} 年{{ years_as_member|pluralize }} 而添加！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          您的 {{ years_as_member }} 年旅程：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} points<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看您的忠诚度仪表板
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          感谢您 {{ years_as_member }} 个精彩的年份{{ years_as_member|pluralize }}！<br/>
          祝您未来有更多 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} 年庆祝！

Hi {{ customer_name }},

今天标志着您加入我们忠诚度计划以来的 {{ years_as_member }} 年{{ years_as_member|pluralize }}。感谢您成为如此宝贵的一员！

周年奖励：
{{ bonus_points }} 积分
为庆祝 {{ years_as_member }} 年{{ years_as_member|pluralize }} 而添加！

您的 {{ years_as_member }} 年旅程：
- 注册时间：{{ member_since }}
- 订单总数：{{ total_orders }}
- 获得积分：{{ lifetime_points }} 积分
- 当前等级：{{ loyalty_tier }}
- 总节省金额：{{ total_savings }}

查看您的忠诚度仪表板：{{ loyalty_dashboard_url }}

感谢您 {{ years_as_member }} 个精彩的年份{{ years_as_member|pluralize }}！
祝您未来有更多 🥂
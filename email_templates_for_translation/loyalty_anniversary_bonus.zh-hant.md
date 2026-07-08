---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} 年 - 感謝您！

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} 年一起！
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          今天是您加入我們忠誠度計劃的 {{ years_as_member }} 年{{ years_as_member|pluralize }}。感謝您成為如此受重視的成員！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              周年禮品
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} 點數
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              為慶祝 {{ years_as_member }} 年{{ years_as_member|pluralize }} 而添加！
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
          查看您的忠誠度儀表板
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          感謝您 {{ years_as_member }} 個精彩的年份{{ years_as_member|pluralize }}！<br/>
          祝您未來有更多美好時光 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} 年一起！

Hi {{ customer_name }},

今天是您加入我們忠誠度計劃的 {{ years_as_member }} 年{{ years_as_member|pluralize }}。感謝您成為如此受重視的成員！

周年禮品：
{{ bonus_points }} 點數
為慶祝 {{ years_as_member }} 年{{ years_as_member|pluralize }} 而添加！

您的 {{ years_as_member }} 年旅程：
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} points
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

View your loyalty dashboard: {{ loyalty_dashboard_url }}

感謝您 {{ years_as_member }} 個精彩的年份{{ years_as_member|pluralize }}！
祝您未來有更多美好時光 🥂
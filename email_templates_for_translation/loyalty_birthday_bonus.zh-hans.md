---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 生日快乐 {{ customer_name }}！来自 {{ shop_name }} 的特别礼物

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          生日快乐！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          生日快乐，{{ customer_name }}！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          为庆祝您的特殊日子，我们已将 {{ bonus_points }} 积分添加到您的忠诚账户！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              您的生日礼物
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} 积分
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              已添加到您的账户！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          您的忠诚账户：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>积分余额：</strong>{{ total_points }} 积分<br/>
          <strong>当前等级：</strong>{{ loyalty_tier }}<br/>
          <strong>生日奖励：</strong>+{{ bonus_points }} 积分
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          开始购物并使用您的积分
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          祝您度过一个美好的生日！🎉<br/>
          - {{ shop_name }} 团队
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 生日快乐！

生日快乐，{{ customer_name }}！

为庆祝您的特殊日子，我们已将 {{ bonus_points }} 积分添加到您的忠诚账户！

您的生日礼物：
{{ bonus_points }} 积分
已添加到您的账户！

您的忠诚账户：
- 积分余额：{{ total_points }} 积分
- 当前等级：{{ loyalty_tier }}
- 生日奖励：+{{ bonus_points }} 积分

开始购物并使用您的积分：{{ shop_url }}

祝您度过一个美好的生日！🎉
- {{ shop_name }} 团队
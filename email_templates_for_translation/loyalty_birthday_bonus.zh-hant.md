---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 生日快樂 {{ customer_name }}！這是來自 {{ shop_name }} 的特別禮物

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          生日快樂！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          生日快樂，{{ customer_name }}！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          為了慶祝您的特別日子，我們已將 {{ bonus_points }} 個額外積分添加到您的忠誠度賬戶中！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              您的生日禮物
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} 點數
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              已添加到您的賬戶！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          您的忠誠度賬戶：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>積分餘額：</strong>{{ total_points }} 點數<br/>
          <strong>當前等級：</strong>{{ loyalty_tier }}<br/>
          <strong>生日贈禮：</strong>+{{ bonus_points }} 點數
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          開始購物並使用您的積分
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          祝您度過一個美好的生日！🎉<br/>
          - {{ shop_name }} 團隊
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 生日快樂！

生日快樂，{{ customer_name }}！

為了慶祝您的特別日子，我們已將 {{ bonus_points }} 個額外積分添加到您的忠誠度賬戶中！

您的生日禮物：
{{ bonus_points }} 點數
已添加到您的賬戶！

您的忠誠度賬戶：
- 積分餘額：{{ total_points }} 點數
- 當前等級：{{ loyalty_tier }}
- 生日贈禮：+{{ bonus_points }} 點數

開始購物並使用您的積分：{{ shop_url }}

祝您度過一個美好的生日！🎉
- {{ shop_name }} 團隊
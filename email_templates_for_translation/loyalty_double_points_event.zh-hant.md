---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 現在開始雙倍積分活動！- {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 2X POINTS EVENT!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          為忠誠會員專屬！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          準備好賺大錢了！在有限的時間內，您將在每次購物時獲得 {{ points_multiplier }}X 的積分。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              獲得 {{ points_multiplier }}X 積分
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              在所有購買中<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          範例收益：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              花費 $50 → 正常獲得 {{ example_points_normal }} 點
              <strong style="color: #047857;">在這次活動期間 → 獲得 {{ example_points_bonus }} 點！🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              花費 $100 → 正常獲得 {{ example_points_normal_2 }} 點
              <strong style="color: #047857;">在這次活動期間 → 獲得 {{ example_points_bonus_2 }} 點！🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          您的當前餘額：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>積分：</strong> {{ current_points }} 點<br/>
          <strong>等級：</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          現在購物並獲得 {{ points_multiplier }}X 點數
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          活動於 {{ event_end }} 結束 - 請勿錯過！
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 2X POINTS EVENT!
{{ event_start }} - {{ event_end }}

為忠誠會員專屬！

Hi {{ customer_name }},

準備好賺大錢了！在有限的時間內，您將在每次購物時獲得 {{ points_multiplier }}X 的積分。

EARN {{ points_multiplier }}X POINTS
在所有購買中
{{ event_start }} - {{ event_end }}

EXAMPLE EARNINGS:
- 花費 $50 → 正常獲得 {{ example_points_normal }} 點
  在這次活動期間 → 獲得 {{ example_points_bonus }} 點！🎉

- 花費 $100 → 正常獲得 {{ example_points_normal_2 }} 點
  在這次活動期間 → 獲得 {{ example_points_bonus_2 }} 點！🎉

YOUR CURRENT BALANCE:
- 點數：{{ current_points }} 點
- 等級：{{ loyalty_tier }}

現在購物並獲得 {{ points_multiplier }}X 點數：{{ shop_url }}

活動於 {{ event_end }} 結束 - 請勿錯過！
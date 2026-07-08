---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 2倍ポイントイベントが今すぐ開始！- {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 2倍ポイントイベント！
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ロイヤルティ会員限定！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          お買いものでたくさんポイントをGET！限定期間中、すべての購入で {{ points_multiplier }}倍のポイントを獲得できます。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              {{ points_multiplier }}倍ポイント獲得
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              すべての購入で<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          例：獲得ポイント
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              $50 お支払い → {{ example_points_normal }} ポイント通常獲得<br/>
              <strong style="color: #047857;">イベント期間中 → {{ example_points_bonus }} ポイント獲得！🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              $100 お支払い → {{ example_points_normal_2 }} ポイント通常獲得<br/>
              <strong style="color: #047857;">イベント期間中 → {{ example_points_bonus_2 }} ポイント獲得！🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          現在のポイント残高：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>ポイント：</strong> {{ current_points }} ポイント<br/>
          <strong>ランク：</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          今すぐ購入して {{ points_multiplier }}倍ポイントを獲得
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          イベント終了日：{{ event_end }} - ミスしないでください！
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 2倍ポイントイベント！
{{ event_start }} - {{ event_end }}

ロイヤルティ会員限定！

こんにちは {{ customer_name }}、

お買いものでたくさんポイントをGET！限定期間中、すべての購入で {{ points_multiplier }}倍のポイントを獲得できます。

{{ points_multiplier }}倍ポイント獲得
すべての購入で
{{ event_start }} - {{ event_end }}

例：獲得ポイント：
- $50 お支払い → {{ example_points_normal }} ポイント通常獲得
  イベント期間中 → {{ example_points_bonus }} ポイント獲得！🎉

- $100 お支払い → {{ example_points_normal_2 }} ポイント通常獲得
  イベント期間中 → {{ example_points_bonus_2 }} ポイント獲得！🎉

現在のポイント残高：
- ポイント：{{ current_points }} ポイント
- ランク：{{ loyalty_tier }}

今すぐ購入して {{ points_multiplier }}倍ポイントを獲得：{{ shop_url }}

イベント終了日：{{ event_end }} - ミスしないでください！
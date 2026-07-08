---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 マイナス支払い閾値に達しました！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 支払い閾値に達しました！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          グレートニュース！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ affiliate_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          おめでとうございます！アフィリエイト残高が最低支払い閾値に達しました。今から支払いを依頼できます。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              あなたの残高:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>利用可能な残高：</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>最低支払い：</strong> {{ minimum_payout }}<br/>
              <strong>保留中のコミッション：</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          次のステップ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • アフィリエイトダッシュボードから支払いを依頼してください<br/>
          • 支払いは {{ payout_schedule }} で処理されます<br/>
          • 資金は {{ payment_method }} で送金されます
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          支払いを依頼する
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ダッシュボードを表示
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 支払い閾値に達しました！

グレートニュース！

こんにちは {{ affiliate_name }}、

おめでとうございます！アフィリエイト残高が最低支払い閾値に達しました。今から支払いを依頼できます。

あなたの残高:
- 利用可能な残高：{{ available_balance }}
- 最低支払い：{{ minimum_payout }}
- 保留中のコミッション：{{ pending_balance }}

次のステップ:
• アフィリエイトダッシュボードから支払いを依頼してください
• 支払いは {{ payout_schedule }} で処理されます
• 資金は {{ payment_method }} で送金されます

支払いを依頼する: {{ request_payout_url }}
ダッシュボードを表示: {{ portal_url }}
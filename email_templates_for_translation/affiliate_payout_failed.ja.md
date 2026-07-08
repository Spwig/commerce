---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
アクションが必要です: 支払いが失敗しました

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ 支払いが失敗しました
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          支払いID: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          こんにちは {{ affiliate_name }}、
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ payout_amount }} の支払い処理中に問題が発生しました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          これは通常、支払い情報が間違っているか、支払いプロバイダーの問題によるものです。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          お支払い情報の更新と、弊社のサポートチームへの連絡をお願いいたします。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          お支払い情報の更新
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          お手伝いが必要ですか？ <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートに連絡</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
アクションが必要です: 支払いが失敗しました

こんにちは {{ affiliate_name }},

{{ payout_amount }} の支払い処理中に問題が発生しました (支払いID: {{ payout_id }}).

これは通常、支払い情報が間違っているか、支払いプロバイダーの問題によるものです。

お支払い情報の更新と、弊社のサポートチームへの連絡をお願いいたします。

お支払い情報の更新: {{ portal_url }}

{{ shop_name }}
お手伝いが必要ですか？ {{ support_email }} に連絡してください。
---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
支払いがキャンセルされました - {{ payout_amount }}

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
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          支払いがキャンセルされました
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
          {{ payout_amount }} (支払いID: {{ payout_id }}) の支払いがキャンセルされました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          この支払いがキャンセルされた理由について質問がある場合は、サポートチームにお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          アフィリエイトダッシュボードを表示
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          質問は？ <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートに連絡</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
支払いがキャンセルされました - {{ payout_amount }}

こんにちは {{ affiliate_name }}、

{{ payout_amount }} (支払いID: {{ payout_id }}) の支払いがキャンセルされました。

この支払いがキャンセルされた理由について質問がある場合は、サポートチームにお問い合わせください。

ダッシュボードを表示: {{ portal_url }}

{{ shop_name }}
質問は？ {{ support_email }} に連絡してください。
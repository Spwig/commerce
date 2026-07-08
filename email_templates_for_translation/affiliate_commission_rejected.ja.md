---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
コンミッションステータスの更新 - 注文番号 #{{ order_number }}

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
          コンミッションステータスの更新
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
          注文番号 #{{ order_number }} ({{ commission_amount }}) のコンミッションが承認されませんでした。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          これは、コンミッション期間が終了する前に注文がキャンセルまたは返金された場合に通常起こります。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          このコンミッションについて質問がある場合は、弊社のサポートチームにお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          アフィリエイトダッシュボードを確認する
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ご質問は? <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートに連絡</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
コンミッションステータスの更新 - 注文番号 #{{ order_number }}

こんにちは {{ affiliate_name }}、

注文番号 #{{ order_number }} ({{ commission_amount }}) のコンミッションが承認されませんでした。

これは、コンミッション期間が終了する前に注文がキャンセルまたは返金された場合に通常起こります。

このコンミッションについて質問がある場合は、弊社のサポートチームにお問い合わせください。

アフィリエイトダッシュボードを確認する: {{ portal_url }}

{{ shop_name }}
ご質問は? {{ support_email }} に連絡してください。
---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
重要: アカウントの一時停止

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
          アカウントの一時停止
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
          {{ shop_name }} とのアフィリエイトアカウントが一時停止されました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          これは通常、私たちのアフィリエイトプログラムの利用規約および条件に違反したためです。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          この措置が誤りであるとお考えたり、この決定について話し合いをご希望の場合は、弊社のサポートチームにお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          質問は? <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートに連絡</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
重要: アカウントの一時停止

こんにちは {{ affiliate_name }}、

{{ shop_name }} とのアフィリエイトアカウントが一時停止されました。

これは通常、私たちのアフィリエイトプログラムの利用規約および条件に違反したためです。

この措置が誤りであるとお考えたり、この決定について話し合いをご希望の場合は、弊社のサポートチームにお問い合わせください。

{{ shop_name }}
質問は? {{ support_email }} に連絡してください。
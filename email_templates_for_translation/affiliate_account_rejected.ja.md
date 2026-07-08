---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
アフィリエイト申請の更新

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
          申請の更新
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
          {{ shop_name }} アフィリエイトプログラムへの参加にご関心いただき、ありがとうございます。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          申請内容を確認した結果、このたびは進展を図らないことに決定しました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          この決定は、現在のアフィリエイトプログラムの要件に基づいており、あなたの資格や可能性を反映していない可能性があります。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          ご状況が変化した場合、今後再申請することをお勧めします。
        </mj-text>
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
アフィリエイト申請の更新

こんにちは {{ affiliate_name }}、

{{ shop_name }} アフィリエイトプログラムへの参加にご関心いただき、ありがとうございます。

申請内容を確認した結果、このたびは進展を図らないことに決定しました。

この決定は、現在のアフィリエイトプログラムの要件に基づいており、あなたの資格や可能性を反映していない可能性があります。

ご状況が変化した場合、今後再申請することをお勧めします。

{{ shop_name }}
質問は？ {{ support_email }}
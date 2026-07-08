---
template_type: affiliate_program_approved
category: Affiliate Program
---

# Email Template: affiliate_program_approved

## Subject
「{{ program_name }}」に承認されました！

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
          ✓ プログラムが承認されました！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          {{ program_name }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          承認されました！
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
          ご報告です！{{ program_name }} のプロモーションが承認されました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          このプログラムを共有して、報酬を獲得し始めましょう！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          アフィリエイトリンクを取得
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ご質問は？<a href="mailto:{{ support_email }}" style="color: #007bff;">サポートに連絡</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
「{{ program_name }}」に承認されました！

こんにちは {{ affiliate_name }}、

ご報告です！{{ program_name }} のプロモーションが承認されました。

このプログラムを共有して、報酬を獲得し始めましょう！

アフィリエイトリンクを取得: {{ portal_url }}

{{ shop_name }}
ご質問は？{{ support_email }}
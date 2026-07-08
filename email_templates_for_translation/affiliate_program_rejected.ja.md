---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
アプリケーションの申請状況のお知らせ

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
          アプリケーションの申請状況
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
          {{ program_name }} のプロモーション申請、ありがとうございます。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          申請内容を確認した結果、当面の承認は見合わせることにしました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          他のプログラムのプロモーションも引き続き可能です。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          他のプログラムを確認する
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ご質問は？ <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートチームへお問い合わせ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
プログラム申請状況のお知らせ

こんにちは {{ affiliate_name }}、

{{ program_name }} のプロモーション申請、ありがとうございます。

申請内容を確認した結果、当面の承認は見合わせることにしました。

他のプログラムのプロモーションも引き続き可能です。

他のプログラムを確認する: {{ portal_url }}

{{ shop_name }}
ご質問は？ {{ support_email }}}}
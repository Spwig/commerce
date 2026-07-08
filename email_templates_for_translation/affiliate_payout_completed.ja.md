---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ 支払いが完了しました: {{ payout_amount }}

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
          🎉 支払いが完了しました！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ 支払いが成功しました
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
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
          {{ payout_amount }} の支払いが成功裏に完了しました！
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          お支払いはあなたの支払い方法に送信されました。銀行または支払い処理業者により、1〜2営業日にあなたの口座に反映される場合があります。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }} の宣伝ありがとうございます。素晴らしい仕事を続けてください！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          支払いの詳細を確認
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ご質問は？ <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートに連絡</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 支払いが完了しました: {{ payout_amount }}

こんにちは {{ affiliate_name }}、

{{ payout_amount }} の支払いが成功裏に完了しました！

支払いの詳細:
- 支払いID: {{ payout_id }}
- 金額: {{ payout_amount }}
- 支払い方法: {{ payout_method }}

お支払いはあなたの支払い方法に送信されました。銀行または支払い処理業者により、1〜2営業日にあなたの口座に反映される場合があります。

{{ shop_name }} の宣伝ありがとうございます。素晴らしい仕事を続けてください！

支払いの詳細を確認: {{ portal_url }}

{{ shop_name }}
ご質問は？ {{ support_email }} に連絡してください。
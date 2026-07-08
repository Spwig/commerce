---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
💰 {{ commission_amount }} のコミッションを稼ぎました！

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
          💰 コミッションを稼ぎました！
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ shop_name }} からの嬉しいニュース
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 あなたのコミッション
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          注文番号 #{{ order_number }} から
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
          おめでとうございます！注文番号 #{{ order_number }} から {{ commission_amount }} のコミッションを稼ぎました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }} のプロモーションを続けて、より多くのコミッションを稼いでください。販売を増やすほど、稼ぐことができます！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>注文番号：</strong>#{{ order_number }}<br/>
          <strong>コミッション額：</strong>{{ commission_amount }}<br/>
          <strong>コミッション率：</strong>{{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          アフィリエイトダッシュボードを確認する
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          質問は？ <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートにお問い合わせ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ commission_amount }} のコミッションを稼ぎました！

こんにちは {{ affiliate_name }}、

おめでとうございます！注文番号 #{{ order_number }} から {{ commission_amount }} のコミッションを稼ぎました。

コミッションの詳細：
- 注文番号：#{{ order_number }}
- コミッション額：{{ commission_amount }}
- コミッション率：{{ commission_rate }}%

{{ shop_name }} のプロモーションを続けて、より多くのコミッションを稼いでください。

ダッシュボードを確認：{{ portal_url }}

{{ shop_name }}
質問は？ {{ support_email }} にご連絡ください。
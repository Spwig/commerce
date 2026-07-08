---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
あなたの店舗は準備完了 - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          あなたの店舗は稼働中です！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} はあなたのために準備できました
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          こんにちは {{ name|default:'there' }}、
        </mj-text>
        <mj-text>
          グッドラック！あなたの Spwig 店舗 <strong>{{ store_name }}</strong> はプロビジョニングされ、現在稼働中です。すぐに商品、ブランド、支払い方法の設定を開始できます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          あなたの店舗の詳細
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          店舗URL: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          管理パネル: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          地域: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          クイックスタート
        </mj-text>
        <mj-text font-size="14px">
          1. 注文時に設定したメールアドレスとパスワードを使用して管理パネルにログインしてください
        </mj-text>
        <mj-text font-size="14px">
          2. デザイン > テーマ設定で店舗のロゴとブランドを追加してください
        </mj-text>
        <mj-text font-size="14px">
          3. カタログ > 商品で最初の商品を追加してください
        </mj-text>
        <mj-text font-size="14px">
          4. 設定 > 支払いプロバイダーで支払いプロバイダーを設定してください
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
あなたの店舗は稼働中です！

{{ store_name }} はあなたのために準備できました。

こんにちは {{ name|default:'there' }}、

グッドラック！あなたの Spwig 店舗 {{ store_name }} はプロビジョニングされ、現在稼働中です。すぐに商品、ブランド、支払い方法の設定を開始できます。

あなたの店舗の詳細:
- 店舗URL: {{ store_url }}
- 管理パネル: {{ admin_url }}
- 地域: {{ region }}

クイックスタート:
1. 注文時に設定したメールアドレスとパスワードを使用して管理パネルにログインしてください
2. デザイン > テーマ設定で店舗のロゴとブランドを追加してください
3. カタログ > 商品で最初の商品を追加してください
4. 設定 > 支払いプロバイダーで支払いプロバイダーを設定してください

管理パネルへ: {{ admin_url }}

お手伝いが必要ですか？{{ support_email }} にご連絡ください
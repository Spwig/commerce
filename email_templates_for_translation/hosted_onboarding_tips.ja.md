---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
{{ store_name }} を最大限に活用するためのヒント

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
          初心者向けのヒント
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Spwig ストアを最大限に活用する方法
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
          今や {{ store_name }} が稼働しています。ストアを最大限に活用するためのいくつかのヒントをご紹介します。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          テーマをカスタマイズ
        </mj-text>
        <mj-text font-size="14px">
          <strong>Design > Theme Settings</strong> にアクセスして、テーマを選択し、ロゴをアップロードし、ブランドカラーを設定してください。ストアの外観は即座に更新されるため、変更をリアルタイムでプレビューできます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          商品を追加
        </mj-text>
        <mj-text font-size="14px">
          <strong>Catalog > Products</strong> にアクセスして、商品を追加し始めましょう。商品のバリエーション（サイズ、色）、価格設定、在庫管理、高品質な画像のアップロードが可能です。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          支払い方法を設定
        </mj-text>
        <mj-text font-size="14px">
          <strong>Settings > Payment Providers</strong> にアクセスして、Stripe、PayPal、または他の支払い方法を接続してください。複数の支払い方法を有効にすることで、顧客が希望する方法で支払いできます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          配送設定
        </mj-text>
        <mj-text font-size="14px">
          <strong>Settings > Shipping</strong> で、配送地域と料金を設定してください。さまざまな地域向けに、定額、重量ベース、または無料配送のルールを作成できます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          SEOを強化
        </mj-text>
        <mj-text font-size="14px">
          Spwig は自動的にサイトマップとメタタグを生成します。<strong>Settings > SEO</strong> にアクセスして、ページタイトル、説明、ソーシャル共有画像をカスタマイズし、顧客がストアを簡単に見つけるようにしてください。
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
初心者向けのヒント - {{ store_name }}

こんにちは {{ name|default:'there' }}、

今や {{ store_name }} が稼働しています。ストアを最大限に活用するためのいくつかのヒントをご紹介します。

1. テーマをカスタマイズ
Design > Theme Settings にアクセスして、テーマを選択し、ロゴをアップロードし、ブランドカラーを設定してください。

2. 商品を追加
Catalog > Products にアクセスして、商品を追加し始めましょう。商品のバリエーション（サイズ、色）、価格設定、在庫管理、高品質な画像のアップロードが可能です。

3. 支払い方法を設定
Settings > Payment Providers にアクセスして、Stripe、PayPal、または他の支払い方法を接続してください。

4. 配送設定
Settings > Shipping で、配送地域と料金を設定してください。さまざまな地域向けに、定額、重量ベース、または無料配送のルールを作成できます。

5. SEOを強化
Settings > SEO にアクセスして、ページタイトル、説明、ソーシャル共有画像をカスタマイズし、顧客がストアを簡単に見つけるようにしてください。

Admin Panel へ: {{ admin_url }}

お手伝いが必要ですか？ {{ support_email }} にご連絡ください。
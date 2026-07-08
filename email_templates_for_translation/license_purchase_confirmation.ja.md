---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Spwigライセンス - 注文番号 #{{ order_number }}

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
          ご購入ありがとうございます！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          注文番号 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          こんにちは {{ customer_name }}、
        </mj-text>
        <mj-text>
          {{ product_name }} のご購入が完了しました。以下にライセンスキーおよびセットアップトークンを記載していますので、ご利用ください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          注文概要
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          商品: {{ product_name }}{% if includes_pos %} (POSを含む){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          金額: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          注文番号: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          あなたのライセンスキー
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          このキーを保存してください - 再インストール時に必要です
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          あなたのセットアップトークン
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          インストール時にこのトークンを使用してストアをアクティベートしてください
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          スタートガイド
        </mj-text>
        <mj-text font-size="14px">
          1. ご自分のサーバーにSpwigをインストールするためのセットアップガイドに従ってください
        </mj-text>
        <mj-text font-size="14px">
          2. インストール中にセットアップトークンを入力してください
        </mj-text>
        <mj-text font-size="14px">
          3. ストアは自動的にアクティベートされます
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          アカウントを作成する
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          パスワードを設定して、ライセンスの管理、ダウンロードへのアクセス、アップデートの受信が可能になります。
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          重要:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          このメールを安全に保管してください - 今後のためにライセンスキーおよびセットアップトークンが含まれています。これらの資格情報を他人と共有しないでください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ご購入ありがとうございます！

注文番号 #{{ order_number }}

こんにちは {{ customer_name }}、

{{ product_name }} のご購入が完了しました。以下にライセンスキーおよびセットアップトークンを記載していますので、ご利用ください。

注文概要:
- 商品: {{ product_name }}{% if includes_pos %} (POSを含む){% endif %}
- 金額: {{ price }}
- 注文番号: {{ order_number }}

あなたのライセンスキー:
{{ license_key }}
このキーを保存してください - 再インストール時に必要です。

あなたのセットアップトークン:
{{ setup_token }}
インストール時にこのトークンを使用してストアをアクティベートしてください。

スタートガイド:
1. ご自分のサーバーにSpwigをインストールするためのセットアップガイドに従ってください
2. インストール中にセットアップトークンを入力してください
3. ストアは自動的にアクティベートされます

セットアップガイドを表示: {{ setup_url }}
{% if activation_url %}
アカウントを作成する:
パスワードを設定して、ライセンスの管理、ダウンロードへのアクセス、アップデートの受信が可能になります。
{{ activation_url }}
{% endif %}
重要:
このメールを安全に保管してください - 今後のためにライセンスキーおよびセットアップトークンが含まれています。これらの資格情報を他人と共有しないでください。

お手伝いが必要ですか？ {{ support_email }} にご連絡ください。
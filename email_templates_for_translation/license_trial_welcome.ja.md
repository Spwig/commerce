---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Spwigへようこそ - {{ trial_days }}日間の無料トライアル

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Spwigへようこそ！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ trial_days }}日間の無料トライアルが準備できました
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
          {{ product_name }}のトライアルを試していただきありがとうございます！トライアルが有効化され、Spwigが提供するすべての機能を{{ trial_days }}日間お試しいただけます{% if includes_pos %}。また、ポジションシステムも含まれます{% endif %}。
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
          インストール時にこのトークンを使用してトライアルストアを有効にしてください
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          スタートする
        </mj-text>
        <mj-text font-size="14px">
          1. お手引書に従って、Spwigをサーバーにインストールしてください
        </mj-text>
        <mj-text font-size="14px">
          2. インストール中にプロンプトが表示されたら、セットアップトークンを入力してください
        </mj-text>
        <mj-text font-size="14px">
          3. オンラインストアの構築を開始してください！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          トライアルに含まれるもの
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ trial_days }}日間、すべてのコア機能へのフルアクセス
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          商品カタログ、注文、顧客管理
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          テーマカスタマイズとページビルダー
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          支払いおよび配送プロバイダーの統合
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ポイントオブセール（POS）システム
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          トライアルは{{ trial_days }}日後に終了します。準備が整ったら、フルライセンスにアップグレードして、データの損失なしにストアを稼働させ続けてください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Spwigへようこそ！
{{ trial_days }}日間の無料トライアルが準備できました。

こんにちは {{ customer_name }}、

{{ product_name }}のトライアルを試していただきありがとうございます！トライアルが有効化され、Spwigが提供するすべての機能を{{ trial_days }}日間お試しいただけます{% if includes_pos %}。また、ポジションシステムも含まれます{% endif %}。

YOUR SETUP TOKEN:
{{ setup_token }}
インストール時にこのトークンを使用してトライアルストアを有効にしてください。

Getting Started:
1. お手引書に従って、Spwigをサーバーにインストールしてください
2. インストール中にプロンプトが表示されたら、セットアップトークンを入力してください
3. オンラインストアの構築を開始してください！

View Setup Guide: {{ setup_url }}

What's Included in Your Trial:
- {{ trial_days }}日間、すべてのコア機能へのフルアクセス
- 商品カタログ、注文、顧客管理
- テーマカスタマイズとページビルダー
- 支払いおよび配送プロバイダーの統合
{% if includes_pos %}- ポイントオブセール（POS）システム{% endif %}

Your trial will expire in {{ trial_days }} days. When you're ready, upgrade to a full license to keep your store running with no data loss.

Need help? Contact {{ support_email }}
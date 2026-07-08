---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
歡迎使用 Spwig - 您的 {{ trial_days }} 天免費試用

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
          歡迎使用 Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          您的 {{ trial_days }} 天免費試用已準備好
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          親愛的 {{ customer_name }}，
        </mj-text>
        <mj-text>
          感謝您試用 <strong>{{ product_name }}</strong>！您的試用已啟動，您有 <strong>{{ trial_days }} 天</strong> 的時間來探索 Spwig 提供的所有功能{% if includes_pos %}，包括我們的銷售點系統{% endif %}。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          您的設定令牌
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          在安裝期間使用此令牌以啟動您的試用商店
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          開始使用
        </mj-text>
        <mj-text font-size="14px">
          1. 跟隨我們的設定指南，在您的伺服器上安裝 Spwig
        </mj-text>
        <mj-text font-size="14px">
          2. 在安裝過程中提示時輸入您的設定令牌
        </mj-text>
        <mj-text font-size="14px">
          3. 開始建立您的線上商店！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          您的試用包含哪些內容
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          在 {{ trial_days }} 天內可完全使用所有核心功能
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          產品目錄、訂單和客戶管理
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          主題自定義和頁面構建器
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          支付和運輸供應商整合
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          銷售點（POS）系統
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          您的試用將在 {{ trial_days }} 天後到期。當您準備好時，升級為完整許可證以繼續運行您的商店，不會有任何數據丟失。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
歡迎使用 Spwig!
您的 {{ trial_days }} 天免費試用已準備好。

親愛的 {{ customer_name }}，

感謝您試用 {{ product_name }}！您的試用已啟動，您有 {{ trial_days }} 天的時間來探索 Spwig 提供的所有功能{% if includes_pos %}，包括我們的銷售點系統{% endif %}。

您的設定令牌：
{{ setup_token }}
在安裝期間使用此令牌以啟動您的試用商店。

開始使用：
1. 跟隨我們的設定指南，在您的伺服器上安裝 Spwig
2. 在安裝過程中提示時輸入您的設定令牌
3. 開始建立您的線上商店！

查看設定指南： {{ setup_url }}

您的試用包含哪些內容：
- 在 {{ trial_days }} 天內可完全使用所有核心功能
- 產品目錄、訂單和客戶管理
- 主題自定義和頁面構建器
- 支付和運輸供應商整合
{% if includes_pos %}- 銷售點（POS）系統{% endif %}

您的試用將在 {{ trial_days }} 天後到期。當您準備好時，升級為完整許可證以繼續運行您的商店，不會有任何數據丟失。

需要幫助嗎？請聯繫 {{ support_email }}
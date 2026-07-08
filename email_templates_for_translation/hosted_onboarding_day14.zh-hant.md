---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
更進一步 - {{ store_name }}

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
          開始使用：高級功能
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          發掘 {{ store_name }} 的全部潛力
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好 {{ name|default:'there' }}，
        </mj-text>
        <mj-text>
          你已經運營 {{ store_name }} 一兩個星期了。以下是一些高級功能，幫助你將商店提升到下一個層次。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          設置自動化郵件流程
        </mj-text>
        <mj-text font-size="14px">
          使用郵件流程自動化與客戶的溝通。在 <strong>Marketing > Email Workflows</strong> 下設置歡迎序列、購後追蹤和重新參與活動。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          為你的地區配置稅務規則
        </mj-text>
        <mj-text font-size="14px">
          確保你收取正確的稅率。前往 <strong>Settings > Tax</strong> 為你銷售的每個地區配置稅務規則。你可以設置含稅或不含稅的定價。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          探索 API 進行整合
        </mj-text>
        <mj-text font-size="14px">
          如果你的方案包含 API 存取權，你可以將商店與外部工具和服務整合。前往 <strong>Settings > API</strong> 生成 API 金鑰並查看文件。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          檢視你的分析儀表板
        </mj-text>
        <mj-text font-size="14px">
          留意商店的表現。你的 <strong>Dashboard</strong> 顯示關鍵指標，包括收入、訂單、熱門產品和客戶洞察，幫助你做出數據驅動的決策。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          考慮新增 POS 進行實體店銷售
        </mj-text>
        <mj-text font-size="14px">
          你也想進行實體銷售嗎？Spwig 的 POS 功能讓你處理實體店交易，並與線上庫存和訂單管理同步。前往 <strong>Settings > Point of Sale</strong> 了解更多。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="探索你的儀表板" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
開始使用：高級功能 - {{ store_name }}

你好 {{ name|default:'there' }},

你已經運營 {{ store_name }} 一兩個星期了。以下是一些高級功能，幫助你將商店提升到下一個層次。

1. 設置自動化郵件流程
使用歡迎序列、購後追蹤和重新參與活動自動化與客戶的溝通。

2. 為你的地區配置稅務規則
確保你收取正確的稅率。前往 Settings > Tax 為你銷售的每個地區配置規則。

3. 探索 API 進行整合
如果你的方案包含 API 存取權，將商店與外部工具整合。前往 Settings > API 開始。

4. 檢視你的分析儀表板
你的 Dashboard 顯示關鍵指標，包括收入、訂單、熱門產品和客戶洞察。

5. 考慮新增 POS 進行實體店銷售
你也想進行實體銷售嗎？Spwig 的 POS 功能讓實體店交易與線上庫存同步。

探索你的儀表板：{{ admin_url }}

需要幫助嗎？請聯繫 {{ support_email }}
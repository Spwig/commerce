---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
擴展您的銷售 - {{ store_name }}

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
          開始行動：行銷與增長
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          增加流量並提升 {{ store_name }} 的銷售
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          當 {{ store_name }} 開始成形，現在是時候專注於增加流量並提升銷售。以下有五個行銷技巧幫助你開始。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          建立您的第一個折扣碼
        </mj-text>
        <mj-text font-size="14px">
          提供一個開幕折扣來吸引您的第一批客戶。前往 <strong>Marketing > Discount Codes</strong> 來建立百分比或固定金額的折扣，並可選擇設定使用次數限制和過期日期。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          設定遺漏購物車恢復功能
        </mj-text>
        <mj-text font-size="14px">
          自動恢復遺失的銷售。在 <strong>Marketing > Abandoned Carts</strong> 啟用遺漏購物車恢復郵件，提醒客戶他們遺漏的商品。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          連接您的社交媒體帳號
        </mj-text>
        <mj-text font-size="14px">
          將您的社交媒體資料連結到您的商店，讓客戶可以找到並追蹤您。在 <strong>Settings > Social Media</strong> 添加社交連結，以在商店頁腳顯示。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          設定 Google Analytics 跟蹤
        </mj-text>
        <mj-text font-size="14px">
          了解您的訪客來自哪裡，以及他們如何與您的商店互動。在 <strong>Settings > Analytics</strong> 添加您的 Google Analytics 跟蹤 ID 來開始收集數據。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          建立電子報訂閱表單
        </mj-text>
        <mj-text font-size="14px">
          從第一天開始建立您的電子郵件名單。在商店中添加電子報訂閱表單，以捕捉訪客的電子郵件。利用這些聯繫人進行促銷、產品發佈和客戶互動。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
開始行動：行銷與增長 - {{ store_name }}

Hi {{ name|default:'there' }},

當 {{ store_name }} 開始成形，現在是時候專注於增加流量並提升銷售。以下有五個行銷技巧幫助你開始。

1. 建立您的第一個折扣碼
提供一個開幕折扣來吸引您的第一批客戶。前往 Marketing > Discount Codes 來建立折扣，並可選擇設定使用次數限制和過期日期。

2. 設定遺漏購物車恢復功能
自動恢復遺失的銷售。在 Marketing > Abandoned Carts 啟用遺漏購物車恢復郵件，提醒客戶他們遺漏的商品。

3. 連接您的社交媒體帳號
將您的社交媒體資料連結到您的商店。在 Settings > Social Media 添加社交連結，以在商店頁腳顯示。

4. 設定 Google Analytics 跟蹤
了解您的訪客來自哪裡。在 Settings > Analytics 添加您的 Google Analytics 跟蹤 ID 來開始收集數據。

5. 建立電子報訂閱表單
從第一天開始建立您的電子郵件名單。在商店中添加電子報訂閱表單，以捕捉訪客的電子郵件，用於促銷和互動。

前往 Marketing: {{ admin_url }}

需要幫助嗎？請聯繫 {{ support_email }}
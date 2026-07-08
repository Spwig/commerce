---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
建立您的商品目錄 - {{ store_name }}

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
          開始吧：您的商品
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          為 {{ store_name }} 建立一個出色的目錄
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
          您的商店 <strong>{{ store_name }}</strong> 已經設置完成。現在是時候建立您的商品目錄了。以下有五個小技巧幫助您開始。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          從 CSV 檔案導入商品
        </mj-text>
        <mj-text font-size="14px">
          已經有商品清單了嗎？前往 <strong>管理員 > 商品目錄 > 導入</strong>，從 CSV 檔案批量導入您的商品。這是最快的方式來填滿您的商店。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          用分類與篩選來整理
        </mj-text>
        <mj-text font-size="14px">
          建立分類與屬性篩選，讓顧客輕鬆瀏覽並找到他們想要的東西。整理良好的目錄會提高轉化率。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          寫出吸引人的商品描述
        </mj-text>
        <mj-text font-size="14px">
          優秀的描述能促銷商品。專注於優點，而不僅僅是功能。告訴顧客他們為什麼需要您的商品，以及它如何解決他們的問題。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          上傳高品質的商品圖片
        </mj-text>
        <mj-text font-size="14px">
          清晰且專業的圖片會有很大的差異。上傳多個角度並使用一致的燈光。Spwig 會自動優化圖片以加快載入速度。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          設置商品變體
        </mj-text>
        <mj-text font-size="14px">
          如果您的商品有不同的尺寸、顏色或風格，請建立變體，讓顧客可以精確選擇他們想要的。每個變體都可以有自己的價格、庫存數量和圖片。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Manage Your Products" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
開始吧：您的商品 - {{ store_name }}

Hi {{ name|default:'there' }},

您的商店 {{ store_name }} 已經設置完成。現在是時候建立您的商品目錄了。以下有五個小技巧幫助您開始。

1. 從 CSV 檔案導入商品
已經有商品清單了嗎？前往 Admin > 商品目錄 > 導入，從 CSV 檔案批量導入您的商品。

2. 用分類與篩選來整理
建立分類與屬性篩選，讓顧客輕鬆瀏覽並找到他們想要的東西。

3. 寫出吸引人的商品描述
優秀的描述能促銷商品。專注於優點，而不僅僅是功能。告訴顧客他們為什麼需要您的商品。

4. 上傳高品質的商品圖片
清晰且專業的圖片會有很大的差異。上傳多個角度並使用一致的燈光。

5. 設置商品變體
如果您的商品有不同的尺寸、顏色或風格，請建立變體，讓顧客可以精確選擇他們想要的。

管理您的商品：{{ admin_url }}

需要幫助嗎？請聯繫 {{ support_email }}
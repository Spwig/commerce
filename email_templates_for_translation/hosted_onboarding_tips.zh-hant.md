---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
善用 {{ store_name }} 的小技巧

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
          開始使用小技巧
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          善用你的 Spwig 商店
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
          現在 {{ store_name }} 已經啟動運作，以下是一些幫助你充分利用商店的小技巧。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          自定義外觀
        </mj-text>
        <mj-text font-size="14px">
          訪問 <strong>Design > Theme Settings</strong> 來選擇主題、上傳你的商標，並設定品牌顏色。商店前端會立即更新，讓你可以即時預覽更改。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          添加商品
        </mj-text>
        <mj-text font-size="14px">
          前往 <strong>Catalog > Products</strong> 開始添加商品。你可以創建商品變體（尺寸、顏色），設定價格，管理庫存，並上傳高品質圖片。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          設置付款方式
        </mj-text>
        <mj-text font-size="14px">
          前往 <strong>Settings > Payment Providers</strong> 來連接 Stripe、PayPal 或其他付款方式。你可以啟用多個付款方式，讓客戶可以選擇自己偏好的付款方式。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          設置運送方式
        </mj-text>
        <mj-text font-size="14px">
          在 <strong>Settings > Shipping</strong> 下設置你的運送區域和費用。你可以為不同地區創建固定費用、重量基礎或免運費規則。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          提升 SEO
        </mj-text>
        <mj-text font-size="14px">
          Spwig 會自動生成地圖和 meta 標籤。前往 <strong>Settings > SEO</strong> 自定義你的頁面標題、描述和社交分享圖片，幫助客戶找到你的商店。
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
開始使用小技巧 - {{ store_name }}

Hi {{ name|default:'there' }},

現在 {{ store_name }} 已經啟動運作，以下是一些幫助你充分利用商店的小技巧。

1. 自定義外觀
訪問 Design > Theme Settings 來選擇主題、上傳你的商標，並設定品牌顏色。

2. 添加商品
前往 Catalog > Products 開始添加商品，包括變體、價格和圖片。

3. 設置付款方式
前往 Settings > Payment Providers 來連接 Stripe、PayPal 或其他付款方式。

4. 設置運送方式
在 Settings > Shipping 下設置你的運送區域和費用，針對不同地區。

5. 提升 SEO
前往 Settings > SEO 自定義你的頁面標題、描述和社交分享圖片。

前往管理面板：{{ admin_url }}

需要幫助嗎？請聯繫 {{ support_email }}
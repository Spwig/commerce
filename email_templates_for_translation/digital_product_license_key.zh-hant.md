---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
您的軟體許可證密鑰 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          您的許可證密鑰已準備好
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          您好 {{ customer_name }}，
        </mj-text>
        <mj-text>
          感謝您購買 {{ product_name }}！以下是您的激活許可證密鑰。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          您的許可證密鑰
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          點擊複製或謹慎記下
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          許可證詳情：
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 產品：{{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 版本：{{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 許可證類型：{{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 最大激活次數：{{ max_activations }} 台設備
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 有效期：終身許可證
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 有效至：{{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          如何激活：
        </mj-text>
        <mj-text font-size="14px">
          1. 下載並安裝軟體
        </mj-text>
        <mj-text font-size="14px">
          2. 打開應用程式
        </mj-text>
        <mj-text font-size="14px">
          3. 當提示時輸入您的許可證密鑰
        </mj-text>
        <mj-text font-size="14px">
          4. 點擊 "Activate" 完成流程
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          下載軟體
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ 重要：
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 請妥善保管此郵件 - 您需要許可證密鑰進行重新安裝
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 請勿與他人分享您的許可證密鑰
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 您可以從您的帳戶儀表板停用設備
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          需要激活協助？請聯繫 {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您的許可證密鑰已準備好

您好 {{ customer_name }}，

感謝您購買 {{ product_name }}！以下是您的激活許可證密鑰。

YOUR LICENSE KEY:
{{ license_key }}

License Details:
• Product: {{ product_name }}
• Version: {{ product_version }}
• License Type: {{ license_type }}
• Max Activations: {{ max_activations }} device(s)
{% if is_lifetime %}• Validity: Lifetime License{% else %}• Valid Until: {{ expiration_date }}{% endif %}

How to Activate:
1. Download and install the software
2. Open the application
3. Enter your license key when prompted
4. Click "Activate" to complete the process

{% if download_url %}Download Software: {{ download_url }}

{% endif %}IMPORTANT:
• Keep this email safe - you'll need the license key for reinstallation
• Do not share your license key with others
• You can deactivate devices from your account dashboard

Need help with activation? Contact {{ support_email }}
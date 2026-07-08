---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
您的软件许可证密钥 - 订单 #{{ order_number }}

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
          您的许可证密钥已准备就绪
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好 {{ customer_name }}，
        </mj-text>
        <mj-text>
          感谢您购买 {{ product_name }}！以下是您的激活许可证密钥。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          您的许可证密钥
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          点击复制或仔细记录下来
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          许可证详情：
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 产品：{{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 版本：{{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 许可证类型：{{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 最大激活次数：{{ max_activations }} 台设备
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 有效期：终身许可证
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 有效期至：{{ expiration_date }}
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
          1. 下载并安装软件
        </mj-text>
        <mj-text font-size="14px">
          2. 打开应用程序
        </mj-text>
        <mj-text font-size="14px">
          3. 当提示时输入您的许可证密钥
        </mj-text>
        <mj-text font-size="14px">
          4. 点击“激活”以完成流程
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          下载软件
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
          • 请妥善保管此电子邮件 - 您需要许可证密钥进行重新安装
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 请勿将您的许可证密钥分享给他人
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 您可以从您的账户仪表板中停用设备
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          需要激活帮助？请联系 {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您的许可证密钥已准备就绪

你好 {{ customer_name }}，

感谢您购买 {{ product_name }}！以下是您的激活许可证密钥。

YOUR LICENSE KEY:
{{ license_key }}

许可证详情：
• 产品：{{ product_name }}
• 版本：{{ product_version }}
• 许可证类型：{{ license_type }}
• 最大激活次数：{{ max_activations }} 台设备
{% if is_lifetime %}• 有效期：终身许可证{% else %}• 有效期至：{{ expiration_date }}{% endif %}

如何激活：
1. 下载并安装软件
2. 打开应用程序
3. 当提示时输入您的许可证密钥
4. 点击“激活”以完成流程

{% if download_url %}下载软件：{{ download_url }}

{% endif %}IMPORTANT：
• 请妥善保管此电子邮件 - 您需要许可证密钥进行重新安装
• 请勿将您的许可证密钥分享给他人
• 您可以从您的账户仪表板中停用设备

需要激活帮助？请联系 {{ support_email }}
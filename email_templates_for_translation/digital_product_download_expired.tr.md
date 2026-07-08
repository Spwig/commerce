---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
İndirme Bağlantısı Süresi Doldu - Sipariş #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          İndirme Bağlantısı Süresi Doldu
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Merhaba {{ customer_name }},
        </mj-text>
        <mj-text>
          Sipariş #{{ order_number }} numaralı {{ product_name }} için indirme bağlantınız sona erdi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          Güvenlik nedenleriyle, satın alma tarihinden itibaren indirme bağlantıları {{ expiration_days }} gün sonra sona erer.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Yeni bir indirme bağlantısı istiyorsunuz mu?
        </mj-text>
        <mj-text>
          Hesabınıza giriş yaparak veya destek ekibimize ulaşarak yeni bir indirme bağlantısı talep edebilirsiniz.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Hesabım'a Git
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Sorularınız varsa, {{ support_email }} adresine ulaşın
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
İndirme Bağlantısı Süresi Doldu

Merhaba {{ customer_name }},

Sipariş #{{ order_number }} numaralı {{ product_name }} için indirme bağlantınız sona erdi.

İndirme bağlantıları, güvenlik nedenleriyle satın alma tarihinden itibaren {{ expiration_days }} gün sonra sona erer.

Yeni bir indirme bağlantısı istiyorsunuz mu?
Hesabınıza giriş yaparak veya destek ekibimize ulaşarak yeni bir indirme bağlantısı talep edebilirsiniz.

Hesabım'a Git: {{ account_url }}

Sorularınız varsa, {{ support_email }} adresine ulaşın
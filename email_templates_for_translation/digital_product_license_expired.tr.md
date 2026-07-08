---
template_type: digital_product_license_expired
category: Digital Products
---

# Email Template: digital_product_license_expired

## Subject
Lisans Anahtarınız Yakında Bitmektedir - {{ product_name }}

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
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Lisans Yakında Bitmektedir
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
          {{ product_name }} lisansınız yakında sona erecektir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="#fffbeb" padding="20px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e">
          <strong>Lisans Anahtarı:</strong> {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Sona Erecektir:</strong> {{ expiration_date }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Kalan Gün Sayısı:</strong> {{ days_remaining }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Lisansınızı Yenileyin
        </mj-text>
        <mj-text>
          Bugün lisansınızı yenileyerek {{ product_name }}'i devam ettirin.
        </mj-text>
        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Şimdi Yenile
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Yenileme hakkında sorularınız var mı? {{ support_email }} ile iletişime geçin
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Lisans Yakında Bitmektedir

Merhaba {{ customer_name }},

{{ product_name }} lisansınız yakında sona erecektir.

Lisans Detayları:
• Lisans Anahtarı: {{ license_key }}
• Sona Erecektir: {{ expiration_date }}
• Kalan Gün Sayısı: {{ days_remaining }}

Lisansınızı Yenileyin:
Bugün lisansınızı yenileyerek {{ product_name }}'i devam ettirin.

Şimdi Yenile: {{ renewal_url }}

Yenileme hakkında sorularınız var mı? {{ support_email }} ile iletişime geçin
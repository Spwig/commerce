---
template_type: dev_submission_received
category: Developer Portal
---

# Email Template: dev_submission_received

## Subject
Bileşen gönderimi alınmıştır: {{ component_name }} v{{ version }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Gönderim Alındı
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Bileşeninizi artık inceleme altına aldık
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Merhaba {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Bileşen gönderiminizi aldık ve otomatik doğrulama geçti. Ekibimiz şimdi onu inceleyecektir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Component Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Bileşen:</strong> {{ component_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Tür:</strong> {{ component_type }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Sürüm:</strong> v{{ version }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Timeline Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          İncelemeler genellikle 2-3 iş günü sürer. İnceleme tamamlandığında size bildirilecektir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ submission_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Gönderimi Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig Geliştirici Portalı</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Sorularınız varsa geliştirici desteği ile iletişime geçin
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Merhaba {{ developer_name }},

Bileşen gönderiminizi aldık ve otomatik doğrulama geçti. Ekibimiz şimdi onu inceleyecektir.

Bileşen: {{ component_name }}
Tür: {{ component_type }}
Sürüm: v{{ version }}

İncelemeler genellikle 2-3 iş günü sürer. İnceleme tamamlandığında size bildirilecektir.

Gönderimi Görüntüle: {{ submission_url }}

---
Spwig Geliştirici Portalı
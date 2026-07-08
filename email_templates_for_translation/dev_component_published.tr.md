---
template_type: dev_component_published
category: Developer Portal
---

# Email Template: dev_component_published

## Subject
{{ component_name }} v{{ version }} Spwig Pazarında Şimdi Aktif!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="50px 20px">
      <mj-column>
        <mj-text font-size="36px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Şimdi Aktif!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="15px">
          Componentiniz Spwig Pazarında Aktif
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
          Componentiniz artık pazarın tüm Spwig mağazaları için aktif ve kullanıma açılmıştır!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Component Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Component:</strong> {{ component_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Tür:</strong> {{ component_type }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Sürüm:</strong> v{{ version }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Analytics Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Componentinizin performansını analiz panelinde izleyebilirsiniz — mağazaların kullanmaya başlamasıyla birlikte indirme, puanlama ve incelemeler görünecektir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Analizleri Görüntüle
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
          Sorularınız mı var? Geliştirici desteği ile iletişime geçin
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Merhaba {{ developer_name }},

Componentiniz artık pazarın tüm Spwig mağazaları için aktif ve kullanıma açılmıştır!

Component: {{ component_name }}
Tür: {{ component_type }}
Sürüm: v{{ version }}

Componentinizin performansını analiz panelinde izleyebilirsiniz — mağazaların kullanmaya başlamasıyla birlikte indirme, puanlama ve incelemeler görünecektir.

Analizleri Görüntüle: {{ dashboard_url }}

---
Spwig Geliştirici Portalı
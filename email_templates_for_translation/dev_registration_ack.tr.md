---
template_type: dev_registration_ack
category: Developer Portal
---

# Email Template: dev_registration_ack

## Subject
Geliştirici başvurunuz alındı, {{ developer_name }}

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
          Başvuru Alındı!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Geliştirici başvurunuz inceleniyor
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
          Spwig Geliştirici Programına başvurduğunuz için teşekkür ederiz. Başvurunuzu aldık ve ekiplerimiz kısa süre sonra incelenecektir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          Sonraki Adım Nedir?
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> Ekiplerimiz başvurunuzu inceler (genellikle 2-3 iş günü)
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> Kararımızla ilgili bir e-posta alacaksınız
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>3.</strong> Onaylandıktan sonra geliştirici paneline tam erişim sağlarsınız
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ portal_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Geliştirici Portalını Görüntüle
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

Spwig Geliştirici Programına başvurduğunuz için teşekkür ederiz. Başvurunuzu aldık ve ekiplerimiz kısa süre sonra incelenecektir.

Sonraki Adım Nedir?
1. Ekiplerimiz başvurunuzu inceler (genellikle 2-3 iş günü)
2. Kararımızla ilgili bir e-posta alacaksınız
3. Onaylandıktan sonra geliştirici paneline tam erişim sağlarsınız

Geliştirici Portalını Görüntüle: {{ portal_url }}

---
Spwig Geliştirici Portalı
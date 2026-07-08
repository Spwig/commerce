---
template_type: dev_new_review
category: Developer Portal
---

# Email Template: dev_new_review

## Subject
Yeni {{ rating }} yıldızlı inceleme {{ component_name }} için

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
          Yeni Bir Değerlendirme Alındı
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Bir satıcı {{ component_name }}'i inceledi
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
          Bir satıcı, bileşeninizi <strong>{{ component_name }}</strong> için bir inceleme bırakmıştır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Review Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 25px">
      <mj-column>
        <mj-text font-size="24px" color="{{ theme.color.warning|default:'#f59e0b' }}" align="center" padding-bottom="10px">
          {{ rating_stars }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-bottom="15px">
          {{ rating }}/5 yıldız
        </mj-text>
        {% if review_title %}
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          {{ review_title }}
        </mj-text>
        {% endif %}
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#1f2937' }}" padding="20px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          "{{ review_comment }}"
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right" padding-top="15px">
          — {{ reviewer_name }}{% if is_verified_purchase %} <span style="color: {{ theme.color.success|default:'#10b981' }};">✓ Onaylı Satın Alma</span>{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Action Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Bu inceleme üzerine geliştirici portalınızdan yanıt verebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ reviews_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Görüntüle & Yanıtla
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

Bir satıcı, bileşeninizi {{ component_name }} için bir inceleme bırakmıştır.

{{ rating_stars }} ({{ rating }}/5)
{% if review_title %}{{ review_title }}{% endif %}

{{ review_comment }}

— {{ reviewer_name }}{% if is_verified_purchase %} (Onaylı Satın Alma){% endif %}

Bu inceleme üzerine geliştirici portalınızdan yanıt verebilirsiniz.

Görüntüle & Yanıtla: {{ reviews_url }}

---
Spwig Geliştirici Portalı
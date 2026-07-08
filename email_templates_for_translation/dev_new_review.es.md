---
template_type: dev_new_review
category: Developer Portal
---

# Email Template: dev_new_review

## Subject
Nueva reseña de {{ rating }} estrellas en {{ component_name }}

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
          Nueva reseña recibida
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Un comerciante revisó {{ component_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hola {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Un comerciante ha dejado una reseña en tu componente <strong>{{ component_name }}</strong>.
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
          {{ rating }}/5 estrellas
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
          — {{ reviewer_name }}{% if is_verified_purchase %} <span style="color: {{ theme.color.success|default:'#10b981' }};">✓ Compra verificada</span>{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Action Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Puedes responder a esta reseña desde tu portal del desarrollador.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ reviews_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Ver & Responder
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Portal del Desarrollador de Spwig</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          ¿Tienes preguntas? Contacta al soporte de desarrolladores
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hola {{ developer_name }},

Un comerciante ha dejado una reseña en tu componente {{ component_name }}.

{{ rating_stars }} ({{ rating }}/5)
{% if review_title %}{{ review_title }}{% endif %}

{{ review_comment }}

— {{ reviewer_name }}{% if is_verified_purchase %} (Compra verificada){% endif %}

Puedes responder a esta reseña desde tu portal del desarrollador.

Ver & Responder: {{ reviews_url }}

---
Portal del Desarrollador de Spwig
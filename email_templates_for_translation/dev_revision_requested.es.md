---
template_type: dev_revision_requested
category: Developer Portal
---

# Email Template: dev_revision_requested

## Subject
Solicitud de revisión: {{ component_name }} v{{ version }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Info Accent -->
    <mj-section background-color="{{ theme.color.info|default:'#3b82f6' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Solicitud de revisión
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          Se necesitan algunos cambios antes de la aprobación
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
          Nuestro equipo de revisión ha solicitado algunos cambios en su componente antes de que pueda ser aprobado.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Component Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Componente:</strong> {{ component_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Tipo:</strong> {{ component_type }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Versión:</strong> v{{ version }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Requested Changes (if provided) -->
    {% if review_notes %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          Cambios solicitados:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" border-left="3px solid {{ theme.color.info|default:'#3b82f6' }}">
          {{ review_notes }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Next Steps -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Por favor, revise los comentarios y envíe una versión actualizada.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ submission_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Ver detalles de la entrega
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
          ¿Tiene preguntas? Póngase en contacto con el soporte de desarrolladores
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hola {{ developer_name }},

Nuestro equipo de revisión ha solicitado algunos cambios en su componente antes de que pueda ser aprobado.

Componente: {{ component_name }}
Tipo: {{ component_type }}
Versión: v{{ version }}

{% if review_notes %}Cambios solicitados:
{{ review_notes }}{% endif %}

Por favor, revise los comentarios y envíe una versión actualizada.

Ver detalles de la entrega: {{ submission_url }}

---
Portal del Desarrollador de Spwig
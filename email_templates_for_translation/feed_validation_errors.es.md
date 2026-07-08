---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: {{ error_count }} errores de validación encontrados

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Errores de Validación de Feed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemas de Calidad de Datos Detectados
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ error_count }} error{{ error_count|pluralize }} de validación encontrado en {{ feed_name }}. Estos problemas pueden impedir que los productos aparezcan en {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Resumen de Validación:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Plataforma:</strong> {{ platform_name }}<br/>
              <strong>Validado:</strong> {{ validated_at }}<br/>
              <strong>Total de Productos:</strong> {{ total_products }}<br/>
              <strong>Productos con Errores:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Errores Principales:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} producto{{ error.count|pluralize }} afectado: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué Debe Corregir:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver todos los errores
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Administrar feed
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Corrija estos errores para asegurarse de que todos los productos aparezcan en {{ platform_name }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ERRORES DE VALIDACIÓN DE FEED

Problemas de Calidad de Datos Detectados

{{ error_count }} error{{ error_count|pluralize }} de validación encontrado en {{ feed_name }}. Estos problemas pueden impedir que los productos aparezcan en {{ platform_name }}.

RESUMEN DE VALIDACIÓN:
- Feed: {{ feed_name }}
- Plataforma: {{ platform_name }}
- Validado: {{ validated_at }}
- Total de Productos: {{ total_products }}
- Productos con Errores: {{ affected_products }}

ERRORES PRINCIPALES:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} producto{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

¿QUÉ DEBE CORREGIR:
{{ fix_instructions }}

Ver todos los errores: {{ errors_url }}
Administrar feed: {{ admin_feed_url }}

Corrija estos errores para asegurarse de que todos los productos aparezcan en {{ platform_name }}.
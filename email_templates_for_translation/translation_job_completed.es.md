---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Traducción completada: {{ content_type }} ({{ language_count }} idiomas)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Traducción completada!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¡Sus traducciones están listas!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ¡Buena noticia! Su trabajo de traducción masiva se ha completado con éxito.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Resumen del trabajo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID del trabajo:</strong> {{ job_id }}<br/>
              <strong>Tipo de contenido:</strong> {{ content_type }}<br/>
              <strong>Idiomas:</strong> {{ target_languages }}<br/>
              <strong>Elementos traducidos:</strong> {{ items_translated }}<br/>
              <strong>Palabras totales:</strong> {{ word_count }}<br/>
              <strong>Completado:</strong> {{ completed_at }}<br/>
              <strong>Duración:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Calidad de la traducción:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Puntaje promedio de calidad:</strong> {{ quality_score }}%<br/>
              <strong>Alta calidad:</strong> {{ high_quality_count }} elementos<br/>
              <strong>Revisión recomendada:</strong> {{ review_needed_count }} elementos
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Revisión recomendada
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} traducciones obtuvieron un puntaje inferior al 85% y deberían revisarse antes de publicar.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pasos siguientes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Revisar las traducciones en su panel de administración<br/>
          2. Editar cualquier traducción que necesite refinamiento<br/>
          3. Publicar traducciones para hacerlas activas<br/>
          4. Su contenido multilingüe estará disponible para los clientes
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Revisar traducciones
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Publicar todo
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ TRADUCCIÓN COMPLETADA!

¡Sus traducciones están listas!

¡Buena noticia! Su trabajo de traducción masiva se ha completado con éxito.

RESUMEN DEL TRABAJO:
- ID del trabajo: {{ job_id }}
- Tipo de contenido: {{ content_type }}
- Idiomas: {{ target_languages }}
- Elementos traducidos: {{ items_translated }}
- Palabras totales: {{ word_count }}
- Completado: {{ completed_at }}
- Duración: {{ job_duration }}

CALIDAD DE LA TRADUCCIÓN:
- Puntaje promedio de calidad: {{ quality_score }}%
- Alta calidad: {{ high_quality_count }} elementos
- Revisión recomendada: {{ review_needed_count }} elementos

{% if review_needed_count > 0 %}
⚠️ REVISIÓN RECOMENDADA:
{{ review_needed_count }} traducciones obtuvieron un puntaje inferior al 85% y deberían revisarse antes de publicar.
{% endif %}

PASOS SIGUIENTES:
1. Revisar las traducciones en su panel de administración
2. Editar cualquier traducción que necesite refinamiento
3. Publicar traducciones para hacerlas activas
4. Su contenido multilingüe estará disponible para los clientes

Revisar traducciones: {{ review_url }}
{% if can_publish_all %}Publicar todo: {{ publish_all_url }}{% endif %}
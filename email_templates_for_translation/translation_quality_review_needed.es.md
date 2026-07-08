---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Detectadas traducciones de baja calidad: {{ content_type }} - {{ low_quality_count }} elementos necesitan revisión

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Alerta de Calidad de Traducción
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Revisión Recomendada
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Su trabajo de traducción se completó, pero {{ low_quality_count }} traducciones obtuvieron una puntuación por debajo del umbral de calidad y deben revisarse antes de publicar.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Resumen del Trabajo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID del Trabajo:</strong> {{ job_id }}<br/>
              <strong>Tipo de Contenido:</strong> {{ content_type }}<br/>
              <strong>Total de Elementos:</strong> {{ total_items }}<br/>
              <strong>Calidad Promedio:</strong> {{ average_quality }}%<br/>
              <strong>Baja Calidad:</strong> {{ low_quality_count }} elementos ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Desglose de Calidad:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Excelente (95-100%):</strong> {{ excellent_count }} elementos<br/>
              <strong>Bueno (85-94%):</strong> {{ good_count }} elementos<br/>
              <strong>Regular (70-84%):</strong> {{ fair_count }} elementos<br/>
              <strong>Pobre (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} elementos</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemas Comunes de Calidad:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} ocurrencias
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Revisar traducciones marcadas en el panel de administración<br/>
          2. Editar manualmente las traducciones de baja calidad<br/>
          3. Considerar re-traducir elementos de baja calidad<br/>
          4. Publicar solo después de que la revisión esté completa
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Revisar Traducciones
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Elementos de Baja Calidad
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Consejo: Las puntuaciones de calidad por debajo del 85% indican posibles problemas con la gramática, el contexto o la precisión. Se recomienda fuertemente la revisión humana antes de publicar.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERTA DE CALIDAD DE TRADUCCIÓN

Revisión Recomendada

Su trabajo de traducción se completó, pero {{ low_quality_count }} traducciones obtuvieron una puntuación por debajo del umbral de calidad y deben revisarse antes de publicar.

RESUMEN DEL TRABAJO:
- ID del Trabajo: {{ job_id }}
- Tipo de Contenido: {{ content_type }}
- Total de Elementos: {{ total_items }}
- Calidad Promedio: {{ average_quality }}%
- Baja Calidad: {{ low_quality_count }} elementos ({{ low_quality_percentage }}%)

DESGLOSE DE CALIDAD:
- Excelente (95-100%): {{ excellent_count }} elementos
- Bueno (85-94%): {{ good_count }} elementos
- Regular (70-84%): {{ fair_count }} elementos
- Pobre (<70%): {{ poor_count }} elementos

PROBLEMAS COMUNES DE CALIDAD:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} ocurrencias
{% endfor %}

ACCIONES RECOMENDADAS:
1. Revisar traducciones marcadas en el panel de administración
2. Editar manualmente las traducciones de baja calidad
3. Considerar re-traducir elementos de baja calidad
4. Publicar solo después de que la revisión esté completa

Revisar traducciones: {{ review_url }}
Ver elementos de baja calidad: {{ low_quality_url }}

💡 Consejo: Las puntuaciones de calidad por debajo del 85% indican posibles problemas con la gramática, el contexto o la precisión. Se recomienda fuertemente la revisión humana antes de publicar.
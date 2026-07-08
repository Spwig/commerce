---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Trabajo de traducción iniciado: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Trabajo de traducción iniciado
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Traducción por lotes en proceso
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Su trabajo de traducción por lotes ha sido iniciado y ahora está en proceso.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del trabajo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID del trabajo:</strong> {{ job_id }}<br/>
              <strong>Tipo de contenido:</strong> {{ content_type }}<br/>
              <strong>Idioma de origen:</strong> {{ source_language }}<br/>
              <strong>Idiomas de destino:</strong> {{ target_languages }}<br/>
              <strong>Elementos a traducir:</strong> {{ item_count }}<br/>
              <strong>Iniciado:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Estimación de finalización:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Basado en {{ word_count }} palabras)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué ocurre a continuación:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. El servicio de traducción de IA procesa su contenido<br/>
          2. Las traducciones se guardan como borradores para revisión<br/>
          3. Recibirá un correo electrónico cuando el trabajo esté completo<br/>
          4. Revise y publique las traducciones desde su panel de administración
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver estado del trabajo
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Puede cerrar este correo. Le notificaremos cuando la traducción esté completa.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 TRADUCCIÓN INICIADA

Traducción por lotes en proceso

Su trabajo de traducción por lotes ha sido iniciado y ahora está en proceso.

DETALLES DEL TRABAJO:
- ID del trabajo: {{ job_id }}
- Tipo de contenido: {{ content_type }}
- Idioma de origen: {{ source_language }}
- Idiomas de destino: {{ target_languages }}
- Elementos a traducir: {{ item_count }}
- Iniciado: {{ started_at }}

ESTIMACIÓN DE FINALIZACIÓN:
{{ estimated_completion }}
(Basado en {{ word_count }} palabras)

¿QUÉ OCURRE A CONTINUACIÓN:
1. El servicio de traducción de IA procesa su contenido
2. Las traducciones se guardan como borradores para revisión
3. Recibirá un correo electrónico cuando el trabajo esté completo
4. Revise y publique las traducciones desde su panel de administración

Ver estado del trabajo: {{ job_status_url }}

Puede cerrar este correo. Le notificaremos cuando la traducción esté completa.
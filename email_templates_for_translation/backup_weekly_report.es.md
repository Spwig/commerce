---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
Resumen de copia de seguridad semanal - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumen de copia de seguridad semanal
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Estadísticas de copia de seguridad:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total de copias de seguridad:</strong> {{ total_backups }}<br/>
              <strong>Exitosas:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>Fallidas:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>Tamaño promedio:</strong> {{ average_size }}<br/>
              <strong>Total de almacenamiento usado:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Problemas detectados:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} copia(s) de seguridad fallida(s) esta semana. Por favor, revise y tome medidas correctivas.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Últimas copias de seguridad:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Tamaño: {{ backup.size }} | Duración: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ Éxito</span>
              {% else %}
              <span style="color: #dc2626;">✗ Fallida</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Ver todas las copias de seguridad
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
RESUMEN DE COPIA DE SEGURIDAD SEMANAL
{{ week_start }} - {{ week_end }}

ESTADÍSTICAS DE COPIA DE SEGURIDAD:
- Total de copias de seguridad: {{ total_backups }}
- Exitosas: {{ successful_backups }}
- Fallidas: {{ failed_backups }}
- Tamaño promedio: {{ average_size }}
- Total de almacenamiento usado: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ PROBLEMAS DETECTADOS:
{{ failed_backups }} copia(s) de seguridad fallida(s) esta semana. Por favor, revise y tome medidas correctivas.
{% endif %}

ÚLTIMAS COPIAS DE SEGURIDAD:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Tamaño: {{ backup.size }} | Duración: {{ backup.duration }} | Estado: {{ backup.status }}
{% endfor %}

Ver todas las copias de seguridad: {{ admin_backup_url }}
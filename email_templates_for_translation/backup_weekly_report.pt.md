---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
Resumo Semanal de Backup - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumo Semanal de Backup
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Backup Estatísticas:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total de Backups:</strong> {{ total_backups }}<br/>
              <strong>Sucesso:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>Falhou:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>Tamanho Médio:</strong> {{ average_size }}<br/>
              <strong>Total de Armazenamento Usado:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Problemas Detectados:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} backup(s) falharam nesta semana. Por favor, revise e tome medidas corretivas.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Últimos Backups:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Tamanho: {{ backup.size }} | Duração: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ Sucesso</span>
              {% else %}
              <span style="color: #dc2626;">✗ Falhou</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Ver Todos os Backups
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
RESUMO SEMANAL DE BACKUP
{{ week_start }} - {{ week_end }}

ESTATÍSTICAS DE BACKUP:
- Total de Backups: {{ total_backups }}
- Sucesso: {{ successful_backups }}
- Falhou: {{ failed_backups }}
- Tamanho Médio: {{ average_size }}
- Total de Armazenamento Usado: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ PROBLEMAS DETECTADOS:
{{ failed_backups }} backup(s) falharam nesta semana. Por favor, revise e tome medidas corretivas.
{% endif %}

ÚLTIMOS BACKUPS:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Tamanho: {{ backup.size }} | Duração: {{ backup.duration }} | Status: {{ backup.status }}
{% endfor %}

Ver todos os backups: {{ admin_backup_url }}
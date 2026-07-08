---
template_type: backup_completed
category: Backups
---

# Email Template: backup_completed

## Subject
✓ Backup Concluído com Sucesso - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Backup Concluído com Sucesso
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Seu backup agendado para {{ shop_name }} foi concluído com sucesso.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Backup:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tipo:</strong> {{ backup_type }}<br/>
              <strong>Iniciado:</strong> {{ backup_started_at }}<br/>
              <strong>Concluído:</strong> {{ backup_completed_at }}<br/>
              <strong>Duração:</strong> {{ backup_duration }}<br/>
              <strong>Tamanho:</strong> {{ backup_size }}<br/>
              <strong>Localização:</strong> {{ backup_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Ver Detalhes do Backup
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Próximo Backup Agendado:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BACKUP CONCLUÍDO COM SUCESSO

Olá {{ admin_name }},

Seu backup agendado para {{ shop_name }} foi concluído com sucesso.

DETALHES DO BACKUP:
- Tipo: {{ backup_type }}
- Iniciado: {{ backup_started_at }}
- Concluído: {{ backup_completed_at }}
- Duração: {{ backup_duration }}
- Tamanho: {{ backup_size }}
- Localização: {{ backup_location }}

Ver detalhes do backup: {{ admin_backup_url }}

Próximo Backup Agendado: {{ next_scheduled_backup }}
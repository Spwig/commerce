---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ Backup Agendado Não Executado - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Backup Agendado Faltando
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Um backup agendado para {{ shop_name }} não foi executado conforme esperado. Seus dados podem não estar totalmente protegidos.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Agendamento do Backup:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Hora Agendada:</strong> {{ scheduled_time }}<br/>
              <strong>Tipo de Backup:</strong> {{ backup_type }}<br/>
              <strong>Último Backup Bem-sucedido:</strong> {{ last_successful_backup }}<br/>
              <strong>Tempo Desde o Último Backup:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causas Possíveis:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • O servidor estava offline ou inacessível<br/>
          • O serviço de tarefas agendadas não estava em execução<br/>
          • Permissões insuficientes<br/>
          • Espaço de armazenamento cheio<br/>
          • Problemas de conectividade com o banco de dados
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Executar Backup Manualmente
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Verificar Registros do Sistema
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ BACKUP AGENDADO NÃO EXECUTADO

Olá {{ admin_name }},

Um backup agendado para {{ shop_name }} não foi executado conforme esperado. Seus dados podem não estar totalmente protegidos.

DETALHES DO AGENDAMENTO DO BACKUP:
- Hora Agendada: {{ scheduled_time }}
- Tipo de Backup: {{ backup_type }}
- Último Backup Bem-sucedido: {{ last_successful_backup }}
- Tempo Desde o Último Backup: {{ time_since_last }}

CAUSAS POSSÍVEIS:
• O servidor estava offline ou inacessível
• O serviço de tarefas agendadas não estava em execução
• Permissões insuficientes
• Espaço de armazenamento cheio
• Problemas de conectividade com o banco de dados

Executar backup manualmente: {{ admin_backup_url }}
Verificar registros do sistema: {{ admin_logs_url }}
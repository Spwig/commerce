---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 URGENTE: Backup Falhou - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Backup Falhou
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Olá {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Uma operação de backup crítica falhou para a sua loja {{ shop_name }}. Ação imediata é necessária para garantir a proteção dos dados.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Detalhes do Backup:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Tipo de Backup:</strong> {{ backup_type }}<br/>
              <strong>Iniciado:</strong> {{ backup_started_at }}<br/>
              <strong>Falhou:</strong> {{ backup_failed_at }}<br/>
              <strong>Duração:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Detalhes do Erro:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ações Recomendadas:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Verifique o espaço em disco disponível no seu servidor<br/>
          2. Verifique a conectividade do banco de dados<br/>
          3. Revise o log de erro para obter o rastreamento de pilha detalhado<br/>
          4. Tente o backup manualmente ou espere pela próxima execução agendada<br/>
          5. Entre em contato com o suporte se o problema persistir
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Logs de Backup
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Tente o Backup Agora
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Último Backup Bem-sucedido:</strong> {{ last_successful_backup }}<br/>
          <strong>Próximo Backup Agendado:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 URGENTE: BACKUP FALHOU

Olá {{ admin_name }},

Uma operação de backup crítica falhou para a sua loja {{ shop_name }}. Ação imediata é necessária para garantir a proteção dos dados.

DETALHES DO BACKUP:
- Tipo de Backup: {{ backup_type }}
- Iniciado: {{ backup_started_at }}
- Falhou: {{ backup_failed_at }}
- Duração: {{ backup_duration }}

DETALHES DO ERRO:
{{ error_message }}

AÇÕES RECOMENDADAS:
1. Verifique o espaço em disco disponível no seu servidor
2. Verifique a conectividade do banco de dados
3. Revise o log de erro para obter o rastreamento de pilha detalhado
4. Tente o backup manualmente ou espere pela próxima execução agendada
5. Entre em contato com o suporte se o problema persistir

Ver logs de backup: {{ admin_backup_url }}
Tente o backup agora: {{ retry_backup_url }}

Último Backup Bem-sucedido: {{ last_successful_backup }}
Próximo Backup Agendado: {{ next_scheduled_backup }}

---
Este é um alerta crítico do sistema para administradores de {{ shop_name }}.
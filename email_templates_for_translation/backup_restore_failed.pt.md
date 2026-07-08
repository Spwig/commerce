---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 CRÍTICO: Restauração de Backup Falhou - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 CRÍTICO: Restauração de Backup Falhou
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Olá {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Uma operação crítica de restauração de backup falhou. Seu loja pode estar em um estado inconsistente e requer atenção imediata.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Detalhes da Restauração:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Arquivo de Backup:</strong> {{ backup_filename }}<br/>
              <strong>Iniciado:</strong> {{ restore_started_at }}<br/>
              <strong>Falhou:</strong> {{ restore_failed_at }}<br/>
              <strong>Duração:</strong> {{ restore_duration }}
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 AÇÃO IMEDIATA NECESSÁRIA:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>NÃO</strong> faça alterações no loja<br/>
              2. Verifique a conectividade e integridade do banco de dados<br/>
              3. Revise os logs de erro para obter o rastreamento de pilha detalhado<br/>
              4. Entre em contato imediatamente com o suporte técnico<br/>
              5. Considere voltar para o último estado conhecido bom
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Verificar Logs de Restauração
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Contate o Suporte de Emergência
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 CRÍTICO: RESTAURAÇÃO DE BACKUP FALHOU

Olá {{ admin_name }},

Uma operação crítica de restauração de backup falhou. Seu loja pode estar em um estado inconsistente e requer atenção imediata.

DETALHES DA RESTAURAÇÃO:
- Arquivo de Backup: {{ backup_filename }}
- Iniciado: {{ restore_started_at }}
- Falhou: {{ restore_failed_at }}
- Duração: {{ restore_duration }}

DETALHES DO ERRO:
{{ error_message }}

🚨 AÇÃO IMEDIATA NECESSÁRIA:
1. NÃO faça alterações no loja
2. Verifique a conectividade e integridade do banco de dados
3. Revise os logs de erro para obter o rastreamento de pilha detalhado
4. Entre em contato imediatamente com o suporte técnico
5. Considere voltar para o último estado conhecido bom

Verificar logs de restauração: {{ admin_backup_url }}
Contate o suporte de emergência: {{ support_url }}
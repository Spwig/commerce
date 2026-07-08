---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Quota de Armazenamento de Backup Crítica - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Quota de Armazenamento Crítica
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>URGENTE:</strong> Seu armazenamento de backup está criticamente baixo. Os backups futuros podem falhar se o espaço de armazenamento não for liberado.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Status do Armazenamento:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Usado:</strong> {{ storage_used }} de {{ storage_total }}<br/>
              <strong>Utilização:</strong> {{ storage_percentage }}%<br/>
              <strong>Disponível:</strong> {{ storage_available }}<br/>
              <strong>Status:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Ações Imediatas Necessárias:
            </mj-text>
            <mj-text color="#92400e">
              1. Excluir backups antigos que não são mais necessários<br/>
              2. Arquivar backups em armazenamento externo<br/>
              3. Aumentar a cota de armazenamento/capacidade<br/>
              4. Revisar a política de retenção de backups<br/>
              5. Monitorar o armazenamento diariamente até que seja resolvido
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Gerenciar Armazenamento Agora
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 QUOTA DE ARMAZENAMENTO CRÍTICA

Olá {{ admin_name }},

URGENTE: Seu armazenamento de backup está criticamente baixo. Os backups futuros podem falhar se o espaço de armazenamento não for liberado.

STATUS DO ARMAZENAMENTO:
- Usado: {{ storage_used }} de {{ storage_total }}
- Utilização: {{ storage_percentage }}%
- Disponível: {{ storage_available }}
- Status: {{ storage_status }}

AÇÕES IMEDIATAS NECESSÁRIAS:
1. Excluir backups antigos que não são mais necessários
2. Arquivar backups em armazenamento externo
3. Aumentar a cota de armazenamento/capacidade
4. Revisar a política de retenção de backups
5. Monitorar o armazenamento diariamente até que seja resolvido

Gerenciar armazenamento agora: {{ admin_backup_url }}
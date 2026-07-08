---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ Alerta de Tamanho do Backup - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Alerta de Tamanho do Backup
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Seu backup recente para {{ shop_name }} ultrapassou o limite recomendado de tamanho. Isso pode indicar uma necessidade crescente de armazenamento de dados.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informações do Backup:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tamanho Atual:</strong> {{ backup_size }}<br/>
              <strong>Limite de Alerta:</strong> {{ size_threshold }}<br/>
              <strong>Crescimento desde a Última Semana:</strong> {{ size_increase }}<br/>
              <strong>Data do Backup:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ações Recomendadas:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Revisar a política de retenção de backups<br/>
          2. Considere arquivar backups antigos<br/>
          3. Verificar por arquivos grandes desnecessários na biblioteca de mídia<br/>
          4. Avaliar as necessidades de capacidade de armazenamento<br/>
          5. Monitorar a tendência de crescimento do backup
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Gerenciar Backups
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERTA DE TAMANHO DO BACKUP

Olá {{ admin_name }},

Seu backup recente para {{ shop_name }} ultrapassou o limite recomendado de tamanho. Isso pode indicar uma necessidade crescente de armazenamento de dados.

INFORMAÇÕES DO BACKUP:
- Tamanho Atual: {{ backup_size }}
- Limite de Alerta: {{ size_threshold }}
- Crescimento desde a Última Semana: {{ size_increase }}
- Data do Backup: {{ backup_date }}

AÇÕES RECOMENDADAS:
1. Revisar a política de retenção de backups
2. Considere arquivar backups antigos
3. Verificar por arquivos grandes desnecessários na biblioteca de mídia
4. Avaliar as necessidades de capacidade de armazenamento
5. Monitorar a tendência de crescimento do backup

Gerenciar backups: {{ admin_backup_url }}
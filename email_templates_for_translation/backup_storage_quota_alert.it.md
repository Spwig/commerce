---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Quota di Archiviazione Critica - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Quota di Archiviazione Critica
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>URGENTE:</strong> La quota di archiviazione è criticamente bassa. I futuri backup potrebbero fallire se lo spazio di archiviazione non viene liberato.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Stato dell'Archiviazione:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Utilizzato:</strong> {{ storage_used }} di {{ storage_total }}<br/>
              <strong>Utilizzo:</strong> {{ storage_percentage }}%<br/>
              <strong>Disponibile:</strong> {{ storage_available }}<br/>
              <strong>Stato:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Azioni Immediate Necessarie:
            </mj-text>
            <mj-text color="#92400e">
              1. Elimina i backup vecchi non necessari<br/>
              2. Archivia i backup su un'archiviazione esterna<br/>
              3. Aumenta la quota/capacità di archiviazione<br/>
              4. Rivedi la politica di conservazione dei backup<br/>
              5. Monitora l'archiviazione quotidianamente fino a quando non è risolto
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Gestisci l'Archiviazione Ora
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 QUOTA DI ARCHIVIAZIONE CRITICA

Hi {{ admin_name }},

URGENTE: La quota di archiviazione è criticamente bassa. I futuri backup potrebbero fallire se lo spazio di archiviazione non viene liberato.

STORAGE STATUS:
- Utilizzato: {{ storage_used }} di {{ storage_total }}
- Utilizzo: {{ storage_percentage }}%
- Disponibile: {{ storage_available }}
- Stato: {{ storage_status }}

IMMEDIATE ACTIONS REQUIRED:
1. Elimina i backup vecchi non necessari
2. Archivia i backup su un'archiviazione esterna
3. Aumenta la quota/capacità di archiviazione
4. Rivedi la politica di conservazione dei backup
5. Monitora l'archiviazione quotidianamente fino a quando non è risolto

Gestisci l'archiviazione ora: {{ admin_backup_url }}
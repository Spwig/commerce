---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ Backup Programmato Non Eseguito - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Backup Programmato Mancato
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Un backup programmato per {{ shop_name }} non è stato eseguito come previsto. I tuoi dati potrebbero non essere completamente protetti.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli del Programma di Backup:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Ora Programmata:</strong> {{ scheduled_time }}<br/>
              <strong>Tipo di Backup:</strong> {{ backup_type }}<br/>
              <strong>Ultimo Backup Riuscito:</strong> {{ last_successful_backup }}<br/>
              <strong>Tempo Trascorso dall'Ultimo Backup:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cause Possibili:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • Il server era offline o non raggiungibile<br/>
          • Servizio di compiti programmati non in esecuzione<br/>
          • Permessi insufficienti<br/>
          • Spazio di archiviazione esaurito<br/>
          • Problemi di connettività al database
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Esegui Backup Manualmente
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza i Log del Sistema
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ BACKUP PROGRAMMATO MANCATO

Ciao {{ admin_name }},

Un backup programmato per {{ shop_name }} non è stato eseguito come previsto. I tuoi dati potrebbero non essere completamente protetti.

DETTAGLI DEL PROGRAMMA DI BACKUP:
- Ora Programmata: {{ scheduled_time }}
- Tipo di Backup: {{ backup_type }}
- Ultimo Backup Riuscito: {{ last_successful_backup }}
- Tempo Trascorso dall'Ultimo Backup: {{ time_since_last }}

CAUSE POSSIBILI:
• Il server era offline o non raggiungibile
• Servizio di compiti programmati non in esecuzione
• Permessi insufficienti
• Spazio di archiviazione esaurito
• Problemi di connettività al database

Esegui backup manualmente: {{ admin_backup_url }}
Visualizza i log del sistema: {{ admin_logs_url }}


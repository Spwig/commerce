---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 URGENTE: Backup Fallito - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Backup Fallito
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Ciao {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          È fallita un'operazione di backup critica per il tuo negozio {{ shop_name }}. È richiesta un'azione immediata per garantire la protezione dei dati.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Dettagli del Backup:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Tipo di Backup:</strong> {{ backup_type }}<br/>
              <strong>Iniziato:</strong> {{ backup_started_at }}<br/>
              <strong>Fallito:</strong> {{ backup_failed_at }}<br/>
              <strong>Durata:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dettagli dell'errore:
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
          Azioni Consigliate:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Controlla lo spazio disponibile sul disco del tuo server<br/>
          2. Verifica la connettività del database<br/>
          3. Rivedi il registro degli errori per ottenere il traceback dettagliato<br/>
          4. Riprova il backup manualmente o attendi l'esecuzione successiva pianificata<br/>
          5. Contatta il supporto se il problema persiste
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza i Log del Backup
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Riprova il Backup Ora
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Ultimo Backup Riuscito:</strong> {{ last_successful_backup }}<br/>
          <strong>Prossimo Backup Pianificato:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 URGENTE: BACKUP FALLITO

Ciao {{ admin_name }},

È fallita un'operazione di backup critica per il tuo negozio {{ shop_name }}. È richiesta un'azione immediata per garantire la protezione dei dati.

DETTAGLI DEL BACKUP:
- Tipo di Backup: {{ backup_type }}
- Iniziato: {{ backup_started_at }}
- Fallito: {{ backup_failed_at }}
- Durata: {{ backup_duration }}

DETTAGLI DELL'ERRORE:
{{ error_message }}

AZIONI CONSIGLIATE:
1. Controlla lo spazio disponibile sul disco del tuo server
2. Verifica la connettività del database
3. Rivedi il registro degli errori per ottenere il traceback dettagliato
4. Riprova il backup manualmente o attendi l'esecuzione successiva pianificata
5. Contatta il supporto se il problema persiste

Visualizza i log del backup: {{ admin_backup_url }}
Riprova il backup ora: {{ retry_backup_url }}

Ultimo Backup Riuscito: {{ last_successful_backup }}
Prossimo Backup Pianificato: {{ next_scheduled_backup }}

---
Questo è un avviso critico del sistema per gli amministratori di {{ shop_name }}.
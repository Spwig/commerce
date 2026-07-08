---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ Ripristino del backup completato - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Ripristino del backup completato
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Il ripristino del backup è stato completato con successo. I dati del tuo negozio sono stati ripristinati.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli del ripristino:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>File di backup:</strong> {{ backup_filename }}<br/>
              <strong>Data del backup:</strong> {{ backup_date }}<br/>
              <strong>Iniziato:</strong> {{ restore_started_at }}<br/>
              <strong>Completato:</strong> {{ restore_completed_at }}<br/>
              <strong>Durata:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Passaggi importanti successivi:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. Verifica che il tuo negozio funzioni correttamente<br/>
              2. Controlla i dati principali (prodotti, ordini, clienti)<br/>
              3. Pulisci la cache se necessario<br/>
              4. Testa i flussi di lavoro critici (checkout, accesso all'amministrazione)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Vai al pannello di amministrazione
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ RIPRISTINO DEL BACKUP COMPLETATO

Ciao {{ admin_name }},

Il ripristino del backup è stato completato con successo. I dati del tuo negozio sono stati ripristinati.

DETTAGLI DEL RIPRISTINO:
- File di backup: {{ backup_filename }}
- Data del backup: {{ backup_date }}
- Iniziato: {{ restore_started_at }}
- Completato: {{ restore_completed_at }}
- Durata: {{ restore_duration }}

⚠️ PASSAGGI IMPORTANTI SUCCESSIVI:
1. Verifica che il tuo negozio funzioni correttamente
2. Controlla i dati principali (prodotti, ordini, clienti)
3. Pulisci la cache se necessario
4. Testa i flussi di lavoro critici (checkout, accesso all'amministrazione)

Vai al pannello di amministrazione: {{ admin_dashboard_url }}
---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ Backupwiederherstellung abgeschlossen - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Backupwiederherstellung abgeschlossen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihre Wiederherstellung des Backups wurde erfolgreich abgeschlossen. Ihre Store-Daten wurden wiederhergestellt.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Wiederherstellungsdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Backup-Datei:</strong> {{ backup_filename }}<br/>
              <strong>Backup-Datum:</strong> {{ backup_date }}<br/>
              <strong>Started:</strong> {{ restore_started_at }}<br/>
              <strong>Abgeschlossen:</strong> {{ restore_completed_at }}<br/>
              <strong>Dauer:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Wichtige nächste Schritte:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. Stellen Sie sicher, dass Ihr Store ordnungsgemäß funktioniert<br/>
              2. Prüfen Sie wichtige Daten (Produkte, Bestellungen, Kunden)<br/>
              3. Löschen Sie bei Bedarf den Cache<br/>
              4. Testen Sie kritische Workflows (Kasse, Admin-Zugang)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Zum Admin-Dashboard
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BACKUP WIEDERHERSTELLUNG ABGESCHLOSSEN

Hi {{ admin_name }},

Ihre Wiederherstellung des Backups wurde erfolgreich abgeschlossen. Ihre Store-Daten wurden wiederhergestellt.

WIEDERHERSTELLUNGSDETAILS:
- Backup-Datei: {{ backup_filename }}
- Backup-Datum: {{ backup_date }}
- Started: {{ restore_started_at }}
- Abgeschlossen: {{ restore_completed_at }}
- Dauer: {{ restore_duration }}

⚠️ WICHTIGE NÄCHSTEN SCHREITEN:
1. Stellen Sie sicher, dass Ihr Store ordnungsgemäß funktioniert
2. Prüfen Sie wichtige Daten (Produkte, Bestellungen, Kunden)
3. Löschen Sie bei Bedarf den Cache
4. Testen Sie kritische Workflows (Kasse, Admin-Zugang)

Zum Admin-Dashboard: {{ admin_dashboard_url }}
---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 DRINGEND: Backup fehlgeschlagen - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Backup fehlgeschlagen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Eine kritische Backup-Operation ist bei Ihrem {{ shop_name }}-Geschäft fehlgeschlagen. Sofortige Maßnahmen sind erforderlich, um die Datensicherheit zu gewährleisten.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Backup-Details:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Backup-Typ:</strong> {{ backup_type }}<br/>
              <strong>Started:</strong> {{ backup_started_at }}<br/>
              <strong>Failed:</strong> {{ backup_failed_at }}<br/>
              <strong>Dauer:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Fehlerdetails:
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
          Empfohlene Aktionen:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Prüfen Sie den verfügbaren Speicherplatz auf Ihrem Server<br/>
          2. Überprüfen Sie die Datenbankverbindung<br/>
          3. Untersuchen Sie den Fehlerprotokoll für eine detaillierte Stack-Trace<br/>
          4. Versuchen Sie das Backup manuell erneut oder warten Sie auf die nächste geplante Ausführung<br/>
          5. Kontaktieren Sie den Support, wenn das Problem weiterhin besteht
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Backup-Protokolle ansehen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Backup jetzt erneut ausführen
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Letztes erfolgreiches Backup:</strong> {{ last_successful_backup }}<br/>
          <strong>Nächst geplantes Backup:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 DRINGEND: BACKUP FEHLGESCHLAGEN

Hi {{ admin_name }},

Eine kritische Backup-Operation ist bei Ihrem {{ shop_name }}-Geschäft fehlgeschlagen. Sofortige Maßnahmen sind erforderlich, um die Datensicherheit zu gewährleisten.

BACKUP-DETAILS:
- Backup-Typ: {{ backup_type }}
- Started: {{ backup_started_at }}
- Failed: {{ backup_failed_at }}
- Dauer: {{ backup_duration }}

FEHLERDETAILS:
{{ error_message }}

EMPFOHLENE Aktionen:
1. Prüfen Sie den verfügbaren Speicherplatz auf Ihrem Server
2. Überprüfen Sie die Datenbankverbindung
3. Untersuchen Sie den Fehlerprotokoll für eine detaillierte Stack-Trace
4. Versuchen Sie das Backup manuell erneut oder warten Sie auf die nächste geplante Ausführung
5. Kontaktieren Sie den Support, wenn das Problem weiterhin besteht

Backup-Protokolle ansehen: {{ admin_backup_url }}
Backup jetzt erneut ausführen: {{ retry_backup_url }}

Letztes erfolgreiches Backup: {{ last_successful_backup }}
Nächst geplantes Backup: {{ next_scheduled_backup }}

---
Dies ist ein kritischer Systemalarm für {{ shop_name }}-Administrator.

Erinnern Sie sich: Bewahren Sie alle Django-Vorlagen-Syntax ({{ }}, {% %}), alle MJML-Tags (<mj-*>), alle HTML-Attribute und alle Emojis bei der Übersetzung bei.


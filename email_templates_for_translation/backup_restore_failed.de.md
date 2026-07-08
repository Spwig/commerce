---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 KRITISCH: Wiederherstellung der Sicherung fehlgeschlagen - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 KRITISCH: Wiederherstellung der Sicherung fehlgeschlagen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Eine kritische Wiederherstellung der Sicherung ist fehlgeschlagen. Ihr Geschäft könnte sich in einem inkonsistenten Zustand befinden und erfordert sofortige Aufmerksamkeit.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Wiederherstellungsdetails:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Sicherungsdatei:</strong> {{ backup_filename }}<br/>
              <strong>Started:</strong> {{ restore_started_at }}<br/>
              <strong>Failed:</strong> {{ restore_failed_at }}<br/>
              <strong>Dauer:</strong> {{ restore_duration }}
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 AKUTER HANDLUNGSBEDARF:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>DO NOT</strong> make any changes to the store<br/>
              2. Prüfen Sie die Datenbankverbindung und -integrität<br/>
              3. Untersuchen Sie die Fehlerprotokolle, um den detaillierten Stapelspuren zu erhalten<br/>
              4. Kontaktieren Sie sofort den technischen Support<br/>
              5. Überlegen Sie, sich auf den letzten bekannten stabilen Zustand zurückzukehren
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Wiederherstellungstagebuch ansehen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Notfallsupport kontaktieren
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 KRITISCH: SICHERUNGSWIEDERHERSTELLUNG FEHLGESCHLAGEN

Hi {{ admin_name }},

Eine kritische Sicherungswiederherstellung ist fehlgeschlagen. Ihr Geschäft könnte sich in einem inkonsistenten Zustand befinden und erfordert sofortige Aufmerksamkeit.

Wiederherstellungsdetails:
- Sicherungsdatei: {{ backup_filename }}
- Started: {{ restore_started_at }}
- Failed: {{ restore_failed_at }}
- Dauer: {{ restore_duration }}

Fehlerdetails:
{{ error_message }}

🚨 AKUTER HANDLUNGSBEDARF:
1. DO NOT make any changes to the store
2. Prüfen Sie die Datenbankverbindung und -integrität
3. Untersuchen Sie die Fehlerprotokolle, um den detaillierten Stapelspuren zu erhalten
4. Kontaktieren Sie sofort den technischen Support
5. Überlegen Sie, sich auf den letzten bekannten stabilen Zustand zurückzukehren

Wiederherstellungstagebuch ansehen: {{ admin_backup_url }}
Notfallsupport kontaktieren: {{ support_url }}
---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
Wöchentliche Backup-Zusammenfassung - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Wöchentliche Backup-Zusammenfassung
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Backup-Statistiken:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gesamt Backups:</strong> {{ total_backups }}<br/>
              <strong>Erfolgreich:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>Fehlgeschlagen:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>Durchschnittliche Größe:</strong> {{ average_size }}<br/>
              <strong>Gesamte Speichergröße:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Probleme erkannt:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} Backup(s) sind in dieser Woche fehlgeschlagen. Bitte überprüfen Sie diese und ergreifen Sie korrigierende Maßnahmen.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Letzte Backups:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Größe: {{ backup.size }} | Dauer: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ Erfolg</span>
              {% else %}
              <span style="color: #dc2626;">✗ Fehlgeschlagen</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Alle Backups ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
WÖCHENTLICHE BACKUP-ZUSAMMENFASSUNG
{{ week_start }} - {{ week_end }}

BACKUP-STATISTIKEN:
- Gesamt Backups: {{ total_backups }}
- Erfolgreich: {{ successful_backups }}
- Fehlgeschlagen: {{ failed_backups }}
- Durchschnittliche Größe: {{ average_size }}
- Gesamte Speichergröße: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ PROBLEME ERKANNT:
{{ failed_backups }} Backup(s) sind in dieser Woche fehlgeschlagen. Bitte überprüfen Sie diese und ergreifen Sie korrigierende Maßnahmen.
{% endif %}

LENESTE BACKUPS:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Größe: {{ backup.size }} | Dauer: {{ backup.duration }} | Status: {{ backup.status }}
{% endfor %}

Alle Backups ansehen: {{ admin_backup_url }}
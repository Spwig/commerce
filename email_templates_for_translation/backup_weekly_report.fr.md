---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
Résumé de sauvegarde hebdomadaire - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Résumé de sauvegarde hebdomadaire
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Statistiques de sauvegarde:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total de sauvegardes:</strong> {{ total_backups }}<br/>
              <strong>Réussies:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>Échouées:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>Taille moyenne:</strong> {{ average_size }}<br/>
              <strong>Total d'espace utilisé:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Problèmes détectés:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} sauvegarde(s) ont échoué cette semaine. Veuillez vérifier et prendre des mesures correctives.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dernières sauvegardes:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Taille: {{ backup.size }} | Durée: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ Réussie</span>
              {% else %}
              <span style="color: #dc2626;">✗ Échouée</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Voir toutes les sauvegardes
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
RÉSUMÉ DE SAUVEGARDE HEBDOMADAIRE
{{ week_start }} - {{ week_end }}

STATISTIQUES DE SAUVEGARDE:
- Total de sauvegardes: {{ total_backups }}
- Réussies: {{ successful_backups }}
- Échouées: {{ failed_backups }}
- Taille moyenne: {{ average_size }}
- Total d'espace utilisé: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ PROBLÈMES DÉTÉCTÉS:
{{ failed_backups }} sauvegarde(s) ont échoué cette semaine. Veuillez vérifier et prendre des mesures correctives.
{% endif %}

DERNIÈRES SAUVEGARDES:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Taille: {{ backup.size }} | Durée: {{ backup.duration }} | Statut: {{ backup.status }}
{% endfor %}

Voir toutes les sauvegardes: {{ admin_backup_url }}
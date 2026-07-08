---
template_type: backup_completed
category: Backups
---

# Email Template: backup_completed

## Subject
✓ Sauvegarde terminée avec succès - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Sauvegarde terminée avec succès
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre sauvegarde planifiée pour {{ shop_name }} a été terminée avec succès.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de la sauvegarde:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Type:</strong> {{ backup_type }}<br/>
              <strong>Début:</strong> {{ backup_started_at }}<br/>
              <strong>Terminé:</strong> {{ backup_completed_at }}<br/>
              <strong>Durée:</strong> {{ backup_duration }}<br/>
              <strong>Taille:</strong> {{ backup_size }}<br/>
              <strong>Emplacement:</strong> {{ backup_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Voir les détails de la sauvegarde
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Prochaine sauvegarde planifiée:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ SAUVEGARDE TERMINÉE AVEC SUCCÈS

Bonjour {{ admin_name }},

Votre sauvegarde planifiée pour {{ shop_name }} a été terminée avec succès.

DÉTAILS DE LA SAUVEGARDE:
- Type: {{ backup_type }}
- Début: {{ backup_started_at }}
- Terminé: {{ backup_completed_at }}
- Durée: {{ backup_duration }}
- Taille: {{ backup_size }}
- Emplacement: {{ backup_location }}

Voir les détails de la sauvegarde: {{ admin_backup_url }}

Prochaine sauvegarde planifiée: {{ next_scheduled_backup }}
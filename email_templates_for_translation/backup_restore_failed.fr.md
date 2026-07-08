---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 CRITICAL: Backup Restore Failed - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 CRITICAL: Backup Restore Failed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Une opération de restauration de sauvegarde critique a échoué. Votre magasin peut être dans un état incohérent et nécessite une attention immédiate.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Restore Details:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Fichier de sauvegarde :</strong> {{ backup_filename }}<br/>
              <strong>Début :</strong> {{ restore_started_at }}<br/>
              <strong>Échec :</strong> {{ restore_failed_at }}<br/>
              <strong>Durée :</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Error Details:
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
              🚨 IMMEDIATE ACTION REQUIRED:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>NE PAS</strong> apporter de modifications au magasin<br/>
              2. Vérifier la connectivité et l'intégrité de la base de données<br/>
              3. Examiner les journaux d'erreurs pour obtenir la trace d'empilement détaillée<br/>
              4. Contacter immédiatement le support technique<br/>
              5. Envisager de revenir à l'état connu correct précédent
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Restore Logs
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Contact Emergency Support
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 CRITICAL: BACKUP RESTORE FAILED

Hi {{ admin_name }},

Une opération de restauration de sauvegarde critique a échoué. Votre magasin peut être dans un état incohérent et nécessite une attention immédiate.

RESTORE DETAILS:
- Fichier de sauvegarde : {{ backup_filename }}
- Début : {{ restore_started_at }}
- Échec : {{ restore_failed_at }}
- Durée : {{ restore_duration }}

ERROR DETAILS:
{{ error_message }}

🚨 IMMEDIATE ACTION REQUIRED:
1. NE PAS apporter de modifications au magasin
2. Vérifier la connectivité et l'intégrité de la base de données
3. Examiner les journaux d'erreurs pour obtenir la trace d'empilement détaillée
4. Contacter immédiatement le support technique
5. Envisager de revenir à l'état connu correct précédent

View restore logs: {{ admin_backup_url }}
Contact emergency support: {{ support_url }}
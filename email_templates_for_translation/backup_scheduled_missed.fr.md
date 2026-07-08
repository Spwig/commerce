---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ Sauvegarde planifiée non effectuée - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Sauvegarde planifiée manquante
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Une sauvegarde planifiée pour {{ shop_name }} n'a pas eu lieu comme prévu. Vos données ne sont peut-être pas pleinement protégées.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails du planning de sauvegarde :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Heure planifiée :</strong> {{ scheduled_time }}<br/>
              <strong>Type de sauvegarde :</strong> {{ backup_type }}<br/>
              <strong>Dernière sauvegarde réussie :</strong> {{ last_successful_backup }}<br/>
              <strong>Temps depuis la dernière sauvegarde :</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causes possibles :
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • Le serveur était hors ligne ou inaccessible<br/>
          • Le service de tâche planifiée n'est pas en cours d'exécution<br/>
          • Permissions insuffisantes<br/>
          • Espace de stockage plein<br/>
          • Problèmes de connectivité à la base de données
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Exécuter la sauvegarde manuellement
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir les journaux du système
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ SAUVEGARDE PLANIFIÉE MANQUANTE

Bonjour {{ admin_name }},

Une sauvegarde planifiée pour {{ shop_name }} n'a pas eu lieu comme prévu. Vos données ne sont peut-être pas pleinement protégées.

DÉTAILS DU PLANNING DE SAUVEGARDE :
- Heure planifiée : {{ scheduled_time }}
- Type de sauvegarde : {{ backup_type }}
- Dernière sauvegarde réussie : {{ last_successful_backup }}
- Temps depuis la dernière sauvegarde : {{ time_since_last }}

CAUSES POSSIBLES :
• Le serveur était hors ligne ou inaccessible
• Le service de tâche planifiée n'est pas en cours d'exécution
• Permissions insuffisantes
• Espace de stockage plein
• Problèmes de connectivité à la base de données

Exécuter la sauvegarde manuellement : {{ admin_backup_url }}
Voir les journaux du système : {{ admin_logs_url }}
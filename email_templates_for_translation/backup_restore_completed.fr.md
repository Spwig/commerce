---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ Restauration de sauvegarde terminée - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Restauration de sauvegarde terminée
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre opération de restauration de sauvegarde a été terminée avec succès. Vos données de magasin ont été restaurées.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de la restauration:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Fichier de sauvegarde :</strong> {{ backup_filename }}<br/>
              <strong>Date de sauvegarde :</strong> {{ backup_date }}<br/>
              <strong>Début :</strong> {{ restore_started_at }}<br/>
              <strong>Terminé :</strong> {{ restore_completed_at }}<br/>
              <strong>Durée :</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Étapes importantes à suivre:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. Vérifiez que votre magasin fonctionne correctement<br/>
              2. Vérifiez les données clés (produits, commandes, clients)<br/>
              3. Nettoyez le cache si nécessaire<br/>
              4. Testez les workflows critiques (commande, accès administrateur)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Accédez au tableau de bord administrateur
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ RESTAURATION DE SAUVEGARDE TERMINÉE

Bonjour {{ admin_name }},

Votre opération de restauration de sauvegarde a été terminée avec succès. Vos données de magasin ont été restaurées.

DÉTAILS DE LA RESTAURATION:
- Fichier de sauvegarde : {{ backup_filename }}
- Date de sauvegarde : {{ backup_date }}
- Début : {{ restore_started_at }}
- Terminé : {{ restore_completed_at }}
- Durée : {{ restore_duration }}

⚠️ ÉTAPES IMPORTANTES À SUIVRE:
1. Vérifiez que votre magasin fonctionne correctement
2. Vérifiez les données clés (produits, commandes, clients)
3. Nettoyez le cache si nécessaire
4. Testez les workflows critiques (commande, accès administrateur)

Accédez au tableau de bord administrateur : {{ admin_dashboard_url }}
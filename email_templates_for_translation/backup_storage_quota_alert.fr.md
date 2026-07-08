---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Quota de stockage critique - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Quota de stockage critique
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>URGENT:</strong> Votre stockage de sauvegarde est critique. Les sauvegardes futures peuvent échouer si l'espace de stockage n'est pas libéré.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              État du stockage :
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Utilisé :</strong> {{ storage_used }} de {{ storage_total }}<br/>
              <strong>Taux d'utilisation :</strong> {{ storage_percentage }}%<br/>
              <strong>Disponible :</strong> {{ storage_available }}<br/>
              <strong>Statut :</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Actions immédiates requises :
            </mj-text>
            <mj-text color="#92400e">
              1. Supprimez les sauvegardes anciennes non nécessaires<br/>
              2. Archivez les sauvegardes vers un stockage externe<br/>
              3. Augmentez le quota/capacité de stockage<br/>
              4. Révisez la politique de rétention des sauvegardes<br/>
              5. Surveillez le stockage quotidiennement jusqu'à résolution
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Gérer le stockage maintenant
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 QUOTA DE STOCKAGE CRITIQUE

Hi {{ admin_name }},

URGENT : Votre stockage de sauvegarde est critique. Les sauvegardes futures peuvent échouer si l'espace de stockage n'est pas libéré.

ÉTAT DU STOCKAGE : 
- Utilisé : {{ storage_used }} de {{ storage_total }}
- Taux d'utilisation : {{ storage_percentage }}%
- Disponible : {{ storage_available }}
- Statut : {{ storage_status }}

ACTIONS IMMÉDIATES REQUISES : 
1. Supprimez les sauvegardes anciennes non nécessaires
2. Archivez les sauvegardes vers un stockage externe
3. Augmentez le quota/capacité de stockage
4. Révisez la politique de rétention des sauvegardes
5. Surveillez le stockage quotidiennement jusqu'à résolution

Gérez le stockage maintenant : {{ admin_backup_url }}
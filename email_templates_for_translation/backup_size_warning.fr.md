---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ Avertissement Taille Sauvegarde - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Avertissement Taille Sauvegarde
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre dernière sauvegarde pour {{ shop_name }} a dépassé le seuil de taille recommandé. Cela peut indiquer une demande croissante en stockage de données.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informations sur la sauvegarde :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Taille actuelle :</strong> {{ backup_size }}<br/>
              <strong>Seuil d'avertissement :</strong> {{ size_threshold }}<br/>
              <strong>Croissance depuis la semaine dernière :</strong> {{ size_increase }}<br/>
              <strong>Date de sauvegarde :</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées : 
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Réviser la politique de rétention des sauvegardes<br/>
          2. Considérer l'archivage des anciennes sauvegardes<br/>
          3. Vérifier la présence de fichiers volumineux non nécessaires dans la bibliothèque médias<br/>
          4. Évaluer les besoins en capacité de stockage<br/>
          5. Surveiller l'évolution de la taille des sauvegardes
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Gérer les sauvegardes
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVERTISSEMENT DE LA TAILLE DE LA SAUVEGARDE

Bonjour {{ admin_name }},

Votre dernière sauvegarde pour {{ shop_name }} a dépassé le seuil de taille recommandé. Cela peut indiquer une demande croissante en stockage de données.

INFORMATIONS SUR LA SAUVEGARDE : 
- Taille actuelle : {{ backup_size }}
- Seuil d'avertissement : {{ size_threshold }}
- Croissance depuis la semaine dernière : {{ size_increase }}
- Date de sauvegarde : {{ backup_date }}

ACTIONS RECOMMANDÉES : 
1. Réviser la politique de rétention des sauvegardes
2. Considérer l'archivage des anciennes sauvegardes
3. Vérifier la présence de fichiers volumineux non nécessaires dans la bibliothèque médias
4. Évaluer les besoins en capacité de stockage
5. Surveiller l'évolution de la taille des sauvegardes

Gérer les sauvegardes : {{ admin_backup_url }}
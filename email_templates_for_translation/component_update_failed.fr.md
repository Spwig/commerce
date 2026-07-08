---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Mise à jour échouée : {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Mise à jour échouée
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erreur d'installation
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          La mise à jour de {{ component_name }} vers la version {{ target_version }} n'a pas pu être installée.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de l'échec :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Composant :</strong> {{ component_name }}<br/>
              <strong>Version cible :</strong> {{ target_version }}<br/>
              <strong>Échec à :</strong> {{ failed_at }}<br/>
              <strong>Code d'erreur :</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Message d'erreur : 
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Journal d'erreur complet :</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:50 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          À faire : 
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Vérifier les exigences système et les dépendances<br/>
          2. Examiner le journal d'erreur pour plus de détails<br/>
          3. Réessayer l'installation ou contacter le support<br/>
          4. Votre magasin fonctionne toujours sur {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Réessayer l'installation
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contacter le support
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ MISE À JOUR ÉCHOUÉE

Erreur d'installation

La mise à jour de {{ component_name }} vers la version {{ target_version }} n'a pas pu être installée.

DÉTAILS DE L'ÉCHEC :
- Composant : {{ component_name }}
- Version cible : {{ target_version }}
- Échec à : {{ failed_at }}
- Code d'erreur : {{ error_code }}

MESSAGE D'ERREUR : 
{{ error_message }}

{% if error_log %}
JOURNAL D'ERREUR COMPLET : 
{{ error_log|truncatewords:50 }}
{% endif %}

À FAIRE : 
1. Vérifier les exigences système et les dépendances
2. Examiner le journal d'erreur pour plus de détails
3. Réessayer l'installation ou contacter le support
4. Votre magasin fonctionne toujours sur {{ current_version }}

Réessayer l'installation : {{ retry_url }}
Contacter le support : {{ support_url }}
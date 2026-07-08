---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ {{ feed_name }} synchronisation échouée avec {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Synchronisation Échouée
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erreur de Synchronisation
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Échec de la synchronisation de {{ feed_name }} vers {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de l'Échec:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Error Code:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Message d'Erreur:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causes Courantes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Identifiants API invalides ou jeton expiré<br/>
          • Problèmes de connectivité réseau<br/>
          • Limite de taux d'API de la plateforme dépassée<br/>
          • Le format du feed ne correspond pas aux exigences de la plateforme
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Action Recommandée
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Réessayer la Synchronisation
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Vérifier les Paramètres du Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ SYNCHRONISATION ÉCHOUÉE

Erreur de synchronisation

Échec de la synchronisation de {{ feed_name }} vers {{ platform_name }}.

DÉTAILS DE L'ÉCHEC:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

MESSAGE D'ERREUR:
{{ error_message }}

CAUSES COURANTES:
• Identifiants API invalides ou jeton expiré
• Problèmes de connectivité réseau
• Limite de taux d'API de la plateforme dépassée
• Le format du feed ne correspond pas aux exigences de la plateforme

{% if recommended_action %}
ACTION RECOMMANDÉE:
{{ recommended_action }}
{% endif %}

Réessayer la synchronisation: {{ retry_url }}
Vérifier les paramètres du feed: {{ admin_feed_url }}
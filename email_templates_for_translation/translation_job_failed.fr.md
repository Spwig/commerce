---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Échec de la traduction : {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Échec de la tâche de traduction
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erreur de traduction
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre tâche de traduction en vrac a rencontré un problème et n'a pas pu être terminée.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de la tâche :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID :</strong> {{ job_id }}<br/>
              <strong>Type de contenu :</strong> {{ content_type }}<br/>
              <strong>Langues cibles :</strong> {{ target_languages }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Complétion partielle
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} sur {{ total_items }} éléments ont été correctement traduits avant que l'erreur ne survienne.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causes courantes :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Problèmes de connexion avec l'API du service de traduction<br/>
          • Crédits de traduction insuffisants<br/>
          • Contenu source invalide ou corrompu<br/>
          • Paire de langues non prise en charge
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Vérifiez les paramètres de votre service de traduction<br/>
          2. Vérifiez que des crédits de traduction sont disponibles<br/>
          3. Examinez le message d'erreur pour identifier les problèmes spécifiques<br/>
          4. Réessayez la tâche de traduction
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Réessayer la traduction
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Vérifier les paramètres
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Si le problème persiste, contactez le support avec le code d'erreur {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ ÉCHEC DE LA TÂCHE DE TRADUCTION

Erreur de traduction

Votre tâche de traduction en vrac a rencontré un problème et n'a pas pu être terminée.

DÉTAILS DE LA TÂCHE :
- Job ID : {{ job_id }}
- Type de contenu : {{ content_type }}
- Langues cibles : {{ target_languages }}
- Échec à : {{ failed_at }}
- Code d'erreur : {{ error_code }}

MESSAGE D'ERREUR :
{{ error_message }}

{% if partial_completion %}
COMPLÉTION PARTIELLE : 
{{ items_completed }} sur {{ total_items }} éléments ont été correctement traduits avant que l'erreur ne survienne.
{% endif %}

CAUSES COURANTES : 
• Problèmes de connexion avec l'API du service de traduction
• Crédits de traduction insuffisants
• Contenu source invalide ou corrompu
• Paire de langues non prise en charge

ACTIONS RECOMMANDÉES : 
1. Vérifiez les paramètres de votre service de traduction
2. Vérifiez que des crédits de traduction sont disponibles
3. Examinez le message d'erreur pour identifier les problèmes spécifiques
4. Réessayez la tâche de traduction

Réessayer la traduction : {{ retry_url }}
Vérifier les paramètres : {{ settings_url }}

Si le problème persiste, contactez le support avec le code d'erreur {{ error_code }}.
---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Votre retour a été approuvé - Commande #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Retour approuvé
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Commande #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre demande de retour pour la commande <strong>#{{ order_number }}</strong> a été approuvée.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Étapes suivantes :</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Téléchargez et imprimez l'étiquette de retour ci-dessous<br/>
          2. Emballez les articles de manière sécurisée dans leur emballage d'origine si possible<br/>
          3. Fixez l'étiquette de retour sur l'extérieur du colis<br/>
          4. Déposez le colis au point de livraison le plus proche
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Télécharger l'étiquette de retour
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Numéro de suivi du retour :</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Important :</strong> Veuillez envoyer le retour dans les 7 jours pour garantir un remboursement rapide.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Une fois que nous aurons reçu et inspecté votre retour, nous traiterons votre remboursement vers le mode de paiement original.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Retour approuvé - Commande #{{ order_number }}

Bonjour {{ customer_name }},

Votre demande de retour pour la commande #{{ order_number }} a été approuvée.

Étapes suivantes :
1. Téléchargez et imprimez l'étiquette de retour
2. Emballez les articles de manière sécurisée dans leur emballage d'origine si possible
3. Fixez l'étiquette de retour sur l'extérieur du colis
4. Déposez le colis au point de livraison le plus proche

{% if return_label_url %}Télécharger votre étiquette de retour : {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Numéro de suivi du retour : {{ return_tracking_number }}{% endif %}

Important : Veuillez envoyer le retour dans les 7 jours pour garantir un remboursement rapide.

Une fois que nous aurons reçu et inspecté votre retour, nous traiterons votre remboursement vers le mode de paiement original.
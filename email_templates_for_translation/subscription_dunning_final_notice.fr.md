---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ AVIS FINAL : Votre abonnement sera annulé dans {{ days_until_cancellation }} jours

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ AVIS FINAL
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Annulation de l'abonnement imminente
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Cet avis final. Nous n'avons pas pu traiter le paiement pour votre abonnement {{ plan_name }}. Si nous ne recevons pas de paiement dans {{ days_until_cancellation }} jours, votre abonnement sera annulé.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Paiement échoué - Action requise
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Abonnement:</strong> {{ plan_name }}<br/>
              <strong>Montant dû:</strong> {{ amount_due }}<br/>
              <strong>Essais échoués:</strong> {{ retry_count }}<br/>
              <strong>Dernier essai:</strong> {{ last_retry_date }}<br/>
              <strong>Date d'annulation:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erreur de paiement:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qu'est-ce qui se passera:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Si le paiement n'est pas reçu d'ici {{ cancellation_date }}:<br/>
          • Votre abonnement sera annulé<br/>
          • Vous perdrez l'accès à tous les avantages de l'abonnement<br/>
          • Vos données pourraient être supprimées (voir politique de conservation)<br/>
          • Vous devrez vous réabonner pour retrouver l'accès
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Mettez à jour votre mode de paiement maintenant
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Mettre à jour le mode de paiement
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problèmes courants & Solutions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Carte expirée:</strong> Mettez à jour avec une carte de crédit valide<br/>
          • <strong>Insuffisance de fonds:</strong> Assurez-vous d'avoir un solde suffisant<br/>
          • <strong>Carte refusée:</strong> Contactez votre banque ou utilisez une autre carte<br/>
          • <strong>Incohérence d'adresse:</strong> Vérifiez que l'adresse de facturation correspond à celle de la carte
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Besoin d'aide ?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Si vous rencontrez des problèmes de paiement ou si vous avez besoin d'aide, veuillez contacter immédiatement notre équipe de support.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contacter le support
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Si vous souhaitez annuler votre abonnement, vous pouvez le faire dans les paramètres de votre compte.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVIS FINAL

Annulation de l'abonnement imminente

Bonjour {{ customer_name }},

Cet avis final. Nous n'avons pas pu traiter le paiement pour votre abonnement {{ plan_name }}. Si nous ne recevons pas de paiement dans {{ days_until_cancellation }} jours, votre abonnement sera annulé.

⚠️ PAIEMENT ÉCHOUÉ - ACTION REQUISE:
- Abonnement: {{ plan_name }}
- Montant dû: {{ amount_due }}
- Essais échoués: {{ retry_count }}
- Dernier essai: {{ last_retry_date }}
- Date d'annulation: {{ cancellation_date }}

ERREUR DE PAIEMENT:
{{ payment_error_message }}

QU'EST-CE QUI SE PASSERA:
Si le paiement n'est pas reçu d'ici {{ cancellation_date }}:
• Votre abonnement sera annulé
• Vous perdrez l'accès à tous les avantages de l'abonnement
• Vos données pourraient être supprimées (voir politique de conservation)
• Vous devrez vous réabonner pour retrouver l'accès

METTEZ À JOUR VOTRE MODE DE PAIEMENT MAINTENANT

Problèmes courants & Solutions:
• Carte expirée: Mettez à jour avec une carte de crédit valide
• Insuffisance de fonds: Assurez-vous d'avoir un solde suffisant
• Carte refusée: Contactez votre banque ou utilisez une autre carte
• Incohérence d'adresse: Vérifiez que l'adresse de facturation correspond à celle de la carte

BESOIN D'AIDE ?
Si vous rencontrez des problèmes de paiement ou si vous avez besoin d'aide, veuillez contacter immédiatement notre équipe de support.

Mettre à jour le mode de paiement: {{ update_payment_url }}
Contacter le support: {{ support_url }}

Si vous souhaitez annuler votre abonnement, vous pouvez le faire dans les paramètres de votre compte.
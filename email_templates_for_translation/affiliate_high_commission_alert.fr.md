---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ Activité de commission inhabituelle détectée - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Alerte commission élevée
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Activité inhabituelle détectée
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Une commission inhabituellement élevée a été générée par l'affiliate {{ affiliate_name }}. Cela nécessite une vérification pour la prévention des fraudes.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de l'alerte :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Affiliate:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Montant de la commission:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>Valeur de la commande:</strong> {{ order_value }}<br/>
              <strong>Numéro de commande:</strong> {{ order_number }}<br/>
              <strong>Détecté:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pourquoi cela a été signalé :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Vérifier les détails de la commande pour vérifier leur légitimité<br/>
          • Vérifier l'historique des références de l'affiliate<br/>
          • Vérifier que le client n'est pas affilié au référent<br/>
          • Approuver ou rejeter la commission via le panneau d'administration
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Vérifier la commission
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir les détails de l'affiliate
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Cette commission est en attente de vérification et ne sera pas payée tant qu'elle n'aura pas été approuvée.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERTE COMMISSION ÉLEVÉE

Activité inhabituelle détectée

Une commission inhabituellement élevée a été générée par l'affiliate {{ affiliate_name }}. Cela nécessite une vérification pour la prévention des fraudes.

DÉTAILS DE L'ALERTE :
- Affiliate: {{ affiliate_name }} ({{ affiliate_id }})
- Montant de la commission: {{ commission_amount }}
- Valeur de la commande: {{ order_value }}
- Numéro de commande: {{ order_number }}
- Détecté: {{ detected_at }}

POURQUOI CELA A ÉTÉ SIGNALÉ :
{{ flag_reason }}

ACTIONS RECOMMANDÉES :
• Vérifier les détails de la commande pour vérifier leur légitimité
• Vérifier l'historique des références de l'affiliate
• Vérifier que le client n'est pas affilié au référent
• Approuver ou rejeter la commission via le panneau d'administration

Vérifier la commission: {{ review_commission_url }}
Voir les détails de l'affiliate: {{ affiliate_details_url }}

Cette commission est en attente de vérification et ne sera pas payée tant qu'elle n'aura pas été approuvée.
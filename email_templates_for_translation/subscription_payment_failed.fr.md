---
template_type: subscription_payment_failed
category: Subscriptions
---

# Email Template: subscription_payment_failed

## Subject
⚠️ Paiement échoué pour {{ plan_name }} - Action requise - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⚠️ Paiement échoué
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Nous n'avons pas pu traiter votre paiement
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Failed Payment Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fef2f2" padding="30px" border="2px solid {{ theme.color.error|default:'#ef4444' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#7f1d1d" align="center" padding-bottom="15px">
                Informations de paiement
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Plan:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Montant:</strong> {{ subscription_amount }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Méthode de paiement:</strong> {{ payment_method }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" padding="5px 0">
                <strong>Raison:</strong> {{ failure_reason }}
              </mj-text>

              <mj-divider border-color="#fecaca" border-width="1px" padding="15px 0" />

              <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" padding="5px 0" font-weight="600">
                Veuillez mettre à jour votre méthode de paiement d'ici {{ retry_date|date:"F d, Y" }} pour éviter une interruption du service.
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What to Do Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Que devez-vous faire ?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">1.</span>
          Vérifiez que votre méthode de paiement dispose de fonds suffisants
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">2.</span>
          Mettez à jour votre méthode de paiement si la carte est expirée
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">3.</span>
          Nous allons automatiquement réessayer le paiement dans {{ retry_days }} jours
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ update_payment_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Mettre à jour la méthode de paiement
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ manage_subscription_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            Voir l'abonnement
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Besoin d'aide ? Contactez-nous à {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Propulsé par Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ Paiement échoué

Nous n'avons pas pu traiter votre paiement

INFORMATIONS DE PAIEMENT:
Plan: {{ plan_name }}
Montant: {{ subscription_amount }}
Méthode de paiement: {{ payment_method }}
Raison: {{ failure_reason }}

Veuillez mettre à jour votre méthode de paiement d'ici {{ retry_date|date:"F d, Y" }} pour éviter une interruption du service.

Que devez-vous faire ?
1. Vérifiez que votre méthode de paiement dispose de fonds suffisants
2. Mettez à jour votre méthode de paiement si la carte est expirée
3. Nous allons automatiquement réessayer le paiement dans {{ retry_days }} jours

Mettre à jour la méthode de paiement: {{ update_payment_url }}
Voir l'abonnement: {{ manage_subscription_url }}

Besoin d'aide ? Contactez-nous à {{ support_email }}

---
Propulsé par Spwig - https://spwig.com
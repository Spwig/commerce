---
template_type: subscription_renewal_reminder
category: Subscriptions
---

# Email Template: subscription_renewal_reminder

## Subject
🔔 La tua {{ plan_name }} si rinnova tra {{ days_until_renewal }} giorni - {{ shop_name }}

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🔔 Ricordo di rinnovo
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Il tuo abbonamento si rinnova presto
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Info Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#f0f9ff" padding="30px" border="2px solid #0ea5e9" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#0c4a6e" align="center" padding-bottom="15px">
                Addebito imminente
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Piano:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Importo:</strong> {{ subscription_amount }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Data di rinnovo:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Metodo di pagamento:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- Action Needed Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px" line-height="1.6" align="center">
          Nessun'azione richiesta. Il tuo abbonamento si rinnoverà automaticamente il {{ next_billing_date|date:"F d, Y" }}.
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding="15px 20px 0 20px" line-height="1.6" align="center">
          Devi aggiornare il metodo di pagamento o apportare modifiche? Visita il dashboard del tuo account.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Gestisci l'abbonamento
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ update_payment_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            Aggiorna il metodo di pagamento
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Hai bisogno di aiuto? Contattaci a {{ support_email }}
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
            Powered by Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔔 Ricordo di rinnovo

Il tuo abbonamento si rinnova presto

ADDEBITO IMMINENTE:
Plan: {{ plan_name }}
Amount: {{ subscription_amount }}
Renewal Date: {{ next_billing_date|date:"F d, Y" }}
Payment Method: {{ payment_method }}

Nessun'azione richiesta. Il tuo abbonamento si rinnoverà automaticamente il {{ next_billing_date|date:"F d, Y" }}.

Hai bisogno di aggiornare il metodo di pagamento o apportare modifiche? Visita il dashboard del tuo account.

Gestisci l'abbonamento: {{ manage_subscription_url }}
Aggiorna il metodo di pagamento: {{ update_payment_url }}

Hai bisogno di aiuto? Contattaci a {{ support_email }}

---
Powered by Spwig - https://spwig.com
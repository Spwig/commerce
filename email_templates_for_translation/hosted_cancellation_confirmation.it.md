---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Annullamento confermato - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Annullamento confermato
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          La tua sottoscrizione <strong>{{ plan_name }}</strong> è stata annullata.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Cosa succede adesso
        </mj-text>
        <mj-text font-size="14px">
          Continuerai ad avere accesso completo fino a <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          Dopo tale data, i dati del tuo negozio saranno conservati per 30 giorni fino a <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Se desideri esportare i tuoi dati prima che l'accesso termini, puoi farlo dal pannello di amministrazione. Cambiato idea? Puoi riattivare la tua sottoscrizione in qualsiasi momento.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Annullamento confermato - {{ store_name }}

Ciao {{ name|default:'there' }},

La tua sottoscrizione {{ plan_name }} è stata annullata.

Cosa succede adesso:
- Continuerai ad avere accesso completo fino a {{ access_until_date }}.
- Dopo tale data, i dati del tuo negozio saranno conservati per 30 giorni fino a {{ termination_date }}.

Se desideri esportare i tuoi dati prima che l'accesso termini, puoi farlo dal pannello di amministrazione. Cambiato idea? Puoi riattivare la tua sottoscrizione in qualsiasi momento.

Reactivate Subscription: https://spwig.com/account

Need help? Contact {{ support_email }}
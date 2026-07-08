---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Azione richiesta - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Avviso di sospensione
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Azione richiesta per {{ store_name }}
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
          Il pagamento per <strong>{{ plan_name }}</strong> è in ritardo. Se non risolto entro <strong>{{ grace_end_date }}</strong>, il tuo negozio verrà messo in modalità sola lettura.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Cosa significa la sospensione
        </mj-text>
        <mj-text font-size="14px">
          Se il tuo negozio viene sospeso, rimarrà visibile ai visitatori ma non sarai in grado di apportare modifiche. Le nuove ordinazioni verranno sospese fino al pagamento del saldo rimanente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Per favore aggiorna il tuo metodo di pagamento per evitare qualsiasi interruzione del tuo negozio.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Aggiorna il metodo di pagamento" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Avviso di sospensione - {{ store_name }}

Ciao {{ name|default:'there' }},

Il pagamento per {{ plan_name }} è in ritardo. Se non risolto entro {{ grace_end_date }}, il tuo negozio verrà messo in modalità sola lettura.

Cosa significa la sospensione:
Se il tuo negozio viene sospeso, rimarrà visibile ai visitatori ma non sarai in grado di apportare modifiche. Le nuove ordinazioni verranno sospese fino al pagamento del saldo rimanente.

Per favore aggiorna il tuo metodo di pagamento per evitare qualsiasi interruzione del tuo negozio.

Aggiorna il metodo di pagamento: https://spwig.com/account

Hai bisogno di aiuto? Contatta {{ support_email }}
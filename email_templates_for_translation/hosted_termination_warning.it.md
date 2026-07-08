---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Importante: Eliminazione dei dati in 7 giorni - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Avviso di eliminazione dei dati
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
          Il tuo negozio <strong>{{ store_name }}</strong> e tutti i dati associati saranno eliminati definitivamente il <strong>{{ termination_date }}</strong>. Questa azione non può essere annullata.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Cosa puoi fare
        </mj-text>
        <mj-text font-size="14px">
          Se desideri conservare i tuoi dati, esportali prima di questa data o riacquista l'abbonamento per evitare l'eliminazione.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Riacquista l'abbonamento" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Avviso di eliminazione dei dati - {{ store_name }}

Ciao {{ name|default:'there' }},

Il tuo negozio {{ store_name }} e tutti i dati associati saranno eliminati definitivamente il {{ termination_date }}. Questa azione non può essere annullata.

Cosa puoi fare:
Se desideri conservare i tuoi dati, esportali prima di questa data o riacquista l'abbonamento per evitare l'eliminazione.

Riacquista l'abbonamento: https://spwig.com/account

Hai bisogno di aiuto? Contatta {{ support_email }}
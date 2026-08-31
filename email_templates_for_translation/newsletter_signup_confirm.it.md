---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Conferma la tua iscrizione a {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Conferma la tua iscrizione
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grazie per veder ti iscrivere a {{ store_name }}! Per favore conferma il tuo indirizzo email per iniziare a ricevere i nostri aggiornamenti e offerte.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Conferma l'iscrizione
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Non puoi cliccare sul pulsante? Copia e incolla questo collegamento nel tuo browser:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Perché confermare?</strong><br/>
          Confermare la tua email ci aiuta a verificare che tu voglia davvero i nostri aggiornamenti, e mantiene la tua casella email libera da spam.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Non ti sei iscritto? Puoi tranquillamente ignorare questa email.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Conferma la tua iscrizione a {{ store_name }}

Grazie per averti iscritto a {{ store_name }}! Per favore conferma il tuo indirizzo email per iniziare a ricevere i nostri aggiornamenti e offerte:

{{ confirmation_url }}

Confermare la tua email ci aiuta a verificare che tu voglia davvero i nostri aggiornamenti, e mantiene la tua casella email libera da spam.

Non ti sei iscritto? Puoi tranquillamente ignorare questa email.
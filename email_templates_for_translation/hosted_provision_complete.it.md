---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Il tuo negozio è pronto - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Il tuo negozio è online!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} è pronto per te
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
          Buone notizie! Il tuo negozio Spwig <strong>{{ store_name }}</strong> è stato configurato e ora è online. Puoi iniziare a impostare i tuoi prodotti, la tua branding e i metodi di pagamento subito.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Dettagli del tuo negozio
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          URL del negozio: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Pannello di amministrazione: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Regione: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Avvio rapido
        </mj-text>
        <mj-text font-size="14px">
          1. Accedi al pannello di amministrazione utilizzando l'email e la password che hai impostato durante il checkout
        </mj-text>
        <mj-text font-size="14px">
          2. Aggiungi il logo del tuo negozio e la tua branding sotto Design > Impostazioni del tema
        </mj-text>
        <mj-text font-size="14px">
          3. Aggiungi i tuoi primi prodotti sotto Catalogo > Prodotti
        </mj-text>
        <mj-text font-size="14px">
          4. Configura un fornitore di pagamento sotto Impostazioni > Fornitori di pagamento
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Vai al pannello di amministrazione" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Il tuo negozio è online!

{{ store_name }} è pronto per te.

Ciao {{ name|default:'there' }},

Buone notizie! Il tuo negozio Spwig {{ store_name }} è stato configurato e ora è online. Puoi iniziare a impostare i tuoi prodotti, la tua branding e i metodi di pagamento subito.

Dettagli del tuo negozio:
- URL del negozio: {{ store_url }}
- Pannello di amministrazione: {{ admin_url }}
- Regione: {{ region }}

Avvio rapido:
1. Accedi al pannello di amministrazione utilizzando l'email e la password che hai impostato durante il checkout
2. Aggiungi il logo del tuo negozio e la tua branding sotto Design > Impostazioni del tema
3. Aggiungi i tuoi primi prodotti sotto Catalogo > Prodotti
4. Configura un fornitore di pagamento sotto Impostazioni > Fornitori di pagamento

Vai al pannello di amministrazione: {{ admin_url }}

Hai bisogno di aiuto? Contatta {{ support_email }}
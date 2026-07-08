---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Consigli per Ottenere il Massimo da {{ store_name }}

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
          Consigli per Iniziare
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Ottenere il massimo dal tuo negozio Spwig
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
          Ora che <strong>{{ store_name }}</strong> è attivo, ecco alcuni consigli per aiutarti a ottenere il massimo dal tuo negozio.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Personalizza l'Aspetto
        </mj-text>
        <mj-text font-size="14px">
          Visita <strong>Design > Impostazioni del tema</strong> per scegliere un tema, caricare il tuo logo e impostare i colori del tuo brand. Il tuo negozio si aggiorna immediatamente in modo da poter visualizzare i cambiamenti in tempo reale.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Aggiungi i Tuoi Prodotti
        </mj-text>
        <mj-text font-size="14px">
          Vai a <strong>Catalogo > Prodotti</strong> per iniziare ad aggiungere i tuoi articoli. Puoi creare varianti di prodotto (taglia, colore), impostare i prezzi, gestire l'inventario e caricare immagini di alta qualità.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configura i Pagamenti
        </mj-text>
        <mj-text font-size="14px">
          Vai a <strong>Impostazioni > Fornitori di Pagamento</strong> per collegare Stripe, PayPal o un altro metodo di pagamento. Puoi abilitare diversi fornitori in modo che i tuoi clienti possano pagare come preferiscono.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configura la Consegna
        </mj-text>
        <mj-text font-size="14px">
          In <strong>Impostazioni > Consegna</strong>, configura le tue aree di consegna e le tariffe. Puoi creare regole per consegne a prezzo fisso, basate sul peso o gratuite per diverse regioni.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Migliora il Tuo SEO
        </mj-text>
        <mj-text font-size="14px">
          Spwig genera automaticamente mappe del sito e tag meta. Visita <strong>Impostazioni > SEO</strong> per personalizzare i titoli delle pagine, le descrizioni e le immagini per il condivisione sociale in modo da aiutare i clienti a trovare il tuo negozio.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Vai al Pannello di Amministrazione" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Consigli per Iniziare - {{ store_name }}

Ciao {{ name|default:'there' }},

Ora che {{ store_name }} è attivo, ecco alcuni consigli per aiutarti a ottenere il massimo dal tuo negozio.

1. Personalizza l'Aspetto
Visita Design > Impostazioni del tema per scegliere un tema, caricare il tuo logo e impostare i colori del tuo brand.

2. Aggiungi i Tuoi Prodotti
Vai a Catalogo > Prodotti per iniziare ad aggiungere i tuoi articoli con varianti, prezzi e immagini.

3. Configura i Pagamenti
Vai a Impostazioni > Fornitori di Pagamento per collegare Stripe, PayPal o un altro metodo di pagamento.

4. Configura la Consegna
In Impostazioni > Consegna, configura le tue aree di consegna e le tariffe per diverse regioni.

5. Migliora il Tuo SEO
Visita Impostazioni > SEO per personalizzare i titoli delle pagine, le descrizioni e le immagini per il condivisione sociale in modo da aiutare i clienti a trovare il tuo negozio.

Vai al Pannello di Amministrazione: {{ admin_url }}

Hai bisogno di aiuto? Contatta {{ support_email }}
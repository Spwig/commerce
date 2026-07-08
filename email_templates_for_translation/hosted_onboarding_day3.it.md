---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
Costruisci il tuo catalogo - {{ store_name }}

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
          Getting Started: Your Products
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Build a great catalog for {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Your store <strong>{{ store_name }}</strong> is all set up. Now it's time to build your product catalog. Here are five tips to get you started.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Importa prodotti da CSV
        </mj-text>
        <mj-text font-size="14px">
          Hai già una lista di prodotti? Vai a <strong>Admin > Catalogo > Importa</strong> per importare in blocco i tuoi prodotti da un file CSV. Questo è il modo più veloce per popolare il tuo negozio.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Organizza con categorie e filtri
        </mj-text>
        <mj-text font-size="14px">
          Crea categorie e filtri per attributi in modo che i clienti possano navigare facilmente e trovare ciò di cui hanno bisogno. I cataloghi ben organizzati portano a tassi di conversione più elevati.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Scrivi descrizioni dei prodotti convincenti
        </mj-text>
        <mj-text font-size="14px">
          Le descrizioni eccellenti vendono prodotti. Concentrati sui benefici, non solo sulle caratteristiche. Spiega ai clienti perché hanno bisogno del tuo prodotto e come risolve il loro problema.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Carica immagini di alta qualità dei prodotti
        </mj-text>
        <mj-text font-size="14px">
          Le immagini chiare e professionali fanno una grande differenza. Carica diversi angoli e usa un'illuminazione coerente. Spwig ottimizza automaticamente le immagini per un caricamento rapido.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Crea varianti dei prodotti
        </mj-text>
        <mj-text font-size="14px">
          Se i tuoi prodotti sono disponibili in diverse dimensioni, colori o stili, crea varianti in modo che i clienti possano selezionare esattamente ciò di cui hanno bisogno. Ogni variante può avere il proprio prezzo, livello di scorta e immagini.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Gestisci i tuoi prodotti" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Getting Started: Your Products - {{ store_name }}

Hi {{ name|default:'there' }},

Your store {{ store_name }} is all set up. Now it's time to build your product catalog. Here are five tips to get you started.

1. Import Products from CSV
Already have a product list? Head to Admin > Catalog > Import to bulk-import your products from a CSV file.

2. Organise with Categories and Filters
Create categories and attribute filters so customers can easily browse and find what they're looking for.

3. Write Compelling Product Descriptions
Great descriptions sell products. Focus on benefits, not just features. Tell customers why they need your product.

4. Upload High-Quality Product Images
Clear, professional images make a huge difference. Upload multiple angles and use consistent lighting.

5. Set Up Product Variants
If your products come in different sizes, colours, or styles, create variants so customers can select exactly what they want.

Manage Your Products: {{ admin_url }}

Need help? Contact {{ support_email }}
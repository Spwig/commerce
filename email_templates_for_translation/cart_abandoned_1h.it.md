---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
Il tuo carrello aspetta! Completa l'ordine - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hai lasciato {{ cart_item_count }} articolo{{ cart_item_count|pluralize }} nel tuo carrello
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Abbiamo notato che non hai completato l'acquisto. I tuoi articoli aspettano ancora nel tuo carrello!
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Totale: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Completa l'ordine
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Hai bisogno di aiuto? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contatta il nostro team di supporto</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hai lasciato {{ cart_item_count }} articolo{{ cart_item_count|pluralize }} nel tuo carrello

Ciao {{ customer_name }},

Abbiamo notato che non hai completato l'acquisto. I tuoi articoli aspettano ancora nel tuo carrello!

IL TUO CARRELLO:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

Totale: {{ cart_total }}

Completa l'ordine: {{ cart_url }}

Hai bisogno di aiuto? Contatta il nostro team di supporto: {{ support_url }}

---
Hai ricevuto questa email perché hai aggiunto degli articoli al tuo carrello su {{ shop_name }}.
Per smettere di ricevere i promemoria del carrello, visita: {{ preferences_url }}
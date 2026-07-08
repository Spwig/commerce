---
template_type: back_in_stock
category: Inventory
---

# Email Template: back_in_stock

## Subject
{{ product_name }} ¡Vuelve al stock! - {{ shop_name }}

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.success|default:'#10b981' }}" align="center">
          ¡Buena noticia!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Un artículo de tu lista de deseos vuelve al stock
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column width="40%">
        {% if product_image_url %}
        <mj-image src="{{ product_image_url }}" alt="{{ product_name }}" border-radius="8px" />
        {% else %}
        <mj-image src="{{ shop_url }}/static/img/placeholder-product.png" alt="{{ product_name }}" border-radius="8px" />
        {% endif %}
      </mj-column>
      <mj-column width="60%">
        <mj-text font-size="22px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          {{ product_name }}
        </mj-text>
        {% if variant_name %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-bottom="12px">
          {{ variant_name }}
        </mj-text>
        {% endif %}
        <mj-text font-size="16px" color="{{ theme.color.success|default:'#10b981' }}" font-weight="600" padding-bottom="16px">
          <span style="display: inline-flex; align-items: center;">
            <span style="width: 8px; height: 8px; background-color: {{ theme.color.success|default:'#10b981' }}; border-radius: 50%; margin-right: 8px; display: inline-block;"/>
            En stock
          </span>
        </mj-text>
        <mj-button href="{{ product_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 28px">
          Comprar ahora
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Urgency Message -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e" align="center">
          <strong>¡No te lo pierdas!</strong> Los artículos populares se agotan rápido - asegura el tuyo antes de que se vuelva a agotar.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Browse More -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Continúa navegando por nuestros últimos productos
        </mj-text>
        <mj-button href="{{ shop_url }}" background-color="transparent" color="{{ theme.color.info|default:'#3b82f6' }}" font-size="14px" border="1px solid {{ theme.color.info|default:'#3b82f6' }}" border-radius="6px" padding="12px 24px">
          Visita nuestra tienda
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Unsubscribe Note -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="11px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" line-height="1.5">
          Recibiste este correo porque te registraste para recibir notificaciones cuando este producto estuviera disponible.
          Esta es una notificación única - no recibirás más correos sobre este producto.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          ¿Necesitas ayuda? Contáctanos en {{ support_email }}
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
¡Buena noticia! {{ product_name }} vuelve al stock.

Nos alegramos de informarte que {{ product_name }} vuelve al stock.

DETALLES DEL PRODUCTO:
{{ product_name }}{% if variant_name %}
Variante: {{ variant_name }}{% endif %}

Estado: En stock

Comprar ahora:
{{ product_url }}

¡No te lo pierdas! Los artículos populares se agotan rápido - asegura el tuyo antes de que se vuelva a agotar.

---

Continúa navegando por nuestros últimos productos:
{{ shop_url }}

---

Recibiste este correo porque te registraste para recibir notificaciones cuando este producto estuviera disponible.
Esta es una notificación única - no recibirás más correos sobre este producto.

¿Necesitas ayuda? Contáctanos en {{ support_email }}

---

Powered by Spwig - https://spwig.com
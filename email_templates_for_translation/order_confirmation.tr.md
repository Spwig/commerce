---
template_type: order_confirmation
category: Core E-commerce
---

# Email Template: order_confirmation

## Subject
Sipariş Onayı #{{ order_number }} - Teşekkür Ederiz!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Siparişiniz İçin Teşekkür Ederiz!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Sipariş #{{ order_number }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ order_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Timeline -->
    {% include 'email_system/mjml_components/order_timeline.mjml' with stages=timeline_stages %}

    <!-- Order Items -->
    {% include 'email_system/mjml_components/order_items_table.mjml' with items=items %}

    <!-- Payment Summary -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        {% include 'email_system/mjml_components/payment_summary.mjml' with subtotal=subtotal shipping=shipping tax=tax total=total %}
      </mj-column>
    </mj-section>

    <!-- Delivery Estimate -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          <strong>Tahmini Teslimat:</strong> {{ estimated_delivery_start }} - {{ estimated_delivery_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Shipping Address -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        {% include 'email_system/mjml_components/address_block.mjml' with address=shipping_address title="Shipping Address" %}
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=order_url text="View Order Status" %}

    {% if activation_url %}
    <!-- Guest Account Creation CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Hesap Oluşturun
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Siparişlerinizi izleyin, bir sonraki alışverişinizi daha hızlı yapın ve tercihlerinizi yönetin.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Siparişiniz İçin Teşekkür Ederiz!

Sipariş #{{ order_number }}
{{ order_date }}

Tahmini Teslimat: {{ estimated_delivery_start }} - {{ estimated_delivery_end }}

Sipariş Öğeleri:
{% for item in items %}
- {{ item.name }} (Adet: {{ item.quantity }}) - {{ item.subtotal }}
{% endfor %}

Ara Toplam: {{ subtotal }}
Kargo: {{ shipping }}
Vergi: {{ tax }}
Toplam: {{ total }}

Kargo Adresi:
{{ shipping_address.full_address }}

Sipariş durumunu görüntüleyin: {{ order_url }}
{% if activation_url %}

Hesap Oluşturun
Siparişlerinizi izleyin, bir sonraki alışverişinizi daha hızlı yapın ve tercihlerinizi yönetin.
Hesap oluşturun: {{ activation_url }}
{% endif %}

Yardıma mı ihtiyacınız var?
E-posta: {{ support_email }}
Telefon: {{ support_phone }}
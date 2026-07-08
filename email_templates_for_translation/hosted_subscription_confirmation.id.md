---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
Langganan Dikonfirmasi - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Langganan Dikonfirmasi!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Selamat datang di Spwig
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hai {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Terima kasih telah berlangganan! Langganan <strong>{{ plan_name }}</strong> Anda untuk <strong>{{ store_name }}</strong> telah dikonfirmasi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detail Langganan
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Interval Pembayaran: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Jumlah: {{ currency }}{{ amount }}{% if intro_period %} (tarif pengenalan){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          Tarif pengenalan Anda berlaku selama {{ intro_period }}. Setelah itu, langganan Anda akan diperbarui pada {{ currency }}{{ full_amount }}/{{ billing_interval }}.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          Toko Anda sedang disiapkan dan Anda akan menerima email lain saat siap.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          Tanggal pembayaran berikutnya: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Langganan Dikonfirmasi!

Hai {{ name|default:'there' }},

Terima kasih telah berlangganan! Langganan {{ plan_name }} Anda untuk {{ store_name }} telah dikonfirmasi.

Detail Langganan:
- Plan: {{ plan_name }}
- Interval Pembayaran: {{ billing_interval }}
- Jumlah: {{ currency }}{{ amount }}{% if intro_period %} (tarif pengenalan){% endif %}
{% if intro_period %}
Ini adalah tarif pengenalan Anda selama {{ intro_period }}. Setelah itu, langganan Anda akan diperbarui pada {{ currency }}{{ full_amount }}/{{ billing_interval }}.
{% endif %}
Toko Anda sedang disiapkan dan Anda akan menerima email lain saat siap.

Tanggal pembayaran berikutnya: {{ next_billing_date }}

Butuh bantuan? Hubungi {{ support_email }}
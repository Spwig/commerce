---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Peringatan Penangguhan - {{ store_name }}

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
          Peringatan Penangguhan
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Tindakan diperlukan untuk {{ store_name }}
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
          Pembayaran Anda untuk <strong>{{ plan_name }}</strong> sudah terlambat. Jika tidak segera diselesaikan sebelum <strong>{{ grace_end_date }}</strong>, toko Anda akan ditempatkan dalam mode hanya baca.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Apa Arti Penangguhan
        </mj-text>
        <mj-text font-size="14px">
          Jika toko Anda ditangguhkan, toko tersebut tetap akan terlihat oleh pengunjung, tetapi Anda tidak akan dapat membuat perubahan. Pesanan baru akan dihentikan sampai utang Anda selesai dibayar.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Silakan perbarui metode pembayaran Anda untuk menghindari gangguan pada toko Anda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Perbarui Metode Pembayaran" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Peringatan Penangguhan - {{ store_name }}

Hai {{ name|default:'there' }},

Pembayaran Anda untuk {{ plan_name }} sudah terlambat. Jika tidak segera diselesaikan sebelum {{ grace_end_date }}, toko Anda akan ditempatkan dalam mode hanya baca.

Apa Arti Penangguhan:
Jika toko Anda ditangguhkan, toko tersebut tetap akan terlihat oleh pengunjung, tetapi Anda tidak akan dapat membuat perubahan. Pesanan baru akan dihentikan sampai utang Anda selesai dibayar.

Silakan perbarui metode pembayaran Anda untuk menghindari gangguan pada toko Anda.

Perbarui Metode Pembayaran: https://spwig.com/account

Butuh bantuan? Hubungi {{ support_email }}
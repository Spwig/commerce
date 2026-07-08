---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
Selamat Kembali! {{ store_name }} Kembali Aktif

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
          Selamat Kembali!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} Kembali Aktif
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi there,
        </mj-text>
        <mj-text>
          Berita baik! Toko <strong>{{ store_name }}</strong> Anda telah diaktifkan kembali. Langganan <strong>{{ plan_name }}</strong> Anda sekarang aktif dan toko Anda kembali online.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detail Pembaruan Aktivasi
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Pembayaran yang Diproses: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tanggal Tagihan Berikutnya: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          Toko Anda kembali online sekarang. Mungkin membutuhkan beberapa menit agar semuanya pulih sepenuhnya. Setelah online, toko Anda akan dapat diakses di {{ store_url }}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Selamat Kembali! {{ store_name }} Kembali Aktif

Hi there,

Berita baik! Toko {{ store_name }} Anda telah diaktifkan kembali. Langganan {{ plan_name }} Anda sekarang aktif dan toko Anda kembali online.

Detail Pembaruan Aktivasi:
- Plan: {{ plan_name }}
- Pembayaran yang Diproses: {{ currency }}{{ amount }}
- Tanggal Tagihan Berikutnya: {{ next_billing_date }}

Toko Anda kembali online sekarang. Mungkin membutuhkan beberapa menit agar semuanya pulih sepenuhnya. Setelah online, toko Anda akan dapat diakses di {{ store_url }}.

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}
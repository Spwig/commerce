---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
Toko Dihapus - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Toko Dihapus
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          Toko Anda <strong>{{ store_name }}</strong> telah dihapus secara permanen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Backup Data
        </mj-text>
        <mj-text font-size="14px">
          Backup data Anda akan tersedia selama 90 hari setelah diminta. Hubungi <strong>support@spwig.com</strong> jika Anda memerlukan ekspor data.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Terima kasih telah menjadi pelanggan Spwig. Kami berharap melihat Anda kembali di masa depan.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Toko Dihapus - {{ store_name }}

Hai {{ name|default:'there' }},

Toko Anda {{ store_name }} telah dihapus secara permanen.

Backup Data:
Backup data Anda akan tersedia selama 90 hari setelah diminta. Hubungi support@spwig.com jika Anda memerlukan ekspor data.

Terima kasih telah menjadi pelanggan Spwig. Kami berharap melihat Anda kembali di masa depan.

Butuh bantuan? Hubungi {{ support_email }}
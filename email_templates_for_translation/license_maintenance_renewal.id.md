---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Perpanjangan Pemeliharaan - Pesanan #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Perpanjangan Pemeliharaan!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Pesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hai {{ customer_name }},
        </mj-text>
        <mj-text>
          Langganan pemeliharaan Spwig Anda telah berhasil diperpanjang. Anda akan terus menerima pembaruan platform, perbaikan keamanan, dan fitur baru.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ringkasan Perpanjangan
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Kunci Lisensi: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Pemeliharaan Berlaku Sampai: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Nomor Pesanan: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Apa yang Termasuk
        </mj-text>
        <mj-text font-size="14px">
          Langganan pemeliharaan aktif Anda memberi Anda akses ke:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Pembaruan fitur dan peningkatan platform
        </mj-text>
        <mj-text font-size="14px">
          - Perbaikan keamanan dan bug
        </mj-text>
        <mj-text font-size="14px">
          - Rilis komponen baru melalui server upgrade
        </mj-text>
        <mj-text font-size="14px">
          - Dukungan teknis
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tidak ada tindakan yang diperlukan dari Anda. Pembaruan akan terus tersedia melalui sistem pembaruan komponen di panel administrasi Anda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Perpanjangan Pemeliharaan!

Pesanan #{{ order_number }}

Hai {{ customer_name }},

Langganan pemeliharaan Spwig Anda telah berhasil diperpanjang. Anda akan terus menerima pembaruan platform, perbaikan keamanan, dan fitur baru.

Ringkasan Perpanjangan:
- Kunci Lisensi: {{ license_key }}
- Pemeliharaan Berlaku Sampai: {{ renewal_expires_at }}
- Nomor Pesanan: {{ order_number }}

Apa yang Termasuk:
- Pembaruan fitur dan peningkatan platform
- Perbaikan keamanan dan bug
- Rilis komponen baru melalui server upgrade
- Dukungan teknis

Tidak ada tindakan yang diperlukan dari Anda. Pembaruan akan terus tersedia melalui sistem pembaruan komponen di panel administrasi Anda.

Butuh bantuan? Hubungi {{ support_email }}
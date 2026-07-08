---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
Tautan Unduh Kadaluarsa - Pesanan #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Tautan Unduh Kadaluarsa
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hai {{ customer_name }},
        </mj-text>
        <mj-text>
          Tautan unduh untuk <strong>{{ product_name }}</strong> dari pesanan #{{ order_number }} telah kadaluarsa.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          Tautan unduh kadaluarsa {{ expiration_days }} hari setelah pembelian karena alasan keamanan.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Butuh tautan unduh baru?
        </mj-text>
        <mj-text>
          Anda dapat meminta tautan unduh baru dengan masuk ke akun Anda atau menghubungi tim dukungan kami.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Ke Akun Saya
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Pertanyaan? Hubungi {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Tautan Unduh Kadaluarsa

Hai {{ customer_name }},

Tautan unduh untuk {{ product_name }} dari pesanan #{{ order_number }} telah kadaluarsa.

Tautan unduh kadaluarsa {{ expiration_days }} hari setelah pembelian karena alasan keamanan.

Butuh tautan unduh baru?
Anda dapat meminta tautan unduh baru dengan masuk ke akun Anda atau menghubungi tim dukungan kami.

Ke Akun Saya: {{ account_url }}

Pertanyaan? Hubungi {{ support_email }}
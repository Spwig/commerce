---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
Selamat datang kembali! Akun telah diaktifkan kembali

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          🎉 Akun Telah Diaktifkan Kembali!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Selamat Kembali!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Akun afiliasi Anda kembali aktif
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Halo {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Berita baik! Akun afiliasi Anda dengan {{ shop_name }} telah diaktifkan kembali.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Anda dapat melanjutkan mempromosikan produk kami dan mulai menerima komisi segera.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Akses Panel Afiliasi
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Pertanyaan? <a href="mailto:{{ support_email }}" style="color: #007bff;">Hubungi Dukungan</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Selamat datang kembali! Akun telah diaktifkan kembali

Halo {{ affiliate_name }},

Berita baik! Akun afiliasi Anda dengan {{ shop_name }} telah diaktifkan kembali.

Anda dapat melanjutkan mempromosikan produk kami dan mulai menerima komisi segera.

Akses panel afiliasi Anda: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}
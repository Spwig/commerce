---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Penting: Akun Dijeda

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          Akun Dijeda
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
          Akun afiliasi Anda dengan {{ shop_name }} telah dijeda.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ini biasanya disebabkan oleh pelanggaran terhadap ketentuan program afiliasi kami.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Jika Anda percaya ini adalah kesalahan atau ingin membicarakan keputusan ini, silakan hubungi tim dukungan kami.
        </mj-text>
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
Penting: Akun Dijeda

Halo {{ affiliate_name }},

Akun afiliasi Anda dengan {{ shop_name }} telah dijeda.

Ini biasanya disebabkan oleh pelanggaran terhadap ketentuan program afiliasi kami.

Jika Anda percaya ini adalah kesalahan atau ingin membicarakan keputusan ini, silakan hubungi tim dukungan kami.

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}
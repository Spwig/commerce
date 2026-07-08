---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Pembaruan Pendaftaran Program

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
          Pembaruan Aplikasi
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hai {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Terima kasih telah mendaftar untuk mempromosikan {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Setelah meninjau aplikasi Anda, kami memutuskan untuk tidak menyetujui pada saat ini.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Anda masih dapat mempromosikan program lain dalam jaringan afiliasi kami.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Lihat Program Lain
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
Pembaruan Pendaftaran Program

Hai {{ affiliate_name }},

Terima kasih telah mendaftar untuk mempromosikan {{ program_name }}.

Setelah meninjau aplikasi Anda, kami memutuskan untuk tidak menyetujui pada saat ini.

Anda masih dapat mempromosikan program lain dalam jaringan afiliasi kami.

Lihat program lain: {{ portal_url }}

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}
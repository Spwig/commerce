---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Tindakan Diperlukan - Masalah Pengaturan Toko untuk {{ store_name }}

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Masalah Pengaturan Toko
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
          Kami menemui masalah saat mengatur toko Anda <strong>{{ store_name }}</strong>. Tim kami telah diberitahu dan sedang menanganinya.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          Apa yang terjadi
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Apa yang akan terjadi selanjutnya?
        </mj-text>
        <mj-text font-size="14px">
          Tim dukungan kami telah secara otomatis diberitahu mengenai masalah ini. Anda tidak perlu melakukan tindakan apa pun - kami akan menghubungi Anda setelah masalah ini selesai.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Jika Anda memiliki pertanyaan dalam waktu dekat, jangan ragu untuk menghubungi kami.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Masalah Pengaturan Toko - {{ store_name }}

Hai {{ name|default:'there' }},

Kami menemui masalah saat mengatur toko Anda {{ store_name }}. Tim kami telah diberitahu dan sedang menanganinya.

Apa yang terjadi:
{{ provision_error }}

Apa yang akan terjadi selanjutnya?
Tim dukungan kami telah secara otomatis diberitahu mengenai masalah ini. Anda tidak perlu melakukan tindakan apa pun - kami akan menghubungi Anda setelah masalah ini selesai.

Jika Anda memiliki pertanyaan dalam waktu dekat, jangan ragu untuk menghubungi kami.

Butuh bantuan? Hubungi {{ support_email }}
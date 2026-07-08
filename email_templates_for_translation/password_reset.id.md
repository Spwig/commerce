---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Permintaan Atur Ulang Kata Sandi

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Permintaan Atur Ulang Kata Sandi
        </mj-text>
        <mj-text>
          Kami menerima permintaan untuk mengatur ulang kata sandi Anda. Klik tombol di bawah untuk mengatur ulangnya.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Atur Ulang Kata Sandi
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Jika Anda tidak meminta ini, Anda dapat aman mengabaikan email ini.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          Tautan ini akan kedaluwarsa dalam {{ expiry_hours }} jam.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Permintaan Atur Ulang Kata Sandi

Kami menerima permintaan untuk mengatur ulang kata sandi Anda. Klik tautan di bawah untuk mengatur ulangnya.

{{ reset_url }}

Jika Anda tidak meminta ini, Anda dapat aman mengabaikan email ini.
Tautan ini akan kedaluwarsa dalam {{ expiry_hours }} jam.
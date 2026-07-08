---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Şifre Sıfırlama Talebi

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Şifre Sıfırlama Talebi
        </mj-text>
        <mj-text>
          Şifrenizi sıfırlamak için bir talep aldık. Sıfırlamak için aşağıdaki düğmeye tıklayın.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Şifreyi Sıfırla
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Bu talebi talep etmediyseniz, bu e-postayı güvenle ihmal edebilirsiniz.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          Bu bağlantı {{ expiry_hours }} saat sonra sona erecek.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Şifre Sıfırlama Talebi

Şifrenizi sıfırlamak için bir talep aldık. Sıfırlamak için aşağıdaki bağlantıyı tıklayın.

{{ reset_url }}

Bu talebi talep etmediyseniz, bu e-postayı güvenle ihmal edebilirsiniz.
Bu bağlantı {{ expiry_hours }} saat sonra sona erecek.
---
template_type: subscription_payment_failed
category: Subscriptions
---

# Email Template: subscription_payment_failed

## Subject
⚠️ Pembayaran Gagal untuk {{ plan_name }} - Tindakan Diperlukan - {{ shop_name }}

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
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⚠️ Pembayaran Gagal
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Kami tidak dapat memproses pembayaran Anda
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Gagal Pembayaran Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fef2f2" padding="30px" border="2px solid {{ theme.color.error|default:'#ef4444' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#7f1d1d" align="center" padding-bottom="15px">
                Informasi Pembayaran
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Plan:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Jumlah:</strong> {{ subscription_amount }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Cara Pembayaran:</strong> {{ payment_method }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" padding="5px 0">
                <strong>Alasan:</strong> {{ failure_reason }}
              </mj-text>

              <mj-divider border-color="#fecaca" border-width="1px" padding="15px 0" />

              {% if retry_date %}
              <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" padding="5px 0" font-weight="600">
                Harap perbarui metode pembayaran Anda pada {{ retry_date|date:"F d, Y" }} untuk menghindari gangguan layanan.
              </mj-text>
              {% endif %}
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- Bagian Apa yang Harus Dilakukan -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Apa yang Harus Anda Lakukan?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size="18px" margin-right: 8px;">1.</span>
          Pastikan metode pembayaran Anda memiliki dana yang cukup
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size="18px" margin-right: 8px;">2.</span>
          Perbarui metode pembayaran Anda jika kartu telah kedaluwarsa
        </mj-text>

        {% if retry_days %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size="18px" margin-right: 8px;">3.</span>
          Kami akan mencoba kembali pembayaran secara otomatis dalam {{ retry_days }} hari
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Tombol CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ update_payment_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Perbarui Metode Pembayaran
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ manage_subscription_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            Lihat Langganan
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Blok Bantuan -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Butuh bantuan? Hubungi kami di {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer Branding Spwig -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Dikembangkan oleh Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ Pembayaran Gagal

Kami tidak dapat memproses pembayaran Anda

INFORMASI PEMBAYARAN:
Plan: {{ plan_name }}
Jumlah: {{ subscription_amount }}
Cara Pembayaran: {{ payment_method }}
Alasan: {{ failure_reason }}

{% if retry_date %}Harap perbarui metode pembayaran Anda pada {{ retry_date|date:"F d, Y" }} untuk menghindari gangguan layanan.{% endif %}

Apa yang Harus Anda Lakukan?
1. Pastikan metode pembayaran Anda memiliki dana yang cukup
2. Perbarui metode pembayaran Anda jika kartu telah kedaluwarsa
{% if retry_days %}3. Kami akan mencoba kembali pembayaran secara otomatis dalam {{ retry_days }} hari{% endif %}

Perbarui Metode Pembayaran: {{ update_payment_url }}
Lihat Langganan: {{ manage_subscription_url }}

Butuh bantuan? Hubungi kami di {{ support_email }}

---
Dikembangkan oleh Spwig - https://spwig.com
---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Pembaruan Gagal: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Pembaruan Gagal
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kesalahan Pemasangan
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Pembaruan untuk {{ component_name }} ke versi {{ target_version }} gagal dipasang.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Kegagalan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Komponen:</strong> {{ component_name }}<br/>
              <strong>Versi Target:</strong> {{ target_version }}<br/>
              <strong>Gagal Pada:</strong> {{ failed_at }}<br/>
              <strong>Kode Kesalahan:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pesan Kesalahan:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Log Kesalahan Lengkap:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang Harus Dilakukan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Periksa persyaratan sistem dan ketergantungan<br/>
          2. Periksa log kesalahan untuk detail<br/>
          3. Coba memasang kembali, atau hubungi dukungan<br/>
          4. Toko Anda masih berjalan di {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Coba Pemasangan Kembali
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Hubungi Dukungan
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ PEMBARUAN GAGAL

Kesalahan Pemasangan

Pembaruan untuk {{ component_name }} ke versi {{ target_version }} gagal dipasang.

DETAIL KEGAGALAN:
- Komponen: {{ component_name }}
- Versi Target: {{ target_version }}
- Gagal Pada: {{ failed_at }}
- Kode Kesalahan: {{ error_code }}

PESAN KESALAHAN:
{{ error_message }}

{% if error_log %}
LOG KESALAHAN LENGKAP:
{{ error_log|truncatewords:50 }}
{% endif %}

APA YANG HARUS DILAKUKAN:
1. Periksa persyaratan sistem dan ketergantungan
2. Periksa log kesalahan untuk detail
3. Coba memasang kembali, atau hubungi dukungan
4. Toko Anda masih berjalan di {{ current_version }}

Ulangi pemasangan: {{ retry_url }}
Hubungi dukungan: {{ support_url }}
---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ Sinkronisasi {{ feed_name }} ke {{ platform_name }} gagal

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Sinkronisasi Gagal
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kesalahan Sinkronisasi
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Gagal sinkronisasi {{ feed_name }} ke {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Kegagalan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Penyebab Umum:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Kredensial API tidak valid atau token telah kedaluwarsa<br/>
          • Masalah koneksi jaringan<br/>
          • Batas kecepatan API platform telah terlampaui<br/>
          • Format feed tidak memenuhi persyaratan platform
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Tindakan yang Direkomendasikan
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Coba Sinkronisasi Lagi
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Periksa Pengaturan Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ SINKRONISASI GAGAL

Kesalahan Sinkronisasi

Gagal sinkronisasi {{ feed_name }} ke {{ platform_name }}.

DETAIL KEGAGALAN:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Gagal Pada: {{ failed_at }}
- Kode Kesalahan: {{ error_code }}

PESAN KESALAHAN:
{{ error_message }}

PENYEBAB UMUM:
• Kredensial API tidak valid atau token telah kedaluwarsa
• Masalah koneksi jaringan
• Batas kecepatan API platform telah terlampaui
• Format feed tidak memenuhi persyaratan platform

{% if recommended_action %}
TINDAKAN YANG DIREKOMENDASIKAN:
{{ recommended_action }}
{% endif %}

Coba sinkronisasi lagi: {{ retry_url }}
Periksa pengaturan feed: {{ admin_feed_url }}
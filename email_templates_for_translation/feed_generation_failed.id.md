---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ Pembuatan Feed Gagal: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Pembuatan Feed Gagal
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kesalahan Pembuatan
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Feed produk {{ feed_name }} gagal dibuat karena terjadi kesalahan.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Kesalahan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
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
          <strong>Log Kesalahan:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:30 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Penyebab Umum:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Data produk yang diperlukan hilang (judul, harga, gambar)<br/>
          • Format data produk tidak valid<br/>
          • Masalah koneksi database<br/>
          • Ruang disk atau memori tidak cukup
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Coba Lagi
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Pengaturan Feed
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Jika masalah ini masih terjadi, hubungi dukungan dengan kode kesalahan {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ PEMBUATAN FEED GAGAL

Kesalahan Pembuatan

Feed produk {{ feed_name }} gagal dibuat karena terjadi kesalahan.

DETAIL KESALAHAN:
- Feed: {{ feed_name }}
- Gagal Pada: {{ failed_at }}
- Kode Kesalahan: {{ error_code }}

PESAN KESALAHAN:
{{ error_message }}

{% if error_log %}
LOG KESALAHAN:
{{ error_log|truncatewords:30 }}
{% endif %}

PENYEBAB UMUM:
• Data produk yang diperlukan hilang (judul, harga, gambar)
• Format data produk tidak valid
• Masalah koneksi database
• Ruang disk atau memori tidak cukup

Ulangi pembuatan: {{ retry_url }}
Lihat pengaturan feed: {{ admin_feed_url }}

Jika masalah ini masih terjadi, hubungi dukungan dengan kode kesalahan {{ error_code }}.
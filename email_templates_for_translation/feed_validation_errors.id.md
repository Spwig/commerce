---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: {{ error_count }} kesalahan validasi ditemukan

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Kesalahan Validasi Feed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Masalah Kualitas Data Terdeteksi
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ error_count }} kesalahan validasi{{ error_count|pluralize }} ditemukan di {{ feed_name }}. Masalah ini dapat mencegah produk muncul di {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Ringkasan Validasi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Validated:</strong> {{ validated_at }}<br/>
              <strong>Total Products:</strong> {{ total_products }}<br/>
              <strong>Products with Errors:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kesalahan Teratas:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} produk{{ error.count|pluralize }} terdampak: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang Perlu Diperbaiki:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Semua Kesalahan
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Kelola Feed
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Perbaiki kesalahan ini untuk memastikan semua produk muncul di {{ platform_name }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ KESALAHAN VALIDASI FEED

Masalah Kualitas Data Terdeteksi

{{ error_count }} kesalahan validasi{{ error_count|pluralize }} ditemukan di {{ feed_name }}. Masalah ini dapat mencegah produk muncul di {{ platform_name }}.

RINGKASAN VALIDASI:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Validated: {{ validated_at }}
- Total Products: {{ total_products }}
- Products with Errors: {{ affected_products }}

TOP ERRORS:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} produk{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

WHAT TO FIX:
{{ fix_instructions }}

Lihat semua kesalahan: {{ errors_url }}
Kelola feed: {{ admin_feed_url }}

Perbaiki kesalahan ini untuk memastikan semua produk muncul di {{ platform_name }}.
---
template_type: feed_sync_success
category: Product Feeds
---

# Email Template: feed_sync_success

## Subject
✓ {{ feed_name }} disinkronkan ke {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Sync Berhasil
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feed Disinkronkan Berhasil
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Feed {{ feed_name }} Anda telah berhasil disinkronkan ke {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Sinkronisasi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Sinkronisasi:</strong> {{ synced_at }}<br/>
              <strong>Produk yang Disinkronkan:</strong> {{ products_synced }}<br/>
              <strong>Durasi:</strong> {{ sync_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ringkasan Perubahan:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% if products_added > 0 %}• {{ products_added }} produk{{ products_added|pluralize }} ditambahkan<br/>{% endif %}
          {% if products_updated > 0 %}• {{ products_updated }} produk{{ products_updated|pluralize }} diperbarui<br/>{% endif %}
          {% if products_removed > 0 %}• {{ products_removed }} produk{{ products_removed|pluralize }} dihapus<br/>{% endif %}
        </mj-text>
        {% endif %}

        {% if sync_warnings %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Peringatan Sinkronisasi
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ sync_warnings }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if platform_url %}
        <mj-button href="{{ platform_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat di {{ platform_name }}
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Detail Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ SYNC SUCCESSFUL

Feed Disinkronkan Berhasil

Feed {{ feed_name }} Anda telah berhasil disinkronkan ke {{ platform_name }}.

SYNC DETAILS:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Synced: {{ synced_at }}
- Products Synced: {{ products_synced }}
- Duration: {{ sync_duration }}

{% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
CHANGES SUMMARY:
{% if products_added > 0 %}• {{ products_added }} produk{{ products_added|pluralize }} ditambahkan{% endif %}
{% if products_updated > 0 %}• {{ products_updated }} produk{{ products_updated|pluralize }} diperbarui{% endif %}
{% if products_removed > 0 %}• {{ products_removed }} produk{{ products_removed|pluralize }} dihapus{% endif %}
{% endif %}

{% if sync_warnings %}
⚠️ SYNC WARNINGS:
{{ sync_warnings }}
{% endif %}

{% if platform_url %}Lihat di {{ platform_name }}: {{ platform_url }}{% endif %}
Lihat detail feed: {{ admin_feed_url }}
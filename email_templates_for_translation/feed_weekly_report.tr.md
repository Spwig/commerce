---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 Haftalık Ürün Besleme Raporu - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Haftalık Besleme Performansı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Besleme Performans Özetİ
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ week_range }} tarihleri arasında ürün beslemenizin nasıl performans gösterdiğini burada görebilirsiniz.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Genel İstatistikler:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Feeds:</strong> {{ total_feeds }}<br/>
              <strong>Active Feeds:</strong> {{ active_feeds }}<br/>
              <strong>Total Syncs:</strong> {{ total_syncs }}<br/>
              <strong>Successful Syncs:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>Failed Syncs:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Besleme Bazlı Performans:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Platform: {{ feed.platform }}<br/>
              Syncs: {{ feed.sync_count }} ({{ feed.success_count }} başarılı)<br/>
              Products: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}Hatalar: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          En Sık Karşılaşılan Sorunlar:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} kez
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}
        {% endif %}

        <mj-spacer height="30px" />

        {% if recommendations %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              💡 Öneriler
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Besleme Panelini Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 HAFTALIK BESLEME PERFORMANSI

Besleme Performans Özetİ

{{ week_range }} tarihleri arasında ürün beslemenizin nasıl performans gösterdiğini burada görebilirsiniz.

GENEL İSTATİSTİKLER:
- Toplam Besleme: {{ total_feeds }}
- Aktif Besleme: {{ active_feeds }}
- Toplam Senkronizasyon: {{ total_syncs }}
- Başarılı Senkronizasyon: {{ successful_syncs }} ({{ success_rate }}%)
- Başarısız Senkronizasyon: {{ failed_syncs }}

BESLEME BAŞLIĞINA GÖRE PERFORMANS:
{% for feed in feed_stats %}
{{ feed.name }}
Platform: {{ feed.platform }}
Senkronizasyon: {{ feed.sync_count }} ({{ feed.success_count }} başarılı)
Ürünler: {{ feed.product_count }}
{% if feed.errors > 0 %}Hatalar: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
EN SIK KARŞILAŞILAN SORUNLAR:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} kez
{% endfor %}
{% endif %}

{% if recommendations %}
💡 ÖNERİLER:
{{ recommendations }}
{% endif %}

Besleme panelini görüntüle: {{ feeds_dashboard_url }}
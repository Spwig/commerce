---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 Еженедельный отчет о продуктах - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Еженедельная производительность фида
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Общая производительность фида
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Вот как ваш фид продуктов работал с {{ week_range }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Общая статистика:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Общее количество фидов:</strong> {{ total_feeds }}<br/>
              <strong>Активные фиды:</strong> {{ active_feeds }}<br/>
              <strong>Общее количество синхронизаций:</strong> {{ total_syncs }}<br/>
              <strong>Успешные синхронизации:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>Неудачные синхронизации:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Производительность фида по отдельности:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Платформа: {{ feed.platform }}<br/>
              Синхронизации: {{ feed.sync_count }} ({{ feed.success_count }} успешных)<br/>
              Продукты: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}Ошибки: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Наиболее распространенные проблемы:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} случаев
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
              💡 Рекомендации
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Посмотреть дашборд фидов
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 ЕЖЕНЕДЕЛЬНАЯ ПРОИЗВОДИТЕЛЬНОСТЬ ФИДА

Общая производительность фида

Вот как ваш фид продуктов работал с {{ week_range }}.

ОБЩАЯ СТАТИСТИКА:
- Общее количество фидов: {{ total_feeds }}
- Активные фиды: {{ active_feeds }}
- Общее количество синхронизаций: {{ total_syncs }}
- Успешные синхронизации: {{ successful_syncs }} ({{ success_rate }}%)
- Неудачные синхронизации: {{ failed_syncs }}

ПРОИЗВОДИТЕЛЬНОСТЬ ФИДА ПО ОТДЕЛЬНОСТИ:
{% for feed in feed_stats %}
{{ feed.name }}
Платформа: {{ feed.platform }}
Синхронизации: {{ feed.sync_count }} ({{ feed.success_count }} успешных)
Продукты: {{ feed.product_count }}
{% if feed.errors > 0 %}Ошибки: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
САМЫЕ ЧАСТЫЕ ПРОБЛЕМЫ:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} случаев
{% endfor %}
{% endif %}

{% if recommendations %}
💡 РЕКОМЕНДАЦИИ:
{{ recommendations }}
{% endif %}

Посмотреть дашборд фидов: {{ feeds_dashboard_url }}
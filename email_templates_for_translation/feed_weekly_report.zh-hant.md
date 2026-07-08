---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 本週產品供應報告 - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 本週供應表現
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          供應表現摘要
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          以下是您在 {{ week_range }} 期間的產品供應表現。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          總體數據：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>總共供應：</strong> {{ total_feeds }}<br/>
              <strong>啟用供應：</strong> {{ active_feeds }}<br/>
              <strong>總共同步：</strong> {{ total_syncs }}<br/>
              <strong>成功同步：</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>失敗同步：</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          每個供應的表現：
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              平台：{{ feed.platform }}<br/>
              同步次數：{{ feed.sync_count }} ({{ feed.success_count }} 次成功)<br/>
              產品數量：{{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}錯誤：{{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          最常見的問題：
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}：</strong> {{ error.count }} 次發生
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
              💡 建議
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看供應儀表板
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 本週供應表現

供應表現摘要

以下是您在 {{ week_range }} 期間的產品供應表現。

總體數據：
- 總共供應：{{ total_feeds }}
- 啟用供應：{{ active_feeds }}
- 總共同步：{{ total_syncs }}
- 成功同步：{{ successful_syncs }} ({{ success_rate }}%)
- 失敗同步：{{ failed_syncs }}

每個供應的表現：
{% for feed in feed_stats %}
{{ feed.name }}
平台：{{ feed.platform }}
同步次數：{{ feed.sync_count }} ({{ feed.success_count }} 次成功)
產品數量：{{ feed.product_count }}
{% if feed.errors > 0 %}錯誤：{{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
最常見的問題：
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} 次發生
{% endfor %}
{% endif %}

{% if recommendations %}
💡 建議：
{{ recommendations }}
{% endif %}

查看供應儀表板：{{ feeds_dashboard_url }}
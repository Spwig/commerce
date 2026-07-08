---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 周产品数据源报告 - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 周数据源性能
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          数据源性能概览
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          这是 {{ week_range }} 期间您的产品数据源的运行情况。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          总体统计：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>总数据源数量：</strong> {{ total_feeds }}<br/>
              <strong>活跃数据源数量：</strong> {{ active_feeds }}<br/>
              <strong>总同步次数：</strong> {{ total_syncs }}<br/>
              <strong>成功同步次数：</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>失败同步次数：</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          按数据源性能分析：
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              平台：{{ feed.platform }}<br/>
              同步次数：{{ feed.sync_count }} ({{ feed.success_count }} 次成功)<br/>
              产品数量：{{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}错误：{{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          最常见问题：
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}：</strong> {{ error.count }} 次出现
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
              💡 建议
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看数据源仪表板
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 周数据源性能

数据源性能概览

这是 {{ week_range }} 期间您的产品数据源的运行情况。

总体统计：
- 总数据源数量：{{ total_feeds }}
- 活跃数据源数量：{{ active_feeds }}
- 总同步次数：{{ total_syncs }}
- 成功同步次数：{{ successful_syncs }} ({{ success_rate }}%)
- 失败同步次数：{{ failed_syncs }}

按数据源性能分析：
{% for feed in feed_stats %}
{{ feed.name }}
平台：{{ feed.platform }}
同步次数：{{ feed.sync_count }} ({{ feed.success_count }} 次成功)
产品数量：{{ feed.product_count }}
{% if feed.errors > 0 %}错误：{{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
最常见问题：
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} 次出现
{% endfor %}
{% endif %}

{% if recommendations %}
💡 建议：
{{ recommendations }}
{% endif %}

查看数据源仪表板：{{ feeds_dashboard_url }}
---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: 发现 {{ error_count }} 个验证错误

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Feed 验证错误
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          检测到数据质量问题
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          在 {{ feed_name }} 中发现 {{ error_count }} 个验证错误。这些问题可能导致产品无法在 {{ platform_name }} 上显示。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              验证摘要：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed：</strong> {{ feed_name }}<br/>
              <strong>平台：</strong> {{ platform_name }}<br/>
              <strong>验证时间：</strong> {{ validated_at }}<br/>
              <strong>总产品数：</strong> {{ total_products }}<br/>
              <strong>有错误的产品数：</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          主要错误：
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} 个产品{{ error.count|pluralize }}受影响：{{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          需要修复的内容：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看所有错误
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          管理 Feed
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          修复这些错误以确保所有产品在 {{ platform_name }} 上显示。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ FEED 验证错误

检测到数据质量问题

在 {{ feed_name }} 中发现 {{ error_count }} 个验证错误。这些问题可能导致产品无法在 {{ platform_name }} 上显示。

验证摘要：
- Feed: {{ feed_name }}
- 平台: {{ platform_name }}
- 验证时间: {{ validated_at }}
- 总产品数: {{ total_products }}
- 有错误的产品数: {{ affected_products }}

主要错误：
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} 个产品{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

需要修复的内容：
{{ fix_instructions }}

查看所有错误: {{ errors_url }}
管理 feed: {{ admin_feed_url }}

修复这些错误以确保所有产品在 {{ platform_name }} 上显示。
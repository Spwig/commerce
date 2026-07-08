---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: {{ error_count }} 件の検証エラーが見つかりました

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ フィード検証エラー
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          データ品質の問題が検出されました
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ feed_name }} で {{ error_count }} 件の検証エラーが見つかりました。これらの問題により、{{ platform_name }} に商品が表示されない可能性があります。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              検証概要:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>フィード:</strong> {{ feed_name }}<br/>
              <strong>プラットフォーム:</strong> {{ platform_name }}<br/>
              <strong>検証日時:</strong> {{ validated_at }}<br/>
              <strong>合計商品数:</strong> {{ total_products }}<br/>
              <strong>エラーのある商品数:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          トップエラー:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} 件の商品が影響を受けています: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          修正方法:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          すべてのエラーを表示
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          フィードを管理
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          これらのエラーを修正して、{{ platform_name }} にすべての商品が表示されるようにしてください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ フィード検証エラー

データ品質の問題が検出されました

{{ feed_name }} で {{ error_count }} 件の検証エラーが見つかりました。これらの問題により、{{ platform_name }} に商品が表示されない可能性があります。

検証概要:
- フィード: {{ feed_name }}
- プラットフォーム: {{ platform_name }}
- 検証日時: {{ validated_at }}
- 合計商品数: {{ total_products }}
- エラーのある商品数: {{ affected_products }}

トップエラー:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} 件の商品 - {{ error.message }}
{% endfor %}

修正方法:
{{ fix_instructions }}

すべてのエラーを表示: {{ errors_url }}
フィードを管理: {{ admin_feed_url }}

これらのエラーを修正して、{{ platform_name }} にすべての商品が表示されるようにしてください。
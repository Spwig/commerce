---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ 更新失敗: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ 更新失敗
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          インストールエラー
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} のバージョン {{ target_version }} への更新がインストールに失敗しました。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              失敗の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>コンポーネント:</strong> {{ component_name }}<br/>
              <strong>対象バージョン:</strong> {{ target_version }}<br/>
              <strong>失敗したタイミング:</strong> {{ failed_at }}<br/>
              <strong>エラーコード:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          エラーメッセージ:
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
          <strong>完全なエラーログ:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:50 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          次の手順:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. システム要件と依存関係を確認する<br/>
          2. エラーログを確認して詳細を確認する<br/>
          3. 再度インストールを試みるか、サポートに連絡する<br/>
          4. あなたの店舗はまだ {{ current_version }} で実行されています
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          再度インストールを試みる
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          サポートに連絡する
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ 更新失敗

インストールエラー

{{ component_name }} のバージョン {{ target_version }} への更新がインストールに失敗しました。

失敗の詳細:
- コンポーネント: {{ component_name }}
- 対象バージョン: {{ target_version }}
- 失敗したタイミング: {{ failed_at }}
- エラーコード: {{ error_code }}

エラーメッセージ:
{{ error_message }}

{% if error_log %}
完全なエラーログ:
{{ error_log|truncatewords:50 }}
{% endif %}

次の手順:
1. システム要件と依存関係を確認する
2. エラーログを確認して詳細を確認する
3. 再度インストールを試みるか、サポートに連絡する
4. あなたの店舗はまだ {{ current_version }} で実行されています

再インストール: {{ retry_url }}
サポートに連絡: {{ support_url }}
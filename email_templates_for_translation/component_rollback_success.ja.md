---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} を v{{ previous_version }} にロールバックしました

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ ロールバック完了
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          コンポーネントの復元
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} は前のバージョンに正常にロールバックされました。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ロールバックの詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>コンポーネント:</strong> {{ component_name }}<br/>
              <strong>ロールバック元:</strong> v{{ failed_version }}<br/>
              <strong>復元先:</strong> v{{ previous_version }}<br/>
              <strong>完了日時:</strong> {{ completed_at }}<br/>
              <strong>所要時間:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ロールバックの理由:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ ストアの状態
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              あなたのストアは現在安定したバージョン {{ previous_version }} で動作しています。すべての機能が復元されているはずです。
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>データ復元:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          次の手順:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          コンポーネントの詳細を表示
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          事故報告を表示
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          問題が引き続き発生する場合は、サポートにお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ ロールバック完了

コンポーネントの復元

{{ component_name }} は前のバージョンに正常にロールバックされました。

ロールバックの詳細:
- コンポーネント: {{ component_name }}
- ロールバック元: v{{ failed_version }}
- 復元先: v{{ previous_version }}
- 完了日時: {{ completed_at }}
- 所要時間: {{ rollback_duration }}

{% if rollback_reason %}
ロールバックの理由:
{{ rollback_reason }}
{% endif %}

✓ ストアの状態:
あなたのストアは現在安定したバージョン {{ previous_version }} で動作しています。すべての機能が復元されているはずです。

{% if data_restored %}
データ復元: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
次の手順:
{{ next_steps }}
{% endif %}

コンポーネントの詳細を表示: {{ component_url }}
{% if incident_report_url %}事故報告を表示: {{ incident_report_url }}{% endif %}

問題が引き続き発生する場合は、サポートにお問い合わせください。
---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ {{ component_name }} と {{ conflicting_component }} の互換性問題

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 互換性警告
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          バージョンの競合が検出されました
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Spwig ストアのコンポーネント間で互換性の問題が検出されました。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              競合の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>コンポーネント 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>コンポーネント 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>検出日時:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          互換性の問題:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              潜在的な影響
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          お勧めの対処法:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              互換性のあるバージョン
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          競合を解決する
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          サポートに連絡する
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ストアはまだ正常に運用されていますが、できるだけ早くこの競合を解決することをお勧めします。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 互換性警告

バージョンの競合が検出されました

Spwig ストアのコンポーネント間で互換性の問題が検出されました。

競合の詳細:
- コンポーネント 1: {{ component_name }} v{{ component_version }}
- コンポーネント 2: {{ conflicting_component }} v{{ conflicting_version }}
- 検出日時: {{ detected_at }}

互換性の問題:
{{ incompatibility_description }}

潜在的な影響:
{{ impact_description }}

お勧めの対処法:
{{ recommended_action }}

{% if compatible_versions %}
互換性のあるバージョン:
{{ compatible_versions }}
{% endif %}

{% if update_url %}競合を解決: {{ update_url }}{% endif %}
サポートに連絡: {{ support_url }}

ストアはまだ正常に運用されていますが、できるだけ早くこの競合を解決することをお勧めします。
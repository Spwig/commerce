---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
アップデート利用可能: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 アップデート利用可能
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          新しいバージョンが利用可能です
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Spwigストア用の{{ component_name }}の新しいバージョンが利用可能です。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              アップデートの詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>コンポーネント:</strong> {{ component_name }}<br/>
              <strong>現在のバージョン:</strong> {{ current_version }}<br/>
              <strong>新しいバージョン:</strong> {{ new_version }}<br/>
              <strong>リリース日:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          何が新しくなったか:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 重大な変更
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          アップデートをインストール
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            フル変更履歴を表示
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 アップデート利用可能

新しいバージョンが利用可能です

Spwigストア用の{{ component_name }}の新しいバージョンが利用可能です。

アップデートの詳細:
- コンポーネント: {{ component_name }}
- 現在のバージョン: {{ current_version }}
- 新しいバージョン: {{ new_version }}
- リリース日: {{ release_date }}

何が新しくなったか:
{{ changelog }}

{% if breaking_changes %}
⚠️ 重大な変更:
{{ breaking_changes }}
{% endif %}

アップデートをインストール: {{ update_url }}
フル変更履歴を表示: {{ changelog_url }}
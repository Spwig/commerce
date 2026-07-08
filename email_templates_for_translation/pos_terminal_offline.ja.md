---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ POS端末がオフライン: {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ 端末が切断されました
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          POS端末がオフライン
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} はオフラインになり、もはや応答していません。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              端末情報:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>端末:</strong> {{ terminal_name }}<br/>
              <strong>場所:</strong> {{ location }}<br/>
              <strong>最終確認:</strong> {{ last_seen }}<br/>
              <strong>オフライン開始:</strong> {{ offline_since }}<br/>
              <strong>期間:</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          一般的な原因:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • ネットワーク接続の問題<br/>
          • 端末が電源を切られたり、再起動された<br/>
          • ソフトウェアのクラッシュまたはフリーズ<br/>
          • インターネットサービスの停止
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          お勧めの対処法:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 端末の電源とネットワーク接続を確認<br/>
          2. 端末デバイスを再起動<br/>
          3. インターネット接続を確認<br/>
          4. ファイアウォールおよびセキュリティ設定を確認
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ アクティブシフト警告
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              この端末にはアクティブなシフトがあります。再接続するまで販売データが同期されない可能性があります。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          端末の状態を確認する
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          端末が再接続されたら、もう一度通知を受け取ります。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 端末が切断されました

POS端末がオフライン

{{ terminal_name }} はオフラインになり、もはや応答していません。

端末情報:
- 端末: {{ terminal_name }}
- 場所: {{ location }}
- 最終確認: {{ last_seen }}
- オフライン開始: {{ offline_since }}
- 期間: {{ offline_duration }}

一般的な原因:
• ネットワーク接続の問題
• 端末が電源を切られたり、再起動された
• ソフトウェアのクラッシュまたはフリーズ
• インターネットサービスの停止

お勧めの対処法:
1. 端末の電源とネットワーク接続を確認
2. 端末デバイスを再起動
3. インターネット接続を確認
4. ファイアウォールおよびセキュリティ設定を確認

{% if active_shift %}
⚠️ アクティブシフト警告:
この端末にはアクティブなシフトがあります。再接続するまで販売データが同期されない可能性があります。
{% endif %}

端末の状態を確認する: {{ admin_terminals_url }}

端末が再接続されたら、もう一度通知を受け取ります。
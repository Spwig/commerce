---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
支払いプロバイダーの問題 - {{ provider_name }} SDK の読み込みに失敗しました

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          支払いプロバイダーの問題
        </mj-text>
        <mj-text>
          チェックアウト時に顧客の {{ provider_name }} 支払い SDK の読み込みに失敗しました。これはプロバイダーのサービス障害を示している可能性があります。
        </mj-text>
        <mj-text>
          <strong>プロバイダー:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>エラータイプ:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>時間:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>失敗回数（1時間以内）:</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          この通知は、1プロバイダーあたり1時間に1回のレート制限により送信されています。問題が継続する場合は、プロバイダーのダッシュボードを確認するか、サポートに連絡してください。
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          支払い設定を表示
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
支払いプロバイダーの問題

チェックアウト時に顧客の {{ provider_name }} 支払い SDK の読み込みに失敗しました。これはプロバイダーのサービス障害を示している可能性があります。

プロバイダー: {{ provider_name }}
エラータイプ: {{ error_type }}
時間: {{ timestamp }}
失敗回数（1時間以内）: {{ failure_count }}

この通知は、1プロバイダーあたり1時間に1回のレート制限により送信されています。問題が継続する場合は、プロバイダーのダッシュボードを確認するか、サポートに連絡してください。

支払い設定を表示: {{ admin_url }}
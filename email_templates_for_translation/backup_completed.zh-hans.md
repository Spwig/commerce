---
template_type: backup_completed
category: Backups
---

# Email Template: backup_completed

## Subject
✓ 备份成功完成 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ 备份成功完成
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ admin_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你为 {{ shop_name }} 安排的备份已成功完成。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              备份详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>类型：</strong> {{ backup_type }}<br/>
              <strong>开始时间：</strong> {{ backup_started_at }}<br/>
              <strong>完成时间：</strong> {{ backup_completed_at }}<br/>
              <strong>持续时间：</strong> {{ backup_duration }}<br/>
              <strong>大小：</strong> {{ backup_size }}<br/>
              <strong>位置：</strong> {{ backup_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          查看备份详情
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>下次计划备份：</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 备份成功完成

你好 {{ admin_name }}，

你为 {{ shop_name }} 安排的备份已成功完成。

备份详情：
- 类型：{{ backup_type }}
- 开始时间：{{ backup_started_at }}
- 完成时间：{{ backup_completed_at }}
- 持续时间：{{ backup_duration }}
- 大小：{{ backup_size }}
- 位置：{{ backup_location }}

查看备份详情：{{ admin_backup_url }}

下次计划备份：{{ next_scheduled_backup }}
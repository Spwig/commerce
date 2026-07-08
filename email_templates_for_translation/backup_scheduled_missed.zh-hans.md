---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ 计划备份未运行 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 计划备份未运行
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ admin_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }} 的计划备份未按预期运行。您的数据可能未得到充分保护。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              备份计划详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>计划时间：</strong> {{ scheduled_time }}<br/>
              <strong>备份类型：</strong> {{ backup_type }}<br/>
              <strong>上次成功备份：</strong> {{ last_successful_backup }}<br/>
              <strong>自上次备份以来的时间：</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          可能的原因：
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • 服务器离线或无法访问<br/>
          • 计划任务服务未运行<br/>
          • 权限不足<br/>
          • 存储空间已满<br/>
          • 数据库连接问题
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          手动运行备份
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看系统日志
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 计划备份未运行

你好 {{ admin_name }}，

{{ shop_name }} 的计划备份未按预期运行。您的数据可能未得到充分保护。

备份计划详情：
- 计划时间：{{ scheduled_time }}
- 备份类型：{{ backup_type }}
- 上次成功备份：{{ last_successful_backup }}
- 自上次备份以来的时间：{{ time_since_last }}

可能的原因：
• 服务器离线或无法访问
• 计划任务服务未运行
• 权限不足
• 存储空间已满
• 数据库连接问题

手动运行备份：{{ admin_backup_url }}
查看系统日志：{{ admin_logs_url }}
---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ 备份大小警告 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 备份大小警告
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ admin_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你最近为 {{ shop_name }} 做的备份已超过推荐的大小阈值。这可能表明数据存储需求正在增长。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              备份信息：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>当前大小：</strong> {{ backup_size }}<br/>
              <strong>警告阈值：</strong> {{ size_threshold }}<br/>
              <strong>上周以来的增长：</strong> {{ size_increase }}<br/>
              <strong>备份日期：</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          推荐操作：
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. 审查备份保留策略<br/>
          2. 考虑归档旧备份<br/>
          3. 检查媒体库中不必要的大文件<br/>
          4. 评估存储容量需求<br/>
          5. 监控备份增长趋势
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          管理备份
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 备份大小警告

你好 {{ admin_name }}，

你最近为 {{ shop_name }} 做的备份已超过推荐的大小阈值。这可能表明数据存储需求正在增长。

备份信息：
- 当前大小：{{ backup_size }}
- 警告阈值：{{ size_threshold }}
- 上周以来的增长：{{ size_increase }}
- 备份日期：{{ backup_date }}

推荐操作：
1. 审查备份保留策略
2. 考虑归档旧备份
3. 检查媒体库中不必要的大文件
4. 评估存储容量需求
5. 监控备份增长趋势

管理备份：{{ admin_backup_url }}
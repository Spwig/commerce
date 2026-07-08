---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
新 {{ form_name }} 提交来自 {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 新表单提交
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          新提交已收到
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          已收到一个新的 {{ form_name }} 提交。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              提交信息：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>表单：</strong> {{ form_name }}<br/>
              <strong>提交人：</strong> {{ submitter_name }}<br/>
              <strong>电子邮件：</strong> {{ submitter_email }}<br/>
              <strong>提交时间：</strong> {{ submission_date }}<br/>
              <strong>参考编号：</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          提交的数据：
        </mj-text>

        {% for field in submission_data %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column>
            <mj-text font-size="13px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ field.label }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ field.value }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_submission_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          在管理后台查看
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          回复提交人
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 新表单提交

新提交已收到

已收到一个新的 {{ form_name }} 提交。

提交信息：
- 表单：{{ form_name }}
- 提交人：{{ submitter_name }}
- 电子邮件：{{ submitter_email }}
- 提交时间：{{ submission_date }}
- 参考编号：{{ submission_id }}

提交的数据：
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

在管理后台查看： {{ admin_submission_url }}
{% if reply_to_email %}回复提交人： mailto:{{ reply_to_email }}{% endif %}
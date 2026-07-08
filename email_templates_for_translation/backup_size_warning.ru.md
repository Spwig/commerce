---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ Предупреждение о размере резервной копии - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Предупреждение о размере резервной копии
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваша последняя резервная копия для {{ shop_name }} превысила рекомендуемый порог размера. Это может указывать на рост потребностей в хранении данных.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Информация о резервной копии:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Текущий размер:</strong> {{ backup_size }}<br/>
              <strong>Порог предупреждения:</strong> {{ size_threshold }}<br/>
              <strong>Рост с прошлой недели:</strong> {{ size_increase }}<br/>
              <strong>Дата резервной копии:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемые действия:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Проверьте политику хранения резервных копий<br/>
          2. Рассмотрите возможность архивирования старых резервных копий<br/>
          3. Проверьте наличие ненужных больших файлов в медиатеке<br/>
          4. Оцените потребности в объеме хранилища<br/>
          5. Отслеживайте тенденцию роста резервных копий
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Управление резервными копиями
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ПРЕДУПРЕЖДЕНИЕ О РАЗМЕРЕ РЕЗЕРВНОЙ КОПИИ

Здравствуйте, {{ admin_name }},

Ваша последняя резервная копия для {{ shop_name }} превысила рекомендуемый порог размера. Это может указывать на рост потребностей в хранении данных.

ИНФОРМАЦИЯ О РЕЗЕРВНОЙ КОПИИ:
- Текущий размер: {{ backup_size }}
- Порог предупреждения: {{ size_threshold }}
- Рост с прошлой недели: {{ size_increase }}
- Дата резервной копии: {{ backup_date }}

РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:
1. Проверьте политику хранения резервных копий
2. Рассмотрите возможность архивирования старых резервных копий
3. Проверьте наличие ненужных больших файлов в медиатеке
4. Оцените потребности в объеме хранилища
5. Отслеживайте тенденцию роста резервных копий

Управление резервными копиями: {{ admin_backup_url }}
---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Обнаружены низкокачественные переводы: {{ content_type }} - {{ low_quality_count }} элементов требуют проверки

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Предупреждение о качестве перевода
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуется проверить
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваши переводы завершены, но {{ low_quality_count }} переводов получили оценку ниже порога качества и должны быть проверены перед публикацией.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Сводка задания:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Тип контента:</strong> {{ content_type }}<br/>
              <strong>Общее количество элементов:</strong> {{ total_items }}<br/>
              <strong>Среднее качество:</strong> {{ average_quality }}%<br/>
              <strong>Низкое качество:</strong> {{ low_quality_count }} элементов ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Разбор качества:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Отлично (95-100%):</strong> {{ excellent_count }} элементов<br/>
              <strong>Хорошо (85-94%):</strong> {{ good_count }} элементов<br/>
              <strong>Средне (70-84%):</strong> {{ fair_count }} элементов<br/>
              <strong>Плохо (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} элементов</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Распространенные проблемы качества:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} случаев
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемые действия:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Проверьте помеченные переводы в административной панели<br/>
          2. Вручную отредактируйте переводы низкого качества<br/>
          3. Рассмотрите возможность повторного перевода элементов низкого качества<br/>
          4. Публикуйте только после завершения проверки
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Проверить переводы
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть элементы низкого качества
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Совет: Оценки качества ниже 85% указывают на потенциальные проблемы с грамматикой, контекстом или точностью. Сильно рекомендуется проверить переводы перед публикацией.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ПРЕДУПРЕЖДЕНИЕ О КАЧЕСТВЕ ПЕРЕВОДА

Рекомендуется проверить

Ваши переводы завершены, но {{ low_quality_count }} переводов получили оценку ниже порога качества и должны быть проверены перед публикацией.

СВОДКА ЗАДАНИЯ:
- Job ID: {{ job_id }}
- Тип контента: {{ content_type }}
- Общее количество элементов: {{ total_items }}
- Среднее качество: {{ average_quality }}%
- Низкое качество: {{ low_quality_count }} элементов ({{ low_quality_percentage }}%)

РАЗБОР КАЧЕСТВА:
- Отлично (95-100%): {{ excellent_count }} элементов
- Хорошо (85-94%): {{ good_count }} элементов
- Средне (70-84%): {{ fair_count }} элементов
- Плохо (<70%): {{ poor_count }} элементов

РАСПРОСТРАНЕННЫЕ ПРОБЛЕМЫ КАЧЕСТВА:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} случаев
{% endfor %}

РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:
1. Проверьте помеченные переводы в административной панели
2. Вручную отредактируйте переводы низкого качества
3. Рассмотрите возможность повторного перевода элементов низкого качества
4. Публикуйте только после завершения проверки

Проверить переводы: {{ review_url }}
Просмотреть элементы низкого качества: {{ low_quality_url }}

💡 Совет: Оценки качества ниже 85% указывают на потенциальные проблемы с грамматикой, контекстом или точностью. Сильно рекомендуется проверить переводы перед публикацией.
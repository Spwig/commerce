---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Dịch thuật hoàn tất: {{ content_type }} ({{ language_count }} ngôn ngữ)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Dịch thuật hoàn tất!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bản dịch của bạn đã sẵn sàng
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tin vui! Nhiệm vụ dịch thuật hàng loạt của bạn đã hoàn tất thành công.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Tóm tắt công việc:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Mã công việc:</strong> {{ job_id }}<br/>
              <strong>Loại nội dung:</strong> {{ content_type }}<br/>
              <strong>Ngôn ngữ:</strong> {{ target_languages }}<br/>
              <strong>Số mục đã dịch:</strong> {{ items_translated }}<br/>
              <strong>Tổng số từ:</strong> {{ word_count }}<br/>
              <strong>Hoàn tất:</strong> {{ completed_at }}<br/>
              <strong>Thời gian:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Chất lượng dịch thuật:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Điểm chất lượng trung bình:</strong> {{ quality_score }}%<br/>
              <strong>Chất lượng cao:</strong> {{ high_quality_count }} mục<br/>
              <strong>Gợi ý xem xét:</strong> {{ review_needed_count }} mục
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Gợi ý xem xét
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} bản dịch đạt dưới 85% và nên được xem xét trước khi xuất bản.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các bước tiếp theo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Xem xét các bản dịch trong bảng điều khiển quản trị của bạn<br/>
          2. Chỉnh sửa bất kỳ bản dịch nào cần tinh chỉnh<br/>
          3. Xuất bản bản dịch để đưa chúng vào sử dụng<br/>
          4. Nội dung đa ngôn ngữ của bạn sẽ sẵn sàng cho khách hàng
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem xét bản dịch
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xuất bản tất cả
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ DỊCH THUẬT HOÀN TẤT!

Bản dịch của bạn đã sẵn sàng

Tin vui! Nhiệm vụ dịch thuật hàng loạt của bạn đã hoàn tất thành công.

TÓM TẮT CÔNG VIỆC:
- Mã công việc: {{ job_id }}
- Loại nội dung: {{ content_type }}
- Ngôn ngữ: {{ target_languages }}
- Số mục đã dịch: {{ items_translated }}
- Tổng số từ: {{ word_count }}
- Hoàn tất: {{ completed_at }}
- Thời gian: {{ job_duration }}

CHẤT LƯỢNG DỊCH THUẬT:
- Điểm chất lượng trung bình: {{ quality_score }}%
- Chất lượng cao: {{ high_quality_count }} mục
- Gợi ý xem xét: {{ review_needed_count }} mục

{% if review_needed_count > 0 %}
⚠️ GỢI Ý XEM XÉT:
{{ review_needed_count }} bản dịch đạt dưới 85% và nên được xem xét trước khi xuất bản.
{% endif %}

CÁC BƯỚC TIẾP THEO:
1. Xem xét các bản dịch trong bảng điều khiển quản trị của bạn
2. Chỉnh sửa bất kỳ bản dịch nào cần tinh chỉnh
3. Xuất bản bản dịch để đưa chúng vào sử dụng
4. Nội dung đa ngôn ngữ của bạn sẽ sẵn sàng cho khách hàng

Xem xét bản dịch: {{ review_url }}
{% if can_publish_all %}Xuất bản tất cả: {{ publish_all_url }}{% endif %}
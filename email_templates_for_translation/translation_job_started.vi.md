---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Việc dịch thuật đã bắt đầu: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Việc dịch thuật đã bắt đầu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Việc dịch thuật theo lô đang được xử lý
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Việc dịch thuật theo lô của bạn đã bắt đầu và hiện đang được xử lý.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết công việc:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID công việc:</strong> {{ job_id }}<br/>
              <strong>Loại nội dung:</strong> {{ content_type }}<br/>
              <strong>Ngôn ngữ nguồn:</strong> {{ source_language }}<br/>
              <strong>Ngôn ngữ đích:</strong> {{ target_languages }}<br/>
              <strong>Số mục cần dịch:</strong> {{ item_count }}<br/>
              <strong>Bắt đầu:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thời gian hoàn thành ước tính:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Dựa trên {{ word_count }} từ)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Điều gì sẽ xảy ra tiếp theo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Dịch vụ dịch thuật AI xử lý nội dung của bạn<br/>
          2. Các bản dịch được lưu dưới dạng nháp để xem xét<br/>
          3. Bạn sẽ nhận được email khi công việc hoàn tất<br/>
          4. Xem xét và xuất bản các bản dịch từ bảng điều khiển quản trị của bạn
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem trạng thái công việc
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bạn có thể đóng email này. Chúng tôi sẽ thông báo cho bạn khi bản dịch hoàn tất.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 VIỆC DỊCH THUẬT ĐÃ BẮT ĐẦU

Việc dịch thuật theo lô đang được xử lý

Việc dịch thuật theo lô của bạn đã bắt đầu và hiện đang được xử lý.

CHI TIẾT CÔNG VIỆC:
- ID công việc: {{ job_id }}
- Loại nội dung: {{ content_type }}
- Ngôn ngữ nguồn: {{ source_language }}
- Ngôn ngữ đích: {{ target_languages }}
- Số mục cần dịch: {{ item_count }}
- Bắt đầu: {{ started_at }}

THỜI GIAN HOÀN THÀNH ƯỚC TÍNH:
{{ estimated_completion }}
(Dựa trên {{ word_count }} từ)

ĐIỀU GÌ SẼ XẢY RA TIẾP THEO:
1. Dịch vụ dịch thuật AI xử lý nội dung của bạn
2. Các bản dịch được lưu dưới dạng nháp để xem xét
3. Bạn sẽ nhận được email khi công việc hoàn tất
4. Xem xét và xuất bản các bản dịch từ bảng điều khiển quản trị của bạn

Xem trạng thái công việc: {{ job_status_url }}

Bạn có thể đóng email này. Chúng tôi sẽ thông báo cho bạn khi bản dịch hoàn tất.
---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Phát hiện bản dịch chất lượng thấp: {{ content_type }} - {{ low_quality_count }} mục cần xem xét

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Cảnh báo chất lượng bản dịch
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Khuyến nghị xem xét
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Nhiệm vụ bản dịch của bạn đã hoàn tất, nhưng {{ low_quality_count }} bản dịch đạt điểm dưới ngưỡng chất lượng và cần được xem xét trước khi xuất bản.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Tóm tắt công việc:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID công việc:</strong> {{ job_id }}<br/>
              <strong>Loại nội dung:</strong> {{ content_type }}<br/>
              <strong>Tổng số mục:</strong> {{ total_items }}<br/>
              <strong>Chất lượng trung bình:</strong> {{ average_quality }}%<br/>
              <strong>Chất lượng thấp:</strong> {{ low_quality_count }} mục ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Phân tích chất lượng:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tuyệt vời (95-100%):</strong> {{ excellent_count }} mục<br/>
              <strong>Tốt (85-94%):</strong> {{ good_count }} mục<br/>
              <strong>Khá (70-84%):</strong> {{ fair_count }} mục<br/>
              <strong>Kém (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} mục</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các vấn đề chất lượng phổ biến:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} lần xuất hiện
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gợi ý hành động:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Xem xét các bản dịch được đánh dấu trong bảng điều khiển quản trị<br/>
          2. Chỉnh sửa các bản dịch chất lượng thấp bằng tay<br/>
          3. Xem xét dịch lại các mục chất lượng kém<br/>
          4. Chỉ xuất bản sau khi hoàn tất xem xét
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem xét bản dịch
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem các mục chất lượng thấp
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Gợi ý: Điểm chất lượng dưới 85% cho thấy có thể có vấn đề về ngữ pháp, ngữ cảnh hoặc độ chính xác. Nên kiểm tra kỹ lưỡng trước khi xuất bản.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ CẢNH BÁO CHẤT LƯỢNG BẢN DỊCH

Khuyến nghị xem xét

Nhiệm vụ bản dịch của bạn đã hoàn tất, nhưng {{ low_quality_count }} bản dịch đạt điểm dưới ngưỡng chất lượng và cần được xem xét trước khi xuất bản.

TÓM TẮT CÔNG VIỆC:
- ID công việc: {{ job_id }}
- Loại nội dung: {{ content_type }}
- Tổng số mục: {{ total_items }}
- Chất lượng trung bình: {{ average_quality }}%
- Chất lượng thấp: {{ low_quality_count }} mục ({{ low_quality_percentage }}%)

PHÂN TÍCH CHẤT LƯỢNG:
- Tuyệt vời (95-100%): {{ excellent_count }} mục
- Tốt (85-94%): {{ good_count }} mục
- Khá (70-84%): {{ fair_count }} mục
- Kém (<70%): {{ poor_count }} mục

CÁC VẤN ĐỀ CHẤT LƯỢNG PHỔ BIẾN:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} lần xuất hiện
{% endfor %}

GỢI Ý HÀNH ĐỘNG:
1. Xem xét các bản dịch được đánh dấu trong bảng điều khiển quản trị
2. Chỉnh sửa các bản dịch chất lượng thấp bằng tay
3. Xem xét dịch lại các mục chất lượng kém
4. Chỉ xuất bản sau khi hoàn tất xem xét

Xem xét bản dịch: {{ review_url }}
Xem các mục chất lượng thấp: {{ low_quality_url }}

💡 Gợi ý: Điểm chất lượng dưới 85% cho thấy có thể có vấn đề về ngữ pháp, ngữ cảnh hoặc độ chính xác. Nên kiểm tra kỹ lưỡng trước khi xuất bản.
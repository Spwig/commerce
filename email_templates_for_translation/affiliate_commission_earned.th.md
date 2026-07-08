---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
คุณได้รับค่าคอมมิชชั่น {{ commission_amount }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          💰 ค่าคอมมิชชั่นที่ได้รับ!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          ข่าวดีจาก {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 ค่าคอมมิชชั่นของคุณ
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          จากออเดอร์ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          สวัสดี {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          เฮย! คุณได้รับค่าคอมมิชชั่น {{ commission_amount }} จากออเดอร์ #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          โปรดต่อเนื่องในการโปรโมต {{ shop_name }} เพื่อรับค่าคอมมิชชั่นเพิ่มเติม ยิ่งคุณสร้างยอดขายมากเท่าไร คุณก็จะได้รับมากขึ้นเท่านั้น!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>เลขที่สั่งซื้อ:</strong> #{{ order_number }}<br/>
          <strong>จำนวนค่าคอมมิชชั่น:</strong> {{ commission_amount }}<br/>
          <strong>อัตราค่าคอมมิชชั่น:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          ดูแดชบอร์ดพันธมิตร
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          มีคำถาม? <a href="mailto:{{ support_email }}" style="color: #007bff;">ติดต่อฝ่ายสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
คุณได้รับค่าคอมมิชชั่น {{ commission_amount }}!

คุณ {{ affiliate_name }},

เฮย! คุณได้รับค่าคอมมิชชั่น {{ commission_amount }} จากออเดอร์ #{{ order_number }}.

รายละเอียดค่าคอมมิชชั่น:
- เลขที่สั่งซื้อ: #{{ order_number }}
- จำนวนค่าคอมมิชชั่น: {{ commission_amount }}
- อัตราค่าคอมมิชชั่น: {{ commission_rate }}%

โปรดต่อเนื่องในการโปรโมต {{ shop_name }} เพื่อรับค่าคอมมิชชั่นเพิ่มเติม。

ดูแดชบอร์ดของคุณ: {{ portal_url }}

{{ shop_name }}
คำถาม? ติดต่อ {{ support_email }}
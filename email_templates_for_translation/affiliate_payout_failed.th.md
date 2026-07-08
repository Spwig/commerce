---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
มีการดำเนินการที่จำเป็น: การจ่ายเงินไม่สำเร็จ

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ การจ่ายเงินไม่สำเร็จ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          การจ่ายเงิน ID: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          คุณ {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          เราพบปัญหาในการประมวลผลการจ่ายเงินของคุณ {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          สิ่งนี้มักเกิดจากการระบุข้อมูลการชำระเงินผิดพลาดหรือปัญหาที่เกี่ยวข้องกับผู้ให้บริการชำระเงินของคุณ
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          กรุณาอัปเดตข้อมูลการชำระเงินของคุณในแดชบอร์ดพันธมิตรและติดต่อทีมสนับสนุนของเราเพื่อแก้ไขปัญหานี้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          อัปเดตข้อมูลการชำระเงิน
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ต้องการความช่วยเหลือ? <a href="mailto:{{ support_email }}" style="color: #007bff;">ติดต่อทีมสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
มีการดำเนินการที่จำเป็น: การจ่ายเงินไม่สำเร็จ

คุณ {{ affiliate_name }},

เราพบปัญหาในการประมวลผลการจ่ายเงินของคุณ {{ payout_amount }} (ID การจ่ายเงิน: {{ payout_id }}).

สิ่งนี้มักเกิดจากการระบุข้อมูลการชำระเงินผิดพลาดหรือปัญหาที่เกี่ยวข้องกับผู้ให้บริการชำระเงินของคุณ

กรุณาอัปเดตข้อมูลการชำระเงินของคุณในแดชบอร์ดพันธมิตรและติดต่อทีมสนับสนุนของเราเพื่อแก้ไขปัญหานี้

อัปเดตข้อมูลการชำระเงิน: {{ portal_url }}

{{ shop_name }}
ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}


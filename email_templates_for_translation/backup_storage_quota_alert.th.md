---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 การใช้พื้นที่จัดเก็บข้อมูลใกล้จะเต็ม - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 การใช้พื้นที่จัดเก็บข้อมูลใกล้จะเต็ม
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>เร่งด่วน:</strong> พื้นที่จัดเก็บสำรองของคุณต่ำมาก หากไม่เพิ่มพื้นที่จัดเก็บ งานสำรองข้อมูลในอนาคตอาจล้มเหลว
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              การใช้พื้นที่จัดเก็บ:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>ใช้แล้ว:</strong> {{ storage_used }} ของ {{ storage_total }}<br/>
              <strong>อัตราการใช้:</strong> {{ storage_percentage }}%<br/>
              <strong>ที่เหลือ:</strong> {{ storage_available }}<br/>
              <strong>สถานะ:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              การดำเนินการที่ต้องดำเนินการทันที:
            </mj-text>
            <mj-text color="#92400e">
              1. ลบสำเนาสำรองเก่าที่ไม่จำเป็นอีกต่อไป<br/>
              2. จัดเก็บสำเนาสำรองในสื่อจัดเก็บภายนอก<br/>
              3. เพิ่มปริมาณพื้นที่จัดเก็บ/ความจุ<br/>
              4. ตรวจสอบนโยบายการรักษาสำเนาสำรอง<br/>
              5. ตรวจสอบพื้นที่จัดเก็บทุกวันจนกว่าปัญหาจะได้รับการแก้ไข
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          จัดการพื้นที่จัดเก็บทันที
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 การใช้พื้นที่จัดเก็บข้อมูลใกล้จะเต็ม

Hi {{ admin_name }},

เร่งด่วน: พื้นที่จัดเก็บสำรองของคุณต่ำมาก หากไม่เพิ่มพื้นที่จัดเก็บ งานสำรองข้อมูลในอนาคตอาจล้มเหลว

สถานะการใช้พื้นที่จัดเก็บ:
- ใช้แล้ว: {{ storage_used }} ของ {{ storage_total }}
- อัตราการใช้: {{ storage_percentage }}%
- ที่เหลือ: {{ storage_available }}
- สถานะ: {{ storage_status }}

การดำเนินการที่ต้องดำเนินการทันที:
1. ลบสำเนาสำรองเก่าที่ไม่จำเป็นอีกต่อไป
2. จัดเก็บสำเนาสำรองในสื่อจัดเก็บภายนอก
3. เพิ่มปริมาณพื้นที่จัดเก็บ/ความจุ
4. ตรวจสอบนโยบายการรักษาสำเนาสำรอง
5. ตรวจสอบพื้นที่จัดเก็บทุกวันจนกว่าปัญหาจะได้รับการแก้ไข

จัดการพื้นที่จัดเก็บทันที: {{ admin_backup_url }}
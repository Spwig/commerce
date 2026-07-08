---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
เพิ่มยอดขายของคุณ - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          เริ่มต้น: การตลาดและเติบโต
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          เพิ่มการเข้าถึงและยอดขายให้กับ {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          สวัสดี {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          ตอนนี้ที่ {{ store_name }} เริ่มมีรูปแบบแล้ว ถึงเวลาที่จะมุ่งเน้นไปที่การเพิ่มการเข้าถึงและยอดขายของคุณ นี่คือคำแนะนำ 5 ข้อในการเริ่มต้นการตลาด
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          สร้างโค้ดส่วนลดแรกของคุณ
        </mj-text>
        <mj-text font-size="14px">
          ให้ส่วนลดเปิดตัวเพื่อดึงดูดลูกค้ารายแรกของคุณ ไปที่ <strong>Marketing > Discount Codes</strong> เพื่อสร้างส่วนลดแบบเปอร์เซ็นต์หรือจำนวนคงที่พร้อมตั้งค่าการใช้งานและวันหมดอายุได้ตามต้องการ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ตั้งค่าการกู้คืนตะกร้าสินค้าที่ถูกทิ้งไว้
        </mj-text>
        <mj-text font-size="14px">
          ฟื้นฟูยอดขายที่สูญเสียโดยอัตโนมัติ ตั้งค่าอีเมลการกู้คืนตะกร้าสินค้าที่ถูกทิ้งไว้ภายใต้ <strong>Marketing > Abandoned Carts</strong> เพื่อเตือนลูกค้าเกี่ยวกับสินค้าที่พวกเขาทิ้งไว้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          เชื่อมต่อบัญชีโซเชียลมีเดียของคุณ
        </mj-text>
        <mj-text font-size="14px">
          เชื่อมต่อโปรไฟล์โซเชียลมีเดียของคุณกับร้านค้า เพื่อให้ลูกค้าสามารถค้นหาและติดตามคุณได้ เพิ่มลิงก์โซเชียลภายใต้ <strong>Settings > Social Media</strong> เพื่อแสดงในส่วนท้ายของร้านค้าของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ตั้งค่าการติดตาม Google Analytics
        </mj-text>
        <mj-text font-size="14px">
          ทำความเข้าใจว่าลูกค้าของคุณมาจากที่ไหนและพวกเขาโต้ตอบกับร้านค้าของคุณอย่างไร เพิ่ม ID การติดตาม Google Analytics ของคุณภายใต้ <strong>Settings > Analytics</strong> เพื่อเริ่มรวบรวมข้อมูล
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          สร้างฟอร์มสมัครสมาชิกอีเมลข่าวสาร
        </mj-text>
        <mj-text font-size="14px">
          สร้างรายชื่ออีเมลของคุณตั้งแต่วันแรก เพิ่มฟอร์มสมัครสมาชิกอีเมลข่าวสารในร้านค้าของคุณเพื่อรับอีเมลของผู้เข้าชม ใช้ข้อมูลเหล่านี้เพื่อการส่งเสริมการขาย การเปิดตัวสินค้า และการมีส่วนร่วมกับลูกค้า
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
เริ่มต้น: การตลาดและเติบโต - {{ store_name }}

สวัสดี {{ name|default:'there' }},

ตอนนี้ที่ {{ store_name }} เริ่มมีรูปแบบแล้ว ถึงเวลาที่จะมุ่งเน้นไปที่การเพิ่มการเข้าถึงและยอดขายของคุณ นี่คือคำแนะนำ 5 ข้อในการเริ่มต้นการตลาด

1. สร้างโค้ดส่วนลดแรกของคุณ
ให้ส่วนลดเปิดตัวเพื่อดึงดูดลูกค้ารายแรกของคุณ ไปที่ Marketing > Discount Codes เพื่อสร้างส่วนลดกับตัวเลือกการจำกัดการใช้งานและวันหมดอายุ

2. ตั้งค่าการกู้คืนตะกร้าสินค้าที่ถูกทิ้งไว้
ฟื้นฟูยอดขายที่สูญเสียโดยอัตโนมัติ ตั้งค่าอีเมลการกู้คืนตะกร้าสินค้าที่ถูกทิ้งไว้ภายใต้ Marketing > Abandoned Carts

3. เชื่อมต่อบัญชีโซเชียลมีเดียของคุณ
เชื่อมต่อโปรไฟล์โซเชียลมีเดียของคุณกับร้านค้า เพิ่มลิงก์โซเชียลภายใต้ Settings > Social Media

4. ตั้งค่าการติดตาม Google Analytics
ทำความเข้าใจว่าลูกค้าของคุณมาจากที่ไหน เพิ่ม ID การติดตาม Google Analytics ของคุณภายใต้ Settings > Analytics

5. สร้างฟอร์มสมัครสมาชิกอีเมลข่าวสาร
สร้างรายชื่ออีเมลของคุณตั้งแต่วันแรก เพิ่มฟอร์มสมัครสมาชิกอีเมลข่าวสารในร้านค้าของคุณเพื่อรับอีเมลของผู้เข้าชมสำหรับการส่งเสริมการขายและการมีส่วนร่วม

ไปที่ Marketing: {{ admin_url }}

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}
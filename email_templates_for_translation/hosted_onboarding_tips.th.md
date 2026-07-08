---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
เคล็ดลับในการใช้ {{ store_name }} ให้ได้ประโยชน์สูงสุด

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
          เคล็ดลับในการเริ่มต้นใช้งาน
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          ใช้ประโยชน์จากร้านค้า Spwig ของคุณให้ได้สูงสุด
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
          ตอนนี้ <strong>{{ store_name }}</strong> ได้เปิดใช้งานแล้ว นี่คือเคล็ดลับที่จะช่วยให้คุณใช้ประโยชน์จากร้านค้าของคุณได้ดีที่สุด
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ปรับแต่งรูปลักษณ์ของคุณ
        </mj-text>
        <mj-text font-size="14px">
          ไปที่ <strong>Design > Theme Settings</strong> เพื่อเลือกธีม อัปโหลดโลโก้ และตั้งค่าสีแบรนด์ของคุณ ร้านค้าของคุณจะอัปเดตทันที ทำให้คุณสามารถดูการเปลี่ยนแปลงแบบเรียลไทม์ได้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          เพิ่มสินค้าของคุณ
        </mj-text>
        <mj-text font-size="14px">
          ไปที่ <strong>Catalog > Products</strong> เพื่อเริ่มเพิ่มสินค้าของคุณ คุณสามารถสร้างตัวเลือกสินค้า (ขนาด สี) ตั้งราคา จัดการสต็อก และอัปโหลดรูปภาพคุณภาพสูง
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ตั้งค่าการชำระเงิน
        </mj-text>
        <mj-text font-size="14px">
          ไปที่ <strong>Settings > Payment Providers</strong> เพื่อเชื่อมต่อกับ Stripe, PayPal หรือวิธีการชำระเงินอื่น ๆ คุณสามารถเปิดใช้งานหลายวิธีการชำระเงินเพื่อให้ลูกค้าสามารถชำระเงินตามที่พวกเขาต้องการ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ตั้งค่าการจัดส่ง
        </mj-text>
        <mj-text font-size="14px">
          ภายใต้ <strong>Settings > Shipping</strong> ตั้งค่าโซนและอัตราค่าจัดส่งของคุณ คุณสามารถสร้างกฎการจัดส่งแบบคงที่ ตามน้ำหนัก หรือการจัดส่งฟรีสำหรับภูมิภาคต่าง ๆ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          เพิ่มประสิทธิภาพ SEO ของคุณ
        </mj-text>
        <mj-text font-size="14px">
          Spwig จะสร้างแผนที่เว็บไซต์และแท็กเมตาอัตโนมัติ ไปที่ <strong>Settings > SEO</strong> เพื่อปรับแต่งชื่อหน้า คำอธิบาย และรูปภาพสำหรับการแชร์โซเชียล เพื่อช่วยให้ลูกค้าค้นพบร้านค้าของคุณได้ง่ายขึ้น
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
เคล็ดลับในการเริ่มต้นใช้งาน - {{ store_name }}

สวัสดี {{ name|default:'there' }},

ตอนนี้ {{ store_name }} ได้เปิดใช้งานแล้ว นี่คือเคล็ดลับที่จะช่วยให้คุณใช้ประโยชน์จากร้านค้าของคุณได้ดีที่สุด

1. ปรับแต่งรูปลักษณ์ของคุณ
ไปที่ Design > Theme Settings เพื่อเลือกธีม อัปโหลดโลโก้ และตั้งค่าสีแบรนด์ของคุณ

2. เพิ่มสินค้าของคุณ
ไปที่ Catalog > Products เพื่อเริ่มเพิ่มสินค้าของคุณพร้อมตัวเลือก ราคา และรูปภาพ

3. ตั้งค่าการชำระเงิน
ไปที่ Settings > Payment Providers เพื่อเชื่อมต่อกับ Stripe, PayPal หรือวิธีการชำระเงินอื่น ๆ

4. ตั้งค่าการจัดส่ง
ภายใต้ Settings > Shipping ตั้งค่าโซนและอัตราค่าจัดส่งสำหรับภูมิภาคต่าง ๆ

5. เพิ่มประสิทธิภาพ SEO ของคุณ
ไปที่ Settings > SEO เพื่อปรับแต่งชื่อหน้า คำอธิบาย และรูปภาพสำหรับการแชร์โซเชียล

ไปที่ Admin Panel: {{ admin_url }}

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}
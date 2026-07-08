---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
ไปให้ไกลขึ้น - {{ store_name }}

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
          การเริ่มต้น: ฟีเจอร์ขั้นสูง
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          ปลดล็อกศักยภาพเต็มที่ของ {{ store_name }}
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
          คุณได้เริ่มใช้งาน <strong>{{ store_name }}</strong> ไปแล้วประมาณสองสัปดาห์ นี่คือฟีเจอร์ขั้นสูงที่จะช่วยให้คุณพัฒนาธุรกิจของคุณให้ดีขึ้น
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ตั้งค่าเวิร์กโฟลว์อีเมลแบบอัตโนมัติ
        </mj-text>
        <mj-text font-size="14px">
          อัตโนมัติการสื่อสารกับลูกค้าผ่านเวิร์กโฟลว์อีเมล ตั้งค่าลำดับการต้อนรับ ติดตามหลังการซื้อ และแคมเปญการเรียกคืนความสนใจภายใต้ <strong>การตลาด > เวิร์กโฟลว์อีเมล</strong>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ตั้งค่ากฎเกณฑ์ภาษีสำหรับภูมิภาคของคุณ
        </mj-text>
        <mj-text font-size="14px">
          ตรวจสอบให้แน่ใจว่าคุณเรียกเก็บอัตราภาษีที่ถูกต้อง ไปที่ <strong>การตั้งค่า > ภาษี</strong> เพื่อตั้งค่ากฎเกณฑ์ภาษีสำหรับแต่ละภูมิภาคที่คุณขายสินค้า คุณสามารถตั้งค่าราคาแบบรวมภาษีหรือไม่รวมภาษีได้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          สำรวจ API เพื่อการผสานข้อมูล
        </mj-text>
        <mj-text font-size="14px">
          หากแผนของคุณมีการเข้าถึง API คุณสามารถผสานร้านค้าของคุณกับเครื่องมือและบริการภายนอกได้ ไปที่ <strong>การตั้งค่า > API</strong> เพื่อสร้างคีย์ API และสำรวจเอกสารประกอบ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ตรวจสอบแดชบอร์ดการวิเคราะห์ของคุณ
        </mj-text>
        <mj-text font-size="14px">
          ติดตามประสิทธิภาพของร้านค้าของคุณ แดชบอร์ดของคุณแสดงข้อมูลสำคัญ เช่น รายได้ คำสั่งซื้อ สินค้าขายดี และข้อมูลลูกค้า เพื่อช่วยให้คุณตัดสินใจอย่างมีข้อมูล
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          พิจารณาเพิ่ม POS สำหรับการขายในร้าน
        </mj-text>
        <mj-text font-size="14px">
          คุณขายสินค้าในร้านด้วยหรือไม่? ฟีเจอร์จุดขายของ Spwig ช่วยให้คุณประมวลผลการขายในร้านที่สอดคล้องกับสต็อกออนไลน์และจัดการคำสั่งซื้อ ไปที่ <strong>การตั้งค่า > จุดขาย</strong> เพื่อดูข้อมูลเพิ่มเติม
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="สำรวจแดชบอร์ดของคุณ" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
การเริ่มต้น: ฟีเจอร์ขั้นสูง - {{ store_name }}

สวัสดี {{ name|default:'there' }},

คุณได้เริ่มใช้งาน {{ store_name }} ไปแล้วประมาณสองสัปดาห์ นี่คือฟีเจอร์ขั้นสูงที่จะช่วยให้คุณพัฒนาธุรกิจของคุณให้ดีขึ้น

1. ตั้งค่าเวิร์กโฟลว์อีเมลแบบอัตโนมัติ
อัตโนมัติการสื่อสารกับลูกค้าผ่านลำดับการต้อนรับ ติดตามหลังการซื้อ และแคมเปญการเรียกคืนความสนใจ

2. ตั้งค่ากฎเกณฑ์ภาษีสำหรับภูมิภาคของคุณ
ตรวจสอบให้แน่ใจว่าคุณเรียกเก็บอัตราภาษีที่ถูกต้อง ไปที่ การตั้งค่า > ภาษี เพื่อตั้งค่ากฎเกณฑ์ภาษีสำหรับแต่ละภูมิภาค

3. สำรวจ API เพื่อการผสานข้อมูล
หากแผนของคุณมีการเข้าถึง API คุณสามารถผสานร้านค้าของคุณกับเครื่องมือภายนอก ไปที่ การตั้งค่า > API เพื่อเริ่มต้น

4. ตรวจสอบแดชบอร์ดการวิเคราะห์ของคุณ
แดชบอร์ดของคุณแสดงข้อมูลสำคัญ เช่น รายได้ คำสั่งซื้อ สินค้าขายดี และข้อมูลลูกค้า

5. พิจารณาเพิ่ม POS สำหรับการขายในร้าน
คุณขายสินค้าในร้านด้วยหรือไม่? ฟีเจอร์จุดขายของ Spwig ช่วยให้คุณประมวลผลการขายในร้านที่สอดคล้องกับสต็อกออนไลน์

สำรวจแดชบอร์ดของคุณ: {{ admin_url }}

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}
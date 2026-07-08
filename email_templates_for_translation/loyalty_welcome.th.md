---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
ยินดีต้อนรับสู่โปรแกรมรางวัลของ {{ shop_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 ยินดีต้อนรับสู่โปรแกรมรางวัล!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          เริ่มสะสมแต้มทุกครั้งที่ซื้อสินค้า
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          สวัสดี {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          ยินดีต้อนรับสู่โปรแกรมรางวัลของ {{ shop_name }}! คุณได้รับการลงทะเบียนโดยอัตโนมัติแล้ว และสามารถเริ่มสะสมแต้มได้ทันที
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 โบนัสต้อนรับ: {{ bonus_points }} แต้ม!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ระดับของคุณ:</strong> {{ current_tier }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ tier_benefits }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          วิธีการสะสมแต้ม
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • ซื้อสินค้า - สะสมแต้มทุกครั้งที่สั่งซื้อสินค้า<br/>
          • เขียนรีวิว - แบ่งปันความคิดเห็นของคุณ<br/>
          • ชวนเพื่อน - บอกต่อให้เพื่อนรู้<br/>
          • รางวัลวันเกิด - แต้มพิเศษในวันเกิดของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          ดูรางวัลของคุณ
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          มีคำถาม? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">ติดต่อฝ่ายสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ยินดีต้อนรับสู่โปรแกรมรางวัลของ {{ shop_name }}!

สวัสดี {{ customer_name }},

ยินดีต้อนรับสู่โปรแกรมรางวัลของ {{ shop_name }}! คุณได้รับการลงทะเบียนโดยอัตโนมัติแล้ว และสามารถเริ่มสะสมแต้มได้ทันที

{% if bonus_points %}โบนัสต้อนรับ: {{ bonus_points }} แต้ม!{% endif %}

ระดับของคุณ: {{ current_tier }}
{{ tier_benefits }}

วิธีการสะสมแต้ม:
- ซื้อสินค้า - สะสมแต้มทุกครั้งที่สั่งซื้อสินค้า
- เขียนรีวิว - แบ่งปันความคิดเห็นของคุณ
- ชวนเพื่อน - บอกต่อให้เพื่อนรู้
- รางวัลวันเกิด - แต้มพิเศษในวันเกิดของคุณ

ดูรางวัลของคุณ: {{ account_url }}

{{ shop_name }}
คำถาม? ติดต่อ {{ support_email }}
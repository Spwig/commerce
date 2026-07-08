---
title: การวิเคราะห์และรายงานพันธมิตร
---

การวิเคราะห์พันธมิตรช่วยให้คุณติดตามประสิทธิภาพของโปรแกรมพันธมิตรและระบุพันธมิตรที่มีผลงานยอดเยี่ยม คู่มือนี้จะแสดงให้คุณเห็นวิธีใช้แดชบอร์ดผู้ขาย ตีความสถิติ วิเคราะห์แนวโน้มรายได้ และตัดสินใจโดยใช้ข้อมูลเพื่อปรับปรุงโปรแกรมพันธมิตรของคุณ

## แดชบอร์ดผู้ขาย

ไปที่ **โปรแกรมพันธมิตร > แดชบอร์ด** เพื่อเข้าถึงภาพรวมการวิเคราะห์พันธมิตรที่ครอบคลุม

แดชบอร์ดผู้ขายให้ภาพรวมแบบเรียลไทม์เกี่ยวกับประสิทธิภาพของโปรแกรมพันธมิตรทั้งหมดของคุณ รวมถึงโปรแกรมที่เปิดใช้งาน จำนวนพันธมิตร ความเคลื่อนไหวของค่าคอมมิชชัน และแนวโน้มรายได้ นี่คือศูนย์กลางของคุณสำหรับการตรวจสอบสุขภาพของโปรแกรมและตัดสินใจเชิงกลยุทธ์

![Merchant Dashboard](/static/core/admin/img/help/affiliate-analytics/merchant-dashboard.webp)

## สถิติแดชบอร์ด

แดชบอร์ดแสดงตัวชี้วัดประสิทธิภาพหลักในรูปแบบการ์ดที่ด้านบนของหน้า

### สถิติภาพรวม

| สถิติ | คำอธิบาย | ค่าตัวอย่าง |
|-----------|-------------|---------------|
| **โปรแกรมทั้งหมด** | จำนวนโปรแกรมที่สร้างขึ้น (จำนวนที่เปิดใช้งานแสดงในวงเล็บ) | 3 โปรแกรม (2 โปรแกรมที่เปิดใช้งาน) |
| **พันธมิตรที่เปิดใช้งาน** | พันธมิตรที่ได้รับการอนุมัติและกำลังโปรโมตสินค้าของคุณ | 47 พันธมิตร |
| **การสมัครที่ยังไม่ได้รับการตรวจสอบ** | การสมัครพันธมิตรใหม่ที่รอให้คุณตรวจสอบ | 8 รายการที่ยังไม่ได้รับการตรวจสอบ |
| **คลิกทั้งหมด** | จำนวนคลิกตลอดอายุของลิงก์ติดตามพันธมิตรทั้งหมด | 12,543 คลิก |
| **ค่าคอมมิชชันทั้งหมด** | จำนวนบันทึกค่าคอมมิชชันที่เคยสร้าง | 287 ค่าคอมมิชชัน |
| **จำนวนเงินที่ยังไม่ได้รับการจ่าย** | ค่ารวมของค่าคอมมิชชันที่ได้รับการอนุมัติแต่ยังรอการจ่าย | $4,235.50 |

สถิติเหล่านี้ให้คุณมีมุมมองที่รวดเร็วเกี่ยวกับขนาดของโปรแกรมและภาระทางการเงิน

### การเข้าใจตัวชี้วัด

- **จำนวนที่เปิดใช้งาน** — แสดงจำนวนโปรแกรมที่กำลังรับการสมัครและสร้างค่าคอมมิชชัน
- **การสมัครที่ยังไม่ได้รับการตรวจสอบ** — บ่งบอกถึงภาระงานตรวจสอบของคุณ (จำนวนสูงแสดงว่าคุณควรตรวจสอบการสมัครบ่อยขึ้น)
- **คลิกทั้งหมด** — วัดการมีส่วนร่วมของพันธมิตรและกิจกรรมการโปรโมต
- **จำนวนเงินที่ยังไม่ได้รับการจ่าย** — แสดงภาระการจ่ายเงินให้พันธมิตรในปัจจุบัน

## แผนภูมิรายได้

แดชบอร์ดมีแผนภูมิรายได้ 30 วันที่ใช้ Chart.js แสดงแนวโน้มค่าคอมมิชชันตามเวลา

### คุณสมบัติของแผนภูมิ

- **ช่วงเวลา** — แสดงกิจกรรมค่าคอมมิชชันในช่วง 30 วันที่ผ่านมา
- **การแบ่งรายวัน** — แท่งแต่ละแท่งแสดงค่าคอมมิชชันที่สร้างในวันนั้น
- **รายละเอียดเมื่อชี้เมาส์** — ชี้เมาส์ที่แท่งใดแท่งหนึ่งเพื่อดูวันที่และยอดค่าคอมมิชชันที่แน่นอน
- **การวิเคราะห์แนวโน้ม** — ระบุรูปแบบการเติบโต แนวโน้มตามฤดูกาล และความผิดปกติได้อย่างรวดเร็ว

### การอ่านแผนภูมิ

**ตัวอย่างการวิเคราะห์:**


```
วันที่ 1-7:   $150-$200/วัน  → ประสิทธิภาพพื้นฐาน
วันที่ 8-14:  $300-$450/วัน  → ความกระตือรือร้นของแคมเปญ (ตรวจสอบสิ่งที่ทำให้ได้ผล)
วันที่ 15-21: $100-$150/วัน  → ลดลงหลังแคมเปญ (คาดการณ์ได้)
วันที่ 22-30: $200-$250/วัน  → กลับสู่ระดับพื้นฐาน
```


ใช้แผนภูมินี้เพื่อ:

- **ระบุแคมเปญที่ประสบความสำเร็จ** — ความกระตือรือร้นแสดงถึงการส่งเสริมที่มีประสิทธิภาพ
- **ระบุรูปแบบตามฤดูกาล** — วางแผนสต็อกและกิจกรรมพันธมิตรรอบช่วงเวลาที่มีผู้เข้าชมสูง
- **ตรวจจับปัญหา** — การลดลงอย่างกะทันหันอาจบ่งบอกถึงลิงก์ติดตามที่เสียหายหรือปัญหาของโปรแกรม
- **ตรวจสอบการเปลี่ยนแปลง** — เปรียบเทียบรายได้ก่อนและหลังการปรับอัตราค่าคอมมิชชัน

## พันธมิตรที่มีผลงานยอดเยี่ยม

แดชบอร์ดมีตารางแสดงพันธมิตร 10 อันดับแรกที่มีรายได้สูงสุด

### ตัวชี้วัดประสิทธิภาพพันธมิตร

| คอลัมน์ | คำอธิบาย | ตัวอย่าง |
|--------|-------------|---------|
| **พันธมิตร** | ชื่อและรหัสพันธมิตรที่เป็นเอกลักษณ์ | Sarah Johnson (AFF-12345) |
| **รายได้ทั้งหมด** | ยอดขายตลอดกาลที่เกี่ยวข้องกับพันธมิตรนี้ | $18,450.00 |
| **คำสั่งซื้อ** | จำนวนคำสั่งซื้อที่สำเร็จที่ได้รับการแนะนำ | 87 คำสั่งซื้อ |
| **จำนวนค่าคอมมิชชัน** | จำนวนบันทึกค่าคอมมิชชันที่สร้าง | 87 ค่าคอมมิชชัน |
| **จำนวนเงินทั้งหมดที่จ่าย** | จำนวนเงินที่จ่ายให้พันธมิตรจนถึงขณะนี้ | $2,767.50 |

ตารางนี้ **จัดเรียงตามรายได้ทั้งหมด** (จากสูงสุดไปต่ำสุด) เพื่อช่วยให้คุณระบุพันธมิตรที่มีคุณค่าสูงสุดได้อย่างรวดเร็ว

### การใช้ข้อมูลพันธมิตรที่มีผลงานยอดเยี่ยม

**ระบุพันธมิตร VIP:**


ตรวจสอบพันธมิตรที่มีผลงานสูงสุดและพิจารณา:

- **อัตราพิเศษ** — ให้อัตราค่าคอมมิชชันที่สูงขึ้นแก่พันธมิตร 3 อันดับแรกของคุณ (เช่น เพิ่มจาก 10% เป็น 12%)
- **การเข้าถึงก่อนกำหนด** — แจ้งให้พันธมิตรที่ดีที่สุดทราบล่วงหน้าเกี่ยวกับสินค้าใหม่หรือการขาย
- **สื่อสร้างสรรค์เฉพาะ** — ให้แบนเนอร์หรือภาพสินค้าที่ปรับแต่งเฉพาะ
- **การสนับสนุนโดยตรง** — มอบผู้ติดต่อเฉพาะสำหรับพันธมิตรที่ดีที่สุดของคุณ

**ตัวอย่าง:**


```
พันธมิตร: Emily Chen (AFF-00123)
รายได้:   $24,500
คำสั่งซื้อ:    142
การจ่ายเงิน:   $2,450 (ค่าคอมมิชชัน 10%)

การกระทำ: ให้อัตราค่าคอมมิชชันระดับ 12% + การเข้าถึงสินค้าล่วงหน้า
ผลกระทบที่คาดการณ์: เพิ่มรายได้จากพันธมิตรนี้ 20-30%
```


## การดำเนินการล่าสุด

แดชบอร์ดแสดงกิจกรรมของพันธมิตรล่าสุดเพื่อช่วยให้คุณติดตามการดำเนินการที่ยังไม่ได้รับการดำเนินการ

### การสมัครล่าสุด

แสดงการสมัครพันธมิตรที่ยังไม่ได้รับการตรวจสอบ 5 รายการล่าสุด พร้อมด้วย:

- ชื่อพันธมิตร
- วันที่สมัคร
- โปรแกรมที่สมัคร
- ลิงก์ **ตรวจสอบ** แบบเร็วเพื่ออนุมัติหรือปฏิเสธ

ส่วนนี้ช่วยให้คุณจัดลำดับความสำคัญของการตรวจสอบพันธมิตรใหม่และหลีกเลี่ยงการสะสมการสมัคร

### ค่าคอมมิชชันล่าสุด

แสดงค่าคอมมิชชันที่สร้างขึ้นล่าสุด 10 รายการ (สถานะค้าง) พร้อมด้วย:

- หมายเลขคำสั่งซื้อ (คลิกเพื่อดูรายละเอียดคำสั่งซื้อ)
- ชื่อพันธมิตร
- จำนวนค่าคอมมิชชัน
- วันที่สร้าง
- การดำเนินการ **อนุมัติ** หรือ **ปฏิเสธ** แบบเร็ว

ตรวจสอบส่วนนี้ทุกวันเพื่อให้ค่าคอมมิชชันเคลื่อนผ่านกระบวนการอนุมัติได้อย่างราบรื่น

## สถิติระดับโปรแกรม

ไปที่หน้ารายละเอียดของโปรแกรมเพื่อดูการวิเคราะห์เฉพาะโปรแกรม

### การเข้าถึงสถิติโปรแกรม

1. ไปที่ **โปรแกรมพันธมิตร > โปรแกรม**
2. คลิกชื่อโปรแกรมที่คุณต้องการวิเคราะห์
3. ดูแผงสถิติบนหน้ารายละเอียดโปรแกรม

### ตัวชี้วัดเฉพาะโปรแกรม


| Metric | Description | What It Means |
|--------|-------------|---------------|
| **Active Affiliates** | Approved affiliates in this program | 23 affiliates |
| **Total Clicks** | Clicks on tracking links for this program | 5,432 clicks |
| **Total Commissions** | Commission records created for this program | 127 commissions |
| **Pending Commissions** | Unpaid commission value for this program | $1,245.00 |

### Recent Program Affiliates

The program detail page shows the 10 newest affiliates who joined this program, including:

- Affiliate name and code
- Join date
- Application status

Use this to monitor program growth and identify which programs attract the most interest.

## Affiliate Performance by Program

View detailed per-affiliate statistics within a specific program.

### Viewing Affiliates by Program

1. Navigate to **Affiliate Program > Programs**
2. Click the program name
3. Scroll to the **Affiliates** section
4. Click **View All Affiliates** to see the complete list

The affiliate list is **sorted by total commissions** to highlight top performers within each program.

### Comparison Analysis

**Example: Comparing two programs**

**Influencer Program (10% commission):**
- 47 active affiliates
- 8,234 clicks
- 187 commissions
- Average commission value: $32.50

**Bulk Referral Program (fixed $25 commission):**
- 23 active affiliates
- 3,421 clicks
- 94 commissions
- Average commission value: $25.00

**Insight:** Influencer program has higher engagement and commission values, suggesting percentage-based commissions work better for this store.

## Commission Reports

The commission admin provides advanced filtering and export capabilities for detailed reporting.

### Accessing Commission Reports

Navigate to **Marketing > Commissions** to view the full commission list with filters.

### Advanced Filtering

Use the filter sidebar to create custom reports:

- **By Date Range** — Select commissions created between specific dates (e.g., January 1-31 for monthly reporting)
- **By Affiliate** — View all commissions for a single affiliate
- **By Program** — See commissions from a specific program
- **By Status** — Filter to show only pending, approved, rejected, or paid commissions

### Export Capabilities

Spwig's admin interface includes built-in export functionality:

1. Apply filters to narrow down the commission list
2. Select the commissions you want to export (or use "Select all")
3. Choose **Export Selected** from the **Actions** dropdown
4. Select format (CSV, Excel)
5. Download the report for offline analysis

**Common Reports:**

- **Monthly commission summary** — Filter by date range, export all approved commissions
- **Affiliate performance** — Filter by affiliate, export all commissions to calculate ROI
- **Program comparison** — Export commissions for each program separately, compare in spreadsheet

## Payout Reports

The payout admin provides financial tracking and reconciliation tools.

### Accessing Payout Reports

Navigate to **Affiliate Program > Payouts** to view payout history and statistics.

### Payout Statistics

The payout dashboard shows:

| Status | Description |
|--------|-------------|
| **Pending** | Payouts created but not yet processed |
| **Processing** | Payouts submitted to payment provider (PayPal/Airwallex) |
| **Completed** | Successfully paid to affiliates |
| **Failed** | Payment processing errors |

### Provider Account Breakdown

View payouts organized by payment provider:

- **PayPal** — Payouts processed via PayPal (displays total count and amount)
- **Airwallex** — Payouts processed via bank transfer (displays total count and amount)

This breakdown helps you:

- Monitor provider costs (compare PayPal fees vs Airwallex fees)
- Balance payout methods (encourage affiliates to use lower-cost options)
- Identify processing issues (high failure rates on one provider)

### Historical Payout Data

Filter and export payout history for:

- **Quarterly reports** — Calculate affiliate program costs per quarter
- **Tax documentation** — Export annual payout data for 1099 forms (US) or equivalent
- **Affiliate inquiries** — Quickly look up payment dates and amounts when affiliates have questions

## Using Analytics for Optimization

Leverage your analytics data to continuously improve program performance.

### Identify Top Performers

**Action:** Review the top affiliates table monthly and:

- **Reward excellence** — Increase commission rates for top 10% of affiliates
- **Understand tactics** — Reach out to ask what promotional methods work best
- **Replicate success** — Share top affiliate strategies with other partners (with permission)

**Example:**

```
Top Affiliate: Marcus Lee (AFF-00456)
Revenue:       $31,200 in 3 months
Method:        YouTube product reviews

Action:
1. Increase commission from 10% to 12%
2. Ask Marcus to create an affiliate case study
3. Recruit more YouTube influencers using Marcus's success story
```

### Support Low Performers

**Action:** Filter affiliates by commission count and identify those with < 5 commissions in 90 days:

- **Provide resources** — Send promotional materials, product photos, sample copy
- **Offer training** — Create a webinar showing effective promotion tactics
- **Adjust placement** — If an affiliate's audience doesn't match a program, suggest switching to a different program
- **Remove inactive** — After 6-12 months with no activity, consider removing them from the program

### Program Comparison

**Action:** Compare total commissions and click-to-conversion rates across programs:

| Program | Clicks | Commissions | Conversion Rate | Avg Commission |
|---------|--------|-------------|-----------------|----------------|
| Program A | 8,234 | 187 | 2.27% | $32.50 |
| Program B | 3,421 | 94 | 2.75% | $25.00 |

**Insights:**

- Program B has a **higher conversion rate** despite fewer clicks (better targeting)
- Program A generates **higher commission values** (better for revenue)

**การปรับปรุงประสิทธิภาพ:**

- เพิ่มอัตราค่าคอมมิชชันสำหรับโปรแกรม B เพื่อดึงดูดพันธมิตรมากขึ้น (มีการพิสูจน์แล้วว่ามีการเปลี่ยนผ่าน)
- วิเคราะห์ว่าอะไรทำให้โปรแกรม B มีการเปลี่ยนผ่านได้ดีกว่า และนำความรู้ที่ได้ไปประยุกต์ใช้กับโปรแกรม A

### แนวโน้มตามฤดูกาล

**การกระทำ:** ใช้แผนภูมิรายได้เพื่อระบุรูปแบบตามฤดูกาล:

```
January:  $5,200   → ช่วงหลังเทศกาลลดลง
February: $4,800   → ช่วงต่ำต่อเนื่อง
March:    $6,100   → ยอดขายเพิ่มขึ้นในช่วงฤดูใบไม้ผลิ
April:    $7,300   → แนวโน้มเติบโตยังคงต่อเนื่อง
May:      $6,800   → ยอดขายเริ่มคงที่
```

**วางแผนแคมเปญ:**

- **ช่วง Q1 ที่ชะลอตัว** — เปิดแคมเปญ "Spring Sale" ในเดือนกุมภาพันธ์เพื่อเพิ่มยอดขายในเดือนมีนาคม/เมษายน
- **เตรียมตัวสำหรับเทศกาล** — รับสมัครพันธมิตรใหม่ในเดือนกันยายน/ตุลาคมเพื่อเตรียมตัวสำหรับยอดขายเทศกาลใน Q4
- **วางแผนสต็อกสินค้า** — เพิ่มสต็อกก่อนที่ยอดขายที่ขับเคลื่อนโดยพันธมิตรจะเพิ่มขึ้น

## เคล็ดลับ

- ตรวจสอบ **แดชบอร์ดผู้ขายทุกวัน** เพื่อจับการสมัครที่ยังไม่ได้รับการตรวจสอบและค่าคอมมิชชันก่อนที่จะสะสมมากเกินไป — การตรวจสอบทุกวันเพียง 5 นาทีมีประสิทธิภาพมากกว่าการตรวจสอบทุกสัปดาห์ 2 ชั่วโมง
- ใช้ **แผนภูมิรายได้เพื่อตรวจสอบการเปลี่ยนแปลงของโปรแกรม** — หากคุณปรับอัตราค่าคอมมิชชัน ให้เปรียบเทียบช่วง 30 วันก่อนและหลังการเปลี่ยนแปลงเพื่อวัดผลกระทบ
- **ส่งออกข้อมูลค่าคอมมิชชันรายเดือน** และเก็บรายงานไว้ในระบบบัญชีของคุณเพื่อเตรียมภาษีและทำนายรายได้ได้ง่ายขึ้น
- ติดต่อ **พันธมิตร 3 อันดับแรกทุกไตรมาส** เพื่อรักษาความสัมพันธ์และรวบรวมข้อเสนอแนะเกี่ยวกับการปรับปรุงโปรแกรม
- จับตาดู **การเพิ่มขึ้นของยอดขายในแผนภูมิรายได้** และตรวจสอบว่าสาเหตุคืออะไร — แคมเปญที่ประสบความสำเร็จสามารถนำไปใช้กับพันธมิตรอื่นหรือในฤดูกาลถัดไปได้
- ตั้งค่า **กิจวัตรการตรวจสอบรายเดือน**: สัปดาห์ที่ 1 = ตรวจสอบสถิติ, สัปดาห์ที่ 2 = ติดต่อผู้มีผลงานสูงสุด, สัปดาห์ที่ 3 = สนับสนุนผู้มีผลงานต่ำ, สัปดาห์ที่ 4 = วางแผนแคมเปญในเดือนถัดไป
- เปรียบเทียบ **จำนวนคลิกกับจำนวนค่าคอมมิชชัน** สำหรับแต่ละพันธมิตรเพื่อระบุคุณภาพของการเปลี่ยนผ่าน — พันธมิตรที่มีคลิก 5,000 ครั้งแต่มีค่าคอมมิชชันเพียง 10 ครั้งอาจกำลังดึงดูดผู้ใช้ที่มีคุณภาพต่ำ
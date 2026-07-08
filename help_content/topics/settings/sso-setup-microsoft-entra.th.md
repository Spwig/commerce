---
title: 'การตั้งค่า SSO: Microsoft Entra ID'
---

คู่มือนี้จะช่วยคุณผ่านขั้นตอนการเชื่อมต่อ Spwig กับ Microsoft Entra ID (เดิมคือ Azure Active Directory) เพื่อให้สามารถเข้าสู่ระบบแบบ single sign-on สำหรับผู้ดูแลระบบ เมื่อตั้งค่าเสร็จสิ้น บุคลากรของคุณสามารถเข้าสู่ระบบแดชบอร์ดผู้ดูแลระบบของ Spwig ด้วยบัญชีงาน Microsoft ของพวกเขา

**หมายเหตุ:** Microsoft อาจอัปเดตอินเทอร์เฟซของศูนย์บริหารจัดการ Entra ตามเวลาที่ผ่านไป คำแนะนำนี้ถูกเขียนขึ้นโดยอิงจากอินเทอร์เฟซในช่วงต้นปี 2026 หากมีขั้นตอนใดที่แตกต่างจากสิ่งที่คุณเห็น กรุณาอ้างอิงเอกสารทางการของ Microsoft เกี่ยวกับ [การลงทะเบียนแอปพลิเคชันกับ Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)

## ข้อกำหนดเบื้องต้น

- การสมัครสมาชิก Azure ที่มีการเข้าถึง Microsoft Entra ID
- บทบาท **Application Administrator** หรือ **Global Administrator** ในผู้เช่าของ Entra ID ของคุณ
- URL ร้านค้า Spwig ของคุณ (เช่น `https://your-store.com`)
- บุคลากรต้องมีที่อยู่อีเมลใน Spwig ที่ตรงกับบัญชี Microsoft ของพวกเขา

## ขั้นตอนที่ 1: ลงทะเบียนแอปพลิเคชัน

1. เข้าสู่ระบบกับ [Microsoft Entra admin center](https://entra.microsoft.com)
2. ไปที่ **Identity > Applications > App registrations**
3. คลิก **New registration**
4. ตั้งค่าการลงทะเบียน:

| Field | Value |
|-------|-------|
| **Name** | `Spwig Admin SSO` (หรือชื่อใดก็ตามที่คุณต้องการ) |
| **Supported account types** | **Accounts in this organizational directory only** (Single tenant) |
| **Redirect URI** | Platform: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. คลิก **Register**

**สำคัญ:** URI สำหรับการเปลี่ยนเส้นทางต้องตรงกับ `https://your-store.com/oidc/callback/` อย่างแน่นอน — รวมถึงเครื่องหมาย slash ที่อยู่ด้านท้าย แทนที่ `your-store.com` ด้วยโดเมนร้านค้าจริงของคุณ

## ขั้นตอนที่ 2: จดจำ Application IDs

หลังจากลงทะเบียน คุณจะเห็นหน้า **Overview** ของแอปพลิเคชัน จดจำค่าสองค่าเหล่านี้ — คุณจะต้องใช้它们ในภายหลัง:

| ค่า | หาได้จากที่ไหน | ใช้เพื่ออะไร |
|-------|-----------------|---------------|
| **Application (client) ID** | หน้าภาพรวม หัวข้อส่วนบน | ใส่เป็น **Client ID** ใน Spwig |
| **Directory (tenant) ID** | หน้าภาพรวม หัวข้อส่วนบน | ใช้สร้าง URL สำหรับการค้นหา |

## ขั้นตอนที่ 3: สร้าง Client Secret

1. ในการลงทะเบียนแอป ให้ไปที่ **Certificates & secrets**
2. คลิก **New client secret**
3. ใส่คำอธิบาย (เช่น, `Spwig SSO`) และเลือกช่วงเวลาหมดอายุ
4. คลิก **Add**
5. **คัดลอกค่าทันที** — ค่าดังกล่าวจะแสดงเพียงครั้งเดียวเท่านั้น นี่คือ client secret ที่คุณจะใส่ใน Spwig

**อย่าคัดลอก Secret ID** — คุณต้องคอลัมน์ **Value** ไม่ใช่คอลัมน์ ID

**ตั้งค่าการแจ้งเตือน** เพื่อหมุนเวียน secret ก่อนที่จะหมดอายุ เมื่อ secret หมดอายุ การ SSO จะหยุดทำงานจนกว่าคุณจะสร้างใหม่และอัปเดตใน Spwig

## ขั้นตอนที่ 4: ตั้งค่า API Permissions

1. ไปที่ **API permissions**
2. ตรวจสอบว่า **Microsoft Graph > User.Read** (delegated) ถูกเพิ่มไว้แล้ว นี่คือค่าเริ่มต้น
3. หาก `openid`, `email`, และ `profile` ยังไม่ได้ถูกเพิ่ม ให้คลิก **Add a permission > Microsoft Graph > Delegated permissions** และเพิ่มพวกมัน
4. คลิก **Grant admin consent for [your organization]** หากมีการแจ้งเตือน

## ขั้นตอนที่ 5: สร้าง URL สำหรับการค้นหา (Discovery URL)

URL สำหรับการค้นหา OIDC มีรูปแบบดังนี้:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

แทนที่ `{tenant-id}` ด้วย **Directory (tenant) ID** จากขั้นตอนที่ 2

ตัวอย่าง: หาก ID ของคุณคือ `a1b2c3d4-e5f6-7890-abcd-ef1234567890` URL สำหรับการค้นหาคือ:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## ขั้นตอนที่ 6: ตั้งค่า Group Claims (ไม่จำเป็น)

หากคุณต้องการให้ Spwig กำหนดสถานะพนักงานหรือ superuser ตามการเป็นสมาชิกกลุ่มใน Entra ID:

1.

ในการลงทะเบียนแอป ให้ไปที่ **Token configuration**
2.

คลิก **Add groups claim**
3.



เลือกประเภทกลุ่มที่ต้องการรวม (โดยทั่วไปคือ **Security groups**)
4.

ภายใต้ **Customize token properties by type**, สำหรับ **ID** token เลือก **Group ID**
5.

คลิก **Add**

**Important:** Entra ID ส่ง **Object IDs** ของกลุ่ม (UUIDs เช่น `a1b2c3d4-...`) ไม่ใช่ชื่อกลุ่มที่แสดงผล เมื่อตั้งค่าการจับคู่บทบาทใน Spwig คุณต้องใช้ Object IDs เหล่านี้

เพื่อค้นหา Object ID ของกลุ่ม:
1. ใน Entra admin center ไปที่ **Identity > Groups > All groups**
2. คลิกกลุ่ม
3. คัดลอก **Object ID** จากหน้าต่างสรุปของกลุ่ม

### Group Limit
Microsoft Entra ID รวมกลุ่มสูงสุด **200 groups** ใน token หากผู้ใช้อยู่ในกลุ่มมากกว่า 200 กลุ่ม ข้อมูลกลุ่มจะถูกแทนที่ด้วยลิงก์ไปยัง Microsoft Graph API สำหรับองค์กรที่มีกลุ่มจำนวนมาก ควรสร้างกลุ่มความปลอดภัยเฉพาะสำหรับการเข้าถึง Spwig และใช้ [group filtering](https://learn.microsoft.com/en-us/entra/identity/platform/optional-claims-reference) เพื่อจำกัดกลุ่มที่ต้องการรวม

## Step 7: Configure in Spwig

1. ใน Spwig admin ไปที่ **Enterprise SSO > SSO Provider Configuration**
2. ตั้งค่า **Provider Name** เป็น `Microsoft Entra ID`
3. วาง URL การค้นพบจากขั้นตอนที่ 5 ลงใน **OIDC Discovery URL**
4. คลิก **Auto-Discover** — นี่จะเติมฟิลด์ปลายทางทั้งหมดอัตโนมัติ
5. ใส่ **Client ID** จากขั้นตอนที่ 2
6. ใส่ **Client Secret** (ค่า) จากขั้นตอนที่ 3
7. หากคุณตั้งค่าการเรียกร้องกลุ่มในขั้นตอนที่ 6:
   - ตั้งค่า **Groups Claim** เป็น `groups`
   - ใน **Staff Groups** ใส่ Object IDs ของกลุ่มที่สมาชิกควรเป็นพนักงาน (คั่นด้วยเครื่องหมายจุลภาค)
   - ใน **Superuser Groups** ใส่ Object IDs ของกลุ่มที่สมาชิกควรเป็นผู้ใช้ระดับผู้ดูแล (คั่นด้วยเครื่องหมายจุลภาค)
8. คลิก **Save**

## Step 8: Enable and Test

1.

ไปที่ **Site Settings > Security** tab
2.

ตรวจสอบ **Enable SSO for admin login**
3.

คลิก **Save**
4.

เปิดหน้า login ของ admin ใน **private/incognito window**
5.

คุณควรเห็นปุ่ม **Sign in with Microsoft Entra ID**
6.


# 4. ตั้งค่า SSO ด้วย Microsoft Entra ID

คลิกที่ — คุณควรจะถูกเปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบของ Microsoft
7.

เข้าสู่ระบบด้วยบัญชี Microsoft ที่มีอีเมลตรงกับผู้ใช้พนักงานใน Spwig
8.

คุณควรจะถูกเปลี่ยนเส้นทางกลับไปยังแดชบอร์ดของ Spwig admin

## ปัญหาที่พบบ่อย

| ปัญหา | สาเหตุ | วิธีแก้ไข |
|---------|-------|----------|
| **AADSTS50011: URI การเปลี่ยนเส้นทางไม่ตรงกัน** | URI การเปลี่ยนเส้นทางใน Entra ไม่ตรงกันทั้งหมด | ตรวจสอบให้แน่ใจว่า URI การเปลี่ยนเส้นทางคือ `https://your-store.com/oidc/callback/` พร้อมกับเครื่องหมาย slash ที่ปลายทาง ตรวจสอบความไม่ตรงกันระหว่าง HTTP และ HTTPS |
| **AADSTS700016: แอปพลิเคชันไม่พบ** | Client ID หรือ tenant ผิด | ตรวจสอบ Client ID อีกครั้ง และตรวจสอบให้แน่ใจว่า URL การค้นพบใช้ tenant ID ที่ถูกต้อง |
| การเข้าสู่ระบบสำเร็จที่ Microsoft แต่ล้มเหลวที่ Spwig | ไม่มีผู้ใช้ที่ตรงกันใน Spwig | ตรวจสอบให้แน่ใจว่ามีบัญชีพนักงานใน Spwig ที่มีอีเมลเดียวกับบัญชี Microsoft ตรวจสอบว่าผู้ใช้มีสถานะพนักงานหากเปิดใช้งานตัวเลือก Restrict to Staff |
| **กลุ่ม claim เป็นว่างเปล่า** | กลุ่ม claim ไม่ได้ตั้งค่า | ทำตามขั้นตอนที่ 6 เพื่อเพิ่มกลุ่ม claim ลงในการตั้งค่าโทเคน |
| **กลุ่ม claim คืนค่า URL แทน ID** | ผู้ใช้อยู่ในกลุ่มมากกว่า 200 กลุ่ม | ใช้การกรองกลุ่มเพื่อจำกัดจำนวนกลุ่มในโทเคน หรือกำหนดกลุ่มเฉพาะ |
| **SSO หยุดทำงานหลังจากผ่านไปหลายเดือน** | Secret ของ Client หมดอายุ | สร้าง secret ของ Client ใหม่ใน Entra และอัปเดตในการตั้งค่า SSO Provider ของ Spwig |

## เคล็ดลับ

- **ใช้กลุ่มความปลอดภัย** สำหรับการจัดการบทบาท ไม่ใช่ Microsoft 365 groups หรือ distribution lists.

กลุ่มความปลอดภัยถูกออกแบบมาสำหรับการควบคุมการเข้าถึง และทำงานได้อย่างน่าเชื่อถือที่สุดกับ claim OIDC.
- **แนะนำให้ใช้ single tenant** — การเลือก "Accounts in this organizational directory only" จะจำกัด SSO ให้กับผู้ใช้ในองค์กรของคุณเท่านั้น.


# การตั้งค่าหลายผู้ใช้ต้องการการตรวจสอบเพิ่มเติม
- **ตั้งค่าการหมดอายุของ secret ให้ยาวนาน** — เลือก 24 เดือนเมื่อสร้าง client secret และตั้งการแจ้งเตือนในปฏิทินที่ 22 เดือนเพื่อหมุนเวียนมัน
- **การเข้าถึงแบบมีเงื่อนไข** — คุณสามารถสร้างนโยบายการเข้าถึงแบบมีเงื่อนไขใน Entra ID ที่ใช้กับการลงทะเบียนแอป Spwig ได้อย่างเฉพาะเจาะจง

ตัวอย่างเช่น กำหนดให้ต้องใช้ MFA ปิดการเข้าสู่ระบบจากสถานที่ที่ไม่น่าเชื่อถือ หรือกำหนดให้ต้องใช้อุปกรณ์ที่เป็นไปตามข้อกำหนด
- **ทดสอบด้วยบัญชีที่ไม่ใช่ผู้ดูแล** — สร้างบัญชีพนักงานทดสอบใน Spwig เพื่อตรวจสอบว่า SSO ทำงานได้ก่อนที่จะเปิดใช้งานกับทีมทั้งหมดของคุณ
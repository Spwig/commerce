---
title: 'การตั้งค่า SSO: Google Workspace'
---

คู่มือนี้จะพาคุณผ่านขั้นตอนการเชื่อมต่อ Spwig กับ Google Workspace เพื่อใช้งาน Single Sign-On (SSO) สำหรับผู้ดูแลระบบ เมื่อตั้งค่าเสร็จสิ้น บุคลากรของคุณสามารถเข้าสู่ระบบในแดชบอร์ด Spwig ด้วยบัญชี Google Workspace ของตนเอง

**หมายเหตุ:** Google อาจอัปเดตอินเทอร์เฟซ Cloud Console ตามเวลา คำแนะนำนี้ถูกเขียนขึ้นโดยอิงจากอินเทอร์เฟซในช่วงต้นปี 2026 หากมีขั้นตอนใดที่แตกต่างจากที่คุณเห็น กรุณาอ้างอิงเอกสารทางการของ Google เกี่ยวกับ [การตั้งค่า OAuth 2.0](https://support.google.com/cloud/answer/6158849)

## ข้อกำหนดเบื้องต้น

- การสมัครสมาชิก Google Workspace (Google Workspace Business, Enterprise หรือ Education)
- การเข้าถึงผู้ดูแลระบบใน [Google Cloud Console](https://console.cloud.google.com)
- URL ร้านค้า Spwig ของคุณ (เช่น `https://your-store.com`)
- บุคลากรต้องมีอีเมลใน Spwig ที่ตรงกับบัญชี Google Workspace ของพวกเขา

## ขั้นตอนที่ 1: สร้างหรือเลือกโครงการ Google Cloud

1. ไปที่ [Google Cloud Console](https://console.cloud.google.com)
2. คลิกที่ตัวเลือกโครงการในแถบด้านบน
3. คลิก **New Project** (หรือเลือกโครงการที่มีอยู่หากคุณต้องการ)
4. ใส่ชื่อโครงการ (เช่น `Spwig SSO`)
5. เลือกองค์กรของคุณ
6. คลิก **Create**

## ขั้นตอนที่ 2: ตั้งค่าหน้า OAuth Consent

1. ใน Cloud Console ให้ไปที่ **APIs & Services > OAuth consent screen**
2. เลือก **Internal** เป็นประเภทผู้ใช้ — นี่จะจำกัดการเข้าสู่ระบบให้กับผู้ใช้ภายในองค์กร Google Workspace ของคุณเท่านั้น
3. คลิก **Create**
4. กรอกข้อมูลที่จำเป็น:

| Field | Value |
|-------|-------|
| **App name** | `Spwig Admin` (หรือชื่อร้านค้าของคุณ) |
| **User support email** | อีเมลผู้ดูแลระบบของคุณ |
| **Authorized domains** | `your-store.com` (โดเมนร้านค้าของคุณ โดยไม่ต้องมี `https://`) |
| **Developer contact email** | อีเมลผู้ดูแลระบบของคุณ |

5. คลิก **Save and Continue**
6. บนหน้า **Scopes** คลิก **Add or Remove Scopes** และเพิ่ม:
   - `openid`
   - `email`
   - `profile`
7. คลิก **Save and Continue**
8. ตรวจสอบสรุปและคลิก **Back to Dashboard**

## ขั้นตอนที่ 3: สร้าง OAuth Credentials

1. ไปที่ **APIs & Services > Credentials**
2. คลิก **Create Credentials > OAuth client ID**
3. ตั้งค่าไคลเอนต์:

| Field | Value |
|-------|-------|
| **Application type** | Web application |
| **Name** | `Spwig SSO` |
| **Authorized redirect URIs** | `https://your-store.com/oidc/callback/` |

4. คลิก **Create**
5. หน้าต่างจะแสดง **Client ID** และ **Client Secret** ของคุณ — คัดลอกค่าทั้งสอง คุณยังสามารถดาวน์โหลดเป็นไฟล์ JSON เพื่อเก็บไว้ในที่ปลอดภัยได้ด้วย

**Important:** URI สำหรับการเปลี่ยนเส้นทางต้องตรงกับ `https://your-store.com/oidc/callback/` อย่างแม่นยำ — รวมถึงเครื่องหมายชื่อ `https://` และ slash ที่อยู่ท้าย ให้เปลี่ยน `your-store.com` เป็นโดเมนของร้านค้าจริงของคุณ

## ขั้นตอนที่ 4: รับ Discovery URL

Google ใช้ URL สำหรับการค้นพบเดียวที่เป็นมาตรฐานสำหรับผู้เช่าทั้งหมดใน Workspace:

```
https://accounts.google.com/.well-known/openid-configuration
```

URL นี้เหมือนกันสำหรับองค์กร Google Workspace ทุกแห่ง — คุณไม่จำเป็นต้องปรับแต่งมันด้วยผู้เช่าหรือโดเมน

## ขั้นตอนที่ 5: ตั้งค่าใน Spwig

1. ในแดชบอร์ดของ Spwig ให้ไปที่ **Enterprise SSO > SSO Provider Configuration**
2. ตั้งค่า **Provider Name** เป็น `Google Workspace`
3. ใส่ Discovery URL: `https://accounts.google.com/.well-known/openid-configuration`
4. คลิก **Auto-Discover** — นี่จะเติมฟิลด์ปลายทางทั้งหมดอัตโนมัติ
5. ใส่ **Client ID** จากขั้นตอนที่ 3
6. ใส่ **Client Secret** จากขั้นตอนที่ 3
7. คลิก **Save**

### Claims Mapping

Google ใช้ชื่อ claim ตามมาตรฐาน OIDC ดังนั้นการตั้งค่าเริ่มต้นของ Spwig จึงทำงานได้ทันที:

| Spwig Setting | Google Claim | Default Value |
|---------------|-------------|---------------|
| Email Claim | `email` | `email` |
| First Name Claim | `given_name` | `given_name` |
| Last Name Claim | `family_name` | `family_name` |

ไม่จำเป็นต้องปรับแต่งการจับคู่ claim

## ขั้นตอนที่ 6: เปิดใช้งานและทดสอบ

1.

ไปที่ **Site Settings > Security** tab
2.

ตรวจสอบ **Enable SSO for admin login**
3.

คลิก **Save**
4.


เปิดหน้าเข้าสู่ระบบผู้ดูแลระบบใน **private/incognito window**
5.

คุณควรเห็นปุ่ม **Sign in with Google Workspace**
6.

คลิกที่ปุ่ม — คุณควรจะถูกเปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบของ Google
7.

เข้าสู่ระบบด้วยบัญชี Google Workspace ที่อีเมลตรงกับผู้ใช้พนักงานใน Spwig
8.

คุณควรจะถูกเปลี่ยนเส้นทางกลับไปยังแดชบอร์ดผู้ดูแลระบบของ Spwig

## การจัดการบทบาทตามกลุ่ม

ต่างจาก Microsoft Entra ID หรือ Okta ที่ Google ไม่ได้รวมการเป็นสมาชิกของกลุ่มในโทเค็น OIDC มาตรฐานโดยค่าเริ่มต้น การใช้กลุ่มคลเรม (claims) กับ Google จำเป็นต้องใช้ Google Workspace Directory API และการตั้งค่าเพิ่มเติมนอกเหนือจาก OIDC ทั่วไป

สำหรับการติดตั้ง Google Workspace ส่วนใหญ่ เราแนะนำให้จัดการสถานะพนักงานและผู้ใช้ระดับสูงโดยตรงใน Spwig แทนที่จะใช้การจัดการบทบาทอัตโนมัติผ่านกลุ่ม:

1. สร้างบัญชีพนักงานใน Spwig พร้อมสิทธิ์ที่เหมาะสม
2. ใช้ระบบบทบาทพนักงานของ Spwig เพื่อควบคุมระดับการเข้าถึง
3. พนักงานเข้าสู่ระบบผ่าน SSO และ Spwig จะใช้สิทธิ์ที่มีอยู่ของพวกเขา

หากคุณต้องการการจัดการบทบาทอัตโนมัติผ่านกลุ่ม โปรดอ้างอิง [เอกสารการตั้งค่า API Directory ของ Google Workspace Admin SDK](https://developers.google.com/admin-sdk/directory) สำหรับการกำหนดค่าคลเรมแบบกำหนดเอง

## ปัญหาที่พบบ่อย

| ปัญหา | สาเหตุ | วิธีแก้ไข |
|---------|-------|----------|
| **ข้อผิดพลาด 400: redirect_uri_mismatch** | URI สำหรับการเปลี่ยนเส้นทางใน Google Cloud ไม่ตรงกันทั้งหมด | ตรวจสอบให้แน่ใจว่า URI สำหรับการเปลี่ยนเส้นทางคือ `https://your-store.com/oidc/callback/` พร้อมด้วยเครื่องหมาย slash ที่ปลายทาง ตรวจสอบว่าใช้ HTTP หรือ HTTPS อย่างถูกต้อง |
| **ข้อผิดพลาด 403: access_denied** | ผู้ใช้ไม่ได้อยู่ในองค์กร Google Workspace | เมื่อใช้ประเภทผู้ใช้ "Internal" ผู้ใช้ในองค์กรของคุณเท่านั้นที่สามารถเข้าสู่ระบบได้ ตรวจสอบว่าบัญชีผู้ใช้เป็นส่วนหนึ่งของโดเมน Workspace ของคุณ |
| **หน้าอนุญาต OAuth แสดงข้อความ "แอปนี้ยังไม่ได้รับการยืนยัน"** | เป็นเรื่องปกติสำหรับแอป Internal | การเตือนนี้เป็นเรื่องปกติสำหรับแอป Internal และไม่ส่งผลต่อการทำงาน ผู้ใช้ในองค์กรของคุณยังสามารถเข้าสู่ระบบได้ |
| **การเข้าสู่ระบบสำเร็จที่ Google แต่ล้มเหลวที่ Spwig** | ไม่มีผู้ใช้ที่ตรงกันใน Spwig | ตรวจสอบให้แน่ใจว่ามีบัญชีพนักงานใน Spwig ที่มีอีเมลเดียวกับบัญชี Google Workspace ตรวจสอบว่าการตั้งค่า "จำกัดเฉพาะพนักงาน" ถูกตั้งค่าอย่างถูกต้อง |
| **"การเข้าถึงถูกบล็อก: คำขอของแอปนี้ไม่ถูกต้อง"** | Scope ไม่ได้ตั้งค่าอย่างถูกต้อง | ตรวจสอบให้แน่ใจว่า scope `openid`, `email`, และ `profile` ถูกเพิ่มในหน้าอนุญาต OAuth |

## เคล็ดลับ

- **ใช้ประเภทผู้ใช้ "Internal"** — นี่จะจำกัดการเข้าสู่ระบบให้เป็นเฉพาะองค์กร Google Workspace ของคุณ และไม่จำเป็นต้องผ่านกระบวนการตรวจสอบของ Google
- **คีย์ลับของ Google client ไม่มีวันหมดอายุ** — ต่างจาก Microsoft Entra ID คีย์ลับของ OAuth ของ Google ไม่มีวันหมดอายุ อย่างไรก็ตาม คุณสามารถหมุนเวียนคีย์ลับได้ทุกเมื่อจากหน้า Credentials
- **ใช้โครงการเดียวสำหรับแอปหลายตัว** — คุณสามารถสร้าง ID ของผู้ใช้ OAuth หลายตัวภายในโครงการ Google Cloud เดียวกันได้ หากคุณมีการติดตั้ง Spwig หลายตัว
- **ทดสอบด้วยบัญชีที่ไม่ใช่ผู้ดูแลระบบ** — สร้างบัญชีพนักงานทดสอบใน Spwig และใช้ผู้ใช้ Google Workspace ทั่วไป (ไม่ใช่ผู้ดูแลระบบหลัก) เพื่อตรวจสอบว่า SSO ทำงานตามที่คาดไว้
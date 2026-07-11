<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.vi.md">Tiếng Việt</a> |
  <strong>ไทย</strong>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>อีคอมเมิร์ซแบบ self-hosted สำหรับร้านค้าที่ต้องการเป็นเจ้าของร้านของตนเอง</strong>
</p>

<p align="center">
  <a href="https://spwig.com">เว็บไซต์</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">เอกสารประกอบ</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">ชุมชน</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/th/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/th/demos">เดโมสด</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Spwig คืออะไร?

Spwig เป็นแพลตฟอร์มอีคอมเมิร์ซที่มีฟีเจอร์ครบครัน ได้แก่ แคตตาล็อก ตะกร้าสินค้า การชำระเงิน คำสั่งซื้อ ลูกค้า ระบบชำระเงิน การจัดส่ง ธีม เครื่องมือสร้างหน้าเว็บ API สำหรับผู้ดูแลระบบ POS การสมัครสมาชิก ระบบสมาชิกสะสมคะแนน บล็อก SEO ครบทั้งสแตก สร้างด้วย **Django 5**, **PostgreSQL** และ **Redis** จัดส่งเป็นชุด Docker containers ทำงานได้บน VPS ราคา $5 หรือบนเครื่องของคุณเอง

ต่างจากแพลตฟอร์มแบบโฮสต์ **คุณเป็นเจ้าของโค้ด ฐานข้อมูล และข้อมูลลูกค้า** ไม่มีค่าธรรมเนียมต่อรายการธุรกรรม ไม่มีการผูกมัด หากคุณต้องการ fork โปรเจกต์และไปในทางของคุณเอง สัญญาอนุญาตอนุญาตให้ทำได้อย่างชัดเจน

<br />

## เอดิชัน

ไบนารีเดียวกัน ไฟล์สัญญาอนุญาตที่ลงนามจะสลับ feature flags ในขณะรันไทม์ Community คือสิ่งที่คุณได้รับโดยค่าเริ่มต้นเมื่อรัน `docker compose up` การอัปเกรดคือคีย์ที่คุณวางในหน้าผู้ดูแลระบบ

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| อีคอมเมิร์ซครบครัน ธีม เครื่องมือสร้างหน้าเว็บ UI ของ POS | ✓ | ✓ | ✓ |
| นำผู้ให้บริการชำระเงินของคุณเองมาใช้ | ✓ | ✓ | ✓ |
| นำผู้ให้บริการจัดส่งของคุณเองมาใช้ | ✓ | ✓ | ✓ |
| การเข้าถึง Marketplace (ธีมพรีเมียม + integrations) | ✓ | ✓ | ✓ |
| ระบบเติมที่อยู่อัตโนมัติที่โฮสต์โดย Spwig | ฟรี · จำกัดอัตรา | จำกัดสูงขึ้น | จำกัดสูงสุด |
| GeoIP ที่โฮสต์โดย Spwig (ตำแหน่งผู้เข้าชม) | ฟรี · จำกัดอัตรา | จำกัดสูงขึ้น | จำกัดสูงสุด |
| การแจ้งเตือนแบบ push (แอปผู้ดูแลระบบบน iOS) | ฟรี · จำกัดอัตรา | จำกัดสูงขึ้น | จำกัดสูงสุด |
| จุดขาย (รองรับเทอร์มินัล POS) | ✓ | ✓ | ✓ |
| เกตเวย์อีเมลที่โฮสต์พร้อม warm IPs + DKIM | – | ✓ | ✓ |
| การสนับสนุนแบบมีลำดับความสำคัญ | – | ✓ | ✓ |
| SSO สำหรับองค์กร (Azure AD, Okta) | – | – | ✓ |

<br />

## เริ่มต้นอย่างรวดเร็ว

### ตัวเลือกที่ 1 — ติดตั้งด้วยคำสั่งบรรทัดเดียว (แนะนำ)

[ตัวติดตั้ง Spwig](https://github.com/Spwig/spwig) จะตั้งค่าทุกอย่างในคำสั่งเดียว ได้แก่ Docker, PostgreSQL, Redis, MinIO, TLS ผ่าน Cloudflare หรือแบบ self-signed, wizard สำหรับการบูตครั้งแรก และผู้ใช้ผู้ดูแลระบบ อิมเมจที่ลงนามจะถูกดึงจาก `registry.spwig.com`

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

การอัปเกรดเกิดขึ้นผ่านหน้าผู้ดูแลระบบ ดูรายละเอียดที่ [UPGRADING.md](UPGRADING.md)

### ตัวเลือกที่ 2 — จากซอร์สโค้ด

หากคุณต้องการสร้างจาก repo นี้ แฮ็กกับมัน หรือส่งมอบ fork:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

หน้าร้านอยู่ที่ `http://localhost` และหน้าผู้ดูแลระบบอยู่ที่ `http://localhost/th/admin/` Community edition จะเปิดใช้งานอัตโนมัติในการบูตครั้งแรก โดยไม่ต้องเชื่อมต่อกับเซิร์ฟเวอร์สัญญาอนุญาต และไม่ต้องใช้คีย์ อัปเกรดภายหลังด้วย `git pull` และ `docker compose build`

<br />

## ฟีเจอร์

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>หน้าร้านและการชำระเงิน</h3>
      <p>เรนเดอร์ฝั่งเซิร์ฟเวอร์โดยค่าเริ่มต้น รวดเร็วในการโหลดไบต์แรก ทำงานได้โดยไม่ต้องใช้ JavaScript ออกแบบให้เหมาะกับมือถือก่อน (80% ของทราฟฟิกมาจากหน้าจอขนาดเล็ก) โหมด headless เป็นทางเลือก ผ่าน
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> และ <a href="https://github.com/Spwig/react">React
      components</a></p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/storefront-product.webp" alt="Storefront product page">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/page-builder.webp" alt="Page builder">
    </td>
    <td width="50%" valign="top">
      <h3>เครื่องมือสร้างหน้าเว็บ</h3>
      <p>ร้านค้าสร้างหน้าร้านจากวิดเจ็ตที่ใช้ซ้ำได้ ได้แก่ ส่วนฮีโร่ ตารางสินค้า คำรับรอง embeds และดูตัวอย่างสดในหน้าผู้ดูแลระบบ วิดเจ็ตติดตั้งจาก marketplace หรือจากคลังคอมโพเนนต์ของคุณเอง</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>การจัดการคำสั่งซื้อและลูกค้า</h3>
      <p>ทุกคำสั่งซื้อ การคืนเงิน การต่ออายุการสมัครสมาชิก การดาวน์โหลดดิจิทัล และจุดสัมผัสของลูกค้าอยู่ในที่เดียว รองรับการดำเนินการแบบกลุ่ม บทบาทของพนักงานที่จำกัดด้วยสิทธิ์ ส่งออกเป็น CSV/XLSX และแอปผู้ดูแลระบบบนมือถือ (iOS) พร้อมการแจ้งเตือนแบบ push</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/order-management.webp" alt="Order management">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/branding-builder.webp" alt="Branding builder">
    </td>
    <td width="50%" valign="top">
      <h3>ธีมและแบรนดิ้ง</h3>
      <p>Design tokens (สี ตัวอักษร ระยะห่าง) ควบคุมทุกพื้นผิว ทั้งหน้าร้านและหน้าผู้ดูแลระบบ เปลี่ยน token หนึ่งครั้ง ทุกอย่างจะอัปเดต ธีมอยู่ที่
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      และติดตั้งผ่าน marketplace หรือเขียนธีมของคุณเองด้วย
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>จุดขาย</h3>
      <p>เทอร์มินัล POS แบบเต็มรูปแบบสำหรับร้านค้าหน้าร้านจริง รองรับการสแกนบาร์โค้ด การชำระเงินแบบแยก การพิมพ์ใบเสร็จ การรวมกับลิ้นชักเงินสด จอแสดงผลที่หันหน้าเข้าหาลูกค้า และโหมดออฟไลน์ Community edition มีโค้ดมาให้ แต่หน้าผู้ดูแลระบบแสดง CTA สำหรับการอัปเกรด แพตช์ออกได้หากคุณ fork ไม่เป็นไร</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/pos-terminal.webp" alt="POS terminal">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/developer-portal.webp" alt="Developer portal">
    </td>
    <td width="50%" valign="top">
      <h3>ระบบนิเวศของผู้ให้บริการ</h3>
      <p>สิ่งใดก็ตามที่สื่อสารกับระบบภายนอก ได้แก่ การชำระเงิน การจัดส่ง อัตราแลกเปลี่ยน การแปลภาษา GeoIP SMS อีเมล เป็นผู้ให้บริการที่เสียบเข้าได้ สร้างของคุณเองด้วย
      <a href="https://github.com/Spwig/provider-sdks">provider SDKs</a>
      เผยแพร่ไปยัง marketplace หรือ self-host registry ส่วนตัว</p>
    </td>
  </tr>
</table>

<br />

## สถาปัตยกรรม

- **Single-tenant** การติดตั้งแต่ละครั้งคือหนึ่งร้าน หนึ่งร้านค้า หนึ่ง Django Site ร้านค้าที่มีหลายร้านจะรัน Spwig หนึ่งการติดตั้งต่อร้าน
- **Modular monolith** ไม่ใช่ mesh ของ microservice แต่เป็นโพรเซส Django เดียวที่จัดการหน้าร้าน + หน้าผู้ดูแลระบบ + REST API + Celery workers ง่ายต่อการดีพลอย ทำความเข้าใจ และ fork
- **ประตูฟีเจอร์แบบรันไทม์** Community/Pro/Enterprise รันไบนารีเดียวกันทั้งหมด สัญญาอนุญาตที่ลงนามจะสลับ flags โดยไม่มีการตัดโค้ดออก

ทัวร์ฉบับเต็ม: [ARCHITECTURE.md](ARCHITECTURE.md)

<br />

## ชุมชนและการสนับสนุน

- **Discussions** คำถามปลายเปิด ไอเดีย show-and-tell:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions)
- **ฟอรัมชุมชน** [community.spwig.com](https://community.spwig.com)
  เธรดยาว สูตรแนวปฏิบัติที่ดี การนำเสนอส่วนขยาย
- **รายงานบั๊ก** [Issues](https://github.com/Spwig/commerce/issues)
  พร้อมขั้นตอนการทำซ้ำ ดู [SECURITY.md](SECURITY.md) สำหรับการเปิดเผยช่องโหว่
- **การสนับสนุนเชิงพาณิชย์** มีให้สำหรับสัญญาอนุญาต Pro และ Enterprise

<br />

## การมีส่วนร่วม

เราใช้ **DCO** (Developer Certificate of Origin) ทุก commit จะถูกลงนามด้วย `git commit -s` ไม่มีเอกสาร ไม่มี CLA คู่มือฉบับเต็มที่ [CONTRIBUTING.md](CONTRIBUTING.md)

บันทึกสำหรับผู้ช่วยเขียนโค้ดด้วย AI ที่ทำงานกับ repo นี้อยู่ที่ [CLAUDE.md](CLAUDE.md)

<br />

## ระบบนิเวศ

โปรเจกต์โอเพนซอร์สที่เกี่ยวข้องภายใต้ [Spwig org](https://github.com/Spwig):

| Repo | คำอธิบาย |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Repo นี้ แพลตฟอร์มหลัก (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | ตัวติดตั้งบรรทัดเดียว |
| [Spwig/components](https://github.com/Spwig/components) | ธีม integrations และยูทิลิตี้ (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK สำหรับสร้างธีม (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDKs สำหรับสร้างผู้ให้บริการชำระเงิน / จัดส่ง / ฯลฯ (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | SDK สำหรับไคลเอนต์ headless / API (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | ไลบรารีคอมโพเนนต์ React (Apache-2.0) |

<br />

## สัญญาอนุญาต

Spwig เป็น [AGPL-3.0-or-later](LICENSE) คุณสามารถรัน แก้ไข แจกจ่าย เสนอเป็นบริการโฮสต์ ทั้งหมดได้รับอนุญาต เวอร์ชันที่แก้ไขซึ่งเสนอผ่านเครือข่ายต้องเปิดเผยซอร์สโค้ดให้แก่ผู้ใช้ นั่นคือจุดประสงค์ทั้งหมดของ AGPL เหนือ GPL

Provider integrations ที่สร้างด้วย SDKs เป็น Apache-2.0 ดังนั้นการสร้าง integration การชำระเงิน / จัดส่ง / SMS แบบเป็นกรรมสิทธิ์บน SDKs จึงไม่ทำให้เกิด AGPL นี่เป็นความตั้งใจ เราต้องการระบบนิเวศผู้ให้บริการที่เจริญรุ่งเรือง

<br />

## ความเป็นส่วนตัวและ telemetry

Spwig ส่ง ping ที่ไม่ระบุตัวตนหนึ่งครั้งต่อวันไปยัง `updates.spwig.com/api/v1/telemetry/`:

- UUID การติดตั้ง (สร้างเมื่อบูตครั้งแรก เก็บไว้ในเครื่อง)
- เวอร์ชัน Spwig
- เอดิชัน (community / pro / enterprise / trial / dev)
- ประเทศ (แก้ไขจาก IP ที่ ingress ตัว IP เองไม่ถูกเก็บ)
- จำนวนบักเก็ตของ feature flags (ผู้ให้บริการชำระเงินที่ตั้งค่า ธีมที่ติดตั้ง) ไม่ใช่ข้อมูลลูกค้าหรือคำสั่งซื้อดิบ

**ยกเลิกได้** ด้วย `SPWIG_TELEMETRY=0` ในสภาพแวดล้อมของคุณ ค่านั้นจะสลับ `settings.SPWIG_TELEMETRY_ENABLED` และงาน beat รายวันจะไม่ทำอะไรเลย

<br />

<p align="center">
  <sub>
    สร้างด้วยความใส่ใจในสิงคโปร์
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>

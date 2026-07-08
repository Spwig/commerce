---
title: ตัวแก้ไขตัวอักษร
---

ตัวแก้ไขตัวอักษรคือเครื่องมือจัดรูปแบบที่ใช้ร่วมกัน ซึ่งให้คุณมีการควบคุมทั้งหมดเกี่ยวกับการปรากฏของข้อความ มันจะเปิดขึ้นเป็นแผงลอยเมื่อคุณแก้ไขคุณสมบัติของตัวอักษรในองค์ประกอบใด ๆ ทั่ว Page Builder, Header/Footer Builder หรือ Menu Builder

![ตัวแก้ไขตัวอักษร](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## ตัวอย่างแบบเรียลไทม์

ตัวแก้ไขแสดงเปรียบเทียบแบบข้างเคียงกันที่ด้านบนของแผง:

| กล่อง | วัตถุประสงค์ |
|-------|-------------|
| **ปัจจุบัน** | แสดง "The quick brown fox..." ในสไตล์ตัวอักษรที่มีอยู่ |
| **ใหม่** | อัปเดตแบบเรียลไทม์เมื่อคุณปรับการตั้งค่า แสดงผลลัพธ์ก่อนที่คุณจะนำไปใช้ |

นี่ช่วยให้คุณเปรียบเทียบก่อนและหลังโดยไม่ต้องยืนยันการเปลี่ยนแปลงใด ๆ

## แท็บฟอนต์

แท็บฟอนต์คือมุมมองเริ่มต้นเมื่อตัวแก้ไขเปิด

**Font Family** — รายการแบบเลื่อนลงที่สามารถค้นหาได้ มีฟอนต์มากกว่า 70 แบบ จัดกลุ่มตามประเภท แต่ละฟอนต์จะแสดงตัวอย่างในรูปแบบของมันเอง เพื่อให้คุณเห็นว่ามันดูอย่างไรก่อนเลือก ฟอนต์จะถูกโหลดจาก Google Fonts เมื่อจำเป็น

**Font Size** — กล่องป้อนตัวเลขพร้อมตัวเลือกหน่วยที่รองรับ px, em, rem และ % ค่าเริ่มต้นคือ 16px

**Font Weight** — แถบเลื่อนจาก 100 (Thin) ถึง 900 (Black):

| ค่า | ชื่อ |
|-----|-----|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

ไม่ใช่ทุกฟอนต์ที่รองรับน้ำหนักทั้ง 9 แบบ ตัวแก้ไขจะแสดงน้ำหนักที่มีอยู่สำหรับฟอนต์ที่เลือก

**Font Style** — ปุ่มสลับสำหรับ Normal, Italic และ Oblique

## แท็บ Spacing

ปรับแต่งพื้นที่รอบและระหว่างตัวอักษร:

| ควบคุม | ทำอะไร | ค่าเริ่มต้น |
|---------|---------|---------|
| **Line Height** | พื้นที่แนวตั้งระหว่างบรรทัดข้อความ | normal |
| **Letter Spacing** | พื้นที่แนวนอนระหว่างตัวอักษรแต่ละตัว | normal |
| **Word Spacing** | พื้นที่แนวนอนระหว่างคำ | normal |
| **Text Indent** | การย่อของบรรทัดแรกในย่อหน้า | 0 |

แต่ละการควบคุมพื้นที่มีตัวเลือกหน่วย (px, em, rem, %)

## แท็บ Style

ควบคุมการตกแต่งข้อความและผลลัพธ์ทางภาพ:

- **Text Decoration** — ไม่มี, Underline, Overline หรือ Line-through
- **Decoration Style** — Solid, Dashed, Dotted, Double หรือ Wavy (ใช้ได้เมื่อมีการตกแต่ง)
- **Decoration Color** — ตัวเลือกสีสำหรับเส้นตกแต่ง ค่าเริ่มต้นคือสีข้อความ
- **Text Shadow** — ผลลัพธ์เงาแบบเลือกได้พร้อมการควบคุมการเลื่อน, ความเบลอ และสี

## แท็บ Transform

เปลี่ยนการใช้ตัวพิมพ์ใหญ่ของข้อความโดยไม่ต้องแก้ไขเนื้อหา:

| ตัวเลือก | ผลลัพธ์ |
|--------|--------|
| **None** | ข้อความปรากฏตามที่เขียน |
| **Uppercase** | ALL LETTERS ARE CAPITALIZED |
| **Lowercase** | all letters are lowercase |
| **Capitalize** | First Letter Of Each Word Is Capitalized |

การควบคุมเพิ่มเติมในแท็บนี้รวมถึง **Text Align** (ซ้าย, กลาง, ขวา, จัดให้ตรงกัน), **Vertical Align**, และ **Text Direction** (LTR หรือ RTL)

## ฟอนต์ที่มีอยู่

ตัวแก้ไขมีไลบรารีที่คัดสรรไว้ของฟอนต์ระบบและ Google Fonts จัดกลุ่มตามประเภท:

| หมวดหมู่ | ฟอนต์ |
|----------|-------|
| **ระบบ** | ฟอนต์เริ่มต้นของระบบ, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS |
| **Sans-Serif (สมัยใหม่)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans |
| **Sans-Serif (แบบคลาสสิก)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend |
| **ฟอนต์ Serif** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya |
| **ฟอนต์ Serif (ระบบ)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria |
| **Monospace** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono |
| **Display** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black |

Google Fonts จะถูกโหลดอัตโนมัติเมื่อเลือกแล้ว ฟอนต์ระบบจะใช้ CSS fallback chain ที่เหมาะสมเพื่อให้การเรนเดอร์มีความน่าเชื่อถือในทุกแพลตฟอร์ม

## ที่ใช้ในที่ใด

ตัวแก้ไขฟอนต์มีให้ใช้ในทุกที่ที่ต้องการปรับแต่งสไตล์ข้อความ:

- **Page Builder** — เลือกอิลิเมนต์ใด ๆ คลิกแท็บ Style และคลิกส่วน Typography
- **Header/Footer Builder** — ปรับแต่งข้อความในลิงก์นำทาง, ข้อความโลโก้, รายการเมนู และเนื้อหาในฟุตเตอร์
- **Menu Builder** — ควบคุมฟอนต์สำหรับป้ายชื่อเมนูและรายการย่อย
- **Catalog Admin** — ใช้ในบรรทัดฐานผลิตภัณฑ์และตัวแก้ไขเนื้อหาที่มีการควบคุมฟอนต์

ตัวแก้ไขจะถูกเข้าถึงผ่านอินเทอร์เฟซที่สอดคล้องกันเสมอไม่ว่าจะอยู่ในบริบทใด

## เคล็ดลับ

- **เลือกฟอนต์ให้เหมาะสม** — ใช้ฟอนต์ Display หรือ Serif สำหรับหัวข้อ และใช้ฟอนต์ Sans-Serif ที่สะอาดสำหรับเนื้อหาหลัก ตัวอย่างการจับคู่ที่ดีเช่น Playfair Display + Inter หรือ Montserrat + Merriweather
- **จำกัดจำนวนฟอนต์ต่อหน้า** — ฟอนต์ 2 หรือ 3 ตัวต่อหน้ามักเพียงพอ มากกว่านั้นอาจทำให้การโหลดช้าลงและสร้างความรกตา
- **ใช้หน่วยสัมพัทธ์สำหรับข้อความที่ปรับขนาดได้** — หน่วย em และ rem จะปรับตามขนาดฟอนต์พื้นฐาน ทำให้ฟอนต์ของคุณปรับตัวตามขนาดหน้าจอต่าง ๆ อัตโนมัติ
- **ตรวจสอบความพร้อมของน้ำหนัก** — หากข้อความดูเหมือนกันที่น้ำหนัก 400 และ 500 ฟอนต์ที่เลือกอาจไม่รองรับน้ำหนักนั้น ตัวแก้ไขจะแสดงน้ำหนักที่แต่ละฟอนต์มีให้ใช้
- **ตรวจสอบบนอุปกรณ์ทั้งหมด** — ข้อความที่ดูดีในขนาดหน้าจอคอมพิวเตอร์อาจเล็กเกินไปหรือใหญ่เกินไปบนมือถือ ใช้โหมดดูตัวอย่างอุปกรณ์ใน Page Builder เพื่อตรวจสอบ
- **ใช้โหมดดูตัวอย่างแบบเรียลไทม์** — เปรียบเทียบ Current vs New ในกล่องดูตัวอย่างก่อนนำไปใช้เพื่อหลีกเลี่ยงการเปลี่ยนแปลงที่ไม่คาดคิด
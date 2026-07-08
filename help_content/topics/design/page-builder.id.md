---
title: Page Builder
---

Page Builder adalah editor drag-and-drop visual untuk membuat halaman yang kaya dan responsif tanpa menulis kode. Tambahkan elemen dari perpustakaan 39 komponen, gayakan dengan utilitas yang kuat, atur animasi dan aturan visibilitas, dan terbitkan dengan sejarah versi lengkap.

![Page Builder](/static/core/admin/img/help/page-builder/builder-overview.webp)

## Antarmuka Builder

Builder memiliki empat area utama:

| Area | Lokasi | Tujuan |
|------|----------|---------|
| **Toolbar** | Baris atas | Preview perangkat (desktop/tablet/mobile), undo/redo, pengaturan halaman, simpan draf, terbitkan |
| **Element Library** | Sidebar kiri | Jelajahi dan drag 39 elemen yang diorganisir dalam 9 kategori |
| **Canvas** | Tengah | Area pengeditan WYSIWYG langsung — lihat perubahan saat Anda membuatnya |
| **Properties Panel** | Sidebar kanan | Edit konten, gaya, animasi, dan pengaturan lanjutan dari elemen yang dipilih |

## Element Library

Elemen diorganisir ke dalam kategori. Drag elemen apa pun dari perpustakaan ke canvas untuk menambahkannya ke halaman Anda.

| Kategori | Elemen |
|----------|----------|
| **Layout** | Container, Divider, Hero Section, Modal Popup, Navigation Menu, Spacer |
| **Basic** | Heading, Text, Button, Icon |
| **Content** | Blog Post Carousel, Blog Post Grid, FAQ Accordion, Related Posts, Testimonials |
| **Media** | Image, Image Gallery, Image Accordion, Video Embed |
| **Forms** | Contact Form, Form, Newsletter Signup |
| **Marketing** | Countdown Timer, CTA Banner, Featured Blog Banner, Loyalty Banner, Promotion Banner, Trust Badges, Voucher Code Display |
| **E-commerce** | Category Showcase, Gift Card Promo, Product Carousel, Product Grid, Product List, Reviews Display, Sale Products, Store Locator |
| **Social** | Social Links |
| **Navigation** | Search Bar |

### Containers dan Nesting

Elemen **Container** adalah fondasi untuk tata letak yang kompleks. Container dapat menampung elemen lain — termasuk container lain — memungkinkan Anda membangun grid kolom multi dan struktur bersarang. Gunakan preset tata letak container untuk dengan cepat menyiapkan pengaturan kolom umum (50/50, 33/33/33, 25/75, dll.).

## Menambahkan Elemen

1. Cari elemen yang ingin Anda gunakan di sidebar kiri
2. **Drag**-nya ke canvas dan lepaskan di tempat yang Anda inginkan
3. Elemen dapat dilepaskan antara elemen yang sudah ada, atau di dalam container
4. Garis penyisipan biru menunjukkan di mana elemen akan berada
5. Setelah dilepaskan, elemen secara otomatis dipilih dan panel properti terbuka

Anda juga dapat mengurutkan ulang elemen dengan menyeretnya ke atas atau ke bawah di canvas.

## Mengedit Konten

Pilih elemen apa pun di canvas untuk membuka propertinya di panel sebelah kanan. Tab **Content** menampilkan bidang yang spesifik untuk jenis elemen tersebut.

![Properties Panel](/static/core/admin/img/help/page-builder/properties-panel.webp)

Contohnya:
- **Heading** — teks, tag HTML (H1–H6), penjajaran, ID anchor
- **Image** — sumber gambar (perpustakaan media), teks alternatif, tautan, ukuran
- **Button** — label, URL, variasi gaya, ikon
- **Product Grid** — sumber data, jumlah kolom, produk per halaman, urutan pengurutan
- **Hero Section** — judul, subjudul, deskripsi, latar belakang, tombol panggil tindakan

Bidang konten yang dapat diterjemahkan menampilkan ikon terjemahan — klik untuk menambahkan terjemahan untuk toko multibahasa.

## Styling Elements

Tab **Style** menyediakan kontrol visual untuk setiap elemen. Setiap bagian membuka editor utilitas khusus.

![Style Tab](/static/core/admin/img/help/page-builder/style-tab.webp)

| Bagian | Yang dikontrol | Utilitas |
|---------|-----------------|---------|
| **Typography** | Keluarga font, ukuran, berat, tinggi baris, jarak huruf, gaya teks | Editor Typography |
| **Colors** | Warna teks dengan input hex/RGB/HSL dan token tema | Color Picker |
| **Background** | Warna padat, gradien, gambar, atau latar belakang video dengan keadaan hover | Editor Background |
| **Border** | Lebar, gaya, warna, dan jari-jari border per sisi | Editor Border |
| **Spacing** | Margin dan padding dengan editor model kotak visual | Editor Spacing |
| **Effects** | Bayangan kotak dengan preset dan dukungan lapisan multi, slider opasitas | Shadow Editor |

Setiap utilitas didokumentasikan dalam topik bantuan sendiri — cari "color picker", "background editor", dll. untuk mempelajari lebih lanjut.

## Animasi

Tab **Animations** memungkinkan Anda menambahkan gerakan ke elemen.

### Animasi Masuk

Dipicu saat elemen menggulir ke dalam pandangan:

| Animasi | Deskripsi |
|-----------|-------------|
| Fade In | Muncul secara bertahap |
| Slide In (Up/Down/Left/Right) | Bergeser dari arah tertentu |
| Zoom In | Tumbuh dari ukuran kecil ke ukuran penuh |
| Bounce In | Bounce ke tempatnya |
| Pulse / Shake / Bounce / Flash / Spin | Efek menarik perhatian |

Konfigurasikan **duration** (0.3s–1.5s), **delay** (0–1s), **timing function** (ease, ease-in, ease-out, linear), dan **repeat** (sekali atau tak terbatas).

### Animasi Hover

Dipicu saat pengunjung menghover elemen:

| Efek | Deskripsi |
|--------|-------------|
| Scale Up / Scale Down | Memperbesar atau memperkecil |
| Lift | Melayang ke atas |
| Rotate (CW / CCW) | Berputar searah jarum jam atau berlawanan arah jarum jam |
| Brighten / Fade | Mengubah kecerahan atau opasitas |
| Shadow Grow | Bayangan membesar |
| Lift with Shadow | Melayang dengan bayangan yang membesar |
| Pulse Scale / Skew / Border Glow | Efek khusus |

Konfigurasikan **duration**, **timing**, dan **intensity** (halus, normal, kuat).

## Pengaturan Lanjutan

Tab **Advanced** menyediakan kontrol yang lebih halus:

### Aturan Visibilitas

Kontrol kapan elemen ditampilkan atau disembunyikan berdasarkan kondisi:

- **Status pengguna** — masuk, keluar, pelanggan baru, pelanggan kembali
- **Perangkat** — desktop, tablet, mobile
- **Waktu** — rentang tanggal, waktu hari, hari dalam minggu
- **Kelompok pelanggan** — VIP, grosir, dll.
- **Nilai keranjang** — total keranjang minimum atau maksimum
- **Geografi** — negara, wilayah
- Dan 20+ jenis aturan lainnya

Aturan dapat dikombinasikan dengan logika AND/OR untuk target yang kompleks.

### CSS Kustom

| Bidang | Tujuan |
|-------|---------|
| **Element ID** | ID unik untuk tautan anchor atau penargetan CSS |
| **Custom CSS Classes** | Kelas tambahan untuk diterapkan |
| **Custom CSS Styles** | CSS inline untuk override satu kali |
| **Data Attributes** | Atribut data-* kustom sebagai pasangan kunci-nilai |
| **Z-Index** | Urutan tumpukan untuk elemen yang tumpang tindih |

## Alur Penerbitan

Halaman menggunakan sistem draf/penerbitan dengan sejarah versi lengkap:

| Status | Arti |
|--------|---------|
| **Draft** | Masih dalam proses — tidak terlihat oleh pengunjung |
| **Published** | Aktif di toko Anda |
| **Archived** | Dihapus dari situs tetapi disimpan |

### Cara Kerjanya

1. Buat perubahan di builder — mereka disimpan sebagai **draft**
2. Klik **Save Draft** untuk menyimpan tanpa menerbitkan
3. Klik **Publish** untuk membuat draf saat ini aktif
4. Setiap penerbitan menciptakan **snapshoot versi**
5. Anda dapat **mengembalikan** versi sebelumnya dari sejarah versi (ikon jam di toolbar)

Ini berarti Anda dapat bereksperimen secara bebas — halaman aktif Anda tetap tidak berubah sampai Anda secara eksplisit menerbitkannya.

## Template Halaman

Hemat waktu dengan bekerja menggunakan template:

- **Save as Template** — simpan desain halaman apa pun sebagai template yang dapat digunakan kembali
- **Create from Template** — mulai halaman baru dari template yang sudah ada
- **Template Categories** — kategorikan template berdasarkan tujuan (halaman landing, tentang, tampilan produk, dll.)

Template menangkap struktur halaman penuh termasuk semua elemen, konten, dan gaya.

## Desain Responsif

Gunakan tombol preview perangkat di toolbar untuk melihat bagaimana halaman Anda terlihat pada ukuran layar yang berbeda:

- **Desktop** — tata letak lebar penuh
- **Tablet** — viewport medium
- **Mobile** — viewport sempit

Elemen secara otomatis mengalihkan berdasarkan pengaturan container mereka. Anda juga dapat menggunakan aturan visibilitas untuk menampilkan atau menyembunyikan elemen tertentu pada perangkat tertentu.

## Tips

- **Mulai dengan Container** — sebagian besar tata letak dimulai dengan container untuk membuat kolom dan struktur. Gunakan preset tata letak untuk pengaturan umum.
- **Gunakan bagian Hero untuk header halaman** — elemen Hero menyediakan judul, subjudul, gambar latar belakang, dan tombol CTA dalam satu komponen.
- **Preview sebelum menerbitkan** — klik Preview untuk melihat persis apa yang akan dilihat pengunjung, lalu terbitkan ketika Anda puas.
- **Gunakan aturan visibilitas untuk personalisasi** — tampilkan konten berbeda untuk pengunjung yang masuk vs. yang tidak masuk, atau targetkan kelompok pelanggan tertentu.
- **Jaga animasi tetap halus** — satu atau dua animasi masuk per bagian halaman terlihat profesional. Terlalu banyak animasi dapat terasa membebani.
- **Berikan nama pada container Anda** — gunakan bidang ID Elemen untuk menandai container (misalnya, "hero-section", "features") sehingga mudah ditemukan dalam halaman yang kompleks.
- **Uji pada semua perangkat** — gunakan preview perangkat untuk memeriksa tata letak Anda pada desktop, tablet, dan mobile sebelum menerbitkan.
- **Manfaatkan template** — simpan desain halaman terbaik Anda sebagai template untuk mempercepat pembuatan halaman di masa depan.
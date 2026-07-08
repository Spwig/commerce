---
title: Pengaturan Portal Afiliasi
---

Portal Afiliasi Spwig adalah halaman landing yang menghadap ke publik di mana calon afiliasi mempelajari program Anda dan mendaftar. Mengkustomisasi portal ini memungkinkan Anda menyelaraskan pesan, branding, dan call-to-action dengan posisi unik toko Anda. Portal yang dirancang dengan baik menarik afiliasi berkualitas tinggi dan mengubah pengunjung menjadi mitra aktif.

## Apa Itu Portal Afiliasi?

Portal afiliasi dapat diakses di `/affiliate/` pada domain toko Anda. Portal ini berfungsi sebagai:

- **Halaman penemuan** — Di mana calon afiliasi mempelajari struktur komisi, manfaat, dan persyaratan Anda
- **Titik masuk pendaftaran** — Formulir pendaftaran untuk afiliasi baru (pendaftaran tamu atau berbasis akun)
- **Pintu masuk login** — Afiliasi yang sudah ada dapat masuk untuk mengakses dashboard mereka
- **Pameran merek** — Menampilkan identitas toko Anda dan nilai program afiliasi

Portal ini dapat dikustomisasi sepenuhnya melalui pengaturan afiliasi admin, termasuk pesan hero, fitur menonjol, alur langkah demi langkah, dan opsi pendaftaran.

![Halaman Landing Portal Afiliasi](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Mengakses Pengaturan

Navigasikan ke **Pemasaran > Program Afiliasi > Pengaturan Portal** untuk mengkustomisasi portal.

Model Pengaturan Afiliasi adalah **singleton** — Anda memiliki tepat satu catatan pengaturan untuk seluruh toko Anda. Semua bidang **dapat diterjemahkan** menggunakan sistem terjemahan Spwig, sehingga Anda dapat mengkustomisasi pesan untuk setiap bahasa yang didukung toko Anda.

## Bagian Hero

Bagian hero adalah hal pertama yang dilihat calon afiliasi. Ini mencakup:

- **Judul** — Judul utama (misalnya, "Bergabung dengan Program Afiliasi Kami")
- **Subjudul** — Teks pendukung yang menjelaskan nilai program (misalnya, "Earning komisi dengan mempromosikan produk premium kepada audiens Anda")
- **Statistik** — Metrik yang ditampilkan secara otomatis:
  - Total program aktif
  - Total afiliasi aktif
  - Tingkat komisi rata-rata (dihitung dari semua program aktif)
- **Tombol CTA** — Dihasilkan secara otomatis:
  - **Masuk** — Untuk afiliasi yang sudah ada
  - **Menjadi Afiliasi** — Memicu alur pendaftaran

### Mengkustomisasi Pesan Hero

| Bidang | Nilai Contoh | Tujuan |
|-------|--------------|---------|
| **Judul Hero** | "Bergabung dengan Kami & Dapatkan Penghasilan" | Menarik perhatian dengan judul yang berfokus pada manfaat |
| **Subjudul Hero** | "Bergabung dengan 500+ afiliasi yang mendapatkan komisi kompetitif pada setiap penjualan yang Anda rujuk" | Memberikan bukti sosial dan menjelaskan penawaran |

Statistik ini **dihitung secara otomatis** dan diperbarui secara real-time berdasarkan program dan afiliasi aktif Anda. Anda tidak dapat mengedit nilai-nilai ini secara manual.

## Bagian Fitur

Bagian fitur menampilkan **6 kartu manfaat yang dapat dikustomisasi** yang menjelaskan mengapa afiliasi harus bergabung dengan program Anda. Setiap kartu fitur berisi:

- **Ikon** — Kelas ikon FontAwesome (misalnya, `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Judul** — Judul manfaat (misalnya, "Komisi Kompetitif")
- **Deskripsi** — Penjelasan 1-2 kalimat (misalnya, "Earning hingga 15% pada setiap penjualan yang Anda rujuk")

### Fitur Default

Spwig menyediakan fitur default saat Anda pertama kali menginstal aplikasi afiliasi:

| Ikon | Judul | Deskripsi |
|------|-------|-------------|
| `fa-dollar-sign` | Komisi Kompetitif | Dapatkan komisi yang besar pada setiap penjualan yang Anda rujuk |
| `fa-link` | Tautan Pelacakan yang Mudah | Dapatkan tautan pelacakan unik yang berfungsi di mana saja |
| `fa-chart-line` | Analitik Real-Time | Lacak klik, konversi, dan penghasilan di dashboard Anda |
| `fa-calendar-check` | Pembayaran yang Andal | Dapatkan pembayaran tepat waktu melalui PayPal atau transfer bank |
| `fa-headset` | Dukungan Khusus | Tim kami siap membantu Anda sukses |
| `fa-gift` | Bahan Pemasaran | Akses banner, gambar, dan konten promosi |

### Mengkustomisasi Fitur

Fitur disimpan sebagai **array JSON** di database. Edit secara langsung di formulir admin:

```json
[
  {
    "icon": "fa-percent",
    "title": "Up to 20% Commission",
    "description": "Earn industry-leading commissions on premium product sales"
  },
  {
    "icon": "fa-rocket",
    "title": "Fast Approval",
    "description": "Get approved in 24 hours and start promoting immediately"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Mobile Dashboard",
    "description": "Manage your links and track earnings from any device"
  }
]
```

**Referensi Ikon:** Gunakan kelas ikon apa pun dari FontAwesome 5 Free. Lihat ikon di [fontawesome.com/icons](https://fontawesome.com/icons) dan gunakan nama kelas (misalnya, `fa-trophy`, `fa-users`, `fa-star`).

## Bagian Bagaimana Cara Kerjanya

Bagian "Bagaimana Cara Kerjanya" menampilkan **alur visual 4 langkah** yang menjelaskan perjalanan afiliasi. Setiap langkah mencakup:

- **Judul** — Nama langkah (misalnya, "Daftar")
- **Deskripsi** — Penjelasan 1-2 kalimat tentang apa yang terjadi

### Langkah Default

| Langkah | Judul | Deskripsi |
|------|-------|-------------|
| 1 | Sign Up | Buat akun afiliasi gratis Anda dalam beberapa menit |
| 2 | Get Your Links | Hasilkan tautan pelacakan unik untuk produk atau halaman apa pun |
| 3 | Promote | Bagikan tautan Anda dengan audiens Anda melalui konten, media sosial, atau email |
| 4 | Earn Commissions | Dapatkan pembayaran saat pelanggan membeli menggunakan tautan rujukan Anda |

### Mengkustomisasi Langkah

Langkah disimpan sebagai **array JSON**. Anda dapat mengeditnya di admin:

```json
[
  {
    "title": "Apply to Join",
    "description": "Submit your application and tell us about your platform"
  },
  {
    "title": "Get Approved",
    "description": "Our team reviews your application within 24 hours"
  },
  {
    "title": "Create Links",
    "description": "Access your dashboard and generate tracking links instantly"
  },
  {
    "title": "Start Earning",
    "description": "Earn commissions on every sale you refer — paid monthly via PayPal"
  }
]
```

Alur visual secara otomatis menomori setiap langkah (1, 2, 3, 4) pada halaman landing.

## Bagian CTA

Bagian terakhir sebelum formulir pendaftaran adalah **Bagian Call-to-Action (CTA)**. Ini memberikan dorongan terakhir untuk mendorong pendaftaran.

| Bidang | Nilai Contoh | Tujuan |
|-------|--------------|---------|
| **Judul CTA** | "Siap Mulai Mendapatkan Penghasilan?" | Pertanyaan langsung menciptakan urgensi |
| **Deskripsi CTA** | "Bergabung dengan program afiliasi kami hari ini dan mulai mendapatkan komisi pada produk yang sudah Anda sukai dan rekomendasikan." | Memperkuat manfaat dan menghilangkan hambatan |

Bagian CTA secara otomatis menampilkan tombol **Menjadi Afiliasi** di bawah teks.

## Pengaturan Pendaftaran

Kontrol cara afiliasi baru mendaftar dan informasi apa yang mereka berikan.

### Formulir Pendaftaran Kustom

**Bidang:** `custom_form` (ForeignKey ke formulir FormBuilder)

Jika Anda memiliki formulir pendaftaran kustom yang dibangun dengan FormBuilder Spwig, pilih di sini. Ini memungkinkan Anda mengumpulkan informasi tambahan selama pendaftaran (misalnya, URL situs web, ukuran audiens, saluran promosi).

**Biarkan kosong** untuk menggunakan formulir pendaftaran afiliasi default (email, kata sandi, detail pembayaran).

### Izinkan Pendaftaran Tamu

**Bidang:** `allow_guest_registration` (Boolean)

- **Dicentang** — Pengunjung dapat mendaftar tanpa membuat akun Spwig terlebih dahulu
- **Tidak dicentang** — Pengunjung harus masuk atau membuat akun pelanggan sebelum mendaftar

**Rekomendasi:** Aktifkan pendaftaran tamu untuk mengurangi hambatan. Anda selalu dapat meminta persetujuan untuk meninjau afiliasi sebelum mengaktifkannya.

### Memerlukan Persetujuan

**Bidang:** `require_approval` (Boolean)

- **Dicentang** — Afiliasi baru harus menunggu persetujuan manual sebelum mengakses dashboard mereka
- **Tidak dicentang** — Afiliasi baru secara otomatis disetujui dan dapat membuat tautan segera

**Rekomendasi:** Aktifkan persetujuan manual jika Anda ingin meninjau afiliasi untuk kesesuaian merek, pencegahan penipuan, atau program eksklusif.

### URL Syarat & Ketentuan

**Bidang:** `terms_url` (URL)

Tautan opsional ke syarat dan ketentuan program afiliasi Anda. Jika disediakan, formulir pendaftaran menampilkan kotak centang yang memerlukan afiliasi untuk menyetujui syarat Anda sebelum mendaftar.

**Contoh:** `/pages/affiliate-terms/`

### Pesan Selamat Datang

**Bidang:** `welcome_message` (Text)

Pesan yang ditampilkan kepada afiliasi segera setelah pendaftaran berhasil. Gunakan ini untuk:

- Mengucapkan terima kasih atas keanggotaan mereka
- Menjelaskan langkah selanjutnya (misalnya, "Kami akan meninjau aplikasi Anda dalam 24 jam")
- Menautkan ke sumber daya memulai

**Contoh:*
```
Selamat datang di program afiliasi kami! Kami telah menerima aplikasi Anda dan akan meninjau dalam 24 jam. Periksa email Anda untuk konfirmasi persetujuan dan instruksi login.
```

## Dukungan Multi-Bahasa

Semua bidang teks dalam Pengaturan Afiliasi **dapat diterjemahkan** menggunakan widget terjemahan Spwig:

- Judul Hero
- Subjudul Hero
- Fitur (JSON diterjemahkan per bahasa)
- Langkah Bagaimana Cara Kerjanya (JSON diterjemahkan per bahasa)
- Judul CTA
- Deskripsi CTA
- Pesan Selamat Datang

### Bagaimana Terjemahan Bekerja

Ketika Anda mengedit bidang yang dapat diterjemahkan, Anda akan melihat widget terjemahan yang memungkinkan Anda menyediakan konten untuk setiap bahasa yang diaktifkan. Untuk bidang JSON (fitur, langkah), Anda menyediakan objek JSON terpisah per bahasa:

**Bahasa Inggris:*
```json
[
  {"icon": "fa-dollar-sign", "title": "Competitive Commissions", "description": "Earn up to 15% on every sale"}
]
```

**Bahasa Spanyol:*
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Gana hasta el 15% en cada venta"}
]
```

Portal secara otomatis menampilkan versi bahasa yang benar berdasarkan preferensi bahasa pengunjung.

## Pratinjau Perubahan Anda

Setelah mengkustomisasi pengaturan portal:

1. **Simpan** perubahan Anda di admin
2. Kunjungi `/affiliate/` pada frontend toko Anda (buka di tab baru)
3. **Uji alur pendaftaran** dengan mengklik "Menjadi Afiliasi"
4. **Verifikasi konsistensi branding** — apakah portal sesuai dengan desain dan pesan toko Anda?

Anda dapat membuat perubahan iteratif dan memperbarui halaman untuk melihat pembaruan segera.

## Contoh Pengkustomisasi

### Skenario 1: Toko E-Commerce Pakaian

**Tujuan:** Merekrut influencer dan blogger pakaian.

| Pengaturan | Nilai |
|---------|-------|
| Judul Hero | "Promosikan Gaya yang Anda Sukai & Dapatkan Penghasilan" |
| Subjudul Hero | "Bergabung dengan 1.200+ influencer yang mendapatkan komisi 12% pada setiap penjualan" |
| Fitur 1 | Ikon: `fa-tshirt`, Judul: "Koleksi Pakaian Terpilih", Deskripsi: "Promosikan pakaian premium dan aksesori" |
| Fitur 2 | Ikon: `fa-percentage`, Judul: "Komisi 12%", Deskripsi: "Tarif terkemuka industri pada semua produk" |
| Fitur 3 | Ikon: `fa-camera`, Judul: "Konten Eksklusif", Deskripsi: "Akses foto produk, video, dan aset kampanye" |
| Izinkan Pendaftaran Tamu | Dicentang |
| Memerlukan Persetujuan | Dicentang (tinjauan manual untuk kesesuaian merek) |

### Skenario 2: Program Mitra SaaS B2B

**Tujuan:** Merekrut konsultan bisnis dan agen untuk rujukan perangkat lunak perusahaan.

| Pengaturan | Nilai |
|---------|-------|
| Judul Hero | "Bergabung dengan Kami untuk Meningkatkan Pendapatan" |
| Subjudul Hero | "Dapatkan $500 per rujukan perusahaan melalui program mitra B2B kami" |
| Fitur 1 | Ikon: `fa-handshake`, Judul: "$500 Per Referral", Deskripsi: "Komisi tetap untuk calon klien perusahaan yang memenuhi syarat" |
| Fitur 2 | Ikon: `fa-clock`, Judul: "Cookie 180 Hari", Deskripsi: "Jendela atribusi panjang untuk siklus penjualan kompleks" |
| Fitur 3 | Ikon: `fa-user-tie`, Judul: "Manajer Mitra Khusus", Deskripsi: "Dukungan kelas atas untuk klien Anda" |
| Izinkan Pendaftaran Tamu | Tidak dicentang (B2B memerlukan akun) |
| Memerlukan Persetujuan | Dicentang (program undangan saja) |
| URL Syarat | `/pages/partner-program-terms/` |

## Tips

- Kustomisasi **judul hero** Anda untuk fokus pada manfaat, bukan fitur — "Dapatkan Penghasilan Saat Tidur" lebih menarik daripada "Pendaftaran Program Afiliasi"
- Gunakan **bukti sosial** dalam subjudul (misalnya, "Bergabung dengan 500+ afiliasi") untuk membangun kepercayaan dan kredibilitas
- Pilih **ikon FontAwesome** yang memperkuat visual setiap manfaat — ikon harus segera menyampaikan nilai
- Pertahankan deskripsi fitur hanya **1-2 kalimat** — portal ini tentang konversi, bukan penjelasan yang menyeluruh
- Uji **alur pendaftaran** Anda sendiri sebelum mempromosikan portal — tangkap titik hambatan seperti bidang formulir yang membingungkan atau tautan yang rusak
- Aktifkan **pendaftaran tamu** untuk mengurangi hambatan pendaftaran, lalu gunakan **memerlukan persetujuan** untuk meninjau afiliasi setelah mereka mengirimkan
- Gunakan **pesan selamat datang** untuk menetapkan ekspektasi (waktu persetujuan, langkah selanjutnya, kontak dukungan) dan mengurangi pertanyaan dukungan
- Perbarui portal **secara musiman** untuk selaras dengan kampanye — soroti promosi komisi khusus atau peluncuran produk baru

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis persis seperti yang ditunjukkan dalam aturan pelestarian.
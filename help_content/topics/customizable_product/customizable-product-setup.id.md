---
title: Mengatur Produk yang Dapat Disesuaikan
---

Panduan ini akan membimbing Anda melalui proses pengaturan lengkap untuk produk yang dapat disesuaikan, mulai dari membuat produk hingga mengonfigurasi permukaan, harga, dan pembatasan unggah. Dua contoh praktis digunakan sepanjang panduan ini: sebuah **kaos kustom** (pakaian multi-permukaan) dan sebuah **poster kustom** (cetak satu-permukaan).

## Langkah 1: Membuat produk

1. Navigasikan ke **Produk > Semua Produk** dan klik **+ Tambah Produk**
2. Atur **Jenis Produk** menjadi **Produk yang Dapat Disesuaikan**
3. Isi nama produk, deskripsi, gambar, dan harga seperti yang Anda lakukan untuk produk apa pun
4. Simpan produk

Setelah disimpan, tombol baru **Buka Editor Desain Setup** muncul di formulir produk. Tombol ini akan membawa Anda ke halaman pengaturan khusus di mana Anda mengonfigurasi editor desain visual.

## Langkah 2: Akses editor desain setup

1. Buka produk yang baru saja Anda buat di admin
2. Klik tombol **Buka Editor Desain Setup** (di bagian Produk yang Dapat Disesuaikan)
3. Halaman pengaturan terbuka dengan tiga tab: **Permukaan**, **Pengaturan**, dan **Harga**

Halaman pengaturan ini adalah tempat Anda mendefinisikan segala sesuatu tentang editor desain untuk produk ini.

## Langkah 3: Tambahkan permukaan desain

Sebuah permukaan mewakili satu sisi desain dari produk Anda. Klik **+ Tambahkan Permukaan** untuk membuat setiap permukaan.

### Contoh kaos: 3 permukaan

| Permukaan | Nama | Dimensi | Zona Desain | Catatan |
|---------|------|-----------|-------------|-------|
| 1 | Depan | 300 x 400 mm | Area dada tengah | Area desain utama |
| 2 | Belakang | 300 x 400 mm | Area punggung atas | Area desain sekunder |
| 3 | Lengan Kiri | 100 x 100 mm | Area lengan atas | Hanya area logo kecil |

### Contoh poster: 1 permukaan

| Permukaan | Nama | Dimensi | Zona Desain | Catatan |
|---------|------|-----------|-------------|-------|
| 1 | Depan | 210 x 297 mm (A4) | Area cetak penuh | Satu permukaan, DPI tinggi |

### Mengonfigurasi setiap permukaan

Untuk setiap permukaan, Anda mengonfigurasi hal berikut:

**Informasi dasar:**
- **Nama** — Apa yang dilihat pelanggan di tab permukaan (misalnya, "Depan", "Belakang")
- **Slug** — Identifikasi yang aman untuk URL, dihasilkan secara otomatis dari nama
- **Urutan Pengurutan** — Mengontrol urutan permukaan muncul (angka lebih rendah terlebih dahulu)

**Gambar mockup:**
- Klik area gambar mockup untuk membuka Perpustakaan Media dan pilih foto produk yang menampilkan permukaan ini
- Gunakan foto berkualitas tinggi dari produk Anda dari sudut yang benar

**Posisi zona desain:**
- Setelah memilih gambar mockup, tampilan overlay persegi muncul di pratinjau
- **Tarik** overlay untuk menempatkan di mana zona desain harus berada di mockup
- **Ubah ukuran** overlay dengan menarik tepinya untuk mendefinisikan batas zona desain
- Zona disimpan sebagai koordinat berbasis persentase, sehingga dapat diukur ke ukuran layar apa pun

Zona desain memberi tahu editor tepat di mana pada gambar produk desain pelanggan akan muncul. Letakkan dengan hati-hati untuk cocok dengan area cetak sebenarnya dari produk Anda.

**Dimensi fisik:**
- **Lebar** dan **Tinggi** — Dimensi dunia nyata dari area desain
- **Satuan** — Milimeter, inci, atau piksel
- Dimensi ini menentukan rasio aspek kanvas desain dan digunakan untuk menghitung DPI cetak

**Pengaturan cetak:**
- **DPI Minimum** — Nilai terendah yang diterima dots-per-inch. Pelanggan akan melihat peringatan jika gambar yang diunggah mereka berada di bawah ini. Default: 150
- **DPI Direkomendasikan** — Resolusi ideal untuk kualitas cetak terbaik. Default: 300
- **Bleed (mm)** — Margin tambahan di luar area desain untuk cetak bleed. Atur ke 0 jika tidak diperlukan bleed (umum untuk pakaian), atau 3mm untuk produk cetak profesional
- **Max Warna** — Untuk cetak sablon, Anda dapat membatasi jumlah warna. Biarkan kosong untuk tak terbatas (cetak digital)
- **Warna Latar Belakang** — Warna latar belakang kanvas default

### Pengaturan cetak kaos vs poster

| Pengaturan | Kaos | Poster |
|---------|---------|--------|
| DPI Minimum | 150 | 200 |
| DPI Direkomendasikan | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Max Warna | 6 (cetak sablon) | Kosong (tak terbatas) |
| Warna Latar Belakang | Cocok dengan warna pakaian | `#ffffff` (putih) |

## Langkah 4: Batasan per permukaan

Setiap permukaan dapat menggantikan pengaturan fitur global. Ini memungkinkan Anda mengizinkan alat yang berbeda pada permukaan yang berbeda.

Opsi batasan adalah:

| Pengaturan | Opsi | Deskripsi |
|---------|---------|-------------|
| **Izinkan Teks** | Wariskan / Ya / Tidak | Apakah pelanggan dapat menambahkan teks pada permukaan ini |
| **Izinkan Unggah Gambar** | Wariskan / Ya / Tidak | Apakah pelanggan dapat mengunggah gambar ke permukaan ini |
| **Izinkan Clipart** | Wariskan / Ya / Tidak | Apakah pelanggan dapat menggunakan clipart pada permukaan ini |
| **Maksimal Elemen** | Angka atau kosong | Jumlah maksimal elemen desain yang diperbolehkan pada permukaan ini |

Ketika diatur ke **Wariskan**, permukaan menggunakan konfigurasi yang telah ditentukan dalam pengaturan global (Langkah 6). Ketika diatur ke **Ya** atau **Tidak**, ini menggantikan pengaturan global untuk permukaan tertentu.

### Contoh: Batasan lengan kaos

Untuk permukaan lengan kaos, Anda mungkin ingin membatasi personalisasi hanya pada logo kecil saja:

| Pengaturan | Nilai | Alasan |
|---------|-------|--------|
| Izinkan Teks | Tidak | Terlalu kecil untuk teks yang dapat dibaca |
| Izinkan Unggah Gambar | Ya | Izinkan unggah logo kecil |
| Izinkan Clipart | Tidak | Biarkan sederhana |
| Maksimal Elemen | 1 | Hanya satu logo |

Permukaan depan dan belakang akan tetap diatur ke **Wariskan**, memungkinkan semua alat seperti yang didefinisikan dalam pengaturan global.

### Contoh: Batasan poster

Untuk poster, biasanya semua permukaan mewariskan dari konfigurasi global karena hanya ada satu permukaan dan semua alat harus tersedia. Tidak diperlukan penggantian per permukaan.

## Langkah 5: Konfigurasi batasan unggah

Pada tab **Pengaturan**, konfigurasikan cara pelanggan dapat mengunggah file:

| Pengaturan | Deskripsi | Contoh kaos | Contoh poster |
|---------|-------------|-----------------|----------------|
| **Ukuran Unggah Maksimal** | Ukuran file maksimal per unggah | 10 MB | 20 MB |
| **Jumlah Unggah per Permukaan** | Jumlah gambar per permukaan | 5 | 3 |
| **Jenis Unggah yang Diizinkan** | Format file yang diterima | JPG, PNG, WebP | JPG, PNG, WebP |

Ukuran batas file yang lebih besar disarankan untuk produk cetak di mana pelanggan perlu mengunggah gambar resolusi tinggi.

## Langkah 6: Pengaturan editor

Pada tab **Pengaturan**, konfigurasikan perilaku editor global:

**Mode Editor:**
- **Editor Kanvas** — Editor visual penuh dengan pratinjau kanvas langsung. Disarankan untuk sebagian besar produk.
- **Form Sederhana** — Bidang formulir tradisional untuk personalisasi dasar (misalnya, hanya teks ukir).

**Pengaktifan fitur (default global):**
- **Izinkan Teks** — Izinkan pelanggan menambahkan elemen teks
- **Izinkan Unggah Gambar** — Izinkan pelanggan mengunggah gambar mereka sendiri
- **Izinkan Clipart** — Izinkan pelanggan menjelajahi dan menggunakan perpustakaan clipart Anda

Pengaturan global ini berlaku untuk semua permukaan kecuali diganti oleh batasan per permukaan (Langkah 4).

## Langkah 7: Konfigurasi harga

Pada tab **Harga**, tetapkan biaya desain yang ditambahkan ke harga dasar produk:

| Biaya | Deskripsi |
|-----|-------------|
| **Biaya Desain Dasar** | Biaya tetap yang ditambahkan ketika ada personalisasi yang diterapkan |
| **Biaya per Permukaan** | Biaya tambahan untuk setiap permukaan yang digunakan selain yang pertama |
| **Biaya per Unggah** | Biaya untuk setiap gambar yang diunggah oleh pelanggan |
| **Biaya per Teks** | Biaya untuk setiap elemen teks yang ditambahkan |

### Contoh: Harga kaos

| Biaya | Jumlah | Alasan |
|-----|--------|-----------|
| Biaya Desain Dasar | $5,00 | Menutupi biaya setup untuk setiap pesanan kustom |
| Biaya per Permukaan | $2,00 | Setiap permukaan tambahan menambahkan biaya cetak |
| Biaya per Unggah | $1,00 | Gambar kustom memerlukan pemrosesan |
| Biaya per Teks | $0,50 | Teks lebih sederhana untuk diproduksi dibandingkan gambar |

**Contoh perhitungan:** Seorang pelanggan merancang kaos dengan teks di depan dan logo di belakang:
- Biaya desain dasar: $5,00
- 1 permukaan tambahan (belakang): $2,00
- 1 logo yang diunggah: $1,00
- 1 elemen teks: $0,50
- **Total biaya desain: $8,50** (ditambahkan ke harga dasar produk)

### Contoh: Harga poster


| Biaya | Jumlah | Alasan |
|-----|--------|-----------|
| Biaya Desain Dasar | $0.00 | Tidak ada biaya dasar — harga produk mencakupnya |
| Biaya per Permukaan | $0.00 | Satu permukaan, tidak berlaku |
| Biaya per Unggah | $2.00 | Pemrosesan resolusi tinggi |
| Biaya per Teks | $0.00 | Teks termasuk dalam pengalaman dasar |

**Contoh perhitungan:** Seorang pelanggan membuat poster dengan 2 foto yang diunggah dan 3 elemen teks:
- Biaya desain dasar: $0.00
- 2 foto yang diunggah: $4.00
- 3 elemen teks: $0.00
- **Total biaya desain: $4.00**

Biaya desain ditampilkan kepada pelanggan secara real time saat mereka menambahkan elemen, sehingga mereka dapat melihat dampak biaya dari setiap penambahan sebelum menambahkan ke keranjang.

## Perbandingan pengaturan secara sekilas

| Aspek | Kaos Kustom | Poster Kustom |
|--------|---------------|---------------|
| Permukaan | 3 (depan, belakang, lengan) | 1 (depan) |
| Gambar mockup | 3 foto produk | 1 foto produk |
| Posisi zona | Area dada/ belakang/ lengan | Area cetak penuh |
| Dimensi | 300x400mm, 100x100mm | 210x297mm (A4) |
| DPI minimum | 150 | 200 |
| Bleed | 0 mm | 3 mm |
| Max warna | 6 | Tidak terbatas |
| Keterbatasan per permukaan | Lengan terbatas | Tidak diperlukan |
| Model harga | Dasar + permukaan + unggah + teks | Hanya biaya unggah |

## Tips

- Selalu uji editor desain dari perspektif pelanggan setelah menyelesaikan pengaturan. Kunjungi halaman produk di toko online dan coba menambahkan teks, mengunggah gambar, dan beralih permukaan.
- Unggah gambar mockup yang sangat mirip dengan penampilan produk sebenarnya. Untuk kaos, foto setiap sudut secara terpisah. Untuk poster, gunakan foto flat-lay bersih atau mockup bingkai.
- Tentukan zona desain secara konservatif — lebih baik mendefinisikan zona yang sedikit lebih kecil daripada memiliki desain yang mencetak ke sisi atau tepi.
- Tetapkan DPI minimum berdasarkan metode cetak Anda: 150 untuk cetak sablon, 200 untuk cetak digital standar, 300 untuk cetak offset berkualitas tinggi.
- Gunakan 3 mm bleed untuk produk yang akan dipotong setelah dicetak (poster, kartu bisnis, flyer). Atur bleed ke 0 untuk produk di mana desain diterapkan pada permukaan yang sudah ada (kaos, cangkir, casing ponsel).
- Mulailah dengan harga sederhana dan sesuaikan berdasarkan umpan balik pelanggan. Banyak pedagang mulai hanya dengan biaya desain dasar dan menambahkan biaya per elemen kemudian.
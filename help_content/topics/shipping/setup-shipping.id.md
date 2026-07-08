---
title: Mengatur Pengiriman
---

Panduan ini menjelaskan cara mengonfigurasi pengiriman untuk toko Anda — dari mengatur metode pengiriman dasar hingga menghubungkan integrasi penyedia pengiriman langsung untuk tarif real-time.

## Pengantar Pengiriman

Spwig menawarkan dua pendekatan untuk pengiriman:

- **Metode Pengiriman Manual** — Metode berbasis tarif tetap yang Anda definisikan (contoh: "Pengiriman Standar — $5.99")
- **Integrasi Penyedia Pengiriman** — Tarif real-time dari penyedia seperti FedEx, UPS, dan DHL

Anda dapat menggunakan pendekatan mana pun atau menggabungkan keduanya.

## Metode Pengiriman

Metode pengiriman adalah opsi yang ditampilkan kepada pelanggan saat checkout. Navigasikan ke **Pemesanan > Pengiriman** di sidebar untuk mengelolanya.

![Metode pengiriman](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Membuat Metode Pengiriman

1. Klik **Tambah Metode Pengiriman**
2. Isi detail:
   - **Nama** — Nama tampilan yang ditampilkan kepada pelanggan (contoh: "Pengiriman Ekspres")
   - **Deskripsi** — Deskripsi singkat tentang layanan
   - **Harga** — Biaya pengiriman tetap
   - **Waktu Pengiriman yang Diperkirakan** — Estimasi waktu pengiriman (contoh: "3-5 hari kerja")
3. Klik **Simpan**

## Zona Pengiriman

Zona pengiriman mendefinisikan wilayah geografis di mana metode pengiriman Anda berlaku. Navigasikan ke bagian **Zona Pengiriman** untuk mengelolanya.

![Zona pengiriman](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Membuat Zona

1. Klik **Tambah Zona Pengiriman**
2. Konfigurasikan zona:
   - **Nama Zona** — Nama internal (contoh: "Domestik AS", "Eropa")
   - **Negara** — Pilih negara yang termasuk dalam zona ini
   - **Negara Bagian/Region** — Secara opsional sempitkan ke negara bagian tertentu
   - **Polanya Kode Pos** — Gunakan pola seperti "9*" untuk menargetkan area tertentu
3. Tetapkan metode pengiriman ke zona ini
4. Klik **Simpan**

### Prioritas Zona

Ketika alamat pelanggan cocok dengan beberapa zona, zona yang paling spesifik mendapat prioritas. Zona dengan target tingkat negara bagian akan mengambil alih zona tingkat negara.

## Integrasi Penyedia Pengiriman

Hubungkan dengan penyedia pengiriman untuk menawarkan tarif perhitungan real-time saat checkout.

![Penyedia pengiriman](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Penyedia yang Tersedia

Jelajahi dan instal penyedia pengiriman dari pasar.

![Penyedia pengiriman](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

Penyedia yang didukung termasuk:

- **FedEx** — Ground, Ekspres, Internasional
- **UPS** — Ground, 2 Hari, Malam Hari, Global
- **DHL** — Ekspres, E-commerce
- **USPS** — Prioritas, Kelas Pertama, Pengiriman Media
- Dan lebih banyak tersedia melalui Marketplace

### Mengatur Penyedia

1. Pergi ke halaman penyedia pengiriman dan klik **Pasang** pada penyedia yang Anda pilih
2. Ikuti wizard pengaturan:
   - **Langkah 1** — Tinjau detail penyedia
   - **Langkah 2** — Konfigurasikan pengaturan umum
   - **Langkah 3** — Masukkan kredensial API Anda (nomor akun, kunci API, dll.)
   - **Langkah 4** — Aktifkan layanan tertentu (Ground, Ekspres, dll.)
   - **Langkah 5** — Uji koneksi
3. Setelah terhubung, tarif penyedia akan muncul otomatis saat checkout

### Kredensial API

Setiap penyedia memerlukan akun API:

- **FedEx** — Daftarkan di Portal Pengembang FedEx, buat aplikasi, dan salin kunci API dan rahasia Anda
- **UPS** — Daftarkan di Kit Pengembang UPS, minta kunci akses
- **DHL** — Hubungi DHL untuk mendapatkan kredensial API melalui portal bisnis mereka

## Aturan Pengiriman

Buat aturan lanjutan untuk mengontrol kapan dan bagaimana metode pengiriman ditawarkan.

### Aturan Umum

- **Pengiriman gratis untuk pembelian di atas $50** — Tetapkan minimum keranjang untuk pengiriman gratis
- **Tarif tetap untuk pesanan ringan** — Tarif tetap ketika berat pesanan di bawah ambang batas
- **Nonaktifkan ekspres untuk area terpencil** — Sembunyikan opsi ekspres berdasarkan kode pos
- **Markup persentase** — Tambahkan biaya penanganan sebagai persentase dari tarif penyedia

### Membuat Aturan

1. Navigasikan ke bagian aturan pengiriman
2. Klik **Tambah Aturan**
3. Tetapkan kondisi (total keranjang, berat, zona, dll.)
4. Definisikan tindakan (sesuaikan tarif, sembunyikan metode, aktifkan pengiriman gratis)
5. Simpan aturan

Aturan dievaluasi berdasarkan urutan — aturan pertama yang cocok akan diterapkan.

## Pengiriman Gratis

### Pengiriman Gratis untuk Seluruh Toko

Aktifkan pengiriman gratis secara global di **Pengaturan > Pengaturan Toko**:

- Nyalakan **Pengiriman Gratis**
- Secara opsional tetapkan jumlah pesanan minimum
- Pilih wilayah yang memenuhi syarat

### Pengiriman Gratis Promosi

Buat penawaran pengiriman gratis yang terbatas waktu:

1. Pergi ke **Pemasaran > Penjualan & Promosi**
2. Buat promosi baru
3. Tetapkan kondisi: "Total keranjang di atas X"
4. Tetapkan tindakan: "Pengiriman gratis"
5. Konfigurasikan tanggal mulai dan akhir

## Pengiriman Internasional

Untuk pesanan internasional, pastikan produk Anda memiliki:

- **Kode HS** — Klasifikasi tarif Sistem Harmonis
- **Negara Asal** — Negara manufaktur
- **Nilai Bea Cukai** — Nilai deklarasi untuk bea cukai

Field-field ini berada di tab **Inventaris** dari setiap produk. Penyedia menggunakan informasi ini untuk menghasilkan dokumen bea cukai secara otomatis.

## Tips

- Mulailah dengan metode pengiriman manual untuk memulai toko Anda dengan cepat, lalu tambahkan integrasi penyedia pengiriman nanti.
- Buat zona pengiriman untuk destinasi paling umum terlebih dahulu.
- Selalu uji konfigurasi pengiriman Anda dengan membuat pesanan uji menggunakan alamat yang berbeda.
- Gunakan fitur markup tarif untuk menutupi biaya penanganan dan kemasan.
- Tetapkan ambang batas pengiriman gratis untuk meningkatkan nilai pesanan rata-rata.
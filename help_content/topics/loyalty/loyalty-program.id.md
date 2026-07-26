---
title: Program Keanggotaan
---

Program Keanggotaan memungkinkan Anda memberikan hadiah kepada pelanggan atas pembelian dan partisipasi mereka melalui sistem berbasis poin. Pelanggan memperoleh poin, naik level, dan menukar hadiah. Navigasikan ke **Pemasaran > Program Keanggotaan** di bilah sisi admin.

![Dashboard keanggotaan](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Dashboard Keanggotaan

Dashboard menyediakan gambaran menyeluruh mengenai program keanggotaan Anda:

### Metrik Utama

- **Total Anggota** — Total pelanggan yang terdaftar
- **Anggota Aktif (30d)** — Anggota yang memperoleh atau menukar poin dalam 30 hari terakhir
- **Poin yang Belum Ditebus** — Total poin yang belum ditukar oleh semua anggota
- **Rasio Penukaran** — Persentase poin yang telah ditukar dari poin yang diperoleh
- **Poin yang Diperoleh (30d)** — Poin yang diperoleh dalam 30 hari terakhir
- **Poin yang Ditebus (30d)** — Poin yang ditukar dalam 30 hari terakhir
- **Rata-Rata Poin/Anggota** — Rata-rata poin per anggota
- **Aturan Aktif** — Jumlah aturan pengumpulan poin yang sedang aktif

### Tindakan Cepat

Dashboard memiliki kartu pintas untuk mengelola semua aspek program:
- **Anggota** — Lihat dan kelola anggota keanggotaan
- **Level** — Konfigurasikan level keanggotaan
- **Hadiah** — Buat katalog hadiah
- **Penukaran** — Lihat riwayat penukaran
- **Aturan** — Konfigurasikan cara poin diperoleh
- **Lencana** — Kelola lencana pencapaian
- **Kampanye** — Jalankan kampanye keanggotaan khusus
- **Segmentasi** — Buat segmentasi anggota untuk penargetan

### Grafik dan Analisis

- **Tren Pendaftaran Anggota** — Pendaftaran anggota baru seiring waktu
- **Poin yang Diperoleh vs Ditebus** — Lacak keseimbangan aliran poin
- **Distribusi Level** — Lihat bagaimana anggota didistribusikan di berbagai level

## Menyiapkan Program

### Langkah 1: Membuat Level

Level mendefinisikan tingkat keanggotaan dengan manfaat yang meningkat:

1. Navigasikan ke **Keanggotaan > Level**
2. Buat level seperti Perunggu, Perak, Emas, Platinum
3. Untuk setiap level, atur:
   - **Nama** — Nama tampilan level
   - **Peringkat** — Urutan pengurutan (peringkat yang lebih rendah = level yang lebih rendah, contoh: Perunggu = 1, Perak = 2)
   - **Warna** — Warna aksen visual yang ditampilkan pada lencana anggota
   - **Poin Minimum yang Diperoleh** — Total poin yang diperoleh untuk memenuhi syarat level ini
   - **Pengeluaran Minimum** — Jumlah total pengeluaran untuk memenuhi syarat level ini
   - **Jumlah Pesanan Minimum** — Jumlah pesanan untuk memenuhi syarat level ini
   - **Pengali Poin** — Tingkat bonus pengumpulan poin untuk anggota di level ini (contoh: 2.0 = 2x poin)

Seorang anggota memenuhi syarat untuk level jika **salah satu** dari tiga ambang batas terpenuhi. Anda dapat menggunakan hanya satu ambang batas atau menggabungkan semua tiga.

### Langkah 2: Mengonfigurasi Aturan Pengumpulan Poin

Aturan mendefinisikan cara pelanggan memperoleh poin:

1. Navigasikan ke **Keanggotaan > Aturan**
2. Buat aturan menggunakan salah satu dari empat jenis aturan:

| Jenis Aturan | Deskripsi | Contoh |
|--------------|-----------|--------|
| **Pengeluaran** | Poin per jumlah yang dibelanjakan | 1 poin per $1 |
| **Barang** | Poin per barang yang dibeli | 50 poin per produk dalam kategori tertentu |
| **Aksi** | Poin untuk aksi tertentu | 200 poin untuk mendaftar |
| **Peristiwa** | Poin untuk acara kalender | Bonus poin ulang tahun |

3. Konfigurasikan pengaturan aturan tambahan:
   - **Cakupan / Filter Cakupan** — Batasi aturan ke produk, kategori, atau level keanggotaan tertentu
   - **Jumlah Pesanan Minimum** — Nilai keranjang minimum untuk aturan berlaku
   - **Level yang Diizinkan** — Batasi aturan ke level keanggotaan tertentu
   - **Eksklusif** — Saat diaktifkan, aturan ini tidak dapat digabungkan dengan aturan lain
   - **Hari Poin Tertunda** — Jumlah hari sebelum poin yang diperoleh menjadi tersedia (berguna untuk memperhitungkan jendela pengembalian)
   - **Hari Poin Kadaluarsa** — Jumlah hari setelah diperoleh sebelum poin kadaluarsa (biarkan kosong untuk tidak ada kadaluarsa)
   - **Mulai / Berakhir** — Batasi aturan ke rentang tanggal

### Langkah 3: Menyiapkan Hadiah

Hadiah adalah apa yang dapat ditukar oleh pelanggan dengan poin mereka:

1. Navigasikan ke **Keanggotaan > Hadiah**
2. Buat hadiah seperti:
   - **Kupon $5** — 500 poin
   - **Pengiriman Gratis** — 300 poin
   - **Diskon 10%** — 1000 poin

> **Kode diskon tidak dapat ditukarkan saat ini.** Sebuah hadiah dengan **Tipe Hadiah** yang diatur ke **Kode Diskon** — seperti contoh Kupon $5 Off atau Diskon 10% di atas — saat ini gagal untuk ditukarkan.

Anggota akan melihat kesalahan yang jelas dan poin mereka secara otomatis dikembalikan ke saldonya, sehingga tidak ada yang terbuang, tetapi hadiah tersebut belum bisa digunakan saat ini.

Ini adalah perbaikan yang disengaja: sebelumnya, penukaran melaporkan keberhasilan sementara mengurangi poin dan memberikan sesuatu.

Jika anggota menyebutkan penukaran "tidak berfungsi", itu adalah hal ini — bukan masalah baru.

Hadiah berbasis poin akan mulai berfungsi lagi dalam rilis mendatang.

Ini tidak memengaruhi hadiah Gratis Pengiriman, Gratis Produk, atau Pengalaman/Penghargaan.

### Langkah 4: Membuat Badge (Opsional)

Badge mengakui pencapaian pelanggan:

1. Navigasikan ke **Loyalty > Badges**
2. Buat badge untuk pencapaian:
   - **Pembelian Pertama** — Diberikan setelah pesanan pertama
   - **Pengeluaran Besar** — Diberikan setelah pengeluaran $500+
   - **Pelanggan Setia** — Diberikan setelah 10 pesanan

Badge dapat mencakup pemberian poin bonus saat diperoleh.

## Mengelola Anggota

### Daftar Anggota

Lihat semua anggota loyalitas beserta:
- Tier dan status saat ini
- Saldo poin
- Tanggal pendaftaran
- Aktivitas terbaru

### Pemenang Poin Teratas

Dashboard menyoroti anggota paling aktif dengan leaderboard yang menampilkan peringkat, nama, tier, dan poin yang diperoleh dalam periode tertentu.

### Transaksi Terbaru

Log transaksi menampilkan semua aktivitas poin terbaru. Jenis transaksi meliputi:

| Jenis | Arti |
|------|---------|
| **Mendapatkan** | Poin dikreditkan dari pembelian yang memenuhi syarat atau aturan |
| **Menukar** | Poin yang digunakan untuk hadiah |
| **Bonus** | Poin tambahan dari badge, kampanye, atau pemberian manual |
| **Penyesuaian** | Koreksi poin manual yang dibuat oleh staf |
| **Membatalkan** | Poin yang dihapus (misalnya, setelah pembatalan pesanan) |
| **Kadaluarsa** | Poin yang telah melebihi tanggal kedaluarsa |

### Penyesuaian Poin Manual

Anda dapat menambahkan atau mengurangi poin secara manual untuk anggota mana pun:

1. Buka halaman detail anggota
2. Klik **Penyesuaian Poin**
3. Masukkan jumlah poin (positif untuk menambah, negatif untuk mengurangi)
4. Masukkan alasan penyesuaian
5. Klik **Simpan**

Penyesuaian dicatat sebagai transaksi dan terlihat dalam riwayat transaksi anggota.

## Kampanye

Kampanye loyalitas memungkinkan Anda menjalankan promosi khusus:
- **Minggu Poin Ganda** — Sementara meningkatkan tingkat penambahan poin
- **Peristiwa Poin Bonus** — Memberikan poin tambahan untuk tindakan tertentu
- **Promosi Peningkatan Tier** — Menurunkan ambang batas untuk peningkatan tier

## Tips

- Mulailah dengan aturan penambahan poin yang sederhana (1 poin per $1 yang dibelanjakan) dan perluas seiring waktu.
- Tetapkan ambang batas hadiah yang dapat dicapai untuk menjaga keterlibatan anggota — jika hadiah terasa tidak tercapai, anggota akan kehilangan minat.
- Gunakan badge untuk menggame-ifikasi pengalaman dan mendorong perilaku tertentu.
- Pantau Tingkat Penukaran — program yang sehat memiliki tingkat penukaran 10-30%.
- Jalankan kampanye selama periode sepi untuk meningkatkan keterlibatan.
- Gunakan grafik Poin yang Diperoleh vs. Diturunkan untuk memastikan program Anda berkelanjutan.
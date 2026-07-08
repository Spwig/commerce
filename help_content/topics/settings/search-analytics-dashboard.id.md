---
title: Dashboard Analitik Pencarian
---

Dashboard Analitik Pencarian melacak setiap query pencarian di toko Anda, memberikan wawasan mengenai apa yang dicari pelanggan, pencarian mana yang berhasil atau gagal, dan seberapa cepat sistem pencarian Anda merespons. Gunakan data ini untuk mengidentifikasi produk populer, menemukan inventaris yang hilang, membuat sinonim, dan mengoptimalkan kinerja pencarian.

Pelacakan analitik harus diaktifkan di **Pengaturan Pencarian > Tab Analitik** agar data muncul.

![Dashboard Analitik](/static/core/admin/img/help/search-analytics-dashboard/analytics-dashboard.webp)

## Gambaran Dashboard

Navigasikan ke **Pencarian > Analitik Pencarian** untuk mengakses dashboard. Halaman ini menampilkan:

**Kartu Statistik** - Metrik cepat untuk hari ini dan minggu ini:
- Total pencarian hari ini
- Total pencarian minggu ini
- Query tanpa hasil (pencarian yang mengembalikan tidak ada produk)
- Waktu respons rata-rata dalam milidetik

**Tabel Query Teratas** - Istilah pencarian yang paling sering dengan jumlah hasil

**Query Tanpa Hasil** - Pencarian yang mengembalikan tidak ada hasil (kritis untuk peningkatan)

**Daftar Query** - Semua catatan pencarian individu dengan filter

## Statistik Hari Ini

**Total Pencarian Hari Ini** - Jumlah semua permintaan pencarian sejak tengah malam dalam zona waktu toko Anda. Termasuk baik permintaan autocomplete maupun halaman pencarian penuh.

**Query Unik Hari Ini** - Jumlah istilah pencarian yang berbeda digunakan hari ini. Jika 5 pelanggan semua mencari "laptop", ini dihitung sebagai 1 query unik meskipun ada 5 pencarian total.

**Query Tanpa Hasil Hari Ini** - Pencarian hari ini yang mengembalikan tidak ada produk. Jumlah query tanpa hasil yang tinggi menunjukkan produk yang hilang atau cakupan sinonim yang buruk.

Data terkini diperbarui secara real-time saat pencarian terjadi.

## Statistik Mingguan

**Total Mingguan** - Total pencarian dalam 7 hari terakhir

**Query Unik** - Istilah pencarian yang berbeda digunakan minggu ini

**Pertumbuhan Mingguan** - Persentase perubahan dibandingkan minggu sebelumnya (jika ditampilkan)

Gunakan data mingguan untuk mengidentifikasi tren: peningkatan volume pencarian sering berkorelasi dengan pertumbuhan lalu lintas atau kampanye pemasaran.

## Waktu Respons Rata-Rata

⚠️ **PENGAWASAN KINERJA**

Waktu rata-rata (dalam milidetik) untuk menjalankan query pencarian. Target waktu respons:

| Jenis Query | Target | Ambang Batas Peringatan |
|------------|--------|-------------------|
| Autocomplete | < 200ms | > 300ms secara konsisten |
| Pencarian Penuh | < 500ms | > 800ms secara konsisten |

Jika waktu respons rata-rata melebihi ambang batas peringatan:
1. Periksa **Pengaturan Pencarian > Tab Penyimpanan Sementara** - tingkatkan TTL penyimpanan sementara
2. Tinjau **Tab Pemindaian Mendalam** - nonaktifkan fitur yang mahal (indeksasi dokumen, indeksasi ulasan pada katalog besar)
3. Lihat panduan [Optimasi Kinerja Pencarian](/en/admin/help/search-performance-optimization/)

## Query Teratas

Tabel Query Teratas menampilkan istilah pencarian yang paling sering:

**Gunakan Data Ini Untuk**:
- **Fiturkan produk populer** - Jika "headset nirkabel" adalah query teratas, fiturkan produk tersebut secara menonjol di halaman utama Anda
- **Keputusan Stok** - Volume pencarian tinggi untuk kategori menunjukkan permintaan
- **Identifikasi tren** - Pencarian musiman mengungkapkan apa yang sedang populer saat ini
- **Pembuatan Konten** - Tulis artikel blog atau panduan tentang topik yang sering dicari

Tinjau query teratas setiap bulan untuk menyelaraskan merchandising Anda dengan minat pelanggan.

## Query Tanpa Hasil

**KRITIS UNTUK PENINGKATAN** - Query tanpa hasil adalah harta karun untuk mengoptimalkan toko Anda.

Query tanpa hasil terjadi karena tiga alasan utama:

### 1. Produk yang Hilang

Pelanggan mencari produk yang tidak Anda jual.

**Contoh**: Pencarian berulang untuk "matras yoga" tetapi Anda hanya menjual peralatan kebugaran, bukan peralatan yoga.

**Tindakan**: Pertimbangkan menambahkan produk ini ke katalog Anda jika pencarian sering terjadi.

### 2. Sinonim yang Hilang

Pelanggan menggunakan istilah yang tidak cocok dengan deskripsi produk Anda.

**Contoh**: Pelanggan mencari "laptop" tetapi produk Anda semua menyebutkan "komputer notebook".

**Tindakan**: Buat peta sinonim yang memetakan istilah pelanggan ke bahasa produk Anda. Lihat [Mengelola Sinonim dan Redirect](/en/admin/help/managing-synonyms-redirects/).

### 3. Pemadanan Fuzzy yang Buruk

Kesalahan ketik atau ejaan tidak cocok bahkan dengan pencarian fuzzy yang diaktifkan.

**Contoh**: Pencarian "accomodate" tidak menemukan produk "accommodate".

**Tindakan**:
- Turunkan ambang batas kesamaan di **Pengaturan Pencarian > Tab Pemadanan Fuzzy** (dari 0,80 menjadi 0,75)
- Tambahkan sinonim satu arah untuk kesalahan ejaan umum

**Alur Kerja Mingguan**:
1. Tinjau query tanpa hasil setiap Senin
2. Kategorisasi: Produk yang hilang, sinonim yang hilang, atau kesalahan ejaan
3. Tambahkan sinonim untuk istilah yang sering dicari
4. Catat celah produk untuk perencanaan inventaris

## Detail Query

Klik query apa pun dalam daftar untuk melihat detail lengkap:

**Field yang Ditrack**:
- **Teks Query** - Apa yang dicari oleh pelanggan
- **Timestamp** - Kapan pencarian terjadi
- **Jumlah Hasil** - Berapa banyak hasil yang dikembalikan
- **Waktu Respons** - Milidetik untuk menjalankan (pengawasan kinerja)
- **Pengguna** - Pelanggan yang masuk (jika pelacakan pengguna diaktifkan)
- **ID Sesi** - Penanda pengidentifikasi sesi anonim
- **Bahasa** - Bahasa toko saat pencarian
- **Mesin** - Mesin pencarian yang memproses query

## Penyaringan dan Pencarian

Gunakan penyaring untuk menganalisis segmen tertentu:

**Hierarki Tanggal** - Saring berdasarkan tanggal, bulan, atau tahun

**Penyaring Bahasa** - Lihat pencarian berdasarkan bahasa (berguna untuk toko multi-bahasa)

**Penyaring Mesin** - Bandingkan perilaku pencarian di berbagai mesin

**Toggle Query Tanpa Hasil** - Tampilkan hanya query yang mengembalikan tidak ada hasil

**Kotak Pencarian** - Cari teks query tertentu

## Mengunduh Data

Klik **Unduh** untuk mengunduh data query sebagai CSV untuk analisis lebih lanjut di Excel atau alat data.

**CSV mencakup**:
- Semua teks query
- Timestamps
- Jumlah hasil
- Waktu respons
- Data bahasa dan mesin

Gunakan unduhan untuk:
- Analisis tren seiring waktu
- Mengidentifikasi pola pencarian musiman
- Audit kinerja
- Presentasi kepada pemangku kepentingan

## Pertimbangan Privasi

Pelacakan analitik pencarian menghormati privasi:

**Pelacakan Pengguna** (opsional) - Menghubungkan pencarian dengan akun pelanggan yang masuk. Nonaktifkan untuk kepatuhan GDPR/CCPA di **Pengaturan Pencarian > Tab Analitik**.

**Pelacakan Sesi** (default) - Menggunakan ID sesi anonim untuk melacak pola pencarian tanpa mengidentifikasi pelanggan. Ramah privasi.

**Retensi Data** - Query pencarian tetap berada di database secara permanen. Implementasikan kebijakan retensi khusus jika diperlukan untuk kepatuhan.

## Menggunakan Analitik untuk Meningkatkan Pencarian

Wawasan yang dapat diambil dari analitik pencarian:

**Tugas Mingguan**:
- Tinjau query tanpa hasil dan tambahkan sinonim untuk istilah umum
- Pantau waktu respons dan optimalkan jika konsisten lambat
- Identifikasi pencarian teratas dan pastikan produk tersebut tersedia dalam jumlah yang cukup

**Tugas Bulanan**:
- Analisis query teratas untuk memandu pemilihan produk
- Unduh data untuk mengidentifikasi tren musiman
- Tinjau pola pencarian berdasarkan bahasa
- Lacak jumlah klik redirect untuk mengoptimalkan pintasan navigasi

**Tugas Kuartalan**:
- Audit efektivitas sinonim (apakah jumlah query tanpa hasil berkurang?)
- Bandingkan pertumbuhan volume pencarian dengan lalu lintas secara keseluruhan
- Uji A/B perubahan bobot dan ukur relevansi hasil
- Tinjau apakah kategori produk baru harus ditambahkan berdasarkan permintaan pencarian

## Tips

- **Query tanpa hasil adalah harta karun untuk peningkatan** - Mereka secara langsung memberi tahu Anda apa yang dicari pelanggan tetapi tidak Anda sediakan
- **Tinjau analitik di pagi hari Senin** - Mulai minggu Anda dengan mengoptimalkan berdasarkan data minggu sebelumnya
- **Waktu respons >300ms secara konsisten = selidiki** - Periksa pengaturan penyimpanan sementara terlebih dahulu, lalu fitur pemindaian mendalam
- **Unduh CSV untuk analisis tren** - Analisis spreadsheet mengungkap pola yang tidak terlihat di antarmuka admin
- **Buat sinonim sebelum menambahkan produk** - Jika pelanggan mencari "kasing tablet" tetapi Anda menyebutnya "pelindung" tambahkan sinonim terlebih dahulu
- **Lacak pola pencarian musiman** - "Sepatu musim dingin" di bulan Oktober, "baju renang" di bulan Maret - persiapkan inventaris sesuai


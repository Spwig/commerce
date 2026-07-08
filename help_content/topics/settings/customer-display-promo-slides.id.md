---
title: Customer Display Promo Slides
---

Promotional slides tampil di layar yang menghadap ke pelanggan ketika terminal POS tidak aktif (tidak ada transaksi yang sedang berlangsung). Buat sebuah carousel gambar yang menampilkan promosi musiman, peluncuran produk baru, kebijakan toko, acara mendatang, dan manfaat program loyalitas. Slide dapat ditargetkan ke toko tertentu atau kelompok menggunakan penugasan cakupan - jalankan promosi liburan hanya di toko-toko AS, atau tampilkan informasi acara lokal hanya di lokasi yang relevan. Slide aktif berputar secara otomatis setiap 5-10 detik, menciptakan tanda digital yang menarik yang menjaga pelanggan tetap terinformasi saat menunggu.

Gunakan slide promosi untuk meningkatkan kesadaran akan promosi saat ini, mengedukasi pelanggan tentang kebijakan, dan mendorong keterlibatan dengan program loyalitas dan acara.

![Promo Slide List](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Perilaku Tampilan Pelanggan

Ketika terminal POS tidak aktif (tidak ada pelanggan di meja kasir, tidak ada transaksi yang sedang berlangsung), layar yang menghadap ke pelanggan menampilkan:

**Mode Carousel**:
- Berputar melalui semua slide aktif
- Setiap slide ditampilkan selama 5-10 detik (dapat dikonfigurasi per terminal)
- Transisi perlahan antar slide
- Berputar terus-menerus hingga transaksi dimulai

**Selama Transaksi**:
- Carousel berhenti segera
- Layar beralih ke tampilan transaksi (item, total sementara, prompt pembayaran)
- Carousel melanjutkan ketika transaksi selesai dan terminal kembali ke mode tidak aktif

**Tidak Ada Slide yang dikonfigurasi**:
- Layar menampilkan pesan "Welcome" dengan branding toko
- Layar statis (tidak ada carousel)

**Persyaratan Teknis**:
- Tampilan pelanggan dapat menjadi monitor terpisah atau layar yang sama dengan kasir (aplikasi POS mendukung mode picture-in-picture)
- Layar disinkronkan melalui API BroadcastChannel (komunikasi antar perangkat yang sama) atau WebSocket (layar perangkat terpisah)

## Penargetan Cakupan

Seperti template struk, slide promosi mendukung penargetan berbasis cakupan (prioritas tertinggi ke terendah):

| Prioritas | Cakupan | Contoh | Kasus Penggunaan |
|-----------|--------|------|------------------|
| **1** | Spesifik toko | Slide toko Paris | Slide acara festival musim panas Paris |
| **2** | Spesifik kelompok | Slide toko Eropa | Slide kebijakan privasi GDPR hanya untuk Eropa |
| **3** | Semua toko | Slide global | "Pengiriman gratis untuk pesanan >$50" (promosi perusahaan-wide) |

**Bagaimana Cakupan Bekerja**:
- Terminal menampilkan slide yang cocok dengan cakupan toko (slide spesifik toko)
- Plus slide yang cocok dengan cakupan kelompok (jika toko berada dalam kelompok)
- Plus slide tanpa penugasan cakupan (slide global)
- Hasil: Toko mungkin menampilkan 3-5 slide (campuran cakupan dan global)

**Contoh**:
- Slide global: "Program Loyalitas Baru - Bergabung Hari Ini!" (tanpa cakupan)
- Slide kelompok: "Diskon Memorial Day - 30% Off" (hanya kelompok toko AS)
- Slide toko: "Grand Opening - NYC Flagship" (hanya toko NYC)

**Terminal toko NYC** menampilkan semua 3 slide (toko + kelompok + global)
**Terminal toko London** hanya menampilkan slide global (tidak dalam kelompok toko AS, bukan toko NYC)

## Persyaratan Gambar

Slide promosi adalah gambar penuh layar yang dioptimalkan untuk monitor tampilan pelanggan:

**Rasio Aspek**: 16:9 (widescreen)

**Resolusi Direkomendasikan**: 1920×1080 piksel (Full HD)
- Membesar dengan bersih ke sebagian besar tampilan modern
- Keseimbangan ukuran file (kualitas vs kecepatan muat)

**Resolusi yang Diterima**:
- Minimum: 1280×720 (HD)
- Optimal: 1920×1080 (Full HD)
- Maksimum: 3840×2160 (4K) - tidak disarankan (ukuran file besar, muat lebih lambat)

**Format File**: JPG, PNG, atau WebP
- JPG untuk foto
- PNG untuk grafis dengan transparansi (meskipun latar belakang disarankan)
- WebP untuk ukuran file terkecil

**Ukuran File**: <500KB per slide
- File yang lebih besar memperlambat muat carousel
- Kompres gambar sebelum mengunggah (gunakan optimasi Perpustakaan Media)

**Rekomendasi Desain**:
- Kontras tinggi untuk keterbacaan dari jarak jauh (pelanggan 2-6 kaki dari tampilan)
- Teks besar (minimum 48pt untuk teks utama, 72pt+ untuk judul)
- Font tebal (font tipis menghilang di beberapa tampilan)
- Hindari detail kecil (tidak terlihat dari sudut pandang pelanggan)
- Sertakan ajakan bertindak (apa yang harus dilakukan pelanggan: "Tanyakan kasir untuk detail lebih lanjut", "Daftar hari ini")

## Membuat Slide Promosi

Navigasi ke **POS > Promo Slides** dan klik **+ Tambahkan Slide Promosi**:

![Promo Slide Add Form](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Gambar** - Unggah atau pilih dari Perpustakaan Media:
- Klik **Jelajahi Perpustakaan Media** untuk memilih gambar yang sudah ada
- Atau unggah gambar baru yang memenuhi persyaratan di atas
- Tampilan pratinjau menunjukkan bagaimana gambar akan muncul di layar

**Judul** (Opsional) - Teks overlay di bagian atas slide:
- Maks 60 karakter (teks yang lebih panjang akan dipotong)
- Muncul di bar gelap semi-transparan di bagian atas gambar
- Gunakan untuk judul slide ("Summer Sale", "New Arrivals")
- Biarkan kosong jika gambar sudah memiliki teks judul

**Subjudul** (Opsional) - Teks overlay di bawah judul:
- Maks 120 karakter
- Muncul di bawah judul dalam bar semi-transparan yang sama
- Gunakan untuk detail pendukung ("Up to 50% off", "Free gift with purchase")
- Biarkan kosong jika gambar sudah lengkap

**Apakah Aktif** - Toggle untuk mengaktifkan/menonaktifkan slide:
- Hanya slide aktif yang muncul di carousel
- Gunakan untuk aktivasi musiman (matikan setelah promosi selesai)
- Menonaktifkan tetap menyimpan slide untuk pengaktifan ulang di masa depan

**Urutan Sortir** - Mengontrol posisi slide di carousel:
- Angka yang lebih rendah muncul lebih awal dalam rotasi
- Gunakan kelipatan 10: 10, 20, 30 (memungkinkan memasukkan slide antara yang sudah ada)
- Contoh: Penjualan liburan (urutan sortir 10) ditampilkan sebelum program loyalitas umum (urutan sortir 20)

**Penugasan Cakupan** (Opsional):
- **Gudang** - Pilih untuk menampilkan hanya di toko tertentu
- **Kelompok Toko** - Pilih untuk menampilkan hanya di toko dalam kelompok
- **Biarkan keduanya kosong** - Menampilkan di semua toko (slide global)

## Urutan Sortir dan Alur Carousel

**Contoh Carousel** (terminal toko NYC):
- Slide 1 (urutan sortir 10): "Grand Opening - NYC Flagship" (spesifik toko)
- Slide 2 (urutan sortir 15): "Memorial Day Sale - 30% Off" (kelompok toko AS)
- Slide 3 (urutan sortir 20): "New Loyalty Program - Join Today!" (global)
- Slide 4 (urutan sortir 30): "Follow us @yourstore" (global)

Carousel berputar: 1 → 2 → 3 → 4 → 1 → 2 → ...

**Terminal toko London** (tidak dalam kelompok toko AS, toko berbeda):
- Slide 1 (urutan sortir 20): "New Loyalty Program - Join Today!" (global)
- Slide 2 (urutan sortir 30): "Follow us @yourstore" (global)

Carousel berputar: 1 → 2 → 1 → 2 → ...

Gunakan urutan sortir untuk memprioritaskan konten yang paling penting pertama dalam rotasi.

## Strategi Aktivasi Musiman

**Masalah**: Membuat/menghapus slide untuk setiap promosi musiman adalah tugas yang melelahkan.

**Solusi**: Buat slide sekali, aktifkan/matikan secara musiman:

1. **Buat Slide untuk Acara Besar**:
   - "Summer Sale" (Apakah Aktif: Tidak, dibuat sebelumnya)
   - "Back to School" (Apakah Aktif: Tidak, dibuat sebelumnya)
   - "Black Friday" (Apakah Aktif: Tidak, dibuat sebelumnya)
   - "Holiday Sale" (Apakah Aktif: Tidak, dibuat sebelumnya)

2. **Aktifkan Ketika Relevan**:
   - 1 Juni: Setel "Summer Sale" → Apakah Aktif: Ya
   - 15 Agustus: Setel "Summer Sale" → Apakah Aktif: Tidak, setel "Back to School" → Apakah Aktif: Ya
   - 20 November: Setel "Black Friday" → Apakah Aktif: Ya
   - 1 Desember: Setel "Black Friday" → Apakah Aktif: Tidak, setel "Holiday Sale" → Apakah Aktif: Ya

3. **Matikan Setelah Acara**:
   - Menjaga perpustakaan slide tetap rapi
   - Ulangi slide tahun ke tahun (perbarui gambar jika diperlukan, tetapkan konfigurasi)

## Contoh Kasus Penggunaan

**Kasus Penggunaan 1: Promosi Musiman**
- Gambar: Latar belakang merah dengan teks putih "SUMMER SALE - UP TO 60% OFF"
- Judul: "Summer Sale"
- Subjudul: "50-60% off select items. Ask cashier for details."
- Cakupan: Semua toko (global)
- Urutan sortir: 10 (prioritas tertinggi selama musim panas)
- Aktif: Hanya Juni-Agustus

**Kasus Penggunaan 2: Kebijakan Toko**
- Gambar: Infografis yang menampilkan langkah-langkah kebijakan pengembalian
- Judul: "Easy Returns"
- Subjudul: "30 hari dengan struk. Tidak ada pertanyaan."
- Cakupan: Semua toko (global)
- Urutan sortir: 40 (prioritas lebih rendah dari promosi)
- Aktif: Sepanjang tahun

**Kasus Penggunaan 3: Peluncuran Produk Baru**
- Gambar: Foto produk utama dari item baru
- Judul: "NEW: Wireless Earbuds Pro"
- Subjudul: "Sekarang tersedia di toko dan online. $199.99"
- Cakupan: Semua toko (global)
- Urutan sortir: 5 (prioritas tertinggi selama minggu peluncuran)
- Aktif: Hanya minggu peluncuran, lalu matikan

**Kasus Penggunaan 4: Acara Lokal**
- Gambar: Poster lomba amal lokal
- Judul: "Support Local"
- Subjudul: "Bergabunglah dengan kami di Community 5K pada 15 Juni!"
- Cakupan: Toko spesifik (hanya toko NYC)
- Urutan sortir: 8 (prioritas untuk toko ini)
- Aktif: 2 minggu sebelum acara

**Kasus Penggunaan 5: Program Loyalitas**
- Gambar: Visual kartu loyalitas dengan contoh poin
- Judul: "Earn Rewards"
- Subjudul: "Bergabunglah dengan program loyalitas kami dan dapatkan 1 poin per $1 yang dibelanjakan"
- Cakupan: Semua toko (global)
- Urutan sortir: 30 (konten evergreen)
- Aktif: Sepanjang tahun

## Mengelola Slide

**Tampilan Daftar Slide**:
- Menampilkan semua slide dengan pratinjau gambar, judul, cakupan, status
- Saring berdasarkan aktif/tidak aktif
- Saring berdasarkan cakupan (lihat semua slide global, semua slide kelompok, dll.)

**Aktivasi/Matikan Secara Massal**:
- Pilih beberapa slide dalam daftar
- Gunakan aksi admin untuk mengaktifkan atau menonaktifkan semua sekaligus
- Berguna untuk transisi musiman (matikan semua slide musim panas, aktifkan semua slide musim gugur)

**Menguji Slide**:
- Setelah membuat/memperbarui slide, navigasikan ke terminal POS
- Biarkan terminal menjadi tidak aktif (tidak ada transaksi)
- Verifikasi slide muncul di carousel
- Periksa kualitas gambar, keterbacaan teks overlay, dan waktu tampil

**Memperbarui Slide Aktif**:
- Perubahan berlaku saat carousel diperbarui berikutnya (biasanya <30 detik)
- Tidak perlu merestart terminal

## Tips

- **Desain untuk jarak** - Pelanggan melihat tampilan dari jarak 2-6 kaki; gunakan teks besar dan kontras tinggi
- **Jaga pesan sederhana** - Slide ditampilkan selama <10 detik; satu pesan jelas per slide
- **Gunakan penonaktifan musiman** - Buat sekali, ubah aktif/mati setiap tahun daripada membuat ulang
- **Prioritaskan dengan urutan sortir** - Promosi yang paling penting harus memiliki urutan sortir terendah (muncul pertama)
- **Uji pada perangkat keras sebenarnya** - Kalibrasi warna tampilan bervariasi; verifikasi slide terlihat baik di monitor spesifik Anda
- **Batasi jumlah slide aktif** - 3-5 slide aktif per toko adalah optimal; 10+ slide berarti setiap slide muncul jarang
- **Sertakan ajakan bertindak** - Ceritakan kepada pelanggan apa yang harus dilakukan ("Tanyakan kasir", "Kunjungi situs web", "Skan kode QR di struk")
- **Perbarui secara teratur** - Promosi yang usang (diskon yang sudah berakhir, acara masa lalu) mengurangi kepercayaan pelanggan
- **Gunakan cakupan secara strategis** - Promosi regional (cakupan kelompok) dan acara lokal (cakupan toko) terasa lebih relevan daripada konten global yang konstan


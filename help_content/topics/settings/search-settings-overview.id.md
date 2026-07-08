---
title: Memahami Pengaturan Pencarian
---

Antarmuka SearchSettings mengontrol perilaku pencarian global di toko Spwig Anda. Halaman konfigurasi tunggal ini menggunakan antarmuka 8 tab untuk mengorganisir opsi pencarian, dari pemberdayaan dasar hingga penyetelan kinerja lanjutan. Perubahan di sini berlaku untuk semua mesin pencari kecuali diatasi di tingkat mesin.

Panduan ini menjelajahi setiap tab, menjelaskan apa yang dilakukan setiap pengaturan dan kapan harus menyesuaikannya.

![Tab Umum Pengaturan Pencarian](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## Antarmuka 8 Tab

SearchSettings adalah model singleton - hanya satu catatan konfigurasi yang ada (pk=1) untuk seluruh toko Anda. Antarmuka dibagi menjadi delapan tab:

| Tab | Tujuan |
|-----|---------|
| **Umum** | Menyalakan/mematikan pencarian, mengatur parameter dasar |
| **Autocomplete** | Mengatur perilaku dropdown pencarian prediktif |
| **Jenis Konten** | Pilih jenis konten yang dapat dicari |
| **Indeks Mendalam** | Kontrol data produk apa yang diindeks (dampak kinerja) |
| **Pemadanan Fuzzy** | Toleransi ejaan dan ambang batas kesamaan |
| **Bobot** | Pengali relevansi untuk peringkat hasil |
| **Pencachan** | Pertukaran waktu respons dan kebaruan |
| **Analitik** | Pelacakan kueri dan pengaturan privasi |

Setiap tab fokus pada aspek spesifik dari konfigurasi pencarian.

## Tab Umum

Tab Umum berisi pengaturan inti yang memengaruhi semua pencarian:

**Menyalakan Pencarian** - Sakelar utama untuk sistem pencarian. Ketika dimatikan, semua fitur pencarian tidak aktif di seluruh toko Anda, termasuk autocomplete dan halaman hasil pencarian.

**Panjang Kueri Minimum** - Default: 2 karakter. Pencarian yang lebih pendek dari ini ditolak. Menetapkan ini ke 1 memungkinkan pencarian satu karakter (misalnya, "A") tetapi meningkatkan beban server.

**Hasil Per Halaman** - Default: 20 item. Mengontrol paginasi untuk halaman hasil pencarian. Nilai yang lebih tinggi (30-50) mengurangi klik paginasi tetapi meningkatkan waktu muat halaman.

## Tab Jenis Konten

![Pengaturan Jenis Konten](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Nyalakan/matikan jenis konten yang muncul dalam hasil pencarian:

- **Produk** - Produk fisik, digital, dan langganan
- **Kategori** - Kategori produk
- **Merek** - Merek produk
- **Pos Blog** - Konten blog

**Catatan Kinerja**: Semakin sedikit jenis konten = pencarian yang lebih cepat. Setiap jenis yang diaktifkan menambahkan kueri database tambahan. Jika Anda tidak memiliki blog, matikan Pos Blog untuk meningkatkan waktu respons.

## Tab Indeks Mendalam

⚠️ **PERINGATAN KINERJA** - Pengaturan ini memiliki dampak kinerja yang signifikan.

![Pengaturan Indeks Mendalam](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Indeks mendalam mengontrol data terkait produk apa yang dimasukkan ke dalam pencarian:

**Indeks SKU** - Default: AKTIF, Dampak Rendah. Memasukkan SKU produk dan variasi ke dalam pencarian. Penting untuk toko B2B di mana pelanggan mencari berdasarkan kode produk.

**Indeks Atribut** - Default: AKTIF, Dampak Sedang. Memasukkan atribut produk (warna, ukuran, bahan) ke dalam pencarian. Menambahkan JOIN ke tabel atribut. Penting untuk produk fashion dan produk yang dapat dikonfigurasi.

**Indeks Bidang Kustom** - Default: AKTIF, Dampak Sedang. Memasukkan bidang kustom yang didefinisikan oleh pedagang ke dalam hasil pencarian. Memerlukan traversal JSONField.

**Indeks Ulasan** - Default: AKTIF, Dampak Sedang-Tinggi ⚠️

Indeks ulasan memasukkan judul dan komentar ulasan yang disetujui ke dalam pencarian. Menggabungkan ke tabel ulasan dan menambahkan beban pencarian teks. Berguna untuk katalog yang berfokus pada ulasan.

**Indeks Dokumen** - Default: MATI, **DAMPK TINGGI SEKALI** ⚠️

Indeks dokumen mengekstrak teks dari file PDF, DOCX, dan XLSX yang terlampir ke produk digital. Fitur ini:

- Memerlukan indeks awal yang sangat mahal
- Menambahkan beban kueri yang signifikan pada setiap pencarian
- Dapat menyebabkan timeout pada file besar
- **Hanya boleh diaktifkan untuk toko produk digital dengan dokumen yang dapat dicari**
- **Jangan pernah mengaktifkan secara sembarangan** - uji dampak kinerja secara menyeluruh

## Tab Pemadanan Fuzzy

![Pengaturan Pemadanan Fuzzy](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

Pemadanan fuzzy menggunakan jarak Levenshtein untuk menangani kesalahan ejaan:

**Menyalakan Pemadanan Fuzzy** - Memungkinkan pencarian untuk cocok dengan istilah serupa (misalnya, "laptop" cocok dengan "labtop")

**Ambang Batas Kesamaan** - Default: 0,80 (80% kesamaan). Rentang: 0,0-1,0. Nilai yang lebih tinggi memerlukan cocok yang lebih dekat dan berjalan lebih cepat. Nilai yang lebih rendah menangkap lebih banyak kesalahan ejaan tetapi mungkin mengembalikan hasil yang tidak relevan.

**Jarak Edit Maksimum** - Default: 2 perubahan karakter. Jumlah maksimum dari penyisipan, penghapusan, atau substitusi yang diperbolehkan. Nilai yang lebih rendah (1) meningkatkan kinerja tetapi menangkap lebih sedikit kesalahan ejaan.

## Tab Bobot

Bobot mengontrol skor relevansi - bagaimana hasil diurutkan. Tab Bobot menunjukkan pengali default untuk setiap bidang yang dapat dicari:

- weight_name: 1,50 (nama produk paling penting)
- weight_sku: 1,20
- weight_description: 0,80
- weight_categories: 0,80
- weight_attributes: 0,70
- weight_brands: 0,70
- weight_blog_posts: 0,60
- weight_reviews: 0,50

Pengaturan default ini bekerja dengan baik untuk sebagian besar toko e-commerce. Untuk informasi terperinci tentang menyesuaikan bobot dan memahami dampaknya, lihat topik [Bobot Relevansi dan Indeks Mendalam](/en/admin/help/relevance-weights-deep-indexing/).

## Tab Pencachan

![Pengaturan Pencachan](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

Pencachan meningkatkan kinerja pencarian secara dramatis dengan menyimpan hasil terbaru:

**TTL Cache Autocomplete** - Default: 60 detik. Seberapa lama hasil autocomplete disimpan. TTL yang lebih pendek (30-45 detik) = hasil yang lebih segar tetapi lebih banyak kueri database. TTL yang lebih panjang (90-120 detik) = lebih cepat tetapi hasil yang mungkin sudah ketinggalan.

**TTL Cache Hasil** - Default: 300 detik (5 menit). Durasi cache halaman hasil pencarian lengkap. TTL yang lebih panjang secara signifikan meningkatkan kinerja tetapi menunda visibilitas produk baru.

**Pertukaran**: Pencachan adalah optimasi kinerja yang paling efektif tunggal. Jika pencarian lambat, tingkatkan nilai-nilai ini sebelum menonaktifkan fitur.

## Tab Analitik

![Pengaturan Analitik](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Lacak Kueri Pencarian** - Memungkinkan dashboard analitik pencarian. Merekam teks kueri, jumlah hasil, waktu respons, dan tanda waktu.

**Lacak Informasi Pengguna** - Menghubungkan pencarian dengan pengguna yang masuk. Nonaktifkan untuk kepatuhan privasi (GDPR, CCPA).

**Lacak Informasi Sesi** - Menggunakan ID sesi untuk melacak pencarian pengguna anonim. Berguna untuk mengidentifikasi pola pencarian tanpa data pribadi.

## Pola Singleton

SearchSettings menggunakan pola singleton - hanya satu catatan pengaturan yang ada di database Anda (pk=1). Ketika Anda mengakses Pengaturan Pencarian di admin, Anda selalu mengedit catatan yang sama.

Tidak ada opsi "Tambah" atau "Hapus" - hanya "Ubah". Semua mesin pencari mewarisi pengaturan ini kecuali mereka menentukan penimbalan per-mesin (langka).

## Tips

- **Jaga pengaturan default kecuali Anda memiliki kebutuhan spesifik** - Pengaturan default dioptimalkan untuk toko e-commerce umum
- **JANGAN AKTIFKAN indeks dokumen secara sembarangan** - Hanya untuk toko produk digital dengan dokumen yang dapat dicari, dan uji dampak kinerja terlebih dahulu
- **Pantau waktu respons di analitik** - Targetkan <200ms untuk autocomplete, <500ms untuk pencarian penuh
- **Tingkatkan TTL cache jika kinerja lambat** - Pencachan adalah kemenangan kinerja yang paling mudah
- **Periksa kueri tanpa hasil setiap minggu** - Mereka mengungkapkan produk yang hilang atau sinonim yang diperlukan
- **Matikan jenis konten yang tidak digunakan** - Jika Anda tidak memiliki blog, matikan Pos Blog untuk mempercepat pencarian

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis secara tepat seperti yang ditunjukkan dalam aturan pelestarian.
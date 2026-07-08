---
title: Pekerjaan Terjemahan
---

Pekerjaan terjemahan mengotomatisasi terjemahan besar-besaran dari jumlah besar konten. Sebaliknya dari menerjemahkan produk satu per satu secara manual, buat pekerjaan yang menerjemahkan seluruh katalog Anda—atau himpunan spesifik—di latar belakang. Pekerjaan berjalan secara asinkron, sehingga Anda dapat terus bekerja sementara ratusan atau ribuan bidang diterjemahkan secara otomatis.

Gunakan pekerjaan terjemahan saat mengaktifkan bahasa baru, mengimpor produk baru, atau mengejar konten yang belum diterjemahkan.

## Apa Itu Pekerjaan Terjemahan?

Pekerjaan terjemahan adalah tugas latar belakang yang:

1. **Memindai konten** untuk bidang yang dapat diterjemahkan (produk, halaman, posting blog, dll.)
2. **Mengidentifikasi bidang yang belum diterjemahkan atau usang** berdasarkan cakupan pekerjaan Anda
3. **Mengirimkan bidang ke mesin terjemahan** (model AI lokal atau penyedia eksternal)
4. **Menyimpan terjemahan** kembali ke konten Anda
5. **Melaporkan selesainya** dengan statistik tentang bidang yang diterjemahkan

Pekerjaan berjalan melalui antrian tugas Celery, sehingga mereka tidak menghambat antarmuka admin Anda.

## Kapan Menggunakan Pekerjaan Terjemahan

**Meluncurkan Bahasa Baru**:
- Aktifkan bahasa Jerman sebagai bahasa baru
- Buat pekerjaan: Terjemahkan semua produk dari Inggris ke Jerman
- Hasil: Seluruh katalog tersedia dalam bahasa Jerman dalam beberapa menit/jam (tergantung ukuran)

**Impor Produk Baru**:
- Impor 500 produk baru dalam bahasa Inggris
- Buat pekerjaan: Terjemahkan produk baru ke semua bahasa aktif
- Hasil: Stok baru segera tersedia di semua pasar

**Menyusul Celah**:
- Laporan cakupan menunjukkan Produk hanya 60% diterjemahkan ke Prancis
- Buat pekerjaan: Terjemahkan bidang produk yang hilang ke Prancis saja
- Hasil: Cakupan Prancis meningkat menjadi ~100%

**Memperbarui Terjemahan yang Ketinggalan**:
- Model terjemahan ditingkatkan atau penyedia baru tersedia
- Buat pekerjaan: Terjemahkan ulang semua produk ke Spanyol
- Hasil: Kualitas terjemahan Spanyol meningkat di seluruh katalog

## Membuat Pekerjaan Terjemahan

Navigasikan ke **Pengaturan > Pekerjaan Terjemahan** dan klik **+ Buat Pekerjaan**.

### Konfigurasi Pekerjaan

**Nama Pekerjaan** - Label deskriptif (misalnya, "Terjemahkan produk ke Jerman", "Posting blog baru - semua bahasa")

**Jenis Konten** - Apa yang akan diterjemahkan:
- Produk
- Kategori produk
- Halaman
- Posting blog
- Metadata SEO
- Template email
- Semua jenis konten

**Bahasa Sumber** - Bahasa yang Anda terjemahkan DARI (biasanya bahasa default Anda)

**Bahasa Target** - Satu atau lebih bahasa untuk diterjemahkan KE (pilih beberapa untuk terjemahan paralel)

**Cakupan** - Subset konten apa:
- **Semua item** - Terjemahkan semuanya tanpa memandang terjemahan yang sudah ada
- **Hanya yang belum diterjemahkan** - Lewati bidang yang sudah memiliki terjemahan
- **Dibuat/diperbarui sejak tanggal** - Hanya konten baru atau yang baru saja diubah
- **Item spesifik** - Pilih produk/halaman individu (filter lanjutan)

**Mesin Terjemahan** - Layanan apa yang akan digunakan:
- Model AI lokal (default, tanpa biaya API)
- Penyedia eksternal tertentu (DeepL, Google, Azure, AWS)
- Auto-pilih (menggunakan preferensi yang dikonfigurasi)

**Kunci Terjemahan** - Apakah mengunci bidang terjemahan terhadap penulisan ulang otomatis di masa depan (berguna untuk terjemahan yang telah ditinjau)

### Opsi Lanjutan

**Lewati Bidang Terkunci** - Jika diaktifkan, menghormati terjemahan terkunci yang sudah ada (dianjurkan)

**Tulis Ulang yang Ada** - Terjemahkan ulang meskipun terjemahan sudah ada (gunakan untuk peningkatan kualitas)

**Filter Bidang** - Terjemahkan hanya bidang spesifik (misalnya, nama produk dan deskripsi, lewati atribut)

**Ukuran Batch** - Berapa banyak item yang diproses sekaligus (default: 50, tingkatkan untuk pemrosesan yang lebih cepat jika server dapat menangani)

**Prioritas** - Pekerjaan dengan prioritas tinggi berjalan sebelum pekerjaan dengan prioritas normal (gunakan secara hati-hati)

## Siklus Hidup dan Status Pekerjaan

Pekerjaan berjalan melalui status berikut:

**Diantrikan** - Pekerjaan dibuat, menunggu pekerja untuk mengambilnya

**Diproses** - Pekerja secara aktif menerjemahkan konten

**Selesai** - Semua terjemahan selesai dengan sukses

**Gagal** - Pekerjaan mengalami kesalahan (periksa log kesalahan)

**Dibatalkan** - Dihentikan secara manual oleh admin

**Dijeda** - Dijeda sementara (dapat dilanjutkan)

## Memantau Kemajuan Pekerjaan

Halaman detail pekerjaan menunjukkan:

**Bar Pengembangan** - Persentase yang selesai

**Statistik**:
- Total item yang akan diterjemahkan
- Item yang selesai
- Item yang tersisa
- Waktu estimasi yang tersisa

**Log Real-Time** - Aliran aktivitas terjemahan (berguna untuk menyelesaikan masalah)

**Jumlah Kesalahan** - Berapa banyak bidang yang gagal diterjemahkan (dengan alasan)

## Hasil dan Statistik Pekerjaan

Ketika pekerjaan selesai, halaman hasil menunjukkan:

**Ringkasan**:
- Total bidang yang diproses
- Terjemahan berhasil
- Terjemahan gagal
- Dilewati (sudah diterjemahkan, terkunci, atau dikecualikan oleh filter)

**Pembreakdownan Per-Item**:
- Produk/halaman mana yang diterjemahkan
- Berapa banyak bidang per item
- Apa saja kesalahan yang dihadapi

**Metrik Kinerja**:
- Total waktu yang berlalu
- Rata-rata terjemahan per detik
- Mesin terjemahan yang digunakan

## Menangani Terjemahan yang Gagal

Jika beberapa terjemahan gagal:

**Periksa log kesalahan** - Mengidentifikasi bidang mana yang gagal dan mengapa

**Penyebab kegagalan umum**:
- Batas laju API tercapai (penyedia eksternal)
- Timeout mesin terjemahan (teks sangat panjang)
- Format bidang tidak valid (kesalahan parsing JSON)
- Model tidak mendukung pasangan bahasa

**Opsi Ulang**:
- Perbaiki masalah mendasar
- Buat pekerjaan baru hanya untuk item yang gagal
- Gunakan mesin terjemahan yang berbeda

## Membatalkan dan Menjeda Pekerjaan

**Batal** - Menghentikan pekerjaan segera, membuang terjemahan yang sedang berlangsung (terjemahan yang selesai disimpan)

**Jeda** - Menghentikan pekerjaan sementara, dapat dilanjutkan nanti dari tempat yang ditinggalkan

**Lanjutkan** - Melanjutkan pekerjaan yang dijeda

Gunakan jeda/lanjutkan ketika Anda perlu membebaskan sumber daya server secara sementara.

## Strategi Pekerjaan dalam Batch

**Strategi 1: Bahasa demi Bahasa**:
- Buat pekerjaan terpisah untuk setiap bahasa target
- Lebih mudah memantau kemajuan per bahasa
- Dapat memprioritaskan bahasa penting
- Menyebar beban selama waktu

**Strategi 2: Semua Sekaligus**:
- Satu pekerjaan menerjemahkan ke semua bahasa aktif
- Penyelesaian lebih cepat secara keseluruhan
- Beban server lebih tinggi selama pemrosesan
- Manajemen pekerjaan lebih sederhana

**Strategi 3: Jenis Konten demi Jenis Konten**:
- Terjemahkan produk terlebih dahulu (prioritas tertinggi)
- Lalu kategori, halaman, posting blog
- Memungkinkan peluncuran bertahap
- Lebih mudah menguji dan memverifikasi terjemahan

Pilih berdasarkan kapasitas server Anda, urgensi, dan ukuran katalog.

## Jadwal Pekerjaan

Jadwalkan pekerjaan berulang untuk menangani konten baru secara otomatis:

**Pekerjaan Harian** - Terjemahkan produk yang dibuat/diperbarui dalam 24 jam terakhir

**Pekerjaan Mingguan** - Menyusul celah terjemahan mingguan

**Setelah Impor** - Memicu pekerjaan secara otomatis setelah impor produk dalam jumlah besar

**Saat Aktivasi Bahasa** - Membuat pekerjaan otomatis saat Anda mengaktifkan bahasa baru

Pekerjaan yang dijadwalkan menjaga terjemahan tetap up-to-date tanpa intervensi manual.

## Pertimbangan Kinerja

**Model AI Lokal**:
- ~100-500 terjemahan/detik (tergantung pada server)
- Intensif CPU selama pemrosesan
- Tidak ada batas laju API
- Gratis (tidak ada biaya per terjemahan)

**Penyedia Eksternal**:
- Batas laju bervariasi (DeepL: 500k karakter/bulan di tier gratis)
- Latensi API menambahkan overhead
- Kualitas lebih baik tetapi memerlukan biaya
- Batas permintaan bersamaan

**Pekerjaan besar** (>10.000 bidang):
- Jalankan selama jam non-peak
- Pantau sumber daya server
- Pertimbangkan memecah menjadi batch yang lebih kecil
- Uji dengan subset terlebih dahulu

## Tips

- **Mulai kecil** - Uji pekerjaan pada subset (misalnya, 10 produk) sebelum menjalankan terjemahan katalog penuh
- **Gunakan cakupan "Hanya yang belum diterjemahkan"** - Lebih cepat dan menghindari menerjemahkan ulang konten yang sudah bagus
- **Pantau pekerjaan pertama dengan cermat** - Periksa kesalahan atau masalah kualitas sebelum meluncurkan pekerjaan yang lebih besar
- **Jadwalkan pekerjaan selama periode lalu lintas rendah** - Terjemahan intensif CPU/API
- **Kunci terjemahan yang telah ditinjau** - Mencegah pekerjaan dalam batch dari menimpa perubahan manual Anda
- **Jaga pekerjaan fokus** - Pekerjaan yang lebih kecil dan terarah lebih mudah ditelusuri daripada pekerjaan besar "terjemahkan semuanya"
- **Periksa sampel setelah selesai** - Periksa terjemahan acak untuk kualitas sebelum mempertimbangkan pekerjaan berhasil
- **Ekspor/backup sebelum pekerjaan besar** - Jika Anda perlu mengembalikan perubahan dalam batch

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis tepat seperti yang ditunjukkan dalam aturan preservasi.
---
title: Layanan Terjemahan
---

Layanan terjemahan menyediakan terjemahan berbasis AI untuk deskripsi produk, konten halaman, posting blog, bidang SEO, dan konten merchant lainnya di toko Anda. Terjemahan berjalan secara lokal di server Anda atau melalui penyedia eksternal, sehingga konten Anda tetap pribadi dan terjemahan terjadi dalam beberapa detik.

![Manajemen bahasa](/static/core/admin/img/help/translation-service/language-management.webp)

## Cara Kerjanya

1. Anda **mengaktifkan bahasa** untuk toko Anda (misalnya, Inggris, Jerman, Jepang)
2. Ketika Anda membuat atau mengedit konten (produk, halaman, posting blog), Anda menulis dalam bahasa default Anda
3. Klik **Terjemahkan** pada bidang yang dapat diterjemahkan untuk menghasilkan terjemahan AI ke bahasa aktif Anda
4. Terjemahan disimpan bersama konten asli dan disajikan secara otomatis berdasarkan bahasa pengunjung

## Mengelola Bahasa

Navigasikan ke **Pengaturan > Bahasa** untuk mengelola bahasa toko Anda.

### Dasbor Bahasa

Dasbor menampilkan:
- **Total Bahasa** — Semua bahasa yang tersedia dalam sistem (lebih dari 100)
- **Bahasa Aktif** — Bahasa yang saat ini diaktifkan untuk toko Anda
- **Cakupan Model** — Berapa banyak bahasa yang didukung oleh model terjemahan yang terinstal

### Mengaktifkan Bahasa

1. Cari bahasa di kolom **Bahasa Tersedia**
2. Klik bahasa untuk memindahkannya ke kolom **Bahasa Aktif**
3. Bahasa tersebut segera tersedia untuk terjemahan dan muncul di pengganti bahasa toko Anda

### Bahasa Default

Satu bahasa ditandai sebagai **default**. Ini adalah:
- Bahasa yang Anda gunakan untuk menulis konten
- Cadangan ketika terjemahan tidak ada
- Bahasa yang ditampilkan ketika pengunjung belum memilih preferensi

## Model Terjemahan

Spwig menyertakan mesin terjemahan AI lokal yang berjalan sepenuhnya di server Anda — tidak ada data yang dikirim ke layanan eksternal.

### Model yang Tersedia

| Model | Bahasa | Kecepatan | Kualitas |
|-------|-----------|-------|---------|
| **M2M100-418M** | 100 | Cepat | Baik untuk pasangan bahasa umum |
| **M2M100-1.2B** | 100 | Sedang | Kualitas lebih baik, penggunaan sumber daya lebih tinggi |
| **NLLB-200** | 200+ | Sedang | Cakupan terbaik, termasuk bahasa langka |

### Pemilihan Model

Halaman manajemen bahasa menunjukkan model mana yang terinstal dan cakupan bahasa yang didukung. Model berjalan sebagai layanan lokal menggunakan CTranslate2 untuk inferensi yang efisien.

## Penyedia Eksternal

Untuk toko yang lebih memilih terjemahan berbasis awan atau membutuhkan kualitas bahasa tertentu, Spwig mendukung penyedia terjemahan eksternal.

| Penyedia | Deskripsi |
|----------|-------------|
| **DeepL** | Kualitas terjemahan premium untuk bahasa Eropa dan Asia |
| **Google Translate** | Cakupan bahasa luas dengan terjemahan mesin saraf |
| **Azure Translator** | Layanan terjemahan saraf Microsoft |
| **AWS Translate** | Terjemahan mesin Amazon dengan dukungan terminologi khusus |

### Menghubungkan Penyedia

1. Navigasikan ke **Pengaturan > Penyedia Terjemahan**
2. Pilih penyedia dan masukkan kunci API Anda
3. Tetapkan penyedia sebagai mesin terjemahan yang dipilih
4. Terjemahan akan menggunakan penyedia eksternal alih-alih model lokal

Anda dapat menggunakan penyedia eksternal bersama dengan model lokal — misalnya, gunakan DeepL untuk bahasa Eropa dan model lokal untuk segala sesuatu yang lain.

## Menerjemahkan Konten

### Terjemahan Berbasis Bidang

Bidang yang dapat diterjemahkan (nama produk, deskripsi, judul SEO, dll.) menampilkan tombol **terjemahkan** di sebelah bidang tersebut. Klik tombol tersebut untuk:

1. **Terjemahkan ke semua bahasa aktif** — Menghasilkan terjemahan untuk setiap bahasa aktif sekaligus
2. **Terjemahkan ke bahasa tertentu** — Pilih bahasa individu untuk diterjemahkan

Terjemahan muncul di tab bahasa editor. Anda dapat meninjau dan mengedit secara manual terjemahan mesin apa pun.

### Pekerjaan Terjemahan Massal

Untuk jumlah besar konten, gunakan **pekerjaan terjemahan massal**:

1. Navigasikan ke **Pengaturan > Pekerjaan Terjemahan**
2. Buat pekerjaan baru dengan memilih:
   - **Jenis konten** — Produk, halaman, posting blog, kategori, dll.
   - **Bahasa sumber** — Bahasa yang akan diterjemahkan
   - **Bahasa target** — Satu atau lebih bahasa yang akan diterjemahkan ke dalamnya
   - **Cakupan** — Semua konten, atau hanya bidang yang belum diterjemahkan
3. Kirimkan pekerjaan — berjalan di latar belakang melalui antrian tugas
4. Pantau kemajuan dalam daftar pekerjaan (diantrikan → diproses → selesai)

Pekerjaan massal berguna ketika Anda mengaktifkan bahasa baru dan ingin menerjemahkan seluruh katalog Anda sekaligus.

## Manajemen Terjemahan

### Meninjau Terjemahan

Setiap bidang terjemahan melacak:
- **Status terjemahan** — Apakah bidang tersebut telah diterjemahkan secara otomatis, diedit secara manual, atau masih kosong
- **Status kunci** — Terjemahan yang dikunci tidak akan ditimpa oleh terjemahan otomatis di masa depan
- **Terjemahan terakhir** — Kapan terjemahan tersebut dihasilkan atau diedit terakhir kali

### Mengunci Terjemahan

Jika Anda secara manual mengedit terjemahan mesin untuk meningkatkannya, **kunci** bidang tersebut untuk mencegahnya ditimpa saat pekerjaan terjemahan massal berikutnya berjalan. Bidang yang dikunci dilewati selama terjemahan otomatis.

### Cakupan Terjemahan

Pemantau cakupan menunjukkan persentase konten yang telah diterjemahkan untuk setiap bahasa. Navigasikan ke **Pengaturan > Bahasa** untuk melihat:
- Persentase penyelesaian per bahasa
- Jenis konten yang memiliki celah
- Bidang yang masih memerlukan terjemahan

## Pembaruan Terjemahan UI

Selain konten produk dan halaman, Anda dapat menyesuaikan terjemahan dari **string antarmuka depan** — tombol, label, pesan, dan teks UI lainnya yang ditampilkan kepada pengunjung.

Navigasikan ke **Pengaturan > Pembaruan UI** untuk:
1. Mencari string tertentu (misalnya, "Tambah ke Keranjang")
2. Masukkan terjemahan yang Anda prefer untuk setiap bahasa
3. Simpan — pembaruan akan berlaku segera

Terdapat sekitar 300 string antarmuka depan yang tersedia untuk penyesuaian. Pembaruan memiliki prioritas lebih tinggi dibandingkan terjemahan default.

## Tips

- Mulailah dengan hanya mengaktifkan bahasa yang benar-benar digunakan oleh pelanggan Anda — Anda selalu dapat menambahkan lebih banyak nanti.
- Gunakan **model AI lokal** untuk terjemahan sehari-hari — cepat, pribadi, dan tidak ada biaya per terjemahan.
- Pertimbangkan **DeepL** jika Anda membutuhkan kualitas terbaik untuk bahasa Eropa utama — secara konsisten menghasilkan terjemahan yang lebih alami dibandingkan model umum.
- Selalu **periksa ulang terjemahan mesin** untuk nama produk, istilah merek, dan teks pemasaran — AI menangani konten teknis dengan baik tetapi mungkin melewatkan nuansa dalam teks kreatif.
- **Kunci** terjemahan apa pun yang telah Anda perbaiki secara manual untuk melindunginya dari ditimpa selama jalannya pekerjaan terjemahan massal.
- Gunakan **pekerjaan terjemahan massal** saat mengaktifkan bahasa baru untuk menerjemahkan seluruh katalog Anda dalam satu kali proses daripada menerjemahkan produk satu per satu.
- Sesuaikan **pembaruan UI** untuk cocok dengan suara merek Anda — misalnya, ubah "Tambah ke Keranjang" menjadi "Beli Sekarang" jika itu lebih cocok untuk toko Anda.
---
title: Perpustakaan Media
---

Perpustakaan Media adalah pusat untuk mengelola semua gambar, video, model 3D, dan file yang digunakan di seluruh toko Anda. Unggah file dengan menyeretnya, kelola dengan folder dan tag, dan biarkan sistem secara otomatis mengoptimalkan gambar untuk beban cepat.

![Galeri Media](/static/core/admin/img/help/media-library/media-gallery.webp)

## Antarmuka Galeri

Navigasi ke **Perpustakaan Media** di sidebar untuk membuka galeri. Antarmuka memiliki tiga area:

| Area | Lokasi | Tujuan |
|------|----------|---------|
| **Zona Unggah** | Sidebar kiri, bagian atas | Seret dan lepas file untuk mengunggah (gambar, video, model 3D hingga 100MB) |
| **Folder & Tag** | Sidebar kiri, di bawah | Jelajahi folder, saring berdasarkan tag, akses Tempat Sampah |
| **Kotak Media** | Area utama | Cari, saring, jelajahi, dan kelola semua aset Anda |

### Kontrol Toolbar

Toolbar di atas kotak media menyediakan:

- **Cari** — cari aset berdasarkan judul, teks alternatif, deskripsi, atau nama tag
- **Penyaring Jenis** — tampilkan hanya Gambar, Video, atau Model 3D
- **Penyaring Ukuran** — saring berdasarkan ukuran file (Kecil, Sedang, Besar)
- **Aksi Massal** — Pilih Item, Edit Detail, Hapus Terpilih
- **Mode Tampilan** — Kotak (besar), Kotak Kecil, atau Tampilan Daftar (dipertahankan selama sesi)

## Mengunggah File

Seret satu atau lebih file ke zona **Unggah** di sidebar kiri, atau klik zona tersebut untuk membuka pemilih file.

### Format yang Didukung

| Jenis | Format |
|------|---------|
| **Gambar** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Video** | MP4, WebM, MOV, MKV, AVI |
| **Model 3D** | GLB, glTF |

### Antrean Unggah

Ketika mengunggah beberapa file, manajer antrean muncul menampilkan:

- Nama file dan bar pengunggah progres untuk setiap file
- Unggah bersamaan (hingga 2 sekaligus untuk kinerja)
- Status pemrosesan saat file dioptimalkan setelah diunggah
- Opsi untuk membatalkan pengunggahan individual atau membersihkan item yang selesai

Antrean dapat diseret dan diminimalkan sehingga Anda dapat terus bekerja sementara pengunggahan selesai.

## Optimisasi Gambar Otomatis

Setiap gambar yang Anda unggah secara otomatis dioptimalkan:

- **Konversi ke WebP** — versi WebP dibuat bersama dengan aslinya (kualitas 85%) untuk beban yang lebih cepat
- **Pembuatan Miniatur** — beberapa ukuran versi dibuat berdasarkan preset gambar Anda
- **Orientasi EXIF** — gambar secara otomatis diputar ke orientasi yang benar

### Preset Gambar Sistem

Platform ini memiliki 21 preset bawaan yang mencakup kasus penggunaan umum:

| Preset | Dimensi | Potong | Digunakan Untuk |
|--------|-----------|------|---------|
| **Miniatur** | 150 x 150 | Cover | Daftar admin, pratinjau cepat |
| **Kecil** | 300 x 300 | Cover | Kartu produk kecil |
| **Sedang** | 600 x 600 | Contain | Kartu produk, miniatur blog |
| **Besar** | 1200 x 1200 | Contain | Halaman detail produk |
| **Galeri** | 800 x 800 | Contain | Galeri gambar |
| **Hero** | 1920 x 1080 | Cover | Bagian hero, banner halaman |
| **Banner** | 1200 x 400 | Cover | Banner promosi |
| **Kartu** | 400 x 300 | Cover | Kartu fitur, kartu konten |
| **Avatar** | 200 x 200 | Potong | Avatar pelanggan dan staf |
| **Daftar Produk** | 400 x 400 | Cover | Kartu grid produk |
| **Detail Produk** | 1200 x 1200 | Cover | Gambar produk penuh |
| **Miniatur Produk** | 100 x 100 | Cover | Pemilih variasi, keranjang mini |
| **Banner Kategori** | 1920 x 480 | Cover | Header halaman kategori |
| **Miniatur Kategori** | 300 x 200 | Cover | Kartu kategori |
| **Logo Header** | 300 x 80 | Pad | Logo header situs |
| **Logo Footer** | 200 x 60 | Pad | Logo footer situs |
| **Logo Email** | 400 x 100 | Pad | Logo template email |
| **Logo Persegi** | 160 x 160 | Pad | Penempatan logo persegi |
| **Logo Merek** | 200 x 100 | Pad | Logo merek/mitra |
| **Banner Pengumuman** | 800 x 300 | Cover | Gambar pengumuman |
| **Latar Belakang Pengumuman** | 1200 x 800 | Cover | Latar belakang pengumuman |

Preset sistem tidak dapat diberi nama ulang atau dihapus. Anda dapat membuat preset kustom tambahan di bawah **Perpustakaan Media > Preset Ukuran Gambar** jika Anda memerlukan ukuran yang tidak tertutup oleh default.

### Mode Potong

| Mode | Perilaku |
|------|----------|
| **Cover** | Mengisi seluruh area, memotong tepi jika diperlukan — cocok untuk kartu dan banner |
| **Contain** | Menyisipkan gambar penuh dalam area, menambahkan ruang transparan jika diperlukan — cocok untuk gambar produk |
| **Potong** | Memotong pusat ke ukuran yang tepat |
| **Pad** | Menyisipkan gambar dan menambahkan padding (transparan, putih, atau hitam) — cocok untuk logo |

## Mengelola File

### Folder

Buat folder untuk mengelompokkan media Anda secara logis. Folder dapat disarangkan ke dalam folder lain hingga kedalaman tertentu. Klik folder di sidebar kiri untuk menampilkan hanya aset yang berada di dalamnya. Tautan **Semua File** menampilkan semuanya.

### Tag

Tambahkan tag ke aset untuk pengelolaan lintas folder yang fleksibel. Tag muncul sebagai awan di sidebar kiri. Klik tag untuk menyaring aset berdasarkan tag tersebut. Aset dapat memiliki beberapa tag.

### Cari

Bar pencarian mencari aset berdasarkan judul, teks alternatif, deskripsi, atau nama tag. Gabungkan pencarian dengan penyaring jenis dan ukuran untuk hasil yang tepat.

## Detail Aset

Klik aset untuk membuka tampilan detailnya dengan pratinjau besar dan metadata lengkap.

![Detail Aset](/static/core/admin/img/help/media-library/media-detail.webp)

Tampilan detail menampilkan:

- **Pratinjau** — pratinjau gambar besar dengan dimensi asli
- **Info File** — jenis, dimensi, ukuran file, tanggal unggah
- **Tab** untuk pengeditan:

| Tab | Bidang |
|-----|--------|
| **Umum** | Judul, Teks Alternatif, Deskripsi (semuanya dapat diterjemahkan untuk toko multibahasa) |
| **Teknis** | Jenis MIME, hash file, nama file asli, status versi WebP |
| **Pengelolaan** | Penugasan folder, tag, toggle publik/privat |
| **Lanjutan** | Koordinat titik fokus, ID eksternal, JSON metadata |

### Bidang yang Dapat Diterjemahkan

Judul, teks alternatif, dan deskripsi mendukung terjemahan. Klik ikon terjemahan di sebelah setiap bidang untuk menambahkan terjemahan untuk bahasa yang diaktifkan. Ini memastikan gambar memiliki teks alternatif dan deskripsi yang diterjemahkan dengan benar untuk SEO dan aksesibilitas.

### Pelacakan Penggunaan

Sistem melacak di mana setiap aset digunakan di seluruh platform. Bagian **Penggunaan Media** di bagian bawah menampilkan setiap model dan bidang yang merujuk pada aset ini, membantu Anda memahami dampaknya sebelum membuat perubahan atau menghapusnya.

## Dukungan Video

Video yang diunggah ke perpustakaan media secara otomatis dianalisis:

- **Ekstraksi Metadata** — durasi, resolusi, frame rate, bitrate, dan kodek dicatat
- **Gambar Poster** — thumbnail dibuat dari video untuk pratinjau
- **Streaming** — video mendukung permintaan rentang untuk mencari tanpa mengunduh seluruh file
- **Konversi Opsional** — video dapat dikonversi ke format WebM/AV1 yang dioptimalkan untuk pengiriman yang lebih cepat

## Tempat Sampah

Menghapus aset memindahkannya ke **Tempat Sampah** alih-alih menghapusnya secara permanen. Ini melindungi dari penghapusan tidak sengaja.

| Tindakan | Apa yang Dilakukan |
|--------|-------------|
| **Hapus** | Memindahkan aset ke Tempat Sampah (hapus lunak) |
| **Pulihkan** | Mengembalikan aset yang dihapus ke lokasi aslinya |
| **Hapus Permanen** | Menghapus aset dan semua miniatur yang terkait dari penyimpanan secara permanen |
| **Kosongkan Tempat Sampah** | Menghapus permanen semua item dalam Tempat Sampah |

Klik **Tempat Sampah** di sidebar kiri untuk melihat dan mengelola aset yang dihapus.

## Di Mana Perpustakaan Media Digunakan

Perpustakaan media terintegrasi di seluruh platform:

| Fitur | Bagaimana Media Digunakan |
|---------|------------------|
| **Katalog Produk** | Gambar produk, gambar variasi, banner kategori |
| **Blog** | Gambar utama, gambar dalam konten melalui CKEditor |
| **Pembangun Halaman** | Elemen gambar, latar belakang hero, komponen galeri |
| **Pembangun Header/Footer** | Gambar logo, gambar latar belakang |
| **Pengaturan Situs** | Logo situs dan favicon |
| **Pengumuman** | Gambar pengumuman dan latar belakang |
| **CKEditor** | Semua unggah gambar teks kaya melalui perpustakaan media |
| **Program Keanggotaan** | Gambar hadiah dan tingkat |

Ketika Anda memilih gambar dalam fitur-fitur ini, galeri perpustakaan media terbuka sebagai modal untuk pencarian dan pemilihan yang mudah.

## Tips

- **Gunakan judul dan teks alternatif yang deskriptif** — metadata yang baik meningkatkan SEO dan aksesibilitas. Sistem menggunakan teks alternatif dalam tag gambar di seluruh toko online.
- **Buat struktur folder sejak awal** — buat struktur folder (misalnya, Produk, Blog, Banner, Logo) sebelum mengunggah banyak file. Lebih mudah untuk mengelola saat mengunggah daripada mengatur ulang nanti.
- **Gunakan tag untuk kategori lintas** — tag seperti "musiman", "penjualan", atau "gaya hidup" membantu Anda menemukan aset yang mencakup beberapa folder.
- **Periksa penggunaan sebelum menghapus** — bagian pelacakan penggunaan menunjukkan di mana aset digunakan. Menghapus aset yang digunakan dapat menyebabkan gambar rusak di toko online Anda.
- **Biarkan WebP melakukan pekerjaan** — konversi WebP otomatis biasanya mengurangi ukuran file sebesar 25-35% dibandingkan JPEG tanpa kehilangan kualitas yang terlihat. Anda tidak perlu mengonversi gambar secara manual sebelum mengunggah.
- **Buat preset kustom** — jika Anda memiliki tata letak unik yang memerlukan ukuran gambar tertentu, buat preset kustom daripada mengubah ukuran gambar secara manual.
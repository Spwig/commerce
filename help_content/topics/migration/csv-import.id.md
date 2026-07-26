---
title: Mengimpor dari File CSV
---

Pengimporan CSV adalah rute migrasi cadangan untuk toko Spwig mana pun yang tidak terhubung secara langsung. Jika Anda berasal dari BigCommerce, PrestaShop, Squarespace, Wix, spreadsheet yang Anda kelola secara manual, atau sistem khusus tanpa API yang dipahami Spwig, ini adalah tempat Anda berada — ekspor datanya ke file CSV dan unggah di sini alih-alih terhubung langsung.

Panduan ini mencakup kapan menggunakan CSV, apa yang tidak dapat dibawa oleh CSV, lima file yang terlibat, cara mempersiapkannya, dan cara pemetaan kolom bekerja.

## Kapan Menggunakan CSV Sebagai Alternatif Koneksi API

Spwig terhubung langsung ke WooCommerce, Shopify, dan Magento 2/Adobe Commerce — lihat [Pengantar Migrasi Data](migration-overview) untuk ini. Untuk platform lain, CSV adalah satu-satunya pilihan; tidak ada integrasi langsung untuk BigCommerce, PrestaShop, Squarespace, atau Wix. Ini juga pilihan yang tepat jika Anda sedang mengonsolidasikan data dari spreadsheet, menutup toko yang dibuat secara khusus, atau ingin mengontrol secara tepat apa yang diimpor dengan mengatur file sendiri.

## Apa yang Tidak Bisa Dilakukan CSV

Sebelum Anda mempersiapkan apa pun, ketahui apa yang tertinggal dari rute ini — ini adalah sumber kejutan terbesar bagi pedagang yang menggunakan pengimporan CSV:

- **Tidak ada gambar produk.** Produk diimpor tanpa gambar yang terlampir; unggah gambar tersebut setelahnya.
- **Tidak ada variasi.** Setiap produk dibuat sebagai produk sederhana. Bangun struktur ukuran/warna/gaya kembali di Spwig setelah pengimporan.
- **Tidak ada kupon.** Kode diskon dan promosi bukan bagian dari format CSV.
- **Tidak ada konten blog.** Tidak ada file CSV untuk posting atau artikel.

Tidak ada hal ini yang menghambat pengimporan — hanya berarti produk memerlukan pekerjaan lanjutan setelah berada di Spwig. Lihat [Setelah Migrasi Anda](after-migration-review) untuk daftar pemeriksaan lengkap setelah pengimporan.

## Lima File

Langkah CSV wizard menawarkan lima input file, masing-masing dengan tombol **Unduh Template**. Mulailah dari template ini daripada membangun file dari awal — mereka menjamin nama kolom yang benar dan memungkinkan deteksi otomatis melakukan lebih banyak pekerjaan di langkah 4.

| File | Diperlukan? |
|---|---|
| Produk | **Diperlukan** |
| Kategori | Opsional |
| Pelanggan | Opsional |
| Pesanan | Opsional |
| Ulasan | Opsional |

Produk adalah satu-satunya file yang dipaksakan oleh Spwig — yang lain dapat dibiarkan kosong jika Anda belum memiliki data tersebut.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: Langkah 2 dengan CSV yang dipilih, menampilkan lima input file dan tombol Unduh Template mereka
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Produk (Diperlukan)

| Kolom | Deskripsi |
|---|---|
| `id` | Identifikasi unik dalam data sumber Anda; tidak ditampilkan kepada pelanggan. |
| `name` | Judul produk. **Wajib.** |
| `slug` | Versi yang ramah URL dari nama; dihasilkan secara otomatis dari `name` jika kosong. |
| `description` | Deskripsi yang ditampilkan di toko online. |
| `price` | Harga reguler produk. **Wajib.** |
| `sku` | Unit persediaan — digunakan untuk cocokkan saat **Lewati item yang sudah ada** diaktifkan. |
| `stock_quantity` | Unit yang saat ini tersedia. |
| `category` | Nama kategori yang produk ini termasuk di dalamnya. Harus cocok dengan `name` dalam file kategori Anda. |

### Kategori

| Kolom | Deskripsi |
|---|---|
| `id` | Identifikasi unik dalam data sumber Anda. |
| `name` | Nama kategori. **Wajib.** |
| `slug` | Versi yang ramah URL dari nama; dihasilkan secara otomatis jika kosong. |
| `description` | Teks deskripsi kategori. |
| `parent_id` | `id` dari kategori induk. Kosong berarti tingkat teratas. |

### Pelanggan

| Kolom | Deskripsi |
|---|---|
| `id` | Identifikasi unik dalam data sumber Anda. |
| `email` | Alamat email pelanggan. **Wajib** — menghubungkan pesanan dan ulasan ke pelanggan yang benar. |
| `first_name` | Nama depan pelanggan. |
| `last_name` | Nama belakang pelanggan. |
| `phone` | Nomor telepon pelanggan. |

### Pesanan

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Kolom | Deskripsi |
|---|---|
| `id` | Identifier unik dalam data sumber Anda. |
| `customer_email` | Email pelanggan yang memesan. **Wajib** — menghubungkan pesanan dengan catatan pelanggan. |
| `order_date` | Tanggal pesanan ditempatkan. |
| `status` | Status pesanan (misalnya, selesai, diproses). |
| `total` | Total pesanan. **Wajib.** |
| `currency` | Kode mata uang untuk total pesanan. |

### Ulasan (Opsional)

| Kolom | Deskripsi |
|---|---|
| `id` | Identifier unik dalam data sumber Anda. |
| `product_id` | `id` produk yang diulas, sesuai dengan file produk Anda. **Wajib** — menghubungkan ulasan dengan produk yang benar. |
| `customer_email` | Alamat email peninjau. |
| `rating` | Rating bintang yang diberikan. |
| `comment` | Teks ulasan. |
| `date` | Tanggal ulasan diposting. |

## Menyiapkan File Anda

- **Simpan sebagai UTF-8** untuk menghindari karakter aksen yang rusak, terutama dari encoding sumber yang berbeda.
- **Kutip kolom yang mengandung koma** — bungkus deskripsi atau nama yang mengandung koma dalam tanda kutip ganda agar tidak salah dibaca sebagai pemisah kolom.
- **Sertakan baris header.** Baris pertama harus berisi nama kolom Anda — file tanpa baris header akan ditolak.
- **Bangun hierarki kategori dengan `parent_id`.** Berikan setiap kategori `id` unik, lalu atur `parent_id` subkategori ke `id` induknya. Kosong berarti tingkat teratas.
- **Hubungkan pesanan dengan pelanggan menggunakan `customer_email`**, cocokkan dengan kolom `email` dalam file pelanggan Anda (atau catatan tamu akan dibuat), daripada mengandalkan nomor ID internal, yang jarang sejalan di antara platform.
- **Hubungkan ulasan dengan produk menggunakan `product_id`**, cocokkan dengan nilai dalam kolom `id` file produk Anda, atau ulasan tersebut akan dilewati.

## Memetakan Kolom di Langkah 4

Langkah 4 menampilkan panel Pemetaan Kolom CSV. Spwig memindai header Anda dan secara otomatis mendeteksi kemungkinan cocok terhadap daftar alias umum — misalnya, kolom `sku` juga cocok dengan `barcode`, `part_number`, atau `item_number`. Header yang diekspor langsung dari platform lain sering kali dipetakan dengan benar tanpa pekerjaan manual sama sekali.

Untuk setiap kolom, Anda dapat menerima tebakan yang terdeteksi secara otomatis, menggantinya dengan memilih bidang tujuan yang berbeda, atau memilih "— Lewati kolom ini —" untuk mengecualikannya. Pemetaan disimpan dan digunakan kembali pada migrasi CSV masa depan. Lihat [Pemetaan Bidang Migrasi](migration-field-mapping) untuk gambaran lengkap langkah 4, termasuk pemetaan bidang otomatis, pemetaan kategori, dan opsi pajak/pengiriman.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Panel Pemetaan Kolom CSV Langkah 4 menampilkan pemetaan terdeteksi secara otomatis dengan dropdown pengganti
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Kesalahan Umum dan Artinya

| Kesalahan | Artinya |
|---|---|
| `Products CSV is required.` | Anda mencoba melanjutkan tanpa mengunggah file produk. Ini adalah satu-satunya file yang diperlukan oleh Spwig — unggah satu untuk melanjutkan. |
| `{Type} CSV has no headers.` | Baris pertama file yang dinamai kosong atau hilang. Tambahkan baris header dengan nama kolom dan unggah ulang. |
| `{Type} CSV could not be read: ...` | Spwig tidak dapat memparse file yang dinamai — biasanya file yang rusak, encoding yang salah, atau file yang sebenarnya bukan CSV meskipun ekstensinya. Ekspor ulang dan konfirmasi bahwa file tersebut terbuka dengan bersih sebelum mengunggah ulang. |

## Menjalankan Impor

Setelah pemetaan dikonfirmasi, mulai migrasi dari langkah 5. Ini berjalan di latar belakang, jadi Anda dapat menutup jendela — kemajuan dan log langsung tersedia jika Anda memeriksa kembali sebelum selesai. Lihat [Setelah Migrasi Anda](after-migration-review) untuk memverifikasi hasilnya.

Ingat bahwa impor CSV secara khusus meninggalkan **gambar produk** dan **varian** untuk Anda selesaikan secara manual — tidak ada yang datang secara otomatis, terlepas seberapa lengkap file Anda.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- **Mulai dari tombol Download Template untuk setiap file** — ini menghemat waktu Anda dari mengejar typo nama kolom yang sebaliknya akan terlewat hingga pemetaan manual.
- **Perbaiki ketidakcocokan `product_id` sebelum mengunggah ulasan** — ulasan yang `product_id`-nya tidak cocok dengan `id` produk apa pun tidak memiliki tempat untuk menempelkan dan akan diabaikan.
- **Jangan mengganti nama header dari ekspor platform lain** — deteksi otomatis sering mengenali mereka seperti itu melalui alias, sehingga pemetaan mungkin tidak memerlukan pekerjaan manual sama sekali.
- **Alokasikan waktu untuk gambar dan variasi segera setelah impor** — dua hal ini tidak pernah dibawa oleh CSV, dan mudah untuk terlupakan hingga pelanggan menyadari halaman produk yang kosong.
- **Gunakan `parent_id` untuk memodelkan kategori multi-level** — arahkan `parent_id` kategori turunan ke `id` kategorinya untuk menyematkannya; biarkan kosong untuk kategori tingkat atas.
- **Ekspor ulang dan periksa ulang pada kesalahan "could not be read"** — hampir selalu encoding atau kerusakan dalam file sumber, bukan sesuatu yang perlu diperbaiki di Spwig.
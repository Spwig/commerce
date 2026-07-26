---
title: Pemetaan Bidang Migrasi
---

Setiap platform menamai hal-hal sedikit berbeda — `regular_price` di WooCommerce bukan `price` di Shopify, dan kolom CSV yang disebut `barcode` mungkin persis sama dengan hal yang Spwig harapkan diberi label `sku`. Langkah 4 dari wizard migrasi, **Konfigurasi Pemetaan Bidang**, adalah tempat Anda memeriksa bagaimana data sumber Anda akan mendarat di Spwig sebelum impor benar-benar berjalan. Topik ini mencakup setiap blok di halaman tersebut dan berlaku untuk migrasi WooCommerce, Shopify, Magento, dan CSV, dengan perbedaan platform disebutkan di tempat yang relevan. Untuk kredensial dan langkah wizard sebelumnya, lihat [Migrasi dari WooCommerce](migrate-from-woocommerce) atau panduan setara untuk platform Anda.

Ketika beberapa kategori sumber Anda tidak memiliki kesesuaian yang jelas di Spwig, blok ini menawarkan tiga pilihan: **Buat kategori baru**, **Tetapkan ke kategori default** (sebuah kategori semacam 'Tidak Terkategorisasi'), atau **Lewati item dengan kategori yang tidak terpeta**.

> **Catatan:** Mana pun opsi yang Anda pilih di sini, Spwig saat ini secara otomatis membuat kategori yang cocok untuk setiap produk yang memiliki data kategori sumber, dan hanya beralih ke 'Tidak Terkategorisasi' untuk produk yang sama sekali tidak memiliki informasi kategori. Anda tidak perlu terlalu khawatir tentang pilihan ini — jika akhirnya Anda mendapatkan kategori yang tidak diinginkan, lebih cepat untuk menggabungkan atau menghapusnya di **Katalog > Kategori** setelah impor daripada mengandalkan pengaturan ini.

## Pengaturan pajak, pengiriman, dan harga

Blok terakhir, **Pengaturan Pajak & Pengiriman**, memiliki tiga kontrol: **Impor pengaturan pajak**, **Impor zona pengiriman dan metode**, dan jenis serta nilai **Penyesuaian Harga**.

Dua kotak centang saat ini tidak memengaruhi impor — tidak ada tarif pajak atau zona pengiriman yang datang dari platform lama Anda, terlepas dari bagaimana mereka diatur. Konfigurasikan keduanya secara langsung di Spwig setelah impor selesai: tarif pajak di bawah **Pengaturan > Pajak & Mata Uang**, zona pengiriman dan metode di bawah **Pengaturan > Pengiriman**.

**Penyesuaian Harga** berperilaku berbeda tergantung pada platform sumber Anda:

- **Migrasi WooCommerce, CSV, dan Shopify** — kontrol ini berfungsi seperti yang dijelaskan. Pilih **Persentase** atau **Jumlah Tetap**, masukkan nilai (misalnya `10` untuk peningkatan 10%, atau `-5` untuk penurunan $5), dan harga dasar setiap produk disesuaikan dengan jumlah tersebut saat diimpor. Ini hanya berlaku untuk harga dasar — harga diskon/compare-at datang tanpa penyesuaian.
- **Migrasi Magento** — kontrol yang sama muncul di halaman ini, tetapi tidak memiliki efek; harga Magento diimpor tanpa perubahan, terlepas dari apa yang Anda masukkan. Jika Anda memerlukan perubahan harga secara keseluruhan pada migrasi Magento, terapkan setelahnya menggunakan alat harga katalog dalam jumlah besar Spwig, bukan bidang ini.

> **Peringatan:** Jika Anda bermigrasi dari WooCommerce, CSV, atau Shopify dan tidak ingin harga berubah, biarkan **Penyesuaian Harga** tetap di **Tidak Ada**. Ini adalah satu-satunya kontrol di halaman ini yang benar-benar mengubah data Anda, dan mudah untuk salah mengasumsikan — secara tidak benar — bahwa perilakunya sama dengan kotak centang pajak dan pengiriman di atasnya.

## Pemetaan disimpan untuk penggunaan berikutnya

Apa pun yang Anda konfigurasikan di halaman ini disimpan bersama pekerjaan migrasi, dan Spwig menggunakannya kembali sebagai titik awal untuk migrasi masa depan dari platform yang sama — berguna jika Anda menjalankan migrasi bertahap (kategori dan produk terlebih dahulu, pesanan kemudian) atau perlu mengimpor ulang setelah memperbaiki masalah data. Anda juga dapat kembali dan menyesuaikan pemetaan yang disimpan setelah migrasi selesai dari tombol **Pemetaan Bidang** di dashboard migrasi, tanpa harus menjalankan ulang seluruh wizard.

## Tips

- **Periksa blok Pemetaan Otomatis meskipun Anda tidak dapat mengeditnya** — menangkap pemetaan yang salah sebelum Anda mengklik Mulai Impor jauh lebih murah daripada memperbaiki ratusan catatan yang diimpor setelahnya.
- **Ubah nama header CSV yang ambigu sebelum mengunggah** jika deteksi otomatis tidak mengenali mereka, daripada mencoba memaksa bidang yang tidak cocok melalui dropdown.
- **Gunakan Meta Data (JSON) sebagai tempat overflow bidang kustom Anda** — ini adalah satu-satunya target pemetaan yang tidak memiliki batas setelah dua atau tiga bidang.
- **Jangan mengandalkan halaman ini untuk pajak, pengiriman, atau (pada Magento) harga** — anggap hal tersebut sebagai tugas konfigurasi manual yang harus dilakukan segera setelah impor, bukan sesuatu yang ditangani oleh wizard.
- **Biarkan Penyesuaian Harga tetap di Tidak Ada pada migrasi baru Anda** di putaran pertama, lalu gunakan batch uji kecil untuk memverifikasi perhitungan sebelum menerapkannya ke katalog penuh Anda.
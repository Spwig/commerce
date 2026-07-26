---
title: Migrasi dari Magento
---

Spwig dapat mengimpor katalog, pelanggan, pesanan, kupon, dan halaman CMS langsung dari toko Magento 2 atau Adobe Commerce yang sedang berjalan menggunakan REST API Magento. Panduan ini akan membimbing Anda melalui proses pembuatan kredensial integrasi yang diperlukan oleh Magento, menjalankan wizard migrasi, dan satu kekurangan signifikan yang perlu direncanakan oleh pedagang yang berasal dari Magento: ulasan produk.

Hanya **Magento 2 dan Adobe Commerce** yang didukung. Magento 1 sudah mencapai akhir masa hidupnya beberapa tahun lalu dan tidak menyediakan REST API yang bergantung pada migrasi ini — jika Anda masih menggunakan Magento 1, gunakan [Mengimpor dari File CSV](csv-import) sebagai gantinya.

## Sebelum Anda Mulai

Lihat [Pengantar Migrasi Data](migration-overview) untuk panduan perencanaan umum. Untuk Magento secara khusus:

- **Kategori** — diimpor dengan hierarkinya tetap utuh.
- **Produk** — diimpor, termasuk gambar.
- **Pelanggan dan alamat** — diimpor.
- **Pesanan** — diimpor.
- **Kupon** — diimpor sebagai voucher Spwig, berasal dari aturan penjualan Magento.
- **Halaman CMS** — diimpor sebagai halaman Spwig.
- **Ulasan** — biasanya **tidak** diimpor. Lihat bagian berikut sebelum mengandalkan ini.
- Variasi didukung untuk produk konfigurabel.

> **Catatan:** Migrasi Magento tidak membawa program afiliasi, komisi, atau pembayaran — integrasi jembatan afiliasi Spwig hanya tersedia untuk toko WooCommerce.

### Batasan Ulasan

Edisi Community Magento tidak menyediakan endpoint REST untuk ulasan produk — rute `/reviews` sederhana tidak ada pada instalasi Community standar. Spwig memeriksa rute ini sebelum mengimpor, dan jika tidak ada, akan mencatat pesan dan melanjutkan dengan migrasi Anda, daripada gagal seluruh pekerjaan. Kategori, produk, pelanggan, pesanan, kupon, dan halaman Anda tetap akan diimpor; hanya ulasan yang dilewati.

Ulasan **akan** diimpor jika toko Anda berjalan di **Adobe Commerce** (yang menyediakan endpoint ini) atau jika instalasi Magento Anda memiliki modul kustom yang menambahkan rute ulasan yang kompatibel.

Jika Anda menggunakan Magento Community dan memerlukan ulasan di Spwig, ekspor ulasan secara terpisah (sebagian besar ekstensi ulasan menawarkan ekspor CSV) dan bawa masuk setelahnya menggunakan file ulasan di [Mengimpor dari File CSV](csv-import), yang dikaitkan dengan produk Anda melalui `product_id`.

## Langkah 1: Pilih Magento

Dari dashboard migrasi di **Data Import & Export**, klik **Start New Migration** dan pilih **Magento** sebagai platform Anda.

## Langkah 2: Koneksi ke Toko Anda

Anda memerlukan URL toko Magento Anda dan token akses integrasi. Admin Magento tidak memberikan kunci API sederhana seperti beberapa platform lain — Anda menciptakan **Integration**, yang merupakan kredensial berbasis ruang lingkup yang dianggap oleh Magento seperti aplikasi terhubung.

### Membuat Token Akses Integrasi

1. Di admin Magento Anda, pergi ke **System > Integrations**.
2. Klik **Add New Integration**.
3. Tetapkan nama menjadi `Spwig Migration` agar mudah diidentifikasi nanti.
4. Buka tab **API** dan atur **Resource Access** menjadi **All**.
5. Klik **Save**, lalu klik **Activate**.
6. Konfirmasi dengan mengklik **Allow** pada pop-up yang menampilkan izin yang diberikan.
7. Salin token akses yang ditampilkan setelah aktivasi — Magento hanya menampilkan token tersebut sekali.

> **Catatan:** Resource Access diatur ke **All** karena pohon sumber daya Magento sangat granular — ratusan izin individu mencakup katalog, penjualan, pelanggan, dan CMS — tanpa tombol tunggal "baca semuanya" selain memilih semua. Migrasi hanya pernah membaca dari toko Anda; ia tidak pernah menulis kembali, dan Anda dapat membatalkan integrasi setelah migrasi Anda diverifikasi (dijelaskan di akhir panduan ini).

Kembali ke wizard Spwig, masukkan **Store URL** dan **Access Token** yang Anda salin. Biarkan **Test connection before proceeding** dicentang (secara default aktif) sehingga Spwig memverifikasi bahwa ia dapat mencapai dan mengautentikasi toko Anda sebelum Anda melanjutkan. Jika pengujian gagal, periksa kembali URL dan pastikan integrasi masih aktif di Magento. Klik **Next**.

screenshots-needed

heading

## Langkah 3: Tinjau Apa yang Akan Diimpor

paragraph

Spwig menanyai toko Magento Anda dan menampilkan jumlah langsung untuk setiap jenis data yang ditemukan: kategori, produk, pelanggan, pesanan, kupon (diperoleh dari aturan penjualan), dan halaman CMS. Setiap jenis memiliki kotak centang, secara otomatis dicentang ketika Spwig menemukan item untuk diimpor dan dinonaktifkan ketika jumlahnya nol.

paragraph

Anda juga akan melihat contoh dari lima produk pertama sehingga Anda dapat memverifikasi bahwa judul, harga, dan gambar terlihat benar sebelum menyetujui impor penuh.

paragraph

Di bawah jumlah, **Opsi Impor** memungkinkan Anda mengontrol bagaimana impor berperilaku:

list

paragraph

Jika Anda perlu mengubah cara bidang tertentu dipetakan — atribut kustom, cocok kategori, penanganan pajak atau pengiriman — hal itu terjadi di langkah 4, yang dibahas dalam [Pemetaan Bidang Migrasi](migration-field-mapping). Klik **Berikutnya** untuk melanjutkan ke pemetaan, lalu klik **Mulai Migrasi** setelah Anda meninjau.

heading

## Menjalankan Impor

paragraph

Impor berjalan di latar belakang — Anda dapat menutup jendela dan impor akan tetap berjalan. Halaman kemajuan menampilkan status langsung untuk setiap jenis data (kategori, produk, pelanggan, pesanan, ulasan, kupon) dengan log yang dapat diperluas untuk detail.

paragraph

Setelah selesai, Anda akan tiba di halaman ringkasan hasil. Ikuti [Setelah Migrasi Anda](after-migration-review) untuk memverifikasi apa yang telah dipindahkan, tangani penulisan ulang tautan untuk konten yang merujuk ke URL Magento lama Anda, dan perhatikan konfigurasi pajak dan pengiriman yang dikumpulkan oleh wizard tetapi tidak diterapkan secara otomatis.

screenshots-needed

heading

## Deadline Rollback

paragraph

Magento adalah satu-satunya platform di mana rollback memiliki batas waktu. Setelah migrasi Anda selesai, tombol **Rollback** muncul di halaman ringkasan pekerjaan — tetapi untuk Magento secara khusus, tombol tersebut mungkin berhenti ditawarkan setelah periode tertentu setelah selesai. Jenis migrasi lainnya (WooCommerce, Shopify, CSV) tidak memiliki deadline ini, tetapi Magento memiliki, jadi jangan menunda verifikasi untuk nanti.

blockquote

paragraph

Periksa data yang diimpor Anda secara segera, selagi rollback masih tersedia, dalam kasus Anda membutuhkannya.

heading

## Batalkan Integrasi

paragraph

Setelah Anda memverifikasi data Anda di Spwig — produk, harga, gambar, pelanggan, pesanan, kupon, dan halaman semuanya terlihat benar — kembali ke **Sistem > Integrasi** di Magento, temukan `Spwig Migration`, dan nonaktifkan atau hapus.

Token tidak diperlukan lagi kecuali Anda berencana untuk menjalankan ulang migrasi, dan menghapusnya menutup kredensial akses baca yang tidak lagi Anda butuhkan.

## Tips

- **Ulasan adalah kejutan terbesar bagi pedagang Magento** — rencanakan ekspor/impor terpisah jika Anda menggunakan versi Community dan ulasan penting bagi toko Anda.
- **Salin token akses segera** — Magento hanya menunjukkan token tersebut sekali saat Anda mengaktifkan integrasi; jika Anda kehilangannya, Anda harus menonaktifkan dan membuat ulang integrasi tersebut.
- **Jangan menunda verifikasi** — tombol Rollback hanya tersedia dalam waktu terbatas untuk Magento secara khusus, berbeda dengan platform lain.
- **Gunakan pratinjau contoh di langkah 3** untuk menangkap masalah pemetaan yang jelas (harga yang salah, gambar yang hilang) sebelum menjalankan impor penuh.
- **Kupon berasal dari aturan penjualan** — jika kupon Magento bergantung pada kondisi yang kompleks, periksa kupon tersebut di Spwig setelahnya karena tidak setiap jenis aturan memiliki ekuivalen langsung.
- **Konfigurasikan tarif pajak dan zona pengiriman di Spwig setelah impor** — opsi pajak dan pengiriman dari wizard disimpan tetapi tidak diterapkan secara otomatis ke toko Anda.
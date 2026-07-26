---
title: Migrasi dari WooCommerce
---

Jika toko Anda saat ini berjalan pada WooCommerce, wizard migrasi Spwig dapat mengimpor produk, pelanggan, pesanan, dan konten Anda langsung melalui REST API WooCommerce. Panduan ini mencakup mendapatkan kredensial API, menjalankan impor, dan dua fitur khusus WooCommerce yang sebaiknya diketahui terlebih dahulu: plugin Migration Bridge opsional untuk data afiliasi, dan dukungan bawaan untuk beberapa ekstensi WooCommerce populer.

## Sebelum Anda Mulai

WooCommerce memiliki dukungan terluas dari semua platform sumber dalam wizard migrasi. Berikut ini yang dapat diimpor secara bersih: kategori (dengan hierarki), produk, gambar dan variasi, pelanggan dan alamat, pesanan, ulasan, kupon, dan posting blog beserta kategorinya, tag, dan gambar.

Profil afiliasi, catatan komisi, dan sejarah pembayaran juga dapat diimpor, tetapi hanya jika Anda terlebih dahulu menginstal plugin Spwig Migration Bridge — lihat di bawah. Tanpa plugin tersebut, data tersebut akan diabaikan.

Juga perlu diingat:

- Produk dari beberapa ekstensi WooCommerce (langganan, bundel, pemesanan, kartu hadiah) akan masuk ke fitur Spwig yang sesuai, tetapi tidak semua detail akan terbawa — lihat **Dukungan Ekstensi WooCommerce** di bawah.
- Bidang kustom pada produk, pelanggan, dan pesanan Anda akan terdeteksi secara otomatis dan memerlukan pemetaan pada langkah berikutnya. Lihat [Pemetaan Bidang Migrasi](migration-field-mapping).
- Opsi **Impor pengaturan pajak** dan **Impor zona pengiriman dan metode** dari wizard tidak diterapkan pada data yang diimpor. Atur tingkat pajak dan pengiriman di Spwig sendiri setelahnya — lihat [Setelah Migrasi Anda](after-migration-review).
- Opsi **Penyesuaian Harga** pada langkah yang sama *memang* berlaku untuk impor WooCommerce, mengubah harga dasar setiap produk saat dibuat. Biarkan opsi tersebut tetap pada **Tidak Ada** kecuali Anda sengaja ingin semua harga berubah.

Siapkan login admin WordPress Anda, dan ketahui kira-kira jumlah produk, pelanggan, dan pesanan yang akan Anda impor agar Anda dapat memverifikasi jumlah yang ditampilkan oleh wizard.

## Mendapatkan Kredensial REST API

Spwig terhubung ke WooCommerce menggunakan kunci API REST yang dihasilkan dari admin WordPress Anda. Kunci ini hanya memerlukan akses **Baca** — Spwig hanya membaca dari toko Anda selama migrasi, dan tidak pernah menulis kembali apa pun.

1. Di WordPress, pergi ke **WooCommerce > Pengaturan > Lanjutan > REST API**
2. Klik **Tambahkan kunci**
3. Beri deskripsi (misalnya, `Spwig Migration`) dan atur **Izin** menjadi **Baca**
4. Klik **Buat Kunci API**
5. Salin **Consumer Key** (`ck_...`) dan **Consumer Secret** (`cs_...`) ke tempat yang aman

> **Penting:** WooCommerce hanya menampilkan Consumer Secret sekali, tepat saat Anda menghasilkannya. Jika Anda pergi ke halaman lain sebelum menyalinnya, Anda akan perlu menghasilkan kunci baru.

## Menghubungkan Toko Anda

Pergi ke **Impor Data & Ekspor > Mulai Migrasi Baru** di admin Spwig dan pilih **WooCommerce** pada langkah 1. Pada langkah 2, masukkan:

- **URL Toko** — alamat web lengkap toko Anda, misalnya `https://mystore.com`
- **Consumer Key** dan **Consumer Secret** — nilai yang baru saja Anda salin

Biarkan **Uji koneksi sebelum melanjutkan** dicentang (secara default aktif) agar Spwig memastikan dapat menghubungi toko Anda dan mengautentikasi sebelum Anda melanjutkan — ini menangkap kesalahan ejaan dan masalah izin secara langsung, bukan di tengah proses impor. Klik **Lanjutkan** setelahnya berhasil.

## Meninjau dan Memilih Data

Langkah 3 menarik jumlah data langsung dari toko Anda — kategori, produk, pelanggan, pesanan, ulasan, dan kupon — serta contoh dari lima produk pertama agar Anda dapat memastikan bahwa itu membaca situs yang benar. Setiap kotak centang jenis data akan secara otomatis dicentang ketika jumlahnya di atas nol, dan dinonaktifkan ketika jumlahnya nol.

**Opsi Impor:**

- **Lewati item yang sudah ada** (aktif) — membandingkan catatan yang masuk dengan apa yang sudah ada di Spwig (SKU untuk produk, email untuk pelanggan) dan melewatkan duplikat.

Biarkan aktif kecuali Anda mulai dari toko kosong.
- **Impor gambar produk** (aktif) — lebih lambat, tetapi sepadan.
- **Pertahankan ID asli jika memungkinkan** (nonaktif) — wizard itu sendiri menandai ini sebagai "tidak disarankan". Biarkan nonaktif kecuali Anda memiliki alasan teknis khusus untuk mempertahankan ID numerik WooCommerce.
- **Ukuran batch** — 10, 25 (default), 50 atau 100 catatan sekaligus.

Batch yang lebih kecil cocok untuk koneksi yang tidak stabil; batch yang lebih besar selesai lebih cepat pada koneksi yang stabil.

## Plugin Spwig Migration Bridge

WooCommerce tidak memiliki konsep bawaan untuk program afiliasi, jadi jika Anda menjalankan satu melalui ekstensi afiliasi WooCommerce, data tersebut berada di tabel yang tidak dapat dilihat oleh API REST standar. **Spwig Migration Bridge** adalah plugin pendamping kecil yang Anda instal di situs WordPress Anda untuk mengungkapkannya.

Plugin Bridge membuka akses:

- **Profil afiliasi** — detail afiliasi dan kode referensi mereka
- **Catatan komisi** — riwayat komisi yang terkait dengan setiap afiliasi
- **Riwayat pembayaran** — pembayaran yang telah dibayarkan ke afiliasi

Ini sepenuhnya opsional — lewati jika Anda tidak menjalankan program afiliasi atau tidak memerlukan riwayat tersebut di Spwig.

> **Catatan:** Data afiliasi hanya dapat diimpor jika pesanan dan pelanggan juga diimpor dalam migrasi yang sama, karena komisi dan pembayaran terkait dengan pesanan dan pelanggan tertentu.

Untuk menginstalnya:

1. Pada langkah 3, jika plugin belum terdeteksi di situs Anda, Anda akan melihat tombol **Unduh Plugin Bridge** dengan instruksi instalasi
2. Unduh plugin ZIP
3. Di WordPress, pergi ke **Plugins > Add New > Upload Plugin**, pilih ZIP, klik **Install Now**, lalu **Activate**
4. Kembali ke wizard Spwig dan segarkan halaman — kotak centang **Affiliates** dan blok **Affiliate Program Data** akan muncul, menampilkan jumlah yang ditemukan

Anda dapat menonaktifkan dan menghapus plugin Bridge dari WordPress setelah migrasi Anda selesai.

## Dukungan Ekstensi WooCommerce

Jika toko Anda menggunakan ekstensi populer tertentu, produk yang mereka buat diakui selama proses impor dan dipetakan ke fitur Spwig yang sesuai, bukan sebagai produk biasa:

| Ekstensi WooCommerce | Tiba di |
|---|---|
| Subscriptions | Rencana langganan Spwig |
| Product Add-Ons | Tambahan produk Spwig |
| Product Bundles | Bundle produk Spwig |
| Gift Cards (WooCommerce, YITH dan PW variant) | Kartu hadiah Spwig |
| Composite Products | Produk komposit Spwig |
| Bookings and Accommodation Bookings | Pemesanan Spwig |

> **Catatan:** Impor data ekstensi tidak pernah menghentikan pembuatan produk dasar. Jika data spesifik ekstensi produk tidak dapat dibaca, produk tetap diimpor — hanya sebagai produk biasa, tanpa konfigurasi langganan, bundel, pemesanan, atau kartu hadiah.

Periksa ulang produk langganan, bundel, pemesanan, dan kartu hadiah Anda setelah impor untuk memastikan pengaturan spesifik ekstensinya berhasil diimpor, bukan mengasumsikan bahwa impor sukses membawa semua detail.

## Bidang Kustom

Jika Anda menambahkan bidang meta kustom ke produk, pelanggan, atau pesanan WooCommerce Anda, Spwig akan mengambil sampel sekitar sepuluh catatan dari setiap jenis untuk mendeteksi bidang apa yang ada. Anda akan memetakan masing-masing ke slot bidang kustom Spwig atau ke bidang Meta Data umum pada langkah 4. Lihat [Pemetaan Bidang Migrasi](migration-field-mapping) untuk panduan lengkap, termasuk cara penyimpanan pemetaan untuk migrasi masa depan.

## Melakukan Impor

Setelah Anda meninjau langkah 3 dan memverifikasi pemetaan Anda pada langkah 4, mulailah impor. Ini berjalan di latar belakang — Anda dapat menutup jendela browser dan impor tetap berjalan. Langkah 5 menampilkan kemajuan langsung dengan satu baris per jenis data (kategori, produk, pelanggan, pesanan, ulasan, kupon, posting blog, dan afiliasi/komisi/pembayaran jika plugin Bridge digunakan) ditambah log aktivitas yang dapat diperluas.

Langkah 6 menampilkan hasil Anda: apa yang diimpor, dilewati, atau gagal, plus alat **Rewriting Tautan** jika tautan internal ke domain WooCommerce lama ditemukan dalam konten yang diimpor.

Periksa ringkasan dengan hati-hati, kemudian ikuti daftar pemeriksaan di [Setelah Pemigrasian Anda](after-migration-review) — daftar ini mencakup memverifikasi data Anda, mengatur tarif pajak dan pengiriman (yang tidak dikonfigurasi oleh wizard), serta menulis ulang tautan internal.

## Batalkan Kunci API Anda

Setelah Anda memastikan pemigrasian selesai dengan sukses, kembali ke **WooCommerce > Pengaturan > Lanjutan > REST API** di WordPress dan batalkan atau hapus kunci yang Anda buat untuk Spwig. Tidak ada alasan untuk meninggalkan kunci API aktif di toko lama Anda setelah selesai menggunakan kunci tersebut.

## Tips

- **Buat kunci API tepat sebelum Anda membutuhkannya** — karena Secret Konsumen hanya ditampilkan sekali, buatlah kunci tersebut segera sebelum memulai langkah 2, bukan sebelumnya.
- **Hanya baca saja benar-benar cukup** — jangan pernah memberikan izin Tulis atau Baca/Tulis; Spwig hanya pernah membaca dari toko WooCommerce Anda.
- **Pasang plugin Bridge sebelum memulai impor** — Anda akan membutuhkannya dan memperbarui wizard sebelum mengimpor, jadi periksa keberadaannya sejak awal, bukan di tengah proses.
- **Periksa ulang produk yang didukung ekstensi** — langganan, paket, pemesanan, dan kartu hadiah adalah produk yang paling mungkin memerlukan pemeriksaan manual setelah impor.
- **Impor parsial tidak dibersihkan secara otomatis** — lihat [Pemecahan Masalah Pemigrasian](migration-troubleshooting) sebelum mencoba kembali impor yang gagal.
- **Batalkan kunci API ketika Anda selesai** — jangan biarkan integrasi lama tetap aktif di toko yang telah Anda migrasikan.
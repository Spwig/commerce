---
title: Migrasi dari Shopify
---

Jika toko Anda saat ini berjalan di Shopify, wizard migrasi Spwig dapat mengimpor produk, pelanggan, pesanan, dan konten Anda dengan terhubung ke aplikasi kustom kecil yang Anda buat di dashboard Shopify Partners. Platform Shopify lebih terkunci daripada kebanyakan, jadi sebagian besar panduan ini tentang membuat aplikasi tersebut dengan benar — koneksi itu sendiri adalah langkah lima menit setelah aplikasi ada.

## Sebelum Anda Mulai

Dua batasan khusus Shopify cukup penting untuk disebutkan di sini, bukan hanya di tabel lebih jauh:

> **Penting:** Shopify tidak memiliki API ulasan, jadi **ulasan pelanggan tidak sama sekali dimigrasikan**, terlepas dari cakupan aplikasi apa pun yang Anda izinkan. Jika Anda membutuhkan ulasan Anda, ekspor mereka secara terpisah dari aplikasi ulasan apa pun yang Anda gunakan (Judge.me, Yotpo, Loox, dll.) dan impor mereka ke Spwig sendiri.

> **Penting:** Secara default, Spwig hanya dapat membaca **pesanan dari 60 hari terakhir**. Untuk membawa seluruh riwayat pesanan Anda, Anda harus menambahkan cakupan `read_all_orders` saat Anda membuat aplikasi — lihat daftar cakupan di bawah ini. Ini mudah terlewat karena aplikasi masih terhubung dan mengimpor dengan sukses tanpa itu; hanya saja secara diam-diam membatasi seberapa jauh riwayat pesanan Anda dapat kembali.

Semua hal lain berpindah dengan baik: kategori (sebagai Koleksi — lihat di bawah), produk, gambar, variasi, pelanggan dan alamat, diskon, dan konten blog. Bidang kustom adalah celah yang lain yang menonjol — lihat **Metafield Shopify** di akhir panduan ini.

Juga ingat bahwa:

- Opsi **Import pengaturan pajak** dan **Import zona pengiriman dan metode** dari wizard tidak diterapkan pada data yang diimpor. Atur tarif pajak dan pengiriman di Spwig sendiri setelahnya — lihat [Setelah Migrasi Anda](after-migration-review).
- Opsi **Penyesuaian harga** di langkah yang sama *memang* berlaku untuk migrasi Shopify, mengubah harga dasar setiap produk saat dibuat. Biarkan tetap diatur ke **Tidak ada** kecuali Anda sengaja ingin setiap harga berubah.
- Anda memerlukan akses ke akun Shopify Partners untuk membuat aplikasi. Jika Anda belum memiliki satu, Shopify memungkinkan Anda membuatnya secara gratis di [partners.shopify.com](https://partners.shopify.com).

## Membuat Aplikasi Shopify

Spwig terhubung ke Shopify melalui aplikasi kustom yang Anda buat dan instal di toko Anda sendiri. Ini mencerminkan modal **Shopify API Setup Guide** dalam produk (dibuka melalui **Open Setup Guide** di langkah 2 dari wizard), jadi langkah-langkah di bawah ini cocok dengan apa yang Anda lihat di sana secara tepat — Anda dapat mengikuti salah satunya.

### Langkah 1: Membuat aplikasi

1. Buka [dashboard pengembang Shopify Partners](https://dev.shopify.com/dashboard) Anda dan buka **Apps**
2. Klik **Create app**
3. Pilih **Start from Dev Dashboard**
4. Masukkan nama aplikasi: `Spwig Migration`
5. Klik **Create**

![Membuat aplikasi Spwig Migration di dashboard pengembang Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Langkah 2: Tetapkan URL Aplikasi dan cakupan

Di halaman konfigurasi aplikasi baru, di bawah **Versions**, atur:

- **App URL**: `https://shopify.dev/apps/default-app-home`
- **Scopes**: `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![Menetapkan URL Aplikasi dan cakupan yang diperlukan](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Cakupan | Memberi akses Spwig ke |
|---|---|
| `read_products` | Produk, variasi, gambar, koleksi |
| `read_customers` | Nama pelanggan, email, alamat |
| `read_orders` | Pesanan dari 60 hari terakhir |
| `read_content` | Posting blog dan halaman |
| `read_discounts` | Kode diskon dan aturan |
| `read_files` | File media yang diunggah |

> **Catatan:** Ingin riwayat pesanan penuh, bukan hanya 60 hari terakhir? Tambahkan `read_all_orders` ke daftar cakupan di atas.

### Langkah 3: Salin Client ID dan Secret Anda

Buka **Settings > Credentials** dan salin **Client ID** dan **Secret** yang ditampilkan di sana — Anda akan menempelkannya ke wizard Spwig dalam sebentar.

![Menyalin Client ID dan Secret dari halaman Pengaturan aplikasi](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Langkah 4: Buat tautan distribusi kustom

1.

Pergi ke **Distribusi** dan pilih **Distribusi khusus**
2.

Masukkan domain toko Anda (misalnya, `yourstore.myshopify.com`)
3.

Klik **Buat tautan**, lalu **Salin** tautan instal yang dihasilkan

![Menyalin tautan instal distribusi khusus yang dihasilkan](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Langkah 5: Memasang aplikasi di toko Anda

Buka tautan instal yang baru saja Anda salin di browser Anda (pastikan Anda masuk ke admin toko Shopify Anda), tinjau izin yang diminta, lalu klik **Pasang**.

![Memasang aplikasi di toko Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Penting:** Langkah terakhir ini mudah terlewat. Membuat tautan instal tidak memasang aplikasi — Anda harus benar-benar membuka tautan dan mengklik Pasang, atau Spwig tidak akan bisa terhubung. Jika uji koneksi gagal di bagian berikutnya, ini adalah hal pertama yang perlu Anda periksa.

## Menyalin Kredensial Anda ke Spwig

Di admin Spwig, pergi ke **Impor dan Ekspor Data > Mulai Migrasi Baru**, pilih **Shopify** di langkah 1, dan di langkah 2 masukkan:

- **Domain Toko** — `yourstore.myshopify.com`
- **Client ID** — dari Pengaturan > Kredensial
- **Client Secret** — dari Pengaturan > Kredensial

Jika Anda lebih suka mengikuti panduan dalam produk daripada panduan ini, klik **Buka Panduan Pengaturan** di langkah ini — panduan tersebut mencakup lima langkah yang sama di atas dengan screenshot yang sama, dan memakan waktu sekitar 10 menit dari awal sampai akhir.

Biarkan **Uji koneksi sebelum melanjutkan** dicentang. Jika `read_products`, `read_customers` atau `read_orders` tidak ada dalam cakupan aplikasi Anda, Spwig akan memperingatkan Anda sebelum Anda melanjutkan — kembali ke halaman Versi aplikasi di dashboard Shopify, tambahkan cakupan yang hilang, simpan versi baru, dan coba lagi.

## Melihat dan Memilih Data

Langkah 3 menarik jumlah live dari toko Anda dan menampilkan contoh dari lima produk pertama. Beberapa hal terlihat berbeda dari platform lain:

- **Koleksi, bukan kategori** — Shopify mengelompokkan produk ke dalam Koleksi, bukan kategori, dan Koleksi tidak mendukung penggabungan, sehingga hierarki diimpor secara datar. Jika toko Shopify Anda menggunakan koleksi untuk merepresentasikan pohon kategori, rencanakan untuk membangun struktur tersebut kembali di manajer kategori Spwig setelah impor.
- **Diskon, bukan kupon** — Kode diskon dan aturan Shopify diimpor sebagai diskon Spwig.
- **Tidak ada baris Ulasan** — karena Shopify tidak memiliki API ulasan, jenis data ini tidak muncul sama sekali di langkah ini, berbeda dengan WooCommerce atau impor CSV.

**Opsi Impor** bekerja sama seperti di platform lain: **Lewati item yang sudah ada** (aktif) cocok berdasarkan SKU dan email untuk menghindari duplikat; **Impor gambar produk** (aktif) lebih lambat tetapi disarankan; **Pertahankan ID asli jika memungkinkan** (nonaktif) sebaiknya tetap nonaktif kecuali Anda memiliki alasan khusus untuk mengubahnya; **Ukuran batch** secara default diatur ke 25.

## Metafield Shopify

Jika Anda menggunakan metafield Shopify untuk menyimpan data tambahan pada produk, pelanggan, atau pesanan, perhatikan bahwa Spwig tidak mendeteksi atau membaca mereka — berbeda dengan WooCommerce, tidak ada langkah pemetaan bidang khusus untuk impor Shopify. Data apa pun yang telah Anda simpan di metafield akan perlu dimasukkan ulang secara manual di Spwig menggunakan [bidang khusus](migration-field-mapping) setelah migrasi, jadi sebaiknya ekspor daftar metafield dan nilai-nilainya dari Shopify sebelum Anda memulai.

## Menjalankan Impor

Setelah Anda meninjau langkah 3, mulailah impor. Ini berjalan di latar belakang — Anda dapat menutup jendela browser dan impor tetap berjalan. Langkah 5 menampilkan kemajuan live dengan satu baris per jenis data dan log aktivitas yang dapat diperluas.

Langkah 6 menampilkan hasil Anda: apa yang diimpor, dilewati, atau gagal, serta alat **Penulisan Ulang Tautan** jika tautan internal ke domain lama Anda `myshopify.com` ditemukan dalam konten yang diimpor.

Periksa ringkasan dengan hati-hati, kemudian ikuti checklist di [Setelah Pemindahan Anda](after-migration-review) — ini mencakup memverifikasi data Anda, membangun ulang hierarki koleksi apa pun, mengatur tarif pajak dan pengiriman (yang tidak dikonfigurasi oleh wizard), dan memasukkan kembali hal-hal yang disimpan di metafield.

## Hapus Aplikasi dari Shopify

Setelah Anda memastikan pemindahan selesai dengan sukses, kembali ke halaman **Apps** di admin Shopify Anda, atau dashboard Partners, dan hapus aplikasi Spwig Migration (atau setidaknya uninstall dari toko Anda). Tidak ada alasan untuk meninggalkan akses baca ke data toko Anda aktif setelah pemindahan selesai.

## Tips

- **Riwayat pesanan dibatasi secara default** — jika Anda memerlukan lebih dari 60 hari terakhir dari pesanan, tambahkan `read_all_orders` ke daftar cakupan sebelum menghasilkan tautan instalasi Anda, bukan setelahnya.
- **Ulasan memerlukan ekspor terpisah** — rencanakan hal ini sebelum Anda melakukan pemindahan, karena tidak ada cara untuk membawa ulasan melalui wizard sama sekali.
- **Menghasilkan tautan tidak sama dengan menginstal aplikasi** — selalu selesaikan Langkah 5 dan klik Instal, atau uji koneksi di Spwig akan gagal.
- **Koleksi datang dalam bentuk datar** — jika struktur kategori Anda penting untuk navigasi atau SEO, alokasikan waktu untuk membangun ulang hierarki di Spwig setelah impor.
- **Ekspor metafield Anda terlebih dahulu** — Spwig tidak dapat membacanya, jadi tangkap data tersebut dari Shopify sebelum Anda memulai jika Anda membutuhkannya nanti.
- **Hapus aplikasi setelah Anda diverifikasi** — jangan biarkan integrasi aktif yang menunjuk ke toko lama Anda setelah Anda sudah beralih.
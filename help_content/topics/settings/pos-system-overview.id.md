---
title: Gambaran Sistem POS
---

Sistem POS Spwig mengubah toko Anda menjadi solusi ritel lengkap dengan terminal point-of-sale modern. Ini termasuk dalam setiap edisi — Community, Pro, dan Enterprise — dengan terminal tak terbatas di lokasi tak terbatas tanpa biaya tambahan. Setiap terminal adalah Progressive Web App (PWA) yang berfungsi offline, sinkronisasi otomatis, dan terintegrasi secara mulus dengan inventaris, data pelanggan, dan pemrosesan pembayaran. Kelola semuanya dari dashboard admin—konfigurasi terminal, penyelesaian shift, kustomisasi struk, dan integrasi perangkat keras.

Gunakan sistem POS saat Anda memiliki lokasi ritel fisik, toko pop-up, pameran dagang, atau lingkungan apa pun di mana pelanggan membeli secara langsung daripada secara online.

![Dashboard POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Apa itu Spwig POS?

Spwig POS adalah sistem point-of-sale yang sepenuhnya terintegrasi yang dirancang untuk pedagang yang menjual secara online dan di lokasi fisik. Berbeda dengan sistem POS pihak ketiga yang memerlukan integrasi yang kompleks, Spwig POS dibangun langsung ke dalam platform Anda, memastikan sinkronisasi data yang sempurna di semua saluran penjualan.

**Ciri Khas Utama**:
- **Terminal Tak Terbatas** - Sebarkan sebanyak terminal yang diperlukan tanpa biaya tambahan
- **Arsitektur Offline-First** - Terus memproses penjualan bahkan ketika koneksi internet hilang
- **Progressive Web App** - Tidak memerlukan instalasi dari toko aplikasi; akses melalui browser di perangkat apa pun (tablet, komputer, terminal khusus)
- **Sinkronisasi Stok Nyata** - Pemesanan stok (TTL 15 menit) mencegah penjualan berlebihan di seluruh saluran
- **Dukungan Split Tender** - Terima beberapa metode pembayaran per transaksi (uang tunai + kartu + kartu hadiah)
- **Integrasi Perangkat Keras** - Printer termal ESC/POS, scanner barcode, laci uang, tampilan pelanggan
- **Manajemen Shift** - Rekonsiliasi uang tunai dengan hitungan pembukaan/penutupan dan pelacakan perbedaan
- **Siap Multi-Lokasi** - Kelompok toko dengan pengambilan pengaturan untuk manajemen franchise dan regional

## Edisi

POS termasuk dalam setiap edisi Spwig — Community, Pro, dan Enterprise — sejak Spwig 1.5.8. Tidak ada lisensi POS terpisah, tidak ada langkah aktivasi, dan tidak ada biaya per terminal.

**Apa yang termasuk dalam setiap edisi**:
- Pendaftaran terminal tak terbatas
- Penugasan staf tak terbatas
- Semua fitur POS (shift, manajemen uang tunai, kustomisasi struk, tampilan pelanggan)
- Integrasi penyedia pembayaran (Stripe Terminal dan penyedia lain yang didukung)
- Dukungan integrasi perangkat keras

Pedagang yang menjalankan toko yang dihosting Spwig atau membayar lisensi Pro/Enterprise mendapatkan batas yang lebih tinggi pada layanan yang dihosting Spwig (GeoIP, geocoder, notifikasi push) dan dukungan prioritas, tetapi set fitur POS itu sendiri identik di seluruh edisi.

## Arsitektur Sistem

**Frontend** - Progressive Web App React 18:
- Offline-first dengan caching Service Worker (berfungsi tanpa internet)
- Sistem pembuatan Vite untuk muat cepat
- CSS Modules + token desain (konsisten dengan tema toko Anda)
- IndexedDB untuk penyimpanan data lokal
- 10 bahasa yang didukung (Inggris, Cina Sederhana/Tradisional, Prancis, Jerman, Spanyol, Portugis, Jepang, Rusia, Arab)

**Backend** - Integrasi Backend:
- 13 model POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, dll.)
- 43+ titik akhir REST API untuk operasi terminal
- Sistem pemesanan stok dengan manajemen TTL
- Tugas Celery untuk sinkronisasi latar belakang
- Penyimpanan kredensial terenkripsi untuk penyedia pembayaran

**Keamanan**:
- Pasangan terminal melalui kode 8 karakter (dibuat di sisi server, kedaluwarsa setelah digunakan)
- Kontrol penugasan staf yang menentukan pengguna mana yang dapat mengakses terminal mana
- Kemampuan kunci/unclock jarak jauh untuk keadaan darurat admin
- Kredensial penyedia pembayaran yang terenkripsi
- Otorisasi berbasis sesi dengan dukungan pembukaan biometrik (tergantung browser)

## Alur Kerja Getting Started

Ikuti 4 langkah berikut untuk mendeploy terminal POS pertama Anda.

Untuk panduan langkah demi langkah lengkap yang mencakup pengaturan staf, penyedia pembayaran, dan menjalankan penjualan pertama Anda, lihat [Getting Started with POS](getting-started-with-pos).

**Langkah 1: Membuat Gudang**
- Navigasikan ke **Catalog > Warehouses**
- Buat gudang yang mewakili lokasi ritel Anda
- Konfigurasikan alamat dan informasi kontak
- Gudang ini akan melacak inventaris fisik untuk penjualan POS

**Langkah 2: Mendaftarkan Terminal**
- Navigasikan ke **POS > Terminals**
- Klik **+ Add Terminal**
- Tetapkan nama terminal (misalnya, "Main Register", "Checkout 1")
- Tetapkan gudang dari Langkah 2
- Konfigurasikan pengaturan perangkat keras (printer, scanner, laci uang)
- Simpan untuk menghasilkan kode pasangan 8 karakter

**Langkah 3: Menetapkan Staf**
- Dalam konfigurasi terminal, gulir ke **Assigned Users**
- Pilih staf yang berwenang menggunakan terminal ini
- Hanya pengguna yang ditetapkan yang dapat masuk ke terminal
- Pengguna harus memiliki izin POS yang sesuai dalam peran staf mereka

**Langkah 4: Memasangkan Perangkat**
- Di perangkat terminal Anda (tablet/komputer), navigasikan ke URL `/pos/`
- Masukkan kode pasangan 8 karakter dari Langkah 3
- Terminal mengunduh konfigurasi dan menyinkronkan data awal
- Masuk dengan kredensial staf yang ditetapkan
- Terminal siap untuk penjualan

Setelah dipasangkan, terminal secara otomatis menyinkronkan setiap 5 menit (dapat dikonfigurasi). Mode offline memungkinkan operasi terus berlangsung ketika koneksi internet tidak tersedia—penjualan akan disinkronkan secara otomatis ketika koneksi kembali.

## Fitur POS Inti

**Pemrosesan Penjualan**:
- Pencarian produk berdasarkan nama, SKU, atau kode batang
- Split tender (metode pembayaran ganda per pesanan)
- Keranjang yang ditangguhkan (simpan transaksi yang tidak selesai)
- Pengembalian dan pembatalan dengan pelacakan alasan
- Penerapan diskon (voucher, kartu hadiah, promosi)
- Pencarian pelanggan dan penyelesaian poin loyalitas

**Manajemen Uang Tunai**:
- Pembukaan shift dengan jumlah uang tunai awal
- Penutupan shift dengan rekonsiliasi antara yang diharapkan dan aktual
- Pergerakan uang tunai (penambahan uang kembangan, penarikan uang kecil dengan alasan)
- Perhitungan otomatis uang tunai yang diharapkan berdasarkan penjualan tunai
- Pelacakan dan pelaporan ketidaksesuaian

**Integrasi Perangkat Keras**:
- Printer struk termal ESC/POS (jaringan atau serial)
- Scanner kode batang USB
- Pemicu laci uang melalui pulsa printer
- Tampilan pelanggan (kursi promosi saat tidak aktif)
- Pembaca kartu Stripe Terminal (S700, WisePOS E, P400)

**Kemampuan Offline**:
- Service Worker menyimpan semua aset terminal
- IndexedDB menyimpan pesanan terbaru (dapat dikonfigurasi: 7-30 hari, 200-1000 pesanan)
- Pemesanan stok dengan TTL 15 menit mencegah penjualan berlebihan
- Antrian penjualan untuk disinkronkan ketika koneksi kembali
- Deteksi koneksi ulang otomatis

## Halaman Admin POS

Akses halaman admin ini untuk mengelola semua aspek implementasi POS Anda:

**Dashboard POS** (`/admin/pos/`)
- Gambaran sistem dan statistik cepat
- Aktivitas terminal terbaru
- Ringkasan shift aktif
- Kisi penggunaan layanan terhosting (GeoIP, geocoder, push — lihat [Spwig Hosted Services](hosted-services))

**Manajemen Terminal** (`/admin/pos_app/posterminal/`)
- Daftarkan dan konfigurasikan terminal
- Tetapkan staf dan gudang
- Pantau status online/offline (pelacakan detak jantung)
- Buka ulang terminal secara jarak jauh
- [Pelajari lebih lanjut: Managing POS Terminals](managing-pos-terminals)

**Manajemen Shift** (`/admin/pos_app/posshift/`)
- Lihat semua shift (terbuka, ditutup, historis)
- Tinjau laporan rekonsiliasi uang tunai
- Lacak pergerakan uang tunai dan ketidaksesuaian
- Audit aktivitas shift
- [Pelajari lebih lanjut: POS Shifts and Cash Management](pos-shifts-cash-management)

**Kelompok Toko** (`/admin/pos_app/storegroup/`)
- Kelompokkan terminal berdasarkan lokasi/daerah
- Konfigurasikan pengaturan tingkat kelompok (mata uang, bahasa, zona waktu)
- Implementasikan hierarki pewarisan pengaturan
- [Pelajari lebih lanjut: POS Store Groups](pos-store-groups)

**Template Struk** (`/admin/pos_app/receipttemplate/`)
- Sesuaikan struk cetak (lebar kertas, logo, header/footer)
- Konfigurasikan bidang kepatuhan (NPWP, izin usaha)
- Tambahkan kode QR untuk promosi
- Batasi template ke toko atau grup tertentu
- [Pelajari lebih lanjut: Pengaturan Template Struk](receipt-template-customization)

**Slide Promosi** (`/admin/pos_app/promoslide/`)
- Buat konten carousel tampilan pelanggan
- Targetkan slide ke toko atau grup tertentu
- Jadwalkan promosi musiman
- [Pelajari lebih lanjut: Slide Promosi Tampilan Pelanggan](customer-display-promo-slides)

**Pemroses Pembayaran** (`/admin/pos_app/posterminalprovider/`)
- Konfigurasikan integrasi Stripe Terminal
- Kelola kredensial pemroses pembayaran
- Pantau status koneksi
- [Pelajari lebih lanjut: Pemroses Terminal Pembayaran](payment-terminal-providers)

**Pembaca Kartu** (`/admin/pos_app/posterminalreader/`)
- Daftarkan pembaca kartu fisik
- Hubungkan pembaca ke terminal
- Sesuaikan layar awal (branding tampilan pelanggan)
- Pantau status pembaca (online/offline/busy)
- [Pelajari lebih lanjut: Manajemen Pembaca Kartu](card-reader-management)

## Pengembangan Multi-Lokasi

Untuk pedagang dengan beberapa lokasi ritel, Spwig POS mendukung hierarki pengaturan yang berlapis:

**Hierarki Pengaturan** (prioritas tertinggi ke terendah):
1. Pengaturan terminal spesifik (mengatasi semua)
2. Pengaturan toko spesifik (mengatasi grup dan situs)
3. Pengaturan grup (mengatasi default situs)
4. Default situs (fallback untuk semua)

Konfigurasikan pengaturan bersama di tingkat grup (misalnya, mata uang regional, bahasa) dan atur ulang untuk toko atau terminal tertentu jika diperlukan. Lihat [Grup Toko POS](pos-store-groups) untuk panduan konfigurasi terperinci.

## Tips

- **Mulai dengan satu terminal** - Uji pengaturan POS dan alur kerja dengan satu terminal sebelum diterapkan secara luas
- **Tetapkan gudang sebelum pasangan** - Terminal tidak dapat memproses penjualan tanpa penugasan gudang
- **Konfigurasikan template struk sejak awal** - Bidang kepatuhan (NPWP) bervariasi berdasarkan wilayah; atur sebelum diluncurkan
- **Uji mode offline** - Putuskan koneksi internet dan verifikasi penjualan tetap berjalan; konfirmasi sinkronisasi saat koneksi kembali
- **Gunakan grup toko untuk multi-lokasi** - Mempermudah manajemen konfigurasi untuk pengembangan franchise atau regional
- **Pantau status heartbeat** - Terminal membalas server setiap 5 menit; terminal offline muncul di dashboard admin
- **Konfigurasikan batas sinkronisasi untuk kinerja** - Terminal dengan koneksi lambat akan lebih baik dengan pengaturan sync_days/sync_limit yang lebih rendah
- **Backup konfigurasi perangkat keras** - Dokumentasikan IP printer, pengaturan scanner, konfigurasi laci uang untuk pemulihan bencana
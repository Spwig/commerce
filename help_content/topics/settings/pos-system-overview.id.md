---
title: POS System Overview
---

Sistem POS Spwig mengubah toko Anda menjadi solusi ritel lengkap dengan terminal point-of-sale modern. Sebarkan terminal tak terbatas di lokasi tak terbatas dengan biaya lisensi tahunan flat €499. Setiap terminal adalah Progressive Web App (PWA) yang berfungsi offline, menyinkronkan secara otomatis, dan terintegrasi secara mulus dengan inventaris, data pelanggan, dan pemrosesan pembayaran Anda. Kelola semuanya dari dashboard admin—konfigurasi terminal, penyelesaian shift, kustomisasi struk, dan integrasi perangkat keras.

Gunakan sistem POS saat Anda memiliki lokasi ritel fisik, toko pop-up, pameran dagang, atau lingkungan apa pun di mana pelanggan membeli secara langsung daripada secara online.

![POS Dashboard](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Apa itu Spwig POS?

Spwig POS adalah sistem point-of-sale yang sepenuhnya terintegrasi yang dirancang untuk pedagang yang menjual secara online dan di lokasi fisik. Berbeda dengan sistem POS pihak ketiga yang memerlukan integrasi yang kompleks, Spwig POS dibangun langsung ke dalam platform Anda, memastikan sinkronisasi data sempurna di semua saluran penjualan.

**Ciri Khas Utama**:
- **Terminal Tak Terbatas** - Sebarkan sebanyak terminal yang diperlukan tanpa biaya tambahan
- **Arsitektur Offline-First** - Terus memproses penjualan bahkan ketika koneksi internet hilang
- **Progressive Web App** - Tidak memerlukan instalasi dari toko aplikasi; akses melalui browser di perangkat apa pun (tablet, komputer, terminal khusus)
- **Sinkronisasi Stok Nyata** - Pemesanan stok (TTL 15 menit) mencegah penjualan berlebihan di seluruh saluran
- **Dukungan Split Tender** - Terima beberapa metode pembayaran per transaksi (uang tunai + kartu + kartu hadiah)
- **Integrasi Perangkat Keras** - Printer termal ESC/POS, pemindai kode batang, laci uang, tampilan pelanggan
- **Manajemen Shift** - Rekonsiliasi uang tunai dengan hitungan pembukaan/pembukaan dan pelacakan perbedaan
- **Siap Multi-Lokasi** - Kelompok toko dengan pengambilan pengaturan untuk manajemen waralaba dan regional

## Lisensi dan Aktivasi

**Harga Flat Rate**: €499 per tahun mencakup terminal tak terbatas di lokasi tak terbatas. Tidak ada biaya per terminal, tidak ada biaya transaksi, tidak ada biaya tersembunyi.

**Format Lisensi**: `POS-XXXX-XXXX-XXXX-XXXX` (disediakan setelah pembelian)

**Aktivasi**: Masukkan kunci lisensi Anda di **Pengaturan > Lisensi POS**. Sistem memvalidasi dengan server lisensi Spwig dan mengaktifkan semua fitur POS secara langsung. Lisensi mencakup periode grasi 14 hari setelah kedaluwarsa untuk memungkinkan penundaan pemrosesan pembayaran.

**Apa yang Anda Dapatkan**:
- Pendaftaran terminal tak terbatas
- Penugasan staf tak terbatas
- Semua fitur POS (shift, manajemen uang tunai, kustomisasi struk, tampilan pelanggan)
- Integrasi penyedia pembayaran (Stripe Terminal dan sistem penyedia yang dapat diperluas)
- Dukungan integrasi perangkat keras
- Pembaruan dan perbaikan bug selama masa lisensi

Tidak ada fitur POS yang dapat diakses tanpa lisensi yang valid—antarmuka pasangan terminal, manajemen shift, dan halaman admin POS semua memerlukan aktivasi.

## Arsitektur Sistem

**Frontend** - Progressive Web App React 18:
- Offline-first dengan caching Service Worker (berfungsi tanpa internet)
- Sistem pembuatan Vite untuk muat cepat
- CSS Modules + token desain (konsisten dengan tema toko Anda)
- IndexedDB untuk penyimpanan data lokal
- 10 bahasa yang didukung (Inggris, Cina Sederhana/Tradisional, Prancis, Jerman, Spanyol, Portugis, Jepang, Rusia, Arab)

**Backend** - Integrasi Backend:
- 13 model POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, dll.)
- 43+ endpoint API REST untuk operasi terminal
- Sistem pemesanan stok dengan manajemen TTL
- Tugas Celery untuk sinkronisasi latar belakang
- Penyimpanan kredensial terenkripsi untuk penyedia pembayaran

**Keamanan**:
- Pasangan terminal melalui kode 8 karakter (dibuat di sisi server, kedaluwarsa setelah digunakan)
- Kontrol penugasan staf yang menentukan pengguna mana yang dapat mengakses terminal mana
- Kemampuan kunci jauh untuk situasi darurat admin
- Kredensial penyedia pembayaran yang terenkripsi
- Otorisasi berbasis sesi dengan dukungan pembukaan biometrik (tergantung browser)

## Alur Kerja Getting Started

Ikuti 5 langkah berikut untuk menyebar terminal POS pertama Anda:

**Langkah 1: Aktifkan Lisensi POS**
- Navigasikan ke **Pengaturan > Lisensi POS**
- Masukkan kunci lisensi Anda (`POS-XXXX-XXXX-XXXX-XXXX`)
- Validasi lisensi (memerlukan koneksi internet)
- Konfirmasi aktivasi

**Langkah 2: Membuat Gudang**
- Navigasikan ke **Katalog > Gudang**
- Buat gudang yang mewakili lokasi ritel Anda
- Konfigurasikan alamat dan informasi kontak
- Gudang ini akan melacak inventaris fisik untuk penjualan POS

**Langkah 3: Mendaftarkan Terminal**
- Navigasikan ke **POS > Terminal**
- Klik **+ Tambah Terminal**
- Tetapkan nama terminal (misalnya, "Register Utama", "Checkout 1")
- Tetapkan gudang dari Langkah 2
- Konfigurasikan pengaturan perangkat keras (printer, pemindai, laci uang)
- Simpan untuk menghasilkan kode pasangan 8 karakter

**Langkah 4: Menetapkan Staf**
- Dalam konfigurasi terminal, gulir ke **Pengguna yang Ditetapkan**
- Pilih staf yang diizinkan menggunakan terminal ini
- Hanya pengguna yang ditetapkan yang dapat masuk ke terminal
- Pengguna harus memiliki izin POS yang sesuai dalam peran staf mereka

**Langkah 5: Memasangkan Perangkat**
- Di perangkat terminal Anda (tablet/komputer), navigasikan ke URL `/pos/`
- Masukkan kode pasangan 8 karakter dari Langkah 3
- Terminal mengunduh konfigurasi dan menyinkronkan data awal
- Masuk dengan kredensial staf yang ditetapkan
- Terminal siap untuk penjualan

Setelah dipasangkan, terminal menyinkronkan secara otomatis setiap 5 menit (dapat dikonfigurasi). Mode offline memungkinkan operasi terus berlangsung ketika internet tidak tersedia—penjualan menyinkronkan secara otomatis ketika koneksi kembali.

## Fitur POS Inti

**Pemrosesan Penjualan**:
- Pencarian produk berdasarkan nama, SKU, atau kode batang
- Split tender (metode pembayaran ganda per pesanan)
- Keranjang yang ditangguhkan (simpan transaksi yang tidak selesai)
- Pengembalian dan pembatalan dengan pelacakan alasan
- Penerapan diskon (voucher, kartu hadiah, promosi)
- Pencarian pelanggan dan penyelesaian poin loyalitas

**Manajemen Uang Tunai**:
- Pembukaan shift dengan hitungan uang tunai awal
- Penutupan shift dengan rekonsiliasi yang diharapkan vs aktual
- Pergerakan uang tunai (tambahkan uang kembangan, penarikan uang kecil dengan alasan)
- Perhitungan uang tunai yang diharapkan secara otomatis berdasarkan penjualan uang tunai
- Pelacakan dan pelaporan perbedaan

**Integrasi Perangkat Keras**:
- Printer struk termal ESC/POS (jaringan atau serial)
- Pemindai kode batang USB
- Pemicu laci uang melalui pulsa printer
- Tampilan yang menghadap pelanggan (kursi promosi saat tidak sibuk)
- Pembaca kartu Stripe Terminal (S700, WisePOS E, P400)

**Kemampuan Offline**:
- Service Worker menyimpan semua aset terminal
- IndexedDB menyimpan pesanan terbaru (dapat dikonfigurasi: 7-30 hari, 200-1000 pesanan)
- Pemesanan stok dengan TTL 15 menit mencegah penjualan berlebihan
- Antrian penjualan untuk sinkronisasi ketika koneksi kembali
- Deteksi koneksi ulang otomatis

## Halaman Admin POS

Akses halaman admin ini untuk mengelola semua aspek penyebaran POS Anda:

**Dashboard POS** (`/admin/pos/`)
- Gambaran sistem dan statistik cepat
- Aktivitas terminal terbaru
- Ringkasan shift aktif
- Status lisensi dan tanggal kedaluwarsa

**Manajemen Terminal** (`/admin/pos_app/posterminal/`)
- Daftarkan dan konfigurasikan terminal
- Tetapkan staf dan gudang
- Pantau status online/offline (pelacakan detak jantung)
- Buka ulang terminal secara jarak jauh
- [Pelajari lebih lanjut: Mengelola Terminal POS](managing-pos-terminals)

**Manajemen Shift** (`/admin/pos_app/posshift/`)
- Lihat semua shift (terbuka, ditutup, sejarah)
- Tinjau laporan rekonsiliasi uang tunai
- Lacak pergerakan uang tunai dan perbedaan
- Audit aktivitas shift
- [Pelajari lebih lanjut: Shift POS dan Manajemen Uang Tunai](pos-shifts-cash-management)

**Kelompok Toko** (`/admin/pos_app/storegroup/`)
- Kelompokkan terminal berdasarkan lokasi/daerah
- Konfigurasikan pengaturan tingkat kelompok (mata uang, bahasa, zona waktu)
- Implementasikan hierarki pengambilan pengaturan
- [Pelajari lebih lanjut: Kelompok Toko POS](pos-store-groups)

**Template Struk** (`/admin/pos_app/receipttemplate/`)
- Kustomisasi struk dicetak (lebar kertas, logo, header/footer)
- Konfigurasikan bidang kepatuhan (ID pajak, pendaftaran bisnis)
- Tambahkan kode QR untuk promosi
- Batasi template ke toko atau kelompok tertentu
- [Pelajari lebih lanjut: Kustomisasi Template Struk](receipt-template-customization)

**Slide Promosi** (`/admin/pos_app/promoslide/`)
- Buat konten carousel tampilan pelanggan
- Targetkan slide ke toko atau kelompok tertentu
- Jadwalkan promosi musiman
- [Pelajari lebih lanjut: Slide Promosi Tampilan Pelanggan](customer-display-promo-slides)

**Penyedia Pembayaran** (`/admin/pos_app/posterminalprovider/`)
- Konfigurasikan integrasi Stripe Terminal
- Kelola kredensial penyedia pembayaran
- Pantau status koneksi
- [Pelajari lebih lanjut: Penyedia Terminal Pembayaran](payment-terminal-providers)

**Pembaca Kartu** (`/admin/pos_app/posterminalreader/`)
- Daftarkan pembaca kartu fisik
- Tetapkan pembaca ke terminal
- Kustomisasi layar awal (branding tampilan pelanggan)
- Pantau status pembaca (online/offline/sibuk)
- [Pelajari lebih lanjut: Manajemen Pembaca Kartu](card-reader-management)

## Penyebaran Multi-Lokasi

Untuk pedagang dengan beberapa lokasi ritel, Spwig POS mendukung hierarki pengambilan pengaturan:

**Hierarki Pengaturan** (prioritas tertinggi ke terendah):
1. Pengaturan terminal khusus (mengatasi semua)
2. Pengaturan toko khusus (mengatasi kelompok dan situs)
3. Pengaturan kelompok (mengatasi default situs)
4. Default situs (fallback untuk semua)

Konfigurasikan pengaturan bersama di tingkat kelompok (misalnya, mata uang regional, bahasa) dan atur ulang untuk toko atau terminal tertentu jika diperlukan. Lihat [Kelompok Toko POS](pos-store-groups) untuk panduan konfigurasi yang rinci.

## Tips

- **Mulai dengan satu terminal** - Uji pengaturan POS dan alur kerja dengan satu terminal sebelum menyebar secara luas
- **Tetapkan gudang sebelum memasangkan** - Terminal tidak dapat memproses penjualan tanpa penugasan gudang
- **Konfigurasikan template struk awal** - Bidang kepatuhan (ID pajak) bervariasi menurut wilayah; atur sebelum diluncurkan
- **Uji mode offline** - Putuskan koneksi internet dan verifikasi penjualan tetap berlangsung; konfirmasi sinkronisasi ketika kembali terhubung
- **Gunakan kelompok toko untuk multi-lokasi** - Mempermudah manajemen konfigurasi untuk penyebaran waralaba atau regional
- **Pantau status detak jantung** - Terminal memukul server setiap 5 menit; terminal offline muncul di dashboard admin
- **Konfigurasikan batas sinkronisasi untuk kinerja** - Terminal dengan koneksi lambat manfaat dari pengaturan sync_days/sync_limit yang lebih rendah
- **Backup konfigurasi perangkat keras** - Dokumentasikan IP printer, pengaturan pemindai, konfigurasi laci uang untuk pemulihan bencana

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis persis seperti yang ditunjukkan dalam aturan pelestarian.
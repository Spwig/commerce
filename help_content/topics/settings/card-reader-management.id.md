---
title: Manajemen Pembaca Kartu
---

Manajemen pembaca kartu melacak perangkat keras pembayaran fisik, menetapkan mereka ke terminal POS, dan memantau status operasional mereka. Setiap pembaca kartu mewakili perangkat keras aktual (Stripe S700, WisePOS E, atau P400) yang terdaftar dengan penyedia pembayaran Anda. Pembaca memiliki hubungan satu-ke-satu dengan terminal—setiap register memiliki pembaca kartu yang ditetapkan. Pantau status pembaca (online, offline, busy) secara real-time, kustomisasi layar splash dengan branding Anda, dan atasi masalah koneksi sebelum memengaruhi pengalaman checkout pelanggan.

Gunakan manajemen pembaca kartu untuk memastikan perangkat keras pembayaran dikonfigurasikan, ditetapkan, dan beroperasi dengan baik di semua lokasi.

![Daftar Pembaca Kartu](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Memahami Pembaca Kartu

Pembaca kartu adalah perangkat keras fisik yang memproses pembayaran kartu kredit dan debit:

**Komponen Perangkat Keras**:
- Slot kartu chip EMV
- Antena NFC (tanpa kontak/tap-to-pay)
- Pembaca pita magnetik (legacy, jarang digunakan)
- Layar tampilan (menampilkan jumlah, meminta PIN, tanda tangan)
- Koneksi jaringan (Wi-Fi atau Ethernet, tergantung pada model)

**Integrasi Perangkat Lunak**:
- Pembaca terhubung ke Stripe Terminal API (berbasis awan, bukan koneksi langsung ke perangkat POS)
- Terminal POS meminta pembayaran melalui API
- Stripe mengarahkan permintaan ke pembaca yang terdaftar
- Pembaca memproses kartu dan mengembalikan hasil ke POS
- Tidak diperlukan koneksi USB/Bluetooth antara POS dan pembaca

**Satu Pembaca per Terminal**:
- Setiap terminal POS harus memiliki tepat satu pembaca kartu yang ditetapkan
- Hubungan satu-ke-satu memastikan tanggung jawab yang jelas dan perbaikan masalah yang disederhanakan
- Banyak terminal tidak dapat berbagi satu pembaca (menyebabkan konflik)

## Jenis Pembaca Kartu

Spwig POS mendukung pembaca kartu Stripe Terminal:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- Terminal all-in-one Android dengan layar sentuh berwarna 5"
- Opsi printer bawaan (struk termal)
- Terbaik untuk: Checkout ritel lengkap, restoran (prompt tip pada layar berwarna)
- Koneksi: Hanya Wi-Fi
- Layar splash: Berwarna penuh 480×800 potret

**Stripe Reader S700** (`stripe_s700`):
- Pembaca meja dengan layar monokrom LCD
- Desain kompak, tahan air
- Terbaik untuk: Ritel standar, meja checkout kompak
- Koneksi: Wi-Fi atau Ethernet
- Layar splash: Monokrom 480×800 potret

**Verifone P400** (`verifone_p400`):
- Pembaca meja legacy (model lama)
- Masih didukung tetapi tidak disarankan untuk penggunaan baru
- Terbaik untuk: Penggunaan yang sudah ada (jangan ganti perangkat keras yang berfungsi)
- Koneksi: Wi-Fi atau Ethernet
- Layar splash: Monokrom 480×800 potret

**Kompatibilitas Masa Depan**:
- Model pembaca tambahan mungkin ditambahkan seiring Stripe Terminal memperluas penawaran perangkat keras
- Dropdown jenis pembaca secara otomatis diisi dari kemampuan penyedia

## Alur Kerja Pendaftaran Pembaca

**Langkah 1: Membeli dan Menerima Perangkat Keras**
- Pesan pembaca dari Stripe (stripe.com/terminal) atau penjual resmi yang diizinkan
- Buka kemasan dan nyalakan pembaca
- Hubungkan ke jaringan Wi-Fi (ikuti proses pengaturan di layar pembaca)

**Langkah 2: Daftarkan di Stripe Dashboard**
- Navigasi ke **Stripe Dashboard > Terminal > Pembaca**
- Klik **Daftarkan Pembaca Baru**
- Ikuti proses pasangan di layar (pembaca menampilkan kode pendaftaran)
- Tetapkan pembaca ke Lokasi Stripe (harus cocok dengan lokasi dalam konfigurasi penyedia pembayaran)
- Catat **ID Pembaca** (terlihat seperti `tmr_ABC123...`)

**Langkah 3: Sinkronisasi ke Spwig (Otomatis)**
- Spwig secara otomatis menemukan pembaca yang terdaftar ke lokasi Stripe Anda
- Tugas latar belakang sinkronisasi setiap 30 menit
- Pembaca baru muncul dalam daftar **POS > Pembaca Kartu** dalam 30 menit

**Langkah 4: Tetapkan ke Terminal (Manual)**
- Navigasi ke **POS > Pembaca Kartu**
- Cari pembaca baru yang ditemukan dalam daftar
- Klik untuk mengedit
- Pilih **Terminal** untuk menetapkan pembaca
- Simpan

**Langkah 5: Uji Pembayaran**
- Di terminal POS, proses transaksi uji
- Pilih metode pembayaran kartu
- POS harus menemukan pembaca yang ditetapkan
- Gunakan kartu uji Stripe (4242 4242 4242 4242) untuk menyelesaikan uji
- Verifikasi pembayaran selesai dengan sukses

Jika pembaca tidak muncul selama uji, periksa penugasan terminal dan status pembaca.

## Memantau Status Pembaca

Pembaca melaporkan status ke Stripe Terminal API, yang Spwig sinkronisasi setiap 5 menit:

**Online** (hijau) - Pembaca dinyalakan, terhubung ke jaringan, dan siap menerima pembayaran

**Offline** (merah) - Pembaca dimatikan, terputus dari jaringan, atau tidak dapat dijangkau

**Busy** (kuning) - Pembaca sedang memproses transaksi pembayaran saat ini

**Terakhir Dilihat** - Tanda waktu pembaca terakhir memeriksa-in dengan API Stripe
- Diperbarui setiap ~2 menit saat pembaca online
- Berguna untuk mendiagnosis masalah koneksi ("pembaca pergi offline 3 jam yang lalu" = masalah daya atau jaringan selama jam kerja)

**Kasus Penggunaan Status**:
- **Pemeriksaan sebelum pembukaan**: Verifikasi semua pembaca toko online sebelum membuka pintu
- **Mengatasi masalah**: "Register 3 tidak menerima kartu" → Periksa status pembaca → Menunjukkan offline → Periksa daya/jaringan
- **Audit**: "Apakah pembayaran diproses di Terminal 5 kemarin?" → Periksa tanda waktu terakhir dilihat

## Penugasan Terminal

Pembaca kartu menggunakan **hubungan satu-ke-satu** dengan terminal:

**Mengapa Penugasan Penting**:
- Selama pembayaran, POS perlu mengetahui pembaca mana yang harus dikomunikasikan
- Banyak terminal berbagi satu pembaca menyebabkan konflik (dua kasir tidak dapat menggunakan pembaca yang sama secara bersamaan)
- Pembaca yang tidak ditetapkan tidak akan digunakan (perangkat keras yang terlantar)

**Aturan Penugasan**:
- Setiap terminal dapat memiliki **tepat satu** pembaca kartu yang ditetapkan
- Setiap pembaca kartu dapat ditetapkan ke **tepat satu** terminal
- Menetapkan pembaca ke Terminal A secara otomatis melepas penugasan sebelumnya dari terminal

**Mengubah Penugasan**:
- Edit catatan pembaca
- Ubah bidang **Terminal** ke terminal baru
- Simpan
- Terminal sebelumnya kehilangan penugasan pembaca (akan menampilkan kesalahan "Tidak ada pembaca yang ditetapkan" selama pembayaran)

**Pembaca yang Tidak Ditetapkan**:
- Pembaca baru yang ditemukan mulai tidak ditetapkan
- Pembaca yang tidak ditetapkan muncul dalam daftar tetapi tidak dapat digunakan
- Tetapkan ke terminal untuk mengaktifkannya

## Kustomisasi Layar Splash

Layar splash pembaca menampilkan branding pada layar menghadap ke pelanggan saat tidak aktif:

**Apa itu Layar Splash?**
- Gambar yang ditampilkan pada layar pembaca saat tidak memproses pembayaran
- Mengganti logo Stripe default dengan branding Anda
- Tampil di pelanggan saat menunggu di checkout

**Layar Splash Otomatis vs Kustom**:

**Layar Splash Otomatis** (default):
- Spwig menghasilkan layar splash dari logo toko Anda (jika logo dikonfigurasikan dalam pengaturan toko)
- Secara otomatis ukuran sesuai spesifikasi pembaca (480×800 potret)
- Monokrom untuk S700/P400, berwarna untuk WisePOS E
- Tidak diperlukan konfigurasi

**Layar Splash Kustom** (lanjutan):
- Unggah gambar desain kustom Anda sendiri
- Kontrol penuh atas desain dan branding
- Harus memenuhi persyaratan gambar (lihat di bawah)

**Persyaratan Layar Splash Kustom**:
- **Resolusi**: Tepat 480×800 piksel (orientasi potret)
- **Format**: PNG atau JPG
- **S700/P400**: Hanya monokrom (hitam dan putih, tanpa abu-abu)
- **WisePOS E**: Dukungan warna penuh
- **Ukuran file**: <200KB

**Menetapkan Layar Splash Kustom**:
1. Edit catatan pembaca kartu
2. Unggah gambar ke bidang **Gambar Pengganti Splash** (atau pilih dari Perpustakaan Media)
3. Simpan
4. Sinkronisasi layar splash ke pembaca dalam 5 menit

**Menghapus Layar Splash Kustom**:
- Bersihkan bidang **Gambar Pengganti Splash**
- Simpan
- Pembaca kembali ke layar splash otomatis (atau default Stripe jika tidak ada logo toko)

**Menguji Layar Splash**:
- Setelah mengunggah, tunggu 5 menit untuk sinkronisasi
- Kunjungi perangkat pembaca
- Verifikasi layar splash muncul di layar tidak aktif
- Periksa kualitas gambar, pusat, dan kontras

## Konfigurasi Splash Stripe

Di balik layar, Spwig mengelola konfigurasi layar splash Stripe:

**stripe_splash_file_id** - ID internal Stripe untuk file gambar splash yang diunggah
- Secara otomatis diatur saat splash diunggah
- Digunakan untuk merujuk splash dalam API Stripe

**stripe_splash_config_id** - ID internal Stripe untuk konfigurasi splash
- Menghubungkan file splash ke pembaca
- Dikelola secara otomatis saat menetapkan splash ke pembaca

Bidang-bidang ini hanya baca dan dikelola secara otomatis—Anda tidak perlu berinteraksi dengan mereka secara langsung.

## Menyelesaikan Masalah Umum

**Masalah 1: Pembaca menunjukkan offline tetapi dinyalakan**
- **Penyebab**: Masalah koneksi jaringan, kata sandi Wi-Fi berubah, pembaca di luar jangkauan
- **Solusi**: Periksa pengaturan jaringan pembaca, koneksi ulang ke Wi-Fi, verifikasi API Stripe dapat dijangkau dari jaringan

**Masalah 2: POS mengatakan "Tidak ada pembaca yang ditetapkan" selama pembayaran**
- **Penyebab**: Pembaca tidak ditetapkan ke terminal, atau penugasan tidak lengkap
- **Solusi**: Edit pembaca, tetapkan ke terminal, simpan, uji pembayaran kembali

**Masalah 3: Pembaca sibuk terus-menerus (terjebak di layar pembayaran)**
- **Penyebab**: Transaksi kedaluwarsa atau crash, status pembaca tidak diatur ulang
- **Solusi**: Restart pembaca (siklus daya), hubungi dukungan Stripe jika terus-menerus

**Masalah 4: Layar splash kustom tidak muncul**
- **Penyebab**: Gambar resolusi salah, belum disinkronkan, persyaratan monokrom tidak terpenuhi (S700/P400)
- **Solusi**: Verifikasi gambar tepat 480×800, tunggu 5 menit untuk sinkronisasi, pastikan monokrom untuk pembaca non-warna

**Masalah 5: Pembaca terdaftar di Stripe tetapi tidak muncul di Spwig**
- **Penyebab**: Pembaca terdaftar ke lokasi Stripe berbeda dari ID lokasi penyedia
- **Solusi**: Di Stripe Dashboard, verifikasi lokasi pembaca cocok dengan ID lokasi penyedia

## Tips

- **Satu pembaca per terminal** - Jangan berbagi pembaca antar terminal; mencegah konflik dan menyederhanakan tanggung jawab
- **Daftarkan pembaca sebelum ditempatkan di lantai** - Selesaikan pendaftaran Stripe dan penugasan Spwig sebelum menempatkan pembaca di checkout
- **Uji layar splash di toko** - Kontras tampilan bervariasi berdasarkan model pembaca dan pencahayaan; verifikasi layar splash terlihat baik di lingkungan sebenarnya
- **Pantau status sebelum pembukaan** - Periksa daftar pembaca setiap pagi untuk memastikan semua pembaca online sebelum toko buka
- **Labelkan perangkat keras secara fisik** - Gunakan pembuat label untuk menandai pembaca dengan nama terminal ("Terminal 1 Reader") untuk identifikasi mudah selama penyelesaian masalah
- **Jaga pembaca pada daya tidak terganggu** - Pemadaman listrik di tengah transaksi dapat merusak status pembaca; UPS disarankan
- **Dokumentasikan nomor seri pembaca** - Simpan catatan nomor seri untuk garansi dan dukungan (ditemukan di label perangkat keras pembaca)
- **Perbarui firmware pembaca** - Stripe mendorong pembaruan firmware secara otomatis, tetapi verifikasi pembaca berada di versi terbaru secara berkala (periksa Stripe Dashboard)
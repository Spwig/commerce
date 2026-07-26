---
title: Mode Offline POS & Instalasi Aplikasi
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA at rest — main login/terminal chooser view showing the Spwig POS branding
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Add-to-Home-Screen screenshots (iPad Safari, Android Chrome) are OS/browser-specific
         annotated reference shots. The session capturing this should use device emulation
         or reference images rather than attempting to trigger the browser install prompt.
-->

Spwig POS adalah sebuah Progressive Web App (PWA). Aplikasi ini berjalan sepenuhnya di browser dan dapat diinstal ke layar utama perangkat seperti aplikasi native. Karena aplikasi, katalog produk Anda, dan riwayat pesanan terbaru disimpan secara lokal di perangkat, mesin kasir tetap berfungsi meskipun terjadi gangguan jaringan singkat atau koneksi yang lambat.

Topik ini menjelaskan secara tepat apa yang berfungsi ketika koneksi terputus, bagaimana penjualan yang terkumpel diatasi ketika koneksi kembali, cara menginstal POS ke layar utama perangkat, dan bagaimana pembaruan mencapai perangkat yang telah diinstal.

## Bagaimana mode offline bekerja

Ketika Anda membuka POS untuk pertama kalinya di perangkat, browser akan mengunduh dan menyimpan seluruh aplikasi — antarmuka, gambar, dan semua kode pendukung. Komponen latar belakang yang disebut Service Worker mengelola cache ini. Sejak saat itu, aplikasi akan memuat dari cache lokal bahkan jika server tidak dapat dijangkau.

Di atas cache aplikasi, POS mempertahankan database lokal di perangkat (menggunakan penyimpanan IndexedDB bawaan browser). Database ini menyimpan:

- **Produk dan variasi** — disinkronkan dari katalog Anda dan diperbarui setiap lima menit saat online
- **Kategori** — disinkronkan saat startup dan diperbarui bersama produk
- **Tingkat stok** — disinkronkan setiap dua menit saat online (menggunakan strategi jaringan-pertama yang beralih ke data yang dikach jika server tidak merespons dalam tiga detik)
- **Catatan pelanggan** — hingga 1.000 pelanggan terbaru
- **Riwayat pesanan** — jumlah konfigurasi pesanan POS terbaru (default: 500 pesanan dalam 14 hari; diatur per terminal di **POS > POS Terminals**)
- **Gambar produk** — disimpan secara lokal hingga 24 jam

Ketika POS mendeteksi bahwa perangkat telah offline, banner muncul di bagian atas layar: **"Mode Offline - Penjualan akan disinkronkan ketika koneksi kembali."** Mesin kasir tetap beroperasi menggunakan data yang disimpan secara lokal.

## Fitur yang berfungsi dalam mode offline

| Fitur | Ketersediaan Offline |
|---------|---------------------|
| Pencarian dan penelusuran produk | Tersedia — menggunakan katalog yang disimpan secara lokal |
| Pemindaian kode batang | Tersedia — pemindaian mencari produk dalam cache lokal |
| Menambahkan item ke keranjang | Tersedia |
| Menerapkan diskon manual | Tersedia |
| Menerapkan kode voucher | Tidak tersedia — pengecekan saldo memerlukan koneksi langsung |
| Pembayaran tunai | Tersedia — dicatat secara lokal dan diproses untuk sinkronisasi |
| Pembayaran kartu (Pengisian Manual) | Tersedia — kasir memproses di terminal terpisah dan memasukkan referensi; dicatat secara lokal dan diproses untuk sinkronisasi |
| Pembayaran kartu (pembaca terintegrasi — Stripe Terminal, dll.) | Tidak tersedia — pembaca kartu terintegrasi berkomunikasi dengan jaringan pembayaran secara real-time |
| Pembayaran kartu hadiah | Tidak tersedia — pengecekan saldo memerlukan koneksi langsung |
| Pembayaran terbagi yang menggabungkan tunai dan kartu manual | Tersedia |
| Cetak struk ke printer jaringan | Tersedia jika printer berada di jaringan lokal yang sama dengan perangkat — pencetakan tidak memerlukan akses internet, hanya koneksi jaringan lokal |
| Struk digital (email/SMS/WhatsApp) | Tidak tersedia — pengiriman memerlukan koneksi langsung |
| Penelusuran riwayat pesanan | Tersedia — menampilkan pesanan yang disimpan dengan banner yang menunjukkan bahwa Anda melihat data offline |
| Pengembalian dan pembatalan | Tidak tersedia — ini memerlukan koneksi langsung |
| Pengecekan poin loyalitas pelanggan | Tidak tersedia |
| Membuka dan menutup shift | Tersedia — status shift disimpan secara lokal |

## Penjualan yang terkumpel dan sinkronisasi ketika koneksi kembali

Penjualan offline tidak hilang.

Ketika register tidak dapat terhubung ke server, setiap penjualan yang selesai ditulis ke dalam antrian lokal (penyimpanan `pendingTransactions` di database lokal perangkat).

Penjualan mencakup semua item keranjang, kuantitas, harga, metode pembayaran, dan waktu penyelesaian.

Ketika akses internet kembali pulih, POS secara otomatis:

1. Mendeteksi koneksi ulang melalui acara `online` browser
2. Menampilkan banner: **"Mensinkronkan N transaksi yang tertunda..."**
3. Mengirimkan penjualan yang di-antrikan ke backend secara berurutan, menggunakan jadwal ulang coba eksponensial jika upaya pertama gagal (hingga 10 ulang coba dalam jendela maksimum lima menit per upaya)
4. Menandai setiap penjualan sebagai disinkronkan setelah backend mengonfirmasinya

**Perlindungan dari penjualan duplikat** — setiap penjualan yang di-antrikan diberi ID lokal unik sebelum meninggalkan perangkat. Backend memeriksa ID ini sebelum membuat pesanan. Jika penjualan yang sama dikirim dua kali (misalnya, karena ulang coba tumpang tindih dengan upaya pertama yang berhasil), backend mengabaikan duplikatnya. Anda tidak akan pernah mengalami penjualan yang dihitung dua kali.

**Deteksi konflik** — dalam kasus langka, backend mungkin menandai penjualan yang di-antrikan sebagai konflik (misalnya, jika produk dihapus di sisi server saat perangkat offline). Penjualan yang konflik muncul di **POS > Pengaturan > Transaksi yang Tertunda** sehingga Anda dapat meninjau dan menyelesaikannya secara manual.

**Penyesuaian inventaris** offline ditangani dengan cara yang sama: perubahan stok yang dibuat saat offline di-antrikan dan diulang kembali ketika koneksi kembali. Angka inventaris lokal di perangkat diperbarui segera sehingga kasir melihat jumlah yang akurat (diperkirakan).

## Memasang POS ke layar beranda perangkat

Memasang POS ke layar beranda memberikan pengalaman penuh layar tanpa bilah alamat browser, ikon pintasan di perangkat, dan waktu peluncuran yang lebih cepat.

### iPad (Safari)

1. Buka Safari dan kunjungi URL POS toko Anda: `https://yourstore.com/pos/`
2. Masuk dan lengkapi proses pasangan awal jika ini perangkat baru.
3. Tap tombol **Bagikan** (persegi dengan panah ke atas) di bilah alat Safari.
4. Gulir ke bawah di lembar Bagikan dan tap **Tambahkan ke Beranda**.
5. Ubah nama jika diinginkan (secara default adalah "Spwig POS") dan tap **Tambahkan**.

Ikoon POS sekarang muncul di layar beranda iPad. Menyentuhnya membuka aplikasi secara penuh layar tanpa chrome browser Safari.

> **Catatan:** Safari di iPad diperlukan untuk opsi Tambahkan ke Beranda. Browser pihak ketiga di iOS (Chrome, Firefox) tidak mendukung instalasi PWA hingga pertengahan 2025.

### Android (Chrome)

1. Buka Chrome dan kunjungi URL POS toko Anda: `https://yourstore.com/pos/`
2. Masuk dan lengkapi pasangan jika diperlukan.
3. Tap tombol **tiga titik** (kanan atas) dan tap **Instal aplikasi** (atau **Tambahkan ke Beranda** pada versi lama Chrome).
4. Konfirmasi dengan menap **Instal**.

Ikoon POS muncul di beranda dan di dalam laci aplikasi. Meluncurkannya dari ikon membuka aplikasi dalam mode mandiri.

### Desktop (Chrome atau Edge)

1. Kunjungi URL POS toko Anda di Chrome atau Edge.
2. Cari **ikon instal** di bilah alamat browser (monitor komputer dengan panah ke bawah, atau ikon "+" tergantung versi).
3. Alternatifnya, buka **tiga titik menu** dan pilih **Instal Spwig POS** (Chrome) atau **Apps > Instal situs ini sebagai aplikasi** (Edge).
4. Konfirmasi instalasi.

POS terbuka sebagai jendela mandiri tanpa tab browser atau bilah alamat. Aplikasi muncul di daftar aplikasi sistem dan dapat dipasang ke taskbar.

## Cara aplikasi diperbarui

POS mengelola pembaruan sendiri melalui Service Worker. Anda tidak perlu mengunjungi toko aplikasi atau mengunduh sesuatu secara manual.

**Siklus pembaruan:**

1.

Setiap kali Anda membuka POS (atau tab menjadi aktif setelah berada di latar belakang), Service Worker memeriksa server untuk versi baru.
2.

Jika versi baru tersedia, Service Worker mengunduhnya di latar belakang sementara Anda terus bekerja — sesi saat ini tidak terganggu.
3.

Pembaruan berlaku saat Anda membuka POS berikutnya.

Jika aplikasi sudah terbuka dan ada sinkronisasi yang tertunda, POS menunggu antrian selesai sebelum memberi sinyal bahwa ulang muat siap, untuk menghindari mengganggu shift aktif dengan penjualan yang belum disinkronkan.

**Apa yang dimaksud dengan "reload" ketika ada penjualan yang tertunda** — jika Anda melihat prompt untuk reload untuk pembaruan dan Anda memiliki penjualan offline yang tertunda, tutup shift saat ini secara bersih (atau tunggu hingga banner sinkronisasi hilang) sebelum melakukan reload. Melakukan reload saat penjualan dalam antrian tidak menghapusnya — mereka tetap ada di database lokal — tetapi lebih aman untuk menyinkronkan terlebih dahulu untuk memastikan mereka telah diterima.

**Memeriksa versi yang terinstal** — buka POS, ketuk **ikon menu** (tiga garis horizontal), dan pergi ke **Pengaturan**. Versi build saat ini ditampilkan di bagian bawah panel pengaturan.

## Penyimpanan dan membersihkan instalasi

POS menyimpan beberapa jenis data secara lokal:

| Apa | Ukuran tipek |
|------|-------------|
| App shell (HTML, CSS, JS, ikon) | ~3–5 MB |
| Katalog produk (teks dan metadata) | 1–10 MB tergantung ukuran katalog |
| Gambar produk (dikach) | 5–50 MB tergantung ukuran katalog |
| Riwayat pesanan | 1–5 MB (500 pesanan) |
| Rekam pelanggan | 1–3 MB (1.000 pelanggan) |
| Antrian transaksi tertunda | Minimal; dihapus saat sinkronisasi |

**Jika perangkat kehabisan ruang penyimpanan** — browser menerapkan tekanan pada penyimpanan yang dikach ketika perangkat penuh. POS mengatur cache-nya sebagai persisten di mana browser memungkinkan, tetapi pada perangkat yang sangat penuh, browser mungkin menghapus gambar produk terlebih dahulu. Jika gambar berhenti memuat, POS akan mengkach ulang mereka pada sinkronisasi berikutnya. Penjualan yang disinkronkan dan app shell tidak terpengaruh.

**Mengatur ulang instalasi** — jika POS berperilaku tidak terduga (terjebak di versi lama, katalog tidak segar, sinkronisasi terjebak permanen), Anda dapat melakukan reset bersih:

1. **Uninstall aplikasi** — di mobile, tekan dan tahan ikon POS dan pilih **Hapus** atau **Uninstall**. Di desktop, klik kanan pada bilah judul jendela aplikasi dan pilih **Uninstall**.
2. Buka URL POS secara langsung di browser dan masuk kembali.
3. Perangkat akan diminta kode pasangan 8 karakter terminal lagi. Anda dapat menemukan atau menghasilkan ulang kode ini di admin di **POS > POS Terminals** — buka terminal dan klik **Regenerate pairing code**.
4. Pasangan segar memaksa sinkronisasi ulang lengkap semua data yang dikach.

> **Setelah mereset**: semua penjualan offline yang dalam antrian tetapi belum disinkronkan sebelum reset akan hilang, karena database lokal dihapus. Pastikan koneksi dipulihkan dan banner sinkronisasi hilang sebelum mereset instalasi.

## Penyelesaian Masalah

### POS terjebak di versi lama

Service Worker mungkin belum mengaktifkan versi baru. Coba tutup semua tab browser yang memiliki POS terbuka, lalu buka kembali. Jika masalah tetap berlanjut, reset instalasi seperti yang dijelaskan di atas.

### Banner "Tidak ada koneksi" tidak hilang

Periksa apakah perangkat memiliki akses internet di luar POS (coba muat situs lain). Jika perangkat online tetapi banner tetap muncul:

- Server POS mungkin sementara tidak dapat dijangkau — tunggu sebentar dan POS akan mencoba otomatis.
- Jika Anda berada di jaringan yang memerlukan halaman masuk (captive portal), buka tab browser baru, lengkapi masuk, lalu kembali ke POS.

### Produk hilang dari POS yang ada di admin

POS menyinkronkan produk setiap lima menit saat online. Jika Anda menambahkan produk di admin sangat baru-baru ini, ketuk **ikon menu** dan pergi ke **Pengaturan > Sync Now** untuk memicu sinkronisasi segera. Jika produk masih tidak muncul, konfirmasi bahwa produk tersebut ditandai sebagai **Aktif** dan tidak dikecualikan dari ketersediaan POS di pengaturan produk.

### Transaksi tertunda terjebak dalam status "Conflict"

Buka **POS > Pengaturan** (di aplikasi POS itu sendiri) dan periksa panel **Transaksi Tertunda**.

Transaksi yang konflik biasanya disebabkan oleh perubahan produk atau harga antara saat penjualan dilakukan secara offline dan saat disinkronkan.


Anda dapat melihat detail penjualan dan, jika penjualan diterima dengan benar, tandai sebagai telah diperiksa.

## Tips

- Jalankan POS pada perangkat dedikasi yang tetap terhubung ke Wi-Fi lokal Anda. Drop Wi-Fi yang singkat akan ditangani secara otomatis, tetapi perangkat yang menghabiskan waktu lama dalam mode offline akan memerlukan waktu lebih lama untuk menyinkronkan kembali saat kembali terhubung.
- Interval sinkronisasi adalah per perangkat. Jika Anda memiliki beberapa terminal, masing-masing terminal menyinkronkan secara independen. Sebuah penjualan di satu terminal akan muncul di admin secara langsung saat sinkronisasi, tetapi cache pesanan lokal terminal lain hanya diperbarui saat siklus sinkronisasi miliknya sendiri.
- Sebelum kejadian pemadaman internet yang direncanakan (misalnya, pindah ke acara tanpa Wi-Fi), buka POS saat masih terhubung agar data katalog dan inventaris terbaru tersinkronisasi sepenuhnya. Penjualan tunai akan diproses secara andal; hanya hindari pembayaran kartu terintegrasi sampai Anda kembali online.
- Jika Anda hanya memerlukan penjualan tunai di acara tersebut, metode pembayaran kartu manual (kasir memproses di terminal mandiri dan memasukkan referensi) juga berfungsi offline untuk transaksi kartu.
- Tetap colokkan perangkat selama shift yang panjang — database lokal dan proses sinkronisasi tidak secara signifikan memengaruhi baterai dibandingkan layar, tetapi perangkat yang terisi penuh selalu lebih aman untuk transaksi.
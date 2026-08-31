---
title: Mengonfigurasi Pengaturan Toko
---

Pengaturan Toko adalah tempat pusat untuk mengonfigurasi identitas, lokalisasi, branding, dan preferensi operasional toko Anda. Navigasi ke **Pengaturan > Pengaturan Toko** untuk memulai.

![Tab umum pengaturan toko](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Tab Umum

Tab **Umum** menyimpan pengaturan identitas inti toko Anda.

### Identitas Toko

- **Nama Toko** — Nama tampilan yang ditampilkan di judul halaman, email, dan header admin.
- **Tagline** — Deskripsi singkat tentang toko Anda, digunakan dalam SEO dan berbagi media sosial.
- **URL Situs** — Alamat web publik toko Anda. Ini digunakan dalam email, pembuatan sitemap, dan pembangunan tautan.

### Informasi Kontak

- **Email Kontak** — Menerima notifikasi pesanan dan ditampilkan dalam komunikasi pelanggan.
- **Nomor Telepon** — Nomor telepon dukungan opsional yang ditampilkan di footer dan email.

### Alamat Bisnis

Masukkan alamat lengkap Anda (jalan, kota, provinsi, kode pos, negara). Ini digunakan untuk:
- Perhitungan asal pengiriman
- Perhitungan pajak
- Persyaratan hukum dan faktur

## Branding

### Logo

Unggah logo toko Anda (PNG atau SVG disarankan, ~200x50px dengan latar belakang transparan). Logo muncul di:
- Header storefront
- Template email
- Panel admin

### Favicon

Unggah favicon persegi (ICO atau PNG, 32x32px). Muncul sebagai:
- Ikon tab browser
- Ikon bookmark
- Ikon layar utama mobile

## Lokalisasi

### Bahasa Default

Pilih bahasa utama toko Anda dari 10 opsi yang didukung:

| Bahasa | Kode |
|----------|------|
| English | en |
| Spanish | es |
| French | fr |
| German | de |
| Portuguese | pt |
| Japanese | ja |
| Chinese Simplified | zh-hans |
| Chinese Traditional | zh-hant |
| Russian | ru |
| Arabic | ar |

Bahasa default mengontrol bahasa antarmuka admin dan fallback untuk konten storefront.

### Zona Waktu

Pilih zona waktu toko Anda untuk timestamp pesanan yang akurat, promosi terjadwal, dan pelaporan.

### Mata Uang

- **Mata Uang Default** — Mata uang utama untuk harga dan akuntansi.
- **Multi-Mata Uang** — Aktifkan untuk memungkinkan pelanggan melihat harga dalam mata uang pilihan mereka dengan konversi otomatis menggunakan kurs real-time.

Konfigurasi mata uang tambahan di **Pengaturan > Pengaturan Toko > Mata Uang**.

## Pengaturan E-Commerce

### Checkout Tamu

Izinkan pembelian tanpa membuat akun:
- Alur checkout lebih cepat
- Hambatan lebih rendah untuk pembeli pertama
- Mengumpulkan data pelanggan lebih sedikit

### Waktu Pembuatan Akun

Kontrol kapan pelanggan diminta untuk membuat akun:

| Opsi | Deskripsi |
|--------|-------------|
| **Setelah Pembelian (Disarankan)** | Minta pembuatan akun setelah pesanan berhasil — memanfaatkan goodwill pasca-pembelian untuk konversi terbaik |
| **Selama Checkout** | Buat akun sebelum pembayaran diproses |
| **Sebelum Checkout** | Wajibkan akun sebelum berbelanja (tidak disarankan — mengurangi konversi) |

Anda juga dapat mengatur **Pesan Pembuatan Akun** kustom untuk menjelaskan manfaat pendaftaran.

### Default Inventaris

- **Lacak Inventaris** — Aktifkan pelacakan stok secara global
- **Ambang Stok Rendah** — Tingkat stok di mana peringatan stok rendah dikirim ke email admin (default: 10 unit)

### Kecerdasan Inventaris

![Kartu Kecerdasan Inventaris yang menunjukkan field Default Reorder Lead Time, Safety Stock Multiplier, Velocity Calculation Window, Allow Backorders by Default, dan Low Stock Alert Frequency](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Pengaturan ini menyesuaikan perhitungan reorder otomatis, stok pengaman, dan kecepatan penjualan, serta mengontrol bagaimana situasi stok habis dan stok rendah ditangani.

- **Default Reorder Lead Time (Hari)** — Berapa hari yang biasanya dibutuhkan untuk menerima restock dari pemasok Anda setelah Anda melakukan pesanan (default: 14).

Peramalan menggunakan ini untuk menandai produk yang perlu dipesan ulang *sekarang* untuk menghindari kekosongan stok sebelum stok baru tiba.
- **Pengali Stok Pengaman** — Bantalan yang diterapkan di atas permintaan yang diharapkan untuk menyerap lonjakan penjualan atau keterlambatan pemasok.

Sebagai contoh, pengali `1.5` membangun bantalan 50% di atas stok pengaman yang dihitung; `2.0` menggandakannya.

Naikkan ini untuk produk di mana kekosongan stok sangat merugikan (penjual terbaik, item musiman); turunkan untuk stok yang bergerak lambat yang tidak ingin Anda pesan berlebihan.
- **Jendela Perhitungan Kecepatan (Hari)** — Jendela tinjauan ke belakang yang digunakan Spwig untuk menghitung kecepatan penjualan setiap produk, yang pada gilirannya mendorong saran pemesanan ulang dan angka hari persediaan (default: 30).

Jendela yang lebih pendek bereaksi lebih cepat terhadap pergeseran permintaan terbaru; jendela yang lebih panjang meratakan lonjakan musiman sehingga satu minggu yang sibuk tidak akan mengacaukan peramalan.
- **Izinkan Pesanan Tertunda Secara Default** — Pengaturan pesanan tertunda awal yang diterapkan pada produk yang baru dibuat (nonaktif secara default).

Setiap produk masih dapat menimpanya secara individual di halaman produknya sendiri, dan produk yang sudah ada tetap mempertahankan pengaturan apa pun yang sudah mereka miliki — mengubah ini hanya mengubah default yang digunakan produk baru, tidak memperbarui katalog Anda secara retroaktif.
- **Frekuensi Peringatan Stok Rendah** — Seberapa sering aplikasi seluler Spwig Anda diberi tahu tentang stok rendah: **Waktu Nyata** mengirim notifikasi push sesaat setelah produk melampaui ambang batas stok rendahnya; **Ringkasan Harian** dan **Ringkasan Mingguan** sebaliknya mengirim satu notifikasi push yang merangkum semua produk stok rendah saat ini pada jadwal tersebut.

Pengaturan ini hanya berlaku saat **Peringatan Stok Rendah** (Pengaturan Email, di bawah) diaktifkan — dengan peringatan nonaktif, tidak ada notifikasi yang dikirim pada frekuensi apa pun.

### Dokumen & Penagihan

![Kartu Dokumen & Penagihan yang menunjukkan Nomor ID Pajak / PPN, Teks Footer Faktur, Teks Footer Slip Pengiriman, dan Lebar Logo Dokumen yang diisi dengan nilai contoh](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Bidang-bidang ini mengisi faktur dan slip pengiriman yang dihasilkan Spwig untuk pesanan — misalnya ketika pedagang mengunduh atau mengirim email faktur PDF, atau mencetak slip pengiriman untuk pengiriman.

- **Nomor ID Pajak / PPN** — Nomor identifikasi pajak bisnis Anda. Dicetak pada faktur yang dihasilkan agar memenuhi persyaratan dokumentasi pajak lokal.
- **Teks Footer Faktur** — Teks bebas yang ditampilkan di bagian bawah setiap faktur yang dihasilkan. Penggunaan umum: syarat pembayaran ("Pembayaran jatuh tempo dalam 30 hari"), pesan terima kasih, atau detail transfer bank.
- **Teks Footer Slip Pengiriman** — Teks bebas yang ditampilkan di bagian bawah setiap slip pengiriman yang dihasilkan. Penggunaan umum: instruksi pengembalian atau catatan untuk tim gudang/penyelenggaraan.
- **Lebar Logo Dokumen (px)** — Lebar logo toko Anda seperti yang muncul pada faktur PDF dan slip pengiriman yang dihasilkan (default: 200px). Tinggi diskalakan secara otomatis untuk menyesuaikan, sehingga proporsi logo Anda dipertahankan. Gambar logo itu sendiri berasal dari **Logo** Anda (Branding, di atas) — logo SVG tidak digambar pada dokumen PDF, jadi unggah versi PNG atau JPG dari logo Anda jika Anda menggunakan seni vektor di storefront.

## Pengaturan Email

Konfigurasi pengaturan pengiriman email di **Settings > Email Accounts** dan **Settings > Email Templates**. Lihat [Konfigurasi Email](/help/email-configuration) untuk detail lengkap.

Pengaturan email utama yang tersedia di Pengaturan Toko:

- **Email Konfirmasi Pesanan** — Aktifkan atau nonaktifkan email konfirmasi otomatis
- **Email Notifikasi Pengiriman** — Aktifkan atau nonaktifkan notifikasi pembaruan pengiriman
- **Peringatan Stok Rendah** — Kirim peringatan ke email admin ketika stok turun di bawah ambang batas
- **Mode Pengiriman Email** — Live (pengiriman normal), Paused (tahan semua email), atau Log Only (catat tetapi tidak pernah kirim)
- **Email Pengalihan Uji** — Alihkan semua email keluar ke satu alamat untuk pengujian

## Pengaturan Keamanan

### Autentikasi Dua Faktor (2FA)

Kendalikan apakah staf diwajibkan menggunakan autentikasi dua faktor:


{
  "Setting": "Penjelasan",
  "---------": "-------------",
  "**Optional**": "Staf dapat memilih untuk mengaktifkan 2FA tetapi tidak wajib",
  "**Recommended**": "Staf melihat pesan yang mendorong mereka untuk menyiapkan 2FA",
  "**Required**": "Staf tidak dapat mengakses admin hingga 2FA diaktifkan",
  "- **Grace Period (Days)**": "Jumlah hari staf memiliki waktu untuk menyiapkan 2FA setelah penerapan diaktifkan",
  "- **Allow Trusted Devices**": "Izinkan staf melewatkan verifikasi 2FA pada perangkat yang dikenali selama jumlah hari tertentu",
  "\n## Cookie Consent\n\nAtur banner persetujuan cookie yang ditampilkan kepada pengunjung toko:",
  "- **Cookie Consent Enabled**": "Tampilkan atau sembunyikan banner cookie",
  "- **Banner Position**": "Di mana banner muncul di layar (bagian bawah, kotak pop-up sudut, dll.)",
  "- **Consent Mode**": "Pernyataan sederhana, opt-in, atau opt-out",
  "- **Banner Title and Text**": "Judul dan deskripsi yang dapat disesuaikan ditampilkan kepada pengunjung",
  "- **Category Descriptions**": "Deskripsi terpisah untuk cookie analitik, pemasaran, dan fungsional",
  "\nSemua bidang teks banner mendukung terjemahan untuk toko berbahasa ganda.\n\n## Communications\n\nTab **Communications** mengontrol bagaimana toko Anda memperoleh, memverifikasi, dan memungkinkan pelanggan mengelola persetujuan untuk email pemasaran dan SMS. Pengaturan ini membentuk posisi kepatuhan hukum Anda (GDPR untuk email, TCPA untuk SMS), jadi tinjau dengan penasihat hukum Anda sebelum peluncuran — Spwig menyediakan kontrolnya, bukan nasihatnya.\n\n![Tab Communications menunjukkan Kartu Persetujuan Email Pemasaran, Preferensi & Unsubscribe, dan Persetujuan SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)\n\n### Persetujuan Email Pemasaran\n\n- **Aktifkan Double Opt-In untuk Email Pemasaran** - Ketika aktif, pelanggan yang berlangganan email pemasaran akan menerima email konfirmasi dan harus mengklik tautannya sebelum Spwig mengirimkan pesan pemasaran apa pun kepada mereka. Ketika dimatikan, mencantumkan kotak opt-in pemasaran cukup cukup. Secara default diaktifkan, sesuai dengan praktik terbaik GDPR.
- **Status Opt-In Pemasaran Default** - Status awal opt-in pemasaran yang diterapkan pada akun pelanggan yang baru dibuat. Secara default dimatikan (GDPR opt-out), jadi pelanggan baru mulai tidak berlangganan email pemasaran hingga mereka secara aktif berlangganan.
\nKetika double opt-in diaktifkan, pilihan masuk memicu email konfirmasi dengan tautan verifikasi. Sebelum pelanggan mengkliknya, mereka dicatat sebagai berlangganan tetapi belum diverifikasi, dan pengiriman pemasaran melewatinya — email transaksional (konfirmasi pesanan, pembaruan pengiriman, reset kata sandi) tidak pernah terpengaruh oleh pengaturan ini.
\n### Preferensi & Unsubscribe\n\n- **Aktifkan Pusat Preferensi Pelanggan** - Ketika diaktifkan, pelanggan dapat mengelola preferensi email dan SMS mereka dari halaman layanan mandiri yang terhubung dari dashboard akun mereka. Ketika dimatikan, halaman tersebut dan API pendukungnya mengembalikan tidak tersedia dan tautan dashboard dihilangkan. Tautan unsubscribe satu klik dalam email Anda tetap berjalan baik — celah ini diperlukan untuk kepatuhan dan tidak terpengaruh oleh pengaturan ini.
- **Kumpulkan Alasan Unsubscribe** - Ketika diaktifkan, halaman unsubscribe satu klik meminta pelanggan untuk memberikan alasan singkat sebelum mengonfirmasi: *Saya menerima terlalu banyak email*, *Isinya tidak relevan bagi saya*, *Saya tidak pernah mendaftar untuk ini*, *Saya tidak lagi tertarik*, atau *Lainnya*. Alasan yang dipilih pelanggan dicatat ke jejak audit persetujuan sehingga Anda dapat meninjau pola unsubscribe seiring waktu.
\n### Persetujuan SMS\n\n- **Wajibkan Verifikasi SMS** - Ketika diaktifkan (default), pelanggan harus memverifikasi nomor telepon mereka dengan kode satu kali sebelum Spwig mengirimkan SMS apa pun, termasuk teks pemasaran. Ketika dimatikan, mencantumkan kotak opt-in SMS cukup cukup. Default ini diubah menjadi **on** untuk keamanan TCPA — nonaktifkan hanya jika Anda memiliki langkah verifikasi lain dalam alur pendaftaran Anda.
\n## Mode Perawatan\n\nAktifkan mode perawatan untuk mengambil toko Anda keluar sementara:
- Menampilkan pesan perawatan kustom kepada pengunjung
- Anda dapat menghubungkan halaman **Mode Perawatan** yang dibuat di Page Builder untuk pengalaman perawatan yang sepenuhnya bermerk
- Membatasi akses hanya untuk pengguna admin
- Berguna selama pembaruan besar atau migrasi
}


# Media Sosial

Hubungkan profil media sosial toko Anda. Tampilkan di bagian bawah halaman dan template email:

- **URL Facebook**
- **URL Twitter**
- **URL Instagram**
- **URL LinkedIn**

## Pengaturan SEO Default

Atur tag meta default yang digunakan ketika halaman tidak memiliki pengaturan SEO sendiri:

- **Judul Meta** — Judul halaman default (maksimal 60 karakter)
- **Deskripsi Meta** — Deskripsi default yang ditampilkan di hasil pencarian (maksimal 160 karakter)
- **Kata Kunci Meta** — Kata kunci terpisah koma default

## Pengaturan Pajak

Atur pengumpulan pajak di **Pengaturan > Pengaturan Pajak**:

1. **Metode Perhitungan** — Berdasarkan alamat pengiriman, alamat tagihan, atau lokasi toko
2. **Tarif Pajak** — Tetapkan tarif berdasarkan wilayah dan kelas pajak produk
3. **Tampilan Harga Pajak** — Tampilkan harga termasuk pajak, tanpa pajak, atau keduanya

## Tips

- Atur zona waktu dengan benar sebelum memproses pesanan apa pun — hal ini memengaruhi semua timestamp dan laporan.
- Aktifkan checkout sebagai tamu untuk meningkatkan tingkat konversi.
- Isi alamat bisnis Anda untuk perhitungan pengiriman dan pajak yang akurat.
- Unggah logo dan favicon untuk pengalaman yang profesional dan bermerk.
- Gunakan **Waktu Pembuatan Akun Setelah Pembelian** untuk tingkat pendaftaran terbaik.
- Aktifkan pemeriksaan dua faktor untuk staf agar melindungi admin toko Anda.
- Uji alur email menggunakan pengaturan **Email Redirect Uji Coba** sebelum diluncurkan.
- Atur **Waktu Lead Pemesanan Default** sesuai dengan pemasok terlambat tercepat Anda — peramalan pemesanan menerapkan nilai tunggal ini di seluruh katalog Anda, jadi lebih baik mengambil produk dengan waktu terpanjang.
- Perpendek **Jendela Perhitungan Kecepatan** jika Anda sering melakukan promosi atau restok dan ingin peramalan merespons cepat terhadap penjualan beberapa hari terakhir; perpanjang jika Anda menginginkan pandangan yang stabil dan tidak mudah mengalami lonjakan permintaan.
- Jika Anda mengaktifkan **Izinkan Pesanan Tunda Secara Default**, ingat bahwa ini hanya menetapkan titik awal untuk produk yang dibuat *setelah* perubahan — kembalilah pada produk yang ada secara individual jika Anda ingin pesanan tunda diaktifkan di seluruh katalog Anda saat ini juga.
- Sesuaikan **Frekuensi Pemberitahuan Stok Rendah** sesuai seberapa aktif Anda mengelola stok: **Real-time** untuk katalog yang bergerak cepat di mana setiap risiko kehabisan stok perlu ditangani segera, **Ringkasan Harian** atau **Ringkasan Mingguan** untuk menghindari kelelahan pemberitahuan pada katalog yang lebih besar.
- Isi **ID Pajak / Nomor PPN** dan teks bagian bawah sebelum invoice pertama Anda yang sebenarnya dikirim ke pelanggan — kedua bidang ini kosong secara default.
- Jika **Logo** Anda berupa SVG, unggah versi PNG atau JPG juga — **Lebar Logo Dokumen** tidak berdampak pada PDF karena Spwig tidak dapat menggambar karya seni SVG pada faktur dan formulir pengiriman yang dibuat.
- Biarkan **Aktifkan Opt-In Ganda untuk Email Pemasaran** dalam keadaan aktif kecuali Anda memiliki alasan khusus untuk menonaktifkannya — ini adalah default yang lebih aman untuk GDPR dan melindungi reputasi pengirim Anda dengan menjaga alamat yang belum diverifikasi tetap di luar pengiriman pemasaran.
- Biarkan **Status Opt-In Pemasaran Default** dalam keadaan non-aktif. Mencentang opsi persetujuan pemasaran untuk akun baru melanggar persyaratan opt-in GDPR bahkan jika pelanggan bisa secara teknis menonaktifkannya.
- Jangan nonaktifkan **Aktifkan Pusat Preferensi Pelanggan** hanya untuk menyederhanakan antarmuka akun Anda — tanpa itu, pelanggan tetap bisa berhenti menerima satu jenis pesan, tetapi mereka kehilangan kemampuan untuk menyetel preferensi secara rinci (misalnya, tetap menerima pembaruan pengiriman tetapi menghilangkan surat kabar).
- Pertahankan **Wajib Verifikasi SMS** dalam keadaan aktif kecuali alur pendaftaran Anda sudah memverifikasi nomor telepon dengan cara lain (misalnya, login berbasis SMS) — pengaturan ini secara khusus dibuat untuk menjaga agar Anda tetap dalam aturan TCPA.

**Pertukaran mata uang tidak berfungsi:**
- Pastikan penyedia tingkat pertukaran Anda terhubung
- Periksa kredensial API di pengaturan tingkat pertukaran
- Coba perbarui tingkat pertukaran secara manual

**Email pemasaran tidak sampai pada pelanggan yang berlangganan:**
- Pastikan apakah **Aktifkan Opsi Dua untuk Email Pemasaran** diaktifkan — jika ya, pelanggan harus mengklik tautan konfirmasi dalam email verifikasi sebelum pemasaran dilanjutkan
- Minta pelanggan memeriksa email sampah/junk untuk email konfirmasi
- Pastikan preferensi pelanggan untuk berlangganan pemasaran tetap aktif — klik langganan ulang akan mengaktifkan kembali

**Pelanggan mengatakan mereka tidak dapat menemukan pusat preferensi:**
- Pastikan apakah **Aktifkan Pusat Preferensi Pelanggan** diaktifkan — ketika dimatikan, tautan dashboard disembunyikan dan halaman tidak tersedia secara desain
- Tautan berhenti berlangganan dalam email pemasaran selalu berfungsi terlepasai dari pengaturan ini, jadi tunjukkan pelanggan ke sana sebagai cadangan
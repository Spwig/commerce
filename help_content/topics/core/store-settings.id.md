---
title: Mengatur Pengaturan Toko
---

Pengaturan Toko adalah tempat pusat untuk mengatur identitas, lokalitas, merek, dan preferensi operasional toko Anda. Navigasi ke **Pengaturan > Pengaturan Toko** untuk memulai.

![Tab umum pengaturan toko](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Tab Umum

Tab **Umum** menyimpan pengaturan inti identitas toko Anda.

### Identitas Toko

- **Nama Toko** — nama tampilan yang ditampilkan di judul halaman, email, dan header admin.
- **Tagline** — deskripsi singkat toko Anda, digunakan dalam SEO dan berbagi media sosial.
- **URL Situs** — alamat web publik toko Anda. Digunakan dalam email, pembuatan peta situs, dan pembuatan tautan.

### Informasi Kontak

- **Email Kontak** — menerima pemberitahuan pesanan dan ditampilkan dalam komunikasi pelanggan.
- **Nomor Telepon** — nomor telepon pendukung opsional yang ditampilkan di bagian bawah halaman dan email.

### Alamat Bisnis

Masukkan alamat lengkap Anda (jalan, kota, propinsi, kode pos, negara). Ini digunakan untuk:
- perhitungan asal pengiriman
- perhitungan pajak
- kebutuhan hukum dan faktur

## Branding

### Logo

Unggah logo toko Anda (PNG atau SVG direkomendasikan, ~200x50px dengan latar belakang transparan). Logo muncul di:
- bagian header toko
- template email
- panel admin

### Favicon

Unggah favicon persegi (ICO atau PNG, 32x32px). Muncul sebagai:
- ikon tab browser
- ikon tanda bookmark
- ikon layar utama ponsel

## Lokalisasi

### Bahasa Default

Pilih bahasa utama toko Anda dari 10 opsi yang didukung:

| Bahasa | Kode |
|----------|------|
| Inggris | en |
| Spanyol | es |
| Prancis | fr |
| Jerman | de |
| Portugis | pt |
| Jepang | ja |
| Cina Sederhana | zh-hans |
| Cina Tradisional | zh-hant |
| Rusia | ru |
| Arab | ar |

Bahasa default mengontrol bahasa antarmuka admin dan cadangan untuk konten toko.

### Zona Waktu

Pilih zona waktu toko Anda untuk jam waktu pesanan yang akurat, promosi yang dijadwalkan, dan pelaporan.

### Mata Uang

- **Mata Uang Default** — mata uang utama untuk harga dan akuntansi.
- **Banyak Mata Uang** — aktifkan untuk memungkinkan pelanggan melihat harga dalam mata uang yang disukai dengan konversi otomatis menggunakan tingkat pertukaran real-time.

Atur mata uang tambahan di **Pengaturan > Pengaturan Toko > Mata Uang**.

## Pengaturan E-Commerce

### Pemesanan Langsung

izinkan pembelian tanpa membuat akun:
- alur checkout yang lebih cepat
- fraksi yang lebih rendah untuk pembeli pertama kali
- mengumpulkan data pelanggan yang lebih sedikit

### Waktu Pembuatan Akun

Atur kapan pelanggan diminta untuk membuat akun:

| Opsi | Deskripsi |
|--------|-------------|
| **Setelah Pembelian (Rekomendasikan)** | Minta pembuatan akun setelah pesanan berhasil — memanfaatkan kebaikan setelah pembelian untuk konversi terbaik |
| **Selama Checkout** | Buat akun sebelum pembayaran diproses |
| **Sebelum Checkout** | Wajibkan akun sebelum berbelanja (tidak direkomendasikan — mengurangi konversi) |

Anda juga dapat menyetel pesan **Pembuatan Akun** kustom untuk menjelaskan manfaat pendaftaran.

### Pengaturan Inventaris

- **Lacak Inventaris** — aktifkan pelacakan stok secara keseluruhan
- **Ambang Batas Stok Rendah** — tingkat stok di mana pemberitahuan stok rendah dikirim ke email admin (default: 10 unit)

## Intelegensi Inventaris

![Kartu Intelegensi Inventaris yang menunjukkan bidang Waktu Pemesanan Default dan Multiplier Stok Aman](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Pengaturan ini menyetel perhitungan penyetoran ulang otomatis, stok aman, dan kecepatan penjualan, serta mengontrol bagaimana situasi kehabisan stok dan stok rendah ditangani.

- **Waktu Pemesanan Default (Hari)** — berapa hari biasanya dibutuhkan untuk menerima stok kembali dari pemasok Anda setelah Anda memesan (default: 14).

Peramalan menggunakan ini untuk menandai produk yang perlu dipesan *sekarang* untuk menghindari kehabisan stok sebelum stok baru tiba.
- **Multiplier Stok Aman** — buffer yang diterapkan di atas permintaan yang diharapkan untuk menyerap lonjakan penjualan atau keterlambatan pemasok.

Contoh, faktor pengali `1.5` membangun buffer 50% di atas persediaan aman yang dihitung; `2.0` menggandakannya.

Tingkatkan ini untuk produk di mana kehabisan stok menjadi mahal (produk best seller, barang musiman); turunkan untuk stok yang tidak laku cepat yang tidak ingin Anda pesan berlebihan.
- **Jendela Perhitungan Kecepatan (Hari)** — Jangka waktu pengembalian yang digunakan Spwig untuk menghitung kecepatan penjualan setiap produk, yang pada gilirannya memengaruhi saran penyesuaian ulang dan angka hari persediaan (default: 30).

Jendela yang lebih pendek bereaksi lebih cepat terhadap perubahan permintaan terbaru; jendela yang lebih panjang meratakan lonjakan musiman sehingga satu minggu sibuk tidak mengacaukan prediksi.
- **Izinkan Pesanan Tunda Secara Default** — Pengaturan pesanan tunda awal yang diterapkan pada produk yang baru dibuat (mati secara default).

Setiap produk tetap dapat menggantinya secara individual di halaman produknya sendiri, dan produk yang sudah ada tetap memiliki pengaturan apa pun yang sudah mereka miliki — mengubah ini hanya mengubah default produk baru yang dimulai, tidak memperbarui katalog Anda secara retroaktif.
- **Frekuensi Pemberitahuan Stok Rendah** — Seberapa sering aplikasi seluler Spwig menerima pemberitahuan tentang stok rendah: **Real-time** mengirim notifikasi dorong segera ketika produk melewati ambang batas stok rendah; **Ringkasan Harian** dan **Ringkasan Mingguan** mengirimkan satu notifikasi dorong yang merangkum semua produk dengan stok rendah saat ini pada jadwal tersebut.

Pengaturan ini hanya berlaku saat **Pemberitahuan Stok Rendah** (Pengaturan Email, di bawah) diaktifkan — dengan notifikasi dimatikan, tidak ada notifikasi yang dikeluarkan pada frekuensi apa pun.

### Dokumen & Tagihan

![Kartu Dokumen & Tagihan menunjukkan bidang Tax ID / Nomor PPN, Teks Kaki Tagihan, dan Teks Kaki Surat Jalan yang diisi dengan nilai contoh](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Bidang-bidang ini mengisi faktur dan surat jalan yang Spwig buat untuk pesanan — misalnya ketika seorang penjual mengunduh atau mengirimkan faktur PDF melalui email, atau mencetak surat jalan untuk pengiriman.

- **Nomor ID Pajak / PPN** — Nomor identifikasi pajak usaha Anda. Cetak pada faktur yang dibuat sehingga memenuhi persyaratan dokumentasi pajak setempat.
- **Teks Kaki Faktur** — Teks bebas yang ditampilkan di bagian bawah setiap faktur yang dibuat. Penggunaan umum: ketentuan pembayaran ("Pembayaran jatuh tempo dalam 30 hari"), pesan terima kasih, atau detail transfer bank.
- **Teks Kaki Surat Jalan** — Teks bebas yang ditampilkan di bagian bawah setiap surat jalan yang dibuat. Penggunaan umum: instruksi pengembalian atau catatan untuk tim gudang/pengiriman.
- **Lebar Logo Dokumen (px)** — Lebar logo toko Anda seperti yang terlihat pada faktur dan surat jalan PDF yang dibuat (default: 200px). Tinggi secara otomatis menyesuaikan untuk mencocokkan, sehingga proporsi logo Anda dipertahankan. Gambar logo itu sendiri berasal dari **Logo** (Branding, di atas) — logo SVG tidak digambar pada dokumen PDF, jadi unggah versi PNG atau JPG dari logo Anda jika Anda menggunakan seni vektor di toko Anda.

## Pengaturan Email

Atur pengaturan pengiriman email di **Pengaturan > Akun Email** dan **Pengaturan > Template Email**. Lihat [Konfigurasi Email](/help/email-configuration) untuk detail lengkap.

Pengaturan email kunci yang tersedia di Pengaturan Toko:

- **Email Konfirmasi Pesanan** — Aktifkan atau nonaktifkan email konfirmasi otomatis
- **Email Pemberitahuan Pengiriman** — Aktifkan atau nonaktifkan pemberitahuan pembaruan pengiriman
- **Pemberitahuan Stok Rendah** — Kirim pemberitahuan ke email admin ketika stok turun di bawah ambang batas
- **Mode Pengiriman Email** — Live (pengiriman normal), Paused (menahan semua email), atau Log Only (mencatat tetapi tidak pernah mengirimkan)
- **Email Redirect Uji Coba** — Mengarahkan semua email yang keluar ke satu alamat untuk pengujian

## Pengaturan Keamanan

### Otonisasi Dua Faktor (2FA)

Atur apakah staf diwajibkan menggunakan otonisasi dua faktor:

| Pengaturan | Keterangan |
|---------|-------------|
| **Opsional** | Staf dapat memilih untuk mengaktifkan 2FA tetapi tidak diwajibkan |
| **Rekomendasi** | Staf melihat pesan yang mendorong mereka untuk mendaftarkan 2FA |
| **Wajib** | Staf tidak dapat mengakses admin hingga 2FA diaktifkan |

Simpan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- **Masa Tenang (Hari)** — Berapa hari staf memiliki waktu untuk menyiapkan 2FA setelah penerapan diaktifkan
- **Izinkan Perangkat Tepercaya** — Izinkan staf melewatkan verifikasi 2FA pada perangkat yang dikenali selama jumlah hari yang ditentukan

## Persetujuan Cookie

Atur banner persetujuan cookie yang ditampilkan kepada pengunjung toko:

- **Persetujuan Cookie Diaktifkan** — Tampilkan atau sembunyikan banner cookie
- **Posisi Banner** — Di mana banner muncul di layar (bilah bawah, popup sudut, dll.)
- **Mode Persetujuan** — Pemberitahuan sederhana, opt-in, atau opt-out
- **Judul dan Teks Banner** — Judul dan deskripsi yang dapat disesuaikan yang ditampilkan kepada pengunjung
- **Deskripsi Kategori** — Deskripsi terpisah untuk cookie analitik, pemasaran, dan fungsional

Semua bidang teks banner mendukung terjemahan untuk toko berbahasa ganda.

## Komunikasi

Tab **Komunikasi** mengontrol bagaimana toko Anda memperoleh, memverifikasi, dan memungkinkan pelanggan mengelola persetujuan untuk email pemasaran dan SMS. Pengaturan ini membentuk posisi kepatuhan hukum Anda (GDPR untuk email, TCPA untuk SMS), jadi tinjau dengan penasihat hukum Anda sebelum peluncuran — Spwig menyediakan kontrolnya, bukan nasihatnya.

![Tab Komunikasi yang menunjukkan Kartu Persetujuan Email Pemasaran, Preferensi & Pembatalan Langganan, dan Kartu Persetujuan SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Persetujuan Email Pemasaran

- **Aktifkan Double Opt-In untuk Email Pemasaran** — Ketika diaktifkan, pelanggan yang berlangganan email pemasaran akan menerima email konfirmasi dan harus mengklik tautan di dalamnya sebelum Spwig mengirimkan pesan pemasaran apa pun kepada mereka. Ketika dimatikan, mencantumkan kotak centang penerimaan pemasaran sudah cukup. Secara default diaktifkan, sesuai dengan praktik terbaik GDPR.
- **Status Penerimaan Pemasaran Default** — Status penerimaan pemasaran awal yang diterapkan pada akun pelanggan yang baru dibuat. Secara default dimatikan (GDPR opt-out), jadi pelanggan baru mulai tidak berlangganan email pemasaran hingga mereka secara aktif berlangganan.

Saat double opt-in diaktifkan, pendaftaran berlangganan memicu email konfirmasi dengan tautan verifikasi. Sebelum pelanggan mengkliknya, mereka dicatat sebagai berlangganan tetapi belum diverifikasi, dan pengiriman pemasaran melewatinya — email transaksional (konfirmasi pesanan, pembaruan pengiriman, reset kata sandi) tidak pernah terpengaruh oleh pengaturan ini.

### Preferensi & Pembatalan Langganan

- **Aktifkan Pusat Preferensi Pelanggan** — Ketika diaktifkan, pelanggan dapat mengelola preferensi email dan SMS mereka dari halaman layanan mandiri yang terhubung dari dashboard akun mereka. Ketika dimatikan, halaman tersebut dan API pendukungnya akan tidak tersedia dan tautan dashboard-nya disembunyikan. Tautan pembatalan langganan satu-klik di email Anda tetap berjalan baik — celah ini diperlukan untuk kepatuhan dan tidak terpengaruh oleh pengaturan ini.
- **Kumpulkan Alasan Pembatalan Langganan** — Ketika diaktifkan, halaman pembatalan langganan satu-klik meminta pelanggan untuk memberikan alasan singkat sebelum mengonfirmasi: *Saya menerima terlalu banyak email*, *Isinya tidak relevan bagi saya*, *Saya tidak pernah mendaftar untuk ini*, *Saya tidak lagi tertarik*, atau *Lainnya*. Alasan yang dipilih pelanggan dicatat ke jejak audit persetujuan sehingga Anda dapat meninjau pola pembatalan langganan seiring waktu.

### Persetujuan SMS

- **Wajibkan Verifikasi SMS** — Ketika diaktifkan (default), pelanggan harus memverifikasi nomor ponsel mereka dengan kode satu kali sebelum Spwig mengirimkan SMS apa pun, termasuk pesan pemasaran. Ketika dimatikan, mencantumkan kotak centang penerimaan SMS sudah cukup untuk memulai pengiriman. Default ini diubah menjadi **diaktifkan** untuk keamanan TCPA — nonaktifkan hanya jika Anda memiliki langkah verifikasi lain dalam alur pendaftaran Anda.

## Mode Perawatan

Aktifkan mode perawatan untuk menonaktifkan toko Anda sementara:
- Menampilkan pesan perawatan kustom kepada pengunjung
- Anda dapat menghubungkan halaman **Mode Perawatan** yang dibuat di Page Builder untuk pengalaman merek penuh
- Membatasi akses hanya untuk pengguna admin
- Berguna selama pembaruan besar atau migrasi

## Media Sosial

Hubungkan profil media sosial toko Anda. Mereka muncul di bagian bawah dan template email:

- **URL Facebook**
- **URL Twitter**
- **URL Instagram**
- **URL LinkedIn**

## Default SEO

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

Atur tag meta default yang digunakan ketika halaman tidak memiliki pengaturan SEO mereka sendiri:

- **Judul Meta** — Judul halaman default (maksimal 60 karakter)
- **Deskripsi Meta** — Deskripsi default yang ditampilkan dalam hasil pencarian (maksimal 160 karakter)
- **Kata Kunci Meta** — Kata kunci yang ditentukan secara terpisah oleh koma

## Pengaturan Pajak

Atur pengumpulan pajak di **Pengaturan > Pengaturan Pajak**:

1. **Metode Perhitungan** — Berdasarkan alamat pengiriman, alamat tagihan, atau lokasi toko
2. **Tarif Pajak** — Tentukan tarif berdasarkan wilayah dan kelas pajak produk
3. **Tampilan Pajak** — Tampilkan harga dengan pajak, tanpa pajak, atau keduanya

## Tips

- Atur zona waktu Anda dengan benar sebelum memproses pesanan apa pun — ini memengaruhi semua timestamp dan laporan.
- Aktifkan checkout sebagai tamu untuk meningkatkan tingkat konversi.
- Isi alamat bisnis Anda untuk perhitungan pengiriman dan pajak yang akurat.
- Unggah logo dan favicon untuk pengalaman yang profesional dan bermerk.
- Gunakan **Waktu Pendaftaran Akun Setelah Pembelian** untuk tingkat pendaftaran terbaik.
- Aktifkan pemeriksaan dua faktor untuk staf agar melindungi admin toko Anda.
- Uji alur email menggunakan pengaturan **Email Redirect Uji Coba** sebelum diluncurkan.
- Atur **Waktu Pemesanan Ulang Standar** untuk mencocokkan pemasok terlambat tercepat Anda — peramalan pemesanan mengaplikasikan nilai tunggal ini di seluruh katalog Anda, jadi lebih baik mengambil produk dengan waktu terpanjang.
- Isi **ID Pajak / Nomor PPN** dan teks footer sebelum invoice nyata pertama Anda pergi ke pelanggan — kedua bidang ini kosong secara default.
- Biarkan **Aktifkan Opt-In Ganda untuk Email Pemasaran** aktif kecuali Anda memiliki alasan khusus untuk menonaktifkannya — ini adalah default yang lebih aman untuk GDPR dan melindungi reputasi pengirim Anda dengan menjaga alamat yang tidak diverifikasi dari email pemasaran Anda.
- Biarkan **Status Opt-In Pemasaran Standar** dimatikan. Pemeriksaan pra-persetujuan untuk konsesi pemasaran merusak persyaratan opt-in GDPR bahkan jika pelanggan bisa secara teknis menonaktifkannya.
- Jangan nonaktifkan **Aktifkan Pusat Preferensi Pelanggan** hanya untuk menyederhanakan antarmuka akun Anda — tanpa itu, pelanggan tetap bisa berhenti berlangganan dari satu jenis pesan, tetapi mereka kehilangan kemampuan untuk menyetel preferensi secara rinci (misalnya, tetapkan pembaruan pengiriman tetapi hapus surat kabar).
- Pertahankan **Wajib Verifikasi SMS** aktif kecuali alur pendaftaran Anda sudah memverifikasi nomor telepon dengan cara lain (misalnya, login berbasis SMS) — pengaturan ini ada secara khusus untuk menjaga Anda tetap dalam aturan TCPA.

## Pemecahan Masalah

**Perubahan tidak muncul di toko:**
- Bersihkan cache browser Anda
- Jalankan pembersihan cache dari panel admin
- Periksa apakah mode perawatan secara tidak sengaja diaktifkan

**Email tidak terkirim:**
- Pastikan pengaturan penyedia email Anda di Email Configuration
- Pastikan **Mode Pengiriman Email** diatur ke **Hidup**
- Pastikan **Email Redirect Uji Coba** kosong jika Anda ingin email dikirim ke penerima nyata

**Konversi mata uang tidak berfungsi:**
- Pastikan penyedia tingkat tukar Anda terhubung
- Periksa kredensial API di pengaturan tingkat tukar
- Coba perbarui tingkat tukar secara manual

**Email pemasaran tidak sampai pada pelanggan yang sudah menyetujui:**
- Periksa apakah **Aktifkan Opt-In Ganda untuk Email Pemasaran** aktif — jika ya, pelanggan harus mengklik tautan konfirmasi dalam email verifikasi sebelum pengiriman pemasaran dilanjutkan
- Minta pelanggan memeriksa spam/junk untuk email verifikasi
- Pastikan preferensi opt-in pemasaran pelanggan masih aktif — klik berhenti berlangganan mengembalikan keadaan mati

**Pelanggan mengatakan mereka tidak dapat menemukan pusat preferensi:**
- Pastikan **Aktifkan Pusat Preferensi Pelanggan** aktif — ketika dimatikan, tautan antarmuka pengguna disembunyikan dan halaman tidak tersedia secara desain
- Tautan berhenti berlangganan dalam email pemasaran apa pun selalu berfungsi terlepasai dari pengaturan ini, jadi tunjukkan pelanggan ke sana sebagai cadangan
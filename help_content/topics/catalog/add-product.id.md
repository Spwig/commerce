---
title: Menambahkan Produk
---

Berikut adalah bagian 1 dari 4 dari dokumen yang lebih panjang.

<!-- screenshots-needed:
- url: /admin/catalog/product/<id>/change/
  filename: inventory-tab.webp
  description: Tab Inventaris, digulung untuk menunjukkan kartu Atribut Fisik, Pengiriman,
    dan Pesanan Awal secara bersamaan (Pengiriman yang Dibutuhkan dicentang, Kemasan Pengiriman
    Utama dipilih, dan Apakah Pesanan Awal dicentang dengan tanggal rilis dan pesan
    yang diisi, sehingga semua bidang baru terlihat dalam satu tampilan).
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
  notes: Menggantikan inventory-tab.webp yang lama, yang sudah lama sebelum kartu Pengiriman
    dan Pesanan Awal, dan sekarang tidak lagi sesuai dengan formulir yang sedang berjalan.
- url: /admin/catalog/product/<id>/change/
  filename: tags-card.webp
  description: Tab Informasi Dasar, digulung ke kartu Tag, dengan beberapa tag
    yang sudah diterapkan pada produk di pemilih tag.
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
- url: /admin/catalog/product/<id>/change/
  filename: advanced-tab.webp
  description: Tab Lanjutan menunjukkan kartu Pengaturan Halaman Produk (dropdown Template Halaman
    dengan opsi yang tidak default dipilih) dan kartu Detail Teknis
    di bawahnya.
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
-->

Panduan ini memandu Anda melalui pembuatan produk baru di toko Anda. Formulir produk ini diatur dalam bagian-bagian yang mencakup informasi dasar, media, harga, inventaris, SEO, dan lainnya — sehingga Anda dapat mengisi semuanya sekaligus atau kembali untuk menyelesaikan bagian-bagian lainnya nanti.

## Mulai dari awal

Dari bilah sisi, navigasikan ke **Produk > Semua Produk** untuk melihat katalog produk Anda. Klik tombol **+ Tambahkan Produk** di bagian kanan atas untuk membuka formulir pembuatan produk.

![Halaman daftar produk](/static/core/admin/img/help/add-product/product-list-page.webp)

## Informasi dasar

Bagian **Informasi Dasar** adalah tempat Anda menentukan identitas inti produk Anda.

![Formulir tambah produk](/static/core/admin/img/help/add-product/add-product-form.webp)

### Kolom wajib

- **Nama** — Nama produk yang ditampilkan kepada pelanggan. Klik ikon globe untuk menambahkan terjemahan untuk bahasa lainnya.
- **Slug** — Versi URL yang ramah (otomatis dibuat). Sesuaikan jika diperlukan.
- **SKU** — Kode unit pengelolaan stok internal Anda.
- **Jenis Produk** — Pilih dari: Sederhana, Variabel, Digital, Kemasan, Kartu Hadiah, Dapat Disesuaikan, Dapat Disesuaikan, atau Pemesanan.
- **Kategori** — Tetapkan produk ke kategori untuk pengorganisasian dan navigasi toko.

### Status dan visibilitas

Ditemukan di bagian **Status** di bagian bawah formulir:

- **Status** — Atur menjadi **Draf** saat bekerja, **Diterbitkan** ketika siap dijual, atau **Dihentikan** untuk produk yang tidak lagi Anda tawarkan.
- **Apakah Disarankan** — Centang untuk menonjolkan produk ini di toko Anda.
- **Apakah Produk Digital** — Centang jika produk ini mencakup unduhan digital (file, lisensi). Bisa digabungkan dengan jenis produk apa pun.
- **Sembunyikan dari Toko** — Menyembunyikan produk dari daftar katalog sambil tetap menjaganya tersedia sebagai opsi konfigurasi atau komponen kemasan.

### Kolom opsional

- **Merek** — Hubungkan dengan merek jika berlaku.
- **Tag** — Tetapkan satu atau lebih tag di kartu **Tag** di bagian bawah tab ini. Tag berbeda dari Kumpulan — mereka adalah label bebas bentuk untuk mengatur dan memfilter produk, bukan kelompok merchandising. Mulai mengetik untuk mencari tag yang sudah ada, atau ketik nama baru untuk membuatnya secara langsung. Lihat topik bantuan **Tag Produk** untuk membuat, mengganti nama, dan menghapus tag secara massal secara langsung.

### Deskripsi produk

- **Keterangan Singkat** — Tampil di daftar produk dan kartu. Jaga agar singkat dan menarik.
- **Deskripsi Lengkap** — Deskripsi produk yang rinci ditampilkan di halaman detail produk. Gunakan editor teks kaya untuk menambahkan format, gambar, video, dan tabel.

Kedua bidang deskripsi ini mendukung fitur terjemahan — klik ikon globe untuk memberikan konten dalam bahasa lain.

### Fitur dan spesifikasi

Bagian **Detail Produk** mencakup dua bidang data terstruktur:

- **Fitur** — Pasangan kunci-nilai untuk penekanan produk (misalnya, "Jangka Hidup Baterai: 20 jam).
- **Spesifikasi** — Detail teknis untuk tab spesifikasi di halaman produk (misalnya, "Prosesor: Intel i7").

## Media

Bagian **Media** memungkinkan Anda mengelola gambar produk menggunakan Perpustakaan Media yang terintegrasi.

![Tab Media](/static/core/admin/img/help/add-product/media-tab.webp)

1. Klik **+ Tambahkan Gambar dari Perpustakaan Media** untuk membuka pemilih media.
2. Pilih gambar yang sudah ada atau unggah yang baru secara langsung.
3. Seret gambar untuk mengurutkanya — gambar **pertama** menjadi gambar produk utama yang ditampilkan dalam daftar dan kartu.

Bidang **Jenis Galeri**, dalam kartu **Pengaturan Galeri** di bawah daftar gambar, mengontrol bagaimana gambar ditampilkan di toko: Galeri Standar, Carousel, Tata Letak Grid, Galeri Zoom, atau Tampilan 360°.

## Harga

Atur harga produk Anda dan konfigurasikan penjualan.

![Tab Harga](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Harga biasa

- **Harga Biasa** — Harga ritel standar yang akan dilihat pelanggan. Mata uang ditetapkan bersamaan dengan jumlah harga.
- **Biaya** — Biaya barang Anda, digunakan untuk perhitungan laba. Ini tidak pernah ditampilkan kepada pelanggan.

### Pengaturan diskon

Atur diskon sementara:

- **Jenis Penjualan** — Pilih dari: Tidak Ada Penjualan, Harga Jual Tetap, Jumlah Diskon, atau Persentase Diskon.
- **Nilai Penjualan** — Jumlah diskon atau persentase.
- **Tanggal Mulai Penjualan / Tanggal Berakhir Penjualan** — Jadwalkan kapan penjualan aktif dan berakhir. Biarkan kosong untuk mulai segera atau tidak ada tanggal berakhir.

### Penetapan harga multi-mata uang

Jika multi-mata uang diaktifkan di toko Anda, bidang **Strategi Harga** muncul:

- **Penetapan Harga Dinamis** — Harga dalam mata uang lain dihitung secara otomatis menggunakan tingkat pertukaran yang Anda konfigurasi.
- **Penetapan Harga Tetap** — Tetapkan harga spesifik untuk setiap mata uang secara terpisah menggunakan bagian **Penetapan Harga Multi-Mata Uang** yang muncul di bawahnya.

## Persediaan

Kelola tingkat persediaan, perilaku pengiriman, dan atribut produk fisik.

![Tab Persediaan](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Pengelolaan persediaan

- **Lacak Persediaan** — Aktifkan untuk melacak jumlah persediaan (aktif secara default).
- **Ambang Batas Persediaan Rendah** — Terima peringatan ketika persediaan turun di bawah angka ini (default: 5).
- **Izinkan Pemesanan Ulang** — Aktifkan untuk menerima pesanan bahkan ketika kehabisan stok.
- **Tindakan Kehabisan Stok** — Menimpa perilaku situs atau kategori ketika produk ini kehabisan stok: sembunyikan, tampilkan sebagai tidak tersedia, tampilkan tombol "Beritahu Saya", atau izinkan pemesanan ulang.

Jumlah persediaan dikelola per gudang. Setelah menyimpan produk, gunakan bagian **Barang Persediaan** di bagian bawah formulir (atau navigasi ke **Produk > Barang Persediaan**) untuk menetapkan jumlah di setiap lokasi gudang.

### Atribut fisik

Masukkan berat produk (kg) dan dimensi (panjang, lebar, tinggi dalam cm) untuk perhitungan pengiriman yang akurat.

### Pengiriman

- **Membutuhkan Pengiriman** — Apakah produk ini perlu dikirimkan ke pelanggan. Aktif secara default untuk produk fisik; toko Anda dan checkout menggunakannya untuk memutuskan apakah mengumpulkan alamat pengiriman dan menawarkan ongkos kirim untuk pesanan. Spwig secara otomatis menonaktifkannya untuk produk Digital, Pemesanan, dan Kartu Hadiah, karena produk-produk ini tidak per maih dikirimkan — Anda tidak perlu (dan tidak bisa) mengaktifkannya kembali untuk jenis produk tersebut. Biarkan dicentang untuk produk fisik yang tampaknya mirip digital, seperti kartu hadiah dicetak yang dikirim dalam kotak.
- **Kemasan Pengiriman yang Disukai** — Pilih salah satu kemasan pengiriman yang telah dikonfigurasi secara opsional. Ketika diatur, dimensi kemasan sendiri digunakan untuk perhitungan tarif pengiriman alih-alih berat dan dimensi produk di atas — berguna ketika produk selalu dikirim dalam kotak atau amplop standar yang sama. Biarkan kosong untuk menggunakan atribut fisik produk sendiri. Kelola kemasan yang tersedia di bawah **Pengiriman > Kemasan**.

### Pemesanan terlebih dahulu

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

Gunakan kartu **Pre-order** untuk menjual produk sebelum memiliki stok — berguna untuk rilisan mendatang yang ingin Anda mulai menerima pesanan sebelum peluncuran:

- **Apakah Pre-order** — Aktifkan untuk memungkinkan pelanggan membeli produk ini meskipun sedang habis stok.
- **Tanggal Rilis Pre-order** — Tanggal ketersediaan yang diharapkan, ditampilkan kepada pelanggan.
- **Pesan Pre-order** — Pesan singkat yang ditampilkan kepada pelanggan, maksimal 200 karakter (misalnya, "Dikirim Maret 2026").

### Identifikasi Produk

Kode produk standar untuk daftar pasar dan sistem inventaris:

- **GTIN** — Nomor Barang Perdagangan Global
- **EAN** — Nomor Artikel Eropa
- **UPC** — Kode Produk Universal (AS)
- **ISBN** — Untuk buku-buku
- **ASIN** — Identifikasi Amazon
- **MPN** — Nomor Bagian Pabrikan

### Pengiriman Internasional / Pabean

Dibutuhkan untuk pengiriman internasional (kembangkan bagian **Pengiriman Internasional / Pabean**):

- **Kode HS** — Kode klasifikasi Sistem Harmonisasi
- **Negara Asal** — Di mana produk tersebut diproduksi
- **Harga Unit Pabean** — Nilai yang dinyatakan per unit untuk pabean
- **Nomor Izin Ekspor** — Dibutuhkan hanya untuk barang yang dikendalikan atau dibatasi
- **Tanggal Kedaluarsaan Izin Ekspor** — Tanggal kedaluarsa izin ekspor

## SEO

Optimalkan visibilitas produk Anda di mesin pencari.

![Tab SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Judul Meta** — Judul yang ditampilkan dalam hasil pencarian mesin pencari. Klik ikon dunia untuk menerjemahkan.
- **Deskripsi Meta** — Deskripsi ringkas untuk hasil pencarian (maksimal 160 karakter). Klik ikon dunia untuk menerjemahkan.
- **Buat SEO Otomatis** — Centang untuk secara otomatis membuat konten SEO ketika produk disimpan.

Pratinjau **Hasil Pencarian** secara langsung menunjukkan bagaimana produk Anda akan terlihat dalam hasil pencarian Google.

## Pengaturan Halaman Produk

Pada tab **Lanjutan**, kartu **Pengaturan Halaman Produk** memungkinkan Anda mengontrol bagaimana tampilan halaman toko produk ini:

- **Template Halaman** — Menimpa tata letak halaman produk situs default untuk produk ini: Klasik, Lebar Penuh, Fokus Galeri, atau Digital. Biarkan setel ke **Gunakan Tata Letak Situs Default** untuk mewarisi tata letak apa pun yang ditentukan oleh pengaturan Desain — sebagian besar produk sebaiknya tetap pada default agar perubahan template di sana berlaku secara otomatis.
- **Tampilkan Produk Terkait** — Menampilkan produk terkait di bagian bawah halaman.
- **Tampilkan Ulasan** — Menampilkan ulasan pelanggan.
- **Tampilkan Spesifikasi** — Menampilkan tab spesifikasi.

Bidang **Jenis Galeri** — yang mengontrol bagaimana gambar produk ditampilkan (Galeri Standar, Carousel, Tata Letak Grid, Galeri Zoom, atau Tampilan 360°) — diatur secara terpisah, pada tab **Media**.

## Saluran Penjualan

Bidang **Saluran Penjualan** (di bagian Status) mengontrol di mana produk dapat dijual:

- **Semua Saluran** — Tersedia secara online dan di toko (POS).
- **Hanya Online** — Tidak tersedia melalui terminal POS.
- **Hanya Di Toko** — Tidak terdaftar secara online; hanya tersedia di toko fisik Anda.

Bidang **Barcode** juga tersedia untuk pemindaian barcode POS.

## Menyimpan Produk Anda

Ketika Anda siap, gunakan tombol simpan di sudut kanan atas. Produk Anda akan terlihat di toko setelah statusnya diatur menjadi **Terbitkan**.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Mulai dengan status **Draft** sehingga Anda dapat menyempurnakan produk sebelum pelanggan melihatnya.
- Unggah beberapa gambar — produk dengan beberapa foto cenderung lebih baik dalam konversi.
- Isi bidang **SEO** untuk meningkatkan daya temu di mesin pencari.
- Gunakan **Kategori**, **Merek**, dan **Tag** untuk membantu pelanggan menelusuri katalog Anda.
- Untuk produk yang berubah (misalnya, ukuran atau warna berbeda), pilih jenis **Produk Variabel** dan tambahkan variasinya setelah menyimpan.
- Gunakan **Fitur** dan **Spesifikasi** untuk menambahkan data produk yang terstruktur yang ditampilkan dalam tab khusus di halaman produk.
- Jika **Membutuhkan Pengiriman** tidak tetap dicentang, lihat **Jenis Produk** — Spwig menonaktifkan pengiriman secara otomatis untuk produk Digital, Pemesanan, dan Kartu Hadiah, karena ketiga jenis produk tersebut tidak pernah dikirimkan secara fisik.
- Tetapkan **Kemasan Pengiriman Favorit** untuk produk yang selalu dikirim dalam kotak yang sama — ini menghemat waktu Anda dari harus menjaga kesejajaran berat dan dimensi produk tersebut dengan kotak yang sebenarnya digunakan.
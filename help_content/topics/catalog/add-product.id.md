---
title: Menambahkan Produk
---

Panduan ini akan memandu Anda dalam membuat produk baru di toko Anda. Formulir produk diatur ke dalam bagian-bagian yang mencakup informasi dasar, media, harga, inventaris, SEO, dan lainnya — sehingga Anda dapat mengisi semuanya sekaligus atau kembali nanti untuk melengkapi bagian-bagian tersebut.

## Memulai

Dari bilah sisi, navigasikan ke **Products > All Products** untuk melihat katalog produk Anda. Klik tombol **+ Add Product** di sudut kanan atas untuk membuka formulir pembuatan produk.

![Product list page](/static/core/admin/img/help/add-product/product-list-page.webp)

## Informasi dasar

Bagian **Basic Information** adalah tempat Anda mendefinisikan identitas inti produk Anda.

![Add product form](/static/core/admin/img/help/add-product/add-product-form.webp)

### Field wajib

- **Name** — Nama produk yang ditampilkan kepada pelanggan. Klik ikon globe untuk menambahkan terjemahan untuk bahasa lain.
- **Slug** — Versi nama yang ramah URL (dibuat otomatis). Sesuaikan jika diperlukan.
- **SKU** — Kode unit penyimpanan stok internal Anda.
- **Product Type** — Pilih dari: Simple, Variable, Digital, Bundle, Gift Card, Customizable, Configurable, atau Booking.
- **Category** — Tetapkan produk ke kategori untuk organisasi dan navigasi storefront.

### Status dan visibilitas

Ditemukan di bagian **Status** di bagian bawah formulir:

- **Status** — Atur ke **Draft** saat bekerja, **Published** saat siap dijual, atau **Discontinued** untuk produk yang tidak lagi Anda tawarkan.
- **Is Featured** — Centang untuk menyorot produk ini di storefront Anda.
- **Is Digital Product** — Centang jika produk ini mencakup unduhan digital (file, lisensi). Dapat dikombinasikan dengan jenis produk apa pun.
- **Hide from Storefront** — Menyembunyikan produk dari daftar katalog sambil tetap menjadikannya tersedia sebagai opsi konfigurator atau komponen bundle.

### Field opsional

- **Brand** — Kaitkan dengan merek jika berlaku.
- **Tags** — Tetapkan satu atau lebih tag di kartu **Tags** lebih jauh di tab ini. Tag berbeda dari Collections — mereka adalah label bebas bentuk yang cepat untuk mengorganisasi dan memfilter produk, bukan pengelompokan merchandising. Mulai mengetik untuk mencari tag yang sudah ada, atau ketik nama baru untuk membuatnya secara langsung. Lihat topik bantuan **Product Tags** untuk membuat, mengubah nama, dan menghapus tag secara massal secara langsung.

![The Tags card on the Basic Info tab, with two tags applied in the tag picker](/static/core/admin/img/help/add-product/tags-card.webp)

### Deskripsi produk

- **Short Description** — Muncul dalam daftar produk dan kartu. Jaga agar singkat dan menarik.
- **Full Description** — Deskripsi produk terperinci yang ditampilkan di halaman detail produk. Gunakan editor teks kaya untuk menambahkan format, gambar, video, dan tabel.

Kedua field deskripsi mendukung fitur terjemahan — klik ikon globe untuk menyediakan konten dalam bahasa lain.

### Fitur dan spesifikasi

Bagian **Product Details** berisi dua field data terstruktur:

- **Features** — Pasangan kunci-nilai untuk sorotan produk (misalnya, "Battery Life: 20 hours").
- **Specifications** — Detail teknis untuk tab spesifikasi di halaman produk (misalnya, "Processor: Intel i7").

## Media

Bagian **Media** memungkinkan Anda mengelola gambar produk menggunakan Media Library terintegrasi.

![Media tab](/static/core/admin/img/help/add-product/media-tab.webp)

1. Klik **+ Add Images from Media Library** untuk membuka pemilih media.
2. Pilih gambar yang sudah ada atau unggah yang baru secara langsung.
3. Seret gambar untuk mengubah urutan mereka — **gambar pertama** menjadi gambar produk utama yang ditampilkan dalam daftar dan kartu.

Field **Gallery Type**, di kartu **Gallery Settings** di bawah daftar gambar, mengontrol bagaimana gambar ditampilkan di storefront: Standard Gallery, Carousel, Grid Layout, Zoom Gallery, atau 360° View.

## Harga

Atur harga produk Anda dan konfigurasikan penjualan.

![Pricing tab](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Harga reguler

- **Regular Price** — Harga ritel standar yang akan dilihat pelanggan.

Mata uang diatur bersamaan dengan jumlah harga.
- **Biaya** — Biaya barang Anda, digunakan untuk perhitungan laba.

Hal ini tidak pernah ditampilkan kepada pelanggan.

### Pengaturan penjualan

Konfigurasikan diskon sementara:

- **Jenis Penjualan** — Pilih dari: Tidak Ada Penjualan, Harga Penjualan Tetap, Potongan Nominal, atau Potongan Persentase.
- **Nilai Penjualan** — Jumlah atau persentase diskon.
- **Tanggal Mulai Penjualan / Tanggal Akhir Penjualan** — Jadwalkan kapan penjualan diaktifkan dan kedaluwarsa. Kosongkan untuk mulai segera atau tanpa tanggal akhir.

### Penetapan harga multi-mata uang

Jika multi-mata uang diaktifkan di toko Anda, bidang **Strategi Penetapan Harga** akan muncul:

- **Penetapan Harga Dinamis** — Harga dalam mata uang lain dihitung secara otomatis menggunakan kurs yang Anda konfigurasikan.
- **Penetapan Harga Tetap** — Tetapkan harga spesifik untuk setiap mata uang secara independen menggunakan bagian **Penetapan Harga Multi-Mata Uang** yang muncul di bawah.

## Inventaris

Kelola tingkat stok, perilaku pengiriman, dan atribut produk fisik.

![Tab Inventaris](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Manajemen stok

- **Lacak Inventaris** — Aktifkan untuk melacak kuantitas stok (diaktifkan secara default).
- **Ambang Stok Rendah** — Dapatkan peringatan ketika stok turun di bawah angka ini (default: 5).
- **Izinkan Backorder** — Aktifkan untuk menerima pesanan bahkan ketika stok habis. Produk baru dimulai dengan nilai **Izinkan Backorder Secara Default** dari **Pengaturan > Pengaturan Toko > Komersial**, tetapi Anda dapat menimpanya per produk di sini kapan saja.
- **Tindakan Stok Habis** — Timpa perilaku situs-wide atau kategori ketika produk ini habis: sembunyikan, tampilkan sebagai tidak tersedia, tampilkan tombol "Beri Tahu Saya", atau izinkan backorder.

Kuantitas stok dikelola per gudang. Setelah menyimpan produk, gunakan bagian **Item Stok** di bagian bawah formulir (atau navigasi ke **Produk > Item Stok**) untuk mengatur kuantitas di setiap lokasi gudang.

### Atribut fisik

Masukkan berat produk (kg) dan dimensi (panjang, lebar, tinggi dalam cm) untuk perhitungan pengiriman yang akurat.

### Pengiriman

- **Membutuhkan Pengiriman** — Apakah produk ini perlu dikirim ke pelanggan. Diaktifkan secara default untuk produk fisik; storefront dan checkout Anda menggunakannya untuk memutuskan apakah akan mengumpulkan alamat pengiriman dan mengutip biaya pos untuk pesanan. Spwig secara otomatis mematikannya untuk produk Digital, Booking, dan Gift Card, karena produk tersebut tidak pernah dikirim — Anda tidak perlu (dan tidak bisa) mengaktifkannya kembali untuk jenis produk tersebut. Biarkan tercentang untuk produk fisik yang kebetulan mirip dengan produk digital, seperti gift card cetak yang dikirim dalam kotak.
- **Paket Pengiriman Pilihan** — Secara opsional pilih salah satu paket pengiriman yang Anda konfigurasikan. Ketika diatur, dimensi paket itu sendiri digunakan untuk perhitungan tarif pengiriman alih-alih berat dan dimensi produk ini di atas — berguna ketika produk selalu dikirim dalam kotak atau amplop standar yang sama. Kosongkan untuk menggunakan atribut fisik produk itu sendiri. Kelola paket yang tersedia di bawah **Pengiriman > Paket**.

### Pre-order

Gunakan kartu **Pre-order** untuk menjual produk sebelum memiliki stok — berguna untuk rilis mendatang yang ingin Anda mulai terima pesannya sebelum peluncuran:

- **Apakah Pre-order** — Aktifkan untuk memungkinkan pelanggan membeli produk ini bahkan ketika stok habis.
- **Tanggal Rilis Pre-order** — Tanggal ketersediaan yang diharapkan, ditampilkan kepada pelanggan.
- **Pesan Pre-order** — Pesan kustom singkat yang ditampilkan kepada pelanggan, hingga 200 karakter (misalnya, "Dikirim Maret 2026").

### Identifikasi produk

Kode produk standar untuk daftar marketplace dan sistem inventaris:

- **GTIN** — Global Trade Item Number
- **EAN** — European Article Number
- **UPC** — Universal Product Code (US)
- **ISBN** — Untuk buku
- **ASIN** — Identifikasi Amazon
- **MPN** — Manufacturer Part Number

### Pengiriman internasional / bea cukai

Wajib untuk pengiriman internasional (perluas bagian **Pengiriman Internasional / Bea Cukai**):

- **Kode HS** — Kode klasifikasi Sistem Harmonisasi
- **Negara Asal** — Di mana produk diproduksi
- **Harga Satuan Kepabeanan** — Nilai yang dinyatakan per unit untuk kepabeanan
- **Nomor Izin Ekspor** — Dibutuhkan hanya untuk barang yang dikendalikan atau dibatasi
- **Tanggal Kadaluarsa Izin Ekspor** — Tanggal kadaluarsa izin ekspor

## SEO

Optimalkan visibilitas mesin pencari produk Anda.

![Tab SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Judul Meta** — Judul yang ditampilkan dalam hasil mesin pencari. Klik ikon dunia untuk menerjemahkan.
- **Deskripsi Meta** — Deskripsi ringkas untuk hasil pencarian (maksimal 160 karakter). Klik ikon dunia untuk menerjemahkan.
- **Buat SEO Otomatis** — Centang untuk secara otomatis membuat konten SEO ketika produk disimpan.

Pratinjau **Hasil Pencarian** secara langsung menunjukkan bagaimana produk Anda akan terlihat dalam hasil pencarian Google.

## Pengaturan halaman produk

Pada tab **Lanjutan**, kartu **Pengaturan Halaman Produk** memungkinkan Anda mengontrol bagaimana tampilan halaman toko produk ini:

- **Template Halaman** — Menimpa tata letak halaman produk situs default untuk produk ini: Klasik, Lebar Penuh, Fokus Galeri, atau Digital. Biarkan setel ke **Gunakan Default Situs** untuk mewarisi tata letak apa pun yang ditentukan oleh pengaturan Desain Anda — kebanyakan produk sebaiknya tetap pada default agar perubahan template di sana diterapkan secara otomatis.
- **Tampilkan Produk Terkait** — Menampilkan produk terkait di bagian bawah halaman.
- **Tampilkan Ulasan** — Menampilkan ulasan pelanggan.
- **Tampilkan Spesifikasi** — Menampilkan tab spesifikasi.

Bidang **Jenis Galeri** — yang mengontrol bagaimana gambar produk ditampilkan (Galery Standar, Carousel, Tata Letak Grid, Galeri Zoom, atau Tampilan 360°) — diatur secara terpisah, pada tab **Media**.

![Tab Lanjutan menunjukkan kartu Pengaturan Halaman Produk dengan dropdown Template Halaman, dan kartu Detail Teknis di bawahnya](/static/core/admin/img/help/add-product/advanced-tab.webp)

## Saluran Penjualan

Bidang **Saluran Penjualan** (pada bagian Status) mengontrol di mana produk dapat dijual:

- **Semua Saluran** — Tersedia secara online dan di toko (POS).
- **Hanya Online** — Tidak tersedia melalui terminal POS.
- **Hanya Di Toko** — Tidak terdaftar secara online; hanya tersedia di toko fisik Anda.

Bidang **Barcode** juga tersedia untuk pemindaian barcode POS.

## Menyimpan produk Anda

Ketika Anda siap, gunakan tombol simpan di sudut kanan atas. Produk Anda akan terlihat di toko setelah statusnya diatur menjadi **Terbitkan**.

## Tips

- Mulai dengan status **Draf** sehingga Anda dapat menyempurnakan produk sebelum pelanggan melihatnya.
- Unggah beberapa gambar — produk dengan beberapa foto akan lebih baik dalam konversi.
- Isi bidang **SEO** untuk meningkatkan keterlihatan dalam mesin pencari.
- Gunakan **Kategori**, **Merek**, dan **Tag** untuk membantu pelanggan menavigasi katalog Anda.
- Untuk produk variabel (misalnya, ukuran atau warna berbeda), pilih jenis **Produk Variabel** dan tambahkan variasi setelah menyimpan.
- Gunakan **Fitur** dan **Spesifikasi** untuk menambahkan data produk yang terstruktur yang ditampilkan dalam tab khusus di halaman produk.
- Jika **Membutuhkan Pengiriman** tidak bisa dicentang, lihat **Jenis Produk** — Spwig menonaktifkan pengiriman secara otomatis untuk produk Digital, Pemesanan, dan Kartu Hadiah, karena ketiga jenis tersebut tidak pernah dikirim secara fisik.
- Tetapkan **Kemasan Pengiriman Favorit** untuk produk yang selalu dikirim dalam kotak yang sama — ini menghemat Anda dari harus terus-menerus menyesuaikan berat dan dimensi produk tersebut dengan kotak yang sebenarnya Anda gunakan.
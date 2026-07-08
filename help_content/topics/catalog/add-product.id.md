---
title: Menambahkan Produk
---

# Menambahkan Produk

Panduan ini membimbing Anda melalui proses pembuatan produk baru di toko Anda. Produk dikelompokkan ke dalam beberapa tab — Informasi Dasar, Media, Harga, Persediaan, dan SEO — sehingga Anda dapat mengisi semua informasi dalam satu kali atau kembali untuk menyelesaikan bagian tertentu nanti.

## Memulai

Dari bilah samping, navigasikan ke **Produk > Semua Produk** untuk melihat katalog produk Anda. Klik tombol **+ Tambahkan Produk** di sudut kanan atas untuk membuka formulir pembuatan produk.

![Halaman daftar produk](/static/core/admin/img/help/add-product/product-list-page.webp)

## Tab Informasi Dasar

Tab **Informasi Dasar** adalah tempat Anda mendefinisikan detail inti produk Anda.

![Formulir tambah produk](/static/core/admin/img/help/add-product/add-product-form.webp)

### Bidang Wajib

- **Nama** — Nama produk yang ditampilkan kepada pelanggan. Klik ikon globe untuk menambahkan terjemahan untuk bahasa lain.
- **Slug** — Versi nama yang ramah URL (otomatis dihasilkan). Matikan opsi "Auto" untuk menyesuaikannya.
- **SKU** — Kode unit persediaan internal Anda.
- **Jenis Produk** — Pilih dari: Sederhana, Variabel, Digital, Bundle, Kartu Hadiah, Dapat Disesuaikan, atau Dapat dikonfigurasi.
- **Status** — Tetapkan ke Draf saat bekerja, lalu ubah ke Diterbitkan ketika siap.

### Bidang Opsional

- **Kategori** — Tetapkan produk ke kategori untuk organisasi dan navigasi toko.
- **Merek** — Asosiasikan dengan merek jika relevan.
- **Ditampilkan** — Centang untuk menampilkan produk ini di toko Anda.
- **Produk Digital** — Centang jika produk ini mencakup unduhan digital (file, lisensi).
- **Sembunyikan dari Toko** — Menyembunyikan produk dari daftar katalog tetapi tetap tersedia sebagai opsi konfigurasi atau komponen bundle.

### Deskripsi Produk

- **Deskripsi Singkat** — Muncul di daftar produk dan kartu. Pertahankan singkat dan menarik.
- **Deskripsi Lengkap** — Deskripsi produk rinci yang ditampilkan di halaman detail produk. Gunakan editor teks kaya untuk menambahkan pemformatan, gambar, video, dan tabel.

Kedua bidang deskripsi mendukung fitur terjemahan — klik ikon globe untuk menyediakan konten dalam bahasa lain.

## Tab Media

Tab **Media** memungkinkan Anda mengelola gambar produk menggunakan Perpustakaan Media yang terintegrasi.

![Tab Media](/static/core/admin/img/help/add-product/media-tab.webp)

1. Klik **+ Tambahkan Gambar dari Perpustakaan Media** untuk membuka pemilih media.
2. Pilih gambar yang sudah ada atau unggah yang baru secara langsung.
3. Drag gambar untuk mengurutkannya — **gambar pertama** menjadi gambar utama produk yang ditampilkan di daftar dan kartu.
4. Pilih **Jenis Galeri** untuk mengontrol cara gambar ditampilkan di halaman produk: Galeri Standar, Karusel, Tata Letak Kisi, Galeri Zoom, atau Tampilan 360°.

## Tab Harga

Atur harga produk Anda dan konfigurasikan penjualan.

![Tab Harga](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Harga Reguler

- **Harga Reguler** — Harga ritel standar yang akan dilihat pelanggan.
- **Mata Uang** — Pilih mata uang (mata uang default toko Anda sudah dipilih sebelumnya).
- **Biaya** — Biaya barang Anda, digunakan untuk perhitungan laba. Ini tidak pernah ditampilkan kepada pelanggan.

### Pengaturan Penjualan

Konfigurasikan diskon sementara:

- **Jenis Penjualan** — Pilih dari: Tidak Ada Penjualan, Harga Penjualan Tetap, Jumlah Potongan, atau Persentase Potongan.
- **Nilai Penjualan** — Jumlah diskon atau persentase.
- **Tanggal Mulai/Selesai** — Jadwalkan kapan penjualan diaktifkan dan berakhir. Biarkan kosong untuk mulai segera atau tanpa tanggal akhir.

## Tab Persediaan

Kelola tingkat persediaan dan atribut produk fisik.

![Tab Persediaan](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Manajemen Persediaan

- **Lacak Persediaan** — Aktifkan untuk melacak jumlah persediaan (diaktifkan secara default).
- **Ambang Batas Persediaan Rendah** — Terima pemberitahuan saat persediaan turun di bawah angka ini (default: 5).
- **Jumlah Persediaan** — Total unit yang tersedia.
- **Izinkan Pesanan Kembali** — Aktifkan untuk menerima pesanan meskipun stok habis.

### Atribut Fisik

Masukkan berat produk (kg) dan dimensi (panjang, lebar, tinggi dalam cm) untuk perhitungan pengiriman yang akurat.

### Identifikasi Produk

Kode produk standar untuk daftar pasar dan sistem persediaan:

- **GTIN** — Nomor Item Perdagangan Global
- **EAN** — Nomor Artikel Eropa
- **UPC** — Kode Produk Universal (AS)
- **ISBN** — Untuk buku
- **ASIN** — Identifier Amazon
- **MPN** — Nomor Bagian Pabrikan

### Pengiriman Internasional / Kepabeanan

Diperlukan untuk pengiriman internasional:

- **Kode HS** — Kode Klasifikasi Sistem Harmonis
- **Negara Asal** — Di mana produk dibuat
- **Harga Satuan Kepabeanan** — Nilai deklarasi per unit untuk kepabeanan

## Tab SEO

Optimalkan visibilitas mesin pencari produk Anda.

![Tab SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Judul Meta** — Judul yang ditampilkan dalam hasil pencarian mesin pencari. Klik ikon globe untuk menerjemahkan.
- **Deskripsi Meta** — Deskripsi singkat untuk hasil pencarian (maks 160 karakter). Klik ikon globe untuk menerjemahkan.
- **Otomatis Buat SEO** — Centang untuk secara otomatis membuat konten SEO saat produk disimpan.

**Pratinjau Hasil Pencarian** langsung menunjukkan persis bagaimana produk Anda akan muncul di hasil pencarian Google.

## Menyimpan Produk Anda

Ketika Anda siap, gunakan tombol simpan di sudut kanan atas:

- **Simpan** (tanda centang) — Simpan dan tetap di halaman produk.
- **Simpan dan lanjutkan mengedit** — Simpan dan tetap di formulir untuk terus bekerja.

Produk Anda akan terlihat di toko saat statusnya diatur ke **Diterbitkan**.

## Tips

- Mulailah dengan status **Draf** sehingga Anda dapat memperbaiki produk sebelum pelanggan melihatnya.
- Unggah beberapa gambar — produk dengan beberapa foto berkonversi lebih baik.
- Isi bidang **SEO** untuk meningkatkan keterjangkauan di mesin pencari.
- Gunakan **Kategori** dan **Merek** untuk membantu pelanggan menavigasi katalog Anda.
- Untuk produk variabel (misalnya, ukuran atau warna berbeda), pilih jenis **Produk Variabel** dan tambahkan variasi setelah disimpan.

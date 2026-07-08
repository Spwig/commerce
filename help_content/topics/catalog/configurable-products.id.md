---
title: Produk Konfigurabel
---

Produk konfigurabel memungkinkan pelanggan membangun produk mereka sendiri dengan memilih opsi dari berbagai slot konfigurasi. Ini ideal untuk item yang dibuat sesuai pesanan seperti komputer pribadi khusus, kotak hadiah yang dipersonalisasi, atau perabot yang dibuat sesuai pesanan di mana setiap komponen adalah produk nyata di katalog Anda.

![Admin konfigurasi produk](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## Bagaimana Cara Kerjanya

Produk konfigurabel terdiri dari **slot** (kategori pilihan) dan **opsi** (produk nyata yang dapat dipilih oleh pelanggan). Misalnya, komputer pribadi khusus mungkin memiliki slot untuk Prosesor, Kartu Grafis, RAM, dan Penyimpanan — setiap slot berisi beberapa opsi produk yang dapat dipilih.

## Strategi Penentuan Harga

Pilih cara harga akhir dihitung:

| Strategi | Deskripsi |
|----------|-------------|
| **Jumlah Komponen** | Harga akhir = total harga semua opsi yang dipilih. Tidak diperlukan harga dasar. |
| **Harga Dasar + Penyesuaian** | Mulai dengan harga dasar produk, lalu tambah atau kurangi penyesuaian harga per opsi. |
| **Harga Tetap** | Satu harga flat tanpa memandang opsi apa yang dipilih pelanggan. |

## Menyiapkan Produk Konfigurabel

### Langkah 1: Membuat Produk

1. Navigasikan ke **Produk > Semua Produk** dan klik **+ Tambah Produk**
2. Setel **Jenis Produk** menjadi **Produk Konfigurabel**
3. Pilih **Strategi Penentuan Harga** Anda (Jumlah Komponen adalah yang paling umum)
4. Isi nama produk, deskripsi, dan detail dasar lainnya
5. Simpan produk

### Langkah 2: Menambahkan Slot Konfigurasi

Setelah disimpan, beralih ke tab **Konfigurasi** untuk menyiapkan slot Anda.

1. Klik **+ Tambah Slot** untuk membuat kategori konfigurasi baru
2. Untuk setiap slot, konfigurasikan:
   - **Nama** — Apa yang dilihat pelanggan (misalnya, "Prosesor", "Warna")
   - **Ikon** — Kelas ikon Font Awesome untuk identifikasi visual
   - **Wajib** — Apakah pelanggan harus membuat pemilihan
   - **Min/Max Pemilihan** — Berapa banyak opsi yang dapat dipilih pelanggan (default: tepat 1)
   - **Urutan Penyortiran** — Mengontrol urutan slot muncul di wizard konfigurasi

### Langkah 3: Menambahkan Opsi ke Setiap Slot

Setiap slot membutuhkan opsi produk untuk dipilih oleh pelanggan:

1. Klik **Kelola Opsi** pada sebuah slot
2. Cari dan tambahkan produk yang sudah ada dari katalog Anda
3. Untuk setiap opsi, konfigurasikan:
   - **Penyesuaian Harga** — Jumlah yang ditambahkan atau dikurangi (digunakan dengan strategi harga Dasar + Penyesuaian)
   - **Default** — Pilih opsi ini secara otomatis saat konfigurator dimuat
   - **Populer** — Tunjukkan badge "Populer" untuk membantu pelanggan memutuskan
   - **Kuantitas** — Berapa banyak unit komponen ini yang termasuk
   - **Tag Kompatibilitas** — Tag yang digunakan untuk pembuatan aturan kompatibilitas secara otomatis

**Tips:** Produk komponen dapat disembunyikan dari toko depan dengan memeriksa **Sembunyikan dari Toko Depan** di tab Info Dasar produk komponen. Ini menjaga ketersediaannya sebagai opsi konfigurasi tanpa mengotori katalog produk Anda.

### Langkah 4: Mendefinisikan Aturan Kompatibilitas

Aturan kompatibilitas mencegah pelanggan memilih kombinasi yang tidak kompatibel:

| Jenis Aturan | Deskripsi |
|-----------|-------------|
| **Memerlukan** | Ketika opsi A dipilih, hanya opsi yang terdaftar yang tersedia di slot target |
| **Mengecualikan** | Ketika opsi A dipilih, opsi yang terdaftar disembunyikan dari slot target |

Untuk menambahkan aturan:

1. Gulir ke bagian **Aturan Kompatibilitas** di tab Konfigurasi
2. Klik **+ Tambah Aturan**
3. Pilih **opsi sumber** (pemicu)
4. Pilih **jenis aturan** (Memerlukan atau Mengecualikan)
5. Pilih **slot target** dan **opsi yang terkena**

Anda juga dapat membuat aturan secara otomatis dari tag kompatibilitas yang ditetapkan ke opsi, yang lebih cepat saat mengelola banyak kombinasi.

### Langkah 5: Membuat Preset (Opsional)

Preset adalah konfigurasi yang sudah dibuat sebelumnya yang memberikan pelanggan titik awal cepat:

1. Gulir ke bagian **Preset Konfigurasi**
2. Klik **+ Tambah Preset**
3. Beri nama dan deskripsi preset (misalnya, "Konfigurasi Gaming", "Paket Penghemat")
4. Pilih opsi untuk setiap slot
5. Secara opsional unggah gambar pratinjau dan tandai sebagai **Dipilih**

Pelanggan dapat memulai dari preset dan kemudian menyesuaikan slot individu sesuai preferensi mereka.

## Pengalaman Pelanggan

Ketika pelanggan melihat produk konfigurabel di toko depan Anda:

1. **Antarmuka Wizard** — Slot ditampilkan sebagai langkah-langkah, memandu pelanggan melalui setiap pilihan
2. **Penyaringan** — Opsi yang tidak kompatibel secara otomatis disembunyikan berdasarkan aturan kompatibilitas
3. **Badge Populer** — Opsi yang ditandai sebagai populer menampilkan badge untuk membantu pengambilan keputusan
4. **Preset** — Preset yang dipilih muncul sebagai opsi awal cepat
5. **Pembaruan Harga** — Harga total diperbarui secara real-time saat opsi dipilih
6. **Ringkasan** — Langkah tinjau menampilkan semua opsi yang dipilih sebelum menambahkan ke keranjang

## Tips

- Mulailah dengan strategi penentuan harga "Jumlah Komponen" — ini paling intuitif bagi pelanggan dan paling mudah dipelihara.
- Gunakan aturan kompatibilitas untuk mencegah konfigurasi yang tidak valid daripada mengandalkan pengetahuan pelanggan.
- Buat 2-3 preset untuk konfigurasi paling populer Anda untuk mengurangi kelelahan pengambilan keputusan.
- Sembunyikan produk komponen dari toko depan jika mereka hanya tersedia melalui konfigurator.
- Uji alur konfigurasi lengkap di frontend setelah penyiapan untuk memastikan semua aturan berfungsi seperti yang diharapkan.
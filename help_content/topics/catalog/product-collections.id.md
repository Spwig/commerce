---
title: Koleksi Produk
---

Koleksi memungkinkan Anda mengelompokkan produk untuk ditampilkan di toko online Anda. Berbeda dengan kategori — yang mengorganisir seluruh katalog Anda ke dalam hierarki permanen — koleksi bersifat fleksibel, kelompok yang disusun dengan hati-hati yang Anda buat untuk tujuan tertentu. Sebuah koleksi mungkin menyoroti produk baru, menampilkan item untuk kampanye musiman, atau memperkenalkan seleksi terpilih dari produk terlaris.

Navigasikan ke **Katalog > Koleksi** untuk mengelola koleksi Anda.

## Koleksi vs kategori

Kedua kategori dan koleksi mengelompokkan produk, tetapi mereka memiliki tujuan yang berbeda:

|  | Kategori | Koleksi |
|---|---|---|
| **Tujuan** | Struktur katalog permanen | Kelompok fleksibel yang disusun dengan hati-hati |
| **Hierarki** | Ya — struktur induk/anak yang bersarang | Tidak — kelompok datar |
| **Produk per kelompok** | Setiap produk termasuk dalam satu kategori | Sebuah produk dapat muncul dalam banyak koleksi |
| **Penggunaan umum** | Menu navigasi toko, lihat berdasarkan departemen | Halaman utama, kampanye, set produk yang disorot |

Gunakan kategori untuk "bagaimana toko Anda diorganisir" dan koleksi untuk "apa yang ingin Anda sorot saat ini".

## Jenis koleksi

Ketika membuat koleksi, pilih jenis yang cocok dengan cara Anda ingin mengelola daftar produk:

| Jenis | Cara produk ditambahkan |
|---|---|
| **Pemilihan Manual** | Anda memilih secara eksplisit produk-produk yang akan muncul, satu per satu |
| **Aturan Otomatis** | Produk ditambahkan secara otomatis berdasarkan kriteria yang Anda tentukan |
| **Produk Terpilih** | Sebuah seleksi editorial yang disusun secara manual |
| **Musiman** | Sebuah seleksi berbasis waktu, biasanya dikelola secara manual untuk kampanye |

Jenis Manual dan Produk Terpilih memberi Anda kendali yang tepat. Koleksi otomatis dapat berkembang seiring dengan katalog Anda tanpa perawatan terus-menerus.

## Membuat koleksi

1. Navigasikan ke **Katalog > Koleksi**
2. Klik **+ Tambah Koleksi**
3. Isi bagian **Informasi Dasar**:
   - **Nama** — nama koleksi seperti yang akan muncul di toko online Anda
   - **Slug** — jalur URL untuk halaman koleksi (otomatis diisi dari nama; Anda dapat menyesuaikannya)
   - **Deskripsi** — deskripsi yang ditampilkan di halaman toko online koleksi
4. Pilih **Jenis Koleksi**
5. Tambahkan produk:
   - Untuk jenis **Pemilihan Manual** dan **Produk Terpilih**: gunakan bidang **Produk** untuk mencari dan menambahkan produk
   - Untuk jenis **Otomatis**: tentukan kriteria di bidang **Kriteria Otomatis**
6. Unggah gambar:
   - **Gambar** — gambar utama koleksi yang digunakan di halaman daftar dan thumbnail
   - **Gambar Banner** — gambar banner yang lebih lebar yang ditampilkan di bagian atas halaman koleksi
7. Konfigurasikan bidang **SEO** (opsional tetapi disarankan):
   - **Judul Meta** — judul halaman yang ditampilkan dalam hasil pencarian
   - **Deskripsi Meta** — deskripsi yang ditampilkan di bawah judul dalam hasil pencarian
8. Atur **Opsi Tampilan**:
   - **Aktif** — mengontrol apakah koleksi terlihat di toko online Anda
   - **Terpilih** — menandai koleksi untuk tampilan terpilih di tema Anda
   - **Urutan Penyortiran** — mengontrol urutan di mana koleksi muncul di halaman daftar (angka yang lebih rendah muncul lebih dulu)
9. Klik **Simpan**

## Menambahkan produk ke koleksi

Untuk koleksi manual, gunakan bidang otokompletnasi **Produk** untuk mencari katalog Anda dan memilih item. Anda dapat menambahkan sebanyak produk yang Anda butuhkan — tidak ada batas.

Produk dapat termasuk dalam beberapa koleksi sekaligus. Misalnya, sebuah produk bisa berada di koleksi "Penjualan Musim Panas" dan koleksi "Produk Terlaris" Anda tanpa ada konflik.

## Menampilkan koleksi di toko online Anda

Setiap koleksi secara otomatis mendapatkan halaman sendiri di `/collection/{slug}/`. Anda dapat menghubungkan halaman koleksi dari menu navigasi Anda, pembuat halaman, atau banner promosi.

Bendera **Terpilih** digunakan oleh tema Anda untuk menentukan koleksi mana yang muncul di tempat terpilih — misalnya, grid halaman utama yang menampilkan koleksi yang disorot. Periksa dokumentasi tema Anda untuk memahami secara tepat bagaimana koleksi terpilih ditampilkan.

## Mengelola visibilitas koleksi

- **Aktif** mengontrol apakah halaman koleksi dapat diakses secara publik.

Koleksi yang tidak aktif disembunyikan dari pelanggan tetapi tetap disimpan di admin sehingga Anda dapat mengaktifkannya kembali nanti.
- **Urutan Pengurutan** menentukan urutan di mana koleksi muncul di halaman daftar.

Berikan angka yang lebih rendah pada koleksi yang ingin muncul lebih awal.

## SEO untuk koleksi

Setiap koleksi memiliki bidang **Judul Meta** dan **Deskripsi Meta** sendiri. Bidang-bidang ini mengontrol apa yang muncul di hasil pencarian mesin pencari ketika seseorang menemukan halaman koleksi Anda. Jika Anda meninggalkan bidang-bidang ini kosong, tema Anda biasanya akan kembali ke nama dan deskripsi koleksi.

Judul SEO koleksi yang baik bersifat deskriptif dan spesifik:
- "Dress Musim Panas 2026 — Gaya Bunga & Ringan" bekerja lebih baik daripada "Koleksi Musim Panas"
- "Sepatu Running Pria — Ringan & Menyerap Keringat" bekerja lebih baik daripada "Sepatu Running"

## Tips

- Pertahankan nama koleksi singkat dan jelas — mereka muncul sebagai judul halaman dan teks tautan di navigasi toko online Anda
- Gunakan koleksi musiman atau kampanye dengan rencana mulai dan akhir: buat koleksi tersebut, aktifkannya saat kampanye dimulai, dan non-aktifkan (alih-alih menghapusnya) saat kampanye berakhir agar Anda dapat merujukkannya nanti
- Bidang **Urutan Pengurutan** sebaiknya diatur secara sengaja — defaultnya adalah 0 untuk semua koleksi, yang berarti mereka diurutkan secara alfabetis. Berikan angka spesifik untuk mengontrol koleksi mana yang muncul paling menonjol
- Koleksi tanpa produk akan menampilkan halaman kosong bagi pelanggan — tambahkan produk sebelum mengaktifkannya, atau biarkan koleksi tersebut tidak aktif hingga siap
- Periksa tanda **Ditampilkan** hanya untuk koleksi yang benar-benar ingin Anda sorot; sebagian besar tema menyisihkan slot ditampilkan untuk sejumlah kecil koleksi, dan tampilan dapat terlihat padat jika terlalu banyak yang ditandai
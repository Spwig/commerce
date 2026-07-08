---
title: Merek Produk
---

Merek memungkinkan Anda menghubungkan produk dengan produsen atau labelnya dan memberi pelanggan cara untuk menjelajahi toko Anda berdasarkan merek. Setiap merek memiliki halaman sendiri di toko Anda di mana pelanggan dapat menemukan semua produk dari merek tersebut, membaca cerita merek, dan mengikuti tautan ke situs web merek.

Navigasikan ke **Katalog > Merek** untuk mengelola merek Anda.

## Mengapa menggunakan merek

Merek memiliki dua tujuan di Spwig:

1. **Organisasi** — produk ditandai dengan merek, sehingga memudahkan pelanggan yang loyal pada label tertentu untuk menemukan apa yang mereka cari
2. **Pemasaran** — halaman merek adalah ruang khusus untuk menampilkan cerita merek, logo, dan seluruh rangkaian produk, yang dapat meningkatkan konversi bagi pelanggan yang memperhatikan merek

Merek juga bekerja dengan sistem promosi — Anda dapat menjalankan penjualan yang berlaku untuk semua produk dari merek tertentu tanpa harus memilih produk secara individual.

## Membuat merek

1. Navigasikan ke **Katalog > Merek**
2. Klik **+ Tambah Merek**
3. Isi bagian **Informasi Dasar**:
   - **Nama** — nama merek seperti yang akan muncul di toko Anda (harus unik)
   - **Slug** — jalur URL untuk halaman merek (otomatis diisi dari nama; Anda dapat menyesuaikannya)
   - **Deskripsi** — deskripsi singkat merek yang ditampilkan di halaman merek
   - **Situs Web** — URL situs web resmi merek (opsional — ditampilkan sebagai tautan di halaman merek)
4. Tambahkan aset merek:
   - **Logo** — gambar logo merek, digunakan dalam daftar merek dan di halaman merek
   - **Gambar Banner** — gambar banner lebar yang ditampilkan di bagian atas halaman merek
5. Tulis **Cerita Merek** (opsional) — artikel editorial yang lebih panjang tentang sejarah, nilai, atau hal yang membuat merek tersebut istimewa. Ini muncul di halaman toko merek dan dapat menjadi cara yang efektif untuk menceritakan kisah merek kepada pelanggan yang tertarik.
6. Konfigurasikan bidang **SEO**:
   - **Judul Meta** — judul halaman yang ditampilkan di hasil pencarian mesin pencari
   - **Deskripsi Meta** — deskripsi singkat yang ditampilkan di bawah judul dalam hasil pencarian
7. Atur opsi tampilan:
   - **Tampilkan Halaman Merek** — mengontrol apakah merek memiliki halaman yang dapat diakses secara publik. Centang untuk menyembunyikan merek dari toko sambil tetap menyimpannya di sistem.
   - **Aktif** — mengontrol apakah merek tersedia untuk ditetapkan ke produk dan terlihat di toko
   - **Ditampilkan** — menandai merek untuk penempatan khusus di tema Anda (misalnya, baris logo merek di halaman utama)
8. Klik **Simpan**

## Menetapkan produk ke merek

Merek ditetapkan pada catatan produk individual, bukan dari halaman manajemen merek. Untuk menetapkan merek ke produk:

1. Navigasikan ke **Katalog > Produk** dan buka produk
2. Di formulir produk, cari bidang **Merek**
3. Cari dan pilih merek yang sesuai
4. Simpan produk

Setelah merek ditetapkan, produk akan muncul secara otomatis di halaman toko merek tersebut.

## Halaman merek di toko Anda

Setiap merek dengan **Tampilkan Halaman Merek** diaktifkan memiliki halaman sendiri di `/brand/{slug}/`. Halaman ini menampilkan:

- Logo dan gambar banner merek
- Nama dan deskripsi merek
- Cerita merek (jika disediakan)
- Tautan ke situs web merek (jika disediakan)
- Semua produk aktif yang ditetapkan ke merek tersebut

Pelanggan dapat mencapai halaman merek dengan mengklik nama merek di halaman produk, atau melalui tautan yang Anda buat di navigasi atau pembuat halaman Anda.

## SEO untuk halaman merek

Mengisi bidang **Judul Meta** dan **Deskripsi Meta** untuk setiap merek membantu halaman merek Anda muncul dengan baik di hasil pencarian. Judul SEO merek yang efektif biasanya menggabungkan nama merek dengan apa yang dijual oleh merek tersebut:

| Merek | Judul Meta yang Baik |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

Jika Anda meninggalkan bidang SEO kosong, tema Anda akan kembali ke nama merek.

### Pembuatan SEO otomatis

Jika **SEO Auto Generated** diaktifkan pada sebuah merek, Spwig akan secara otomatis menghasilkan konten judul meta dan deskripsi saat merek tersebut disimpan.

Ini sangat praktis untuk toko yang memiliki banyak merek, tetapi memberikan Anda kontrol yang lebih sedikit terhadap kata-kata yang tepat.

Anda selalu dapat mengganti konten yang dihasilkan dengan mengetik langsung ke dalam bidang tersebut dan menonaktifkan tombol penghasilan otomatis.

## Merek Terpilih

Bendera **Is Featured** digunakan oleh tema untuk menampilkan baris atau grid logo merek yang dipilih — biasanya di halaman utama. Hanya sedikit merek yang sebaiknya ditampilkan sekaligus; konsultasikan dokumentasi tema Anda untuk memahami berapa banyak merek terpilih yang menampilkan secara optimal.

## Tips

- Unggah logo merek sebagai PNG atau WebP dengan latar belakang transparan — logo ini akan ditampilkan dengan bersih pada warna latar belakang apa pun di tema Anda
- Tulis cerita merek yang menarik bahkan untuk merek yang kurang dikenal; pelanggan yang tidak mengenal merek tersebut menghargai konteks yang membantu mereka memutuskan apakah produk tersebut cocok untuk mereka
- Jika Anda menjalankan promosi yang menargetkan merek tertentu, pastikan nama merek di Spwig cocok secara tepat — promosi menggunakan hubungan merek pada produk untuk menentukan kelayakan
- Nonaktifkan merek daripada menghapusnya ketika Anda berhenti menjual produknya — penghapusan menghilangkan referensi merek dari semua produk terkait, sedangkan penonaktifan mempertahankan sejarah
- Gunakan bendera **Is Featured** secara jarang; halaman utama yang menampilkan 20 logo merek kehilangan dampaknya dibandingkan 6–8 yang dipilih secara hati-hati
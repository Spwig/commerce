---
title: Produk Kustomisasi
---

Produk kustomisasi memungkinkan pelanggan Anda merancang produk mereka sendiri menggunakan editor visual langsung di toko online Anda. Baik Anda menjual kemeja kustom, poster pribadi, merchandise berlogo, atau kartu ucapan, fitur ini memberikan alat kepada pelanggan untuk menambahkan teks, mengunggah gambar, dan menggunakan gambar ilustrasi untuk membuat desain unik — semuanya tanpa meninggalkan toko Anda.

## Bagaimana cara kerjanya

Produk kustomisasi menggabungkan produk Spwig standar dengan **editor desain visual**. Anda mendefinisikan permukaan desain produk (seperti depan dan belakang kemeja), mengunggah gambar mockup agar pelanggan dapat melihat desain mereka dalam konteks, dan menetapkan aturan untuk apa yang dapat dilakukan pelanggan di setiap permukaan.

Ketika pelanggan mengunjungi produk kustomisasi di toko online Anda, mereka melihat editor kanvas langsung yang ditampilkan di atas gambar mockup produk. Mereka dapat menambahkan teks, mengunggah gambar mereka sendiri, dan menjelajahi perpustakaan gambar ilustrasi Anda untuk membangun desain mereka. Editor menampilkan desain tepat seperti yang akan terlihat di produk selesai.

### Dua kasus penggunaan

Produk kustomisasi bekerja dengan baik dalam dua skenario umum:

| Kasus penggunaan | Contoh | Permukaan | Pengaturan tipek |
|------------------|--------|-----------|------------------|
| **Desain pakaian** | Kemeja kustom, hoodie, tas belanja | Banyak (depan, belakang, lengan) | Font tebal, ilustrasi humor/sports, batasan per-permukaan |
| **Desain cetak** | Poster, kartu ucapan, kartu bisnis | Tunggal (hanya depan) | DPI tinggi, pengaturan tumpuran, font elegan, batas dekoratif |

Proses pengaturan sama untuk keduanya — perbedaannya terletak pada jumlah permukaan yang Anda definisikan, gambar ilustrasi dan font apa yang Anda sediakan, serta cara Anda mengatur pengaturan cetak.

## Konsep kunci

### Konfigurasi desain

Setiap produk kustomisasi memiliki **konfigurasi desain** yang mengontrol perilaku keseluruhan editor: alat mana yang tersedia (teks, unggah gambar, gambar ilustrasi), batas unggah, dan aturan harga. Ini adalah panel kontrol utama untuk editor desain produk.

### Permukaan

**Permukaan** adalah wajah desain dari produk Anda. Sebuah kemeja biasanya memiliki tiga permukaan (depan, belakang, lengan), sedangkan poster hanya memiliki satu. Setiap permukaan memiliki gambar mockup sendiri, posisi zona desain, dimensi fisik, dan pengaturan kualitas cetak.

### Zona desain

**Zona desain** adalah area persegi panjang pada gambar mockup tempat pelanggan dapat menempatkan elemen desain mereka. Anda menempatkan zona ini secara visual di halaman pengaturan admin dengan menyeret dan mengubah ukurannya di atas gambar mockup. Zona ini mendefinisikan tempat desain muncul di produk selesai.

### Template

**Template desain** adalah desain awal yang sudah dibuat yang Anda buat untuk pelanggan. Sebaliknya dari mulai dari kanvas kosong, pelanggan dapat menjelajahi galeri template Anda, memilih satu yang mereka sukai, dan mengkustomisasi. Template dapat mencakup elemen terkunci yang tidak dapat diubah oleh pelanggan — contohnya, logo perusahaan yang harus selalu muncul di posisi yang sama.

### Gambar ilustrasi dan font

Anda membangun **perpustakaan gambar ilustrasi** dari gambar yang dapat ditambahkan pelanggan ke desain mereka, dikategorikan (misalnya, "Olahraga", "Batas", "Liburan"). Anda juga dapat mengunggah **font kustom** selain font sistem standar, memberikan pelanggan lebih banyak pilihan kreatif.

### Harga

Editor desain mendukung model harga fleksibel dengan empat komponen biaya:

| Jenis biaya | Deskripsi |
|-------------|-----------|
| **Biaya desain dasar** | Biaya tetap yang ditambahkan ketika ada kustomisasi yang diterapkan |
| **Biaya per permukaan** | Biaya tambahan untuk setiap permukaan yang digunakan selain yang pertama |
| **Biaya per unggah** | Biaya untuk setiap gambar yang diunggah oleh pelanggan |
| **Biaya per teks** | Biaya untuk setiap elemen teks yang ditambahkan |

Harga diperbarui secara real time saat pelanggan menambahkan elemen, sehingga tidak ada kejutan saat checkout.

## Mode editor

Spwig menawarkan dua mode editor:

- **Canvas Editor** — Editor desain visual lengkap dengan kanvas langsung, alat teks, unggah gambar, browser gambar ilustrasi, dan pratinjau real time di gambar mockup produk.

Ini adalah mode yang disarankan untuk sebagian besar produk yang dapat dikustomisasi.
- **Form Sederhana** — Pendekatan berbasis formulir tradisional di mana pelanggan mengisi bidang teks dan mengunggah gambar tanpa kanvas visual.

Sesuai untuk produk dengan minimalisasi kustomisasi (misalnya, mengukir nama pada perhiasan).

## Alur kerja pedagang

Membuat produk yang dapat dikustomisasi mengikuti alur kerja berikut:

1. **Buat produk** — Tambahkan produk baru dengan tipe diatur ke **Produk yang Dapat Dikustomisasi**
2. **Atur permukaan** — Definisikan setiap wajah yang dapat dirancang, unggah gambar mockup, dan posisikan zona desain
3. **Konfigurasi pengaturan** — Pilih alat yang ingin diaktifkan, atur batas unggah, dan konfigurasikan harga
4. **Tambahkan aset** — Bangun perpustakaan clipart dan unggah font kustom
5. **Buat template** — Rancang titik awal yang sudah jadi dengan kontrol kunci opsional
6. **Uji dan publikasikan** — Pratinjau editor di toko online dan verifikasi semuanya berfungsi

Untuk instruksi pengaturan terperinci, lihat [Mengatur Produk yang Dapat Dikustomisasi](/admin/customizable-product/).

## Pengalaman pelanggan

Ketika pelanggan mengunjungi produk yang dapat dikustomisasi di toko online Anda:

1. **Jelajahi template** — Mereka dapat memulai dari template yang sudah jadi atau memulai dengan kanvas kosong
2. **Pindah permukaan** — Tab di bagian atas memungkinkan mereka beralih antar permukaan (misalnya, depan dan belakang kaos)
3. **Tambahkan elemen** — Panel alat menyediakan alat teks, unggah gambar, dan clipart
4. **Kustomisasi** — Mereka dapat menyesuaikan font, warna, ukuran, posisi, dan menerapkan filter gambar
5. **Lihat harga** — Biaya desain diperbarui secara real time saat mereka menambahkan elemen
6. **Simpan desain** — Pelanggan yang terdaftar dapat menyimpan desain untuk melanjutkan pengeditan nanti
7. **Tambahkan ke keranjang** — Desain terkait dengan item keranjang dan dibekukan saat pesanan ditempatkan

## Apa yang terjadi setelah memesan

Ketika pelanggan menempatkan pesanan yang berisi produk yang dikustomisasi:

- Desain **dibekukan sebagai snapshot** — tidak dapat diubah setelah pembelian
- Sistem menghasilkan **file penyelesaian resolusi tinggi** untuk setiap permukaan
- Anda dapat mengunduh file siap cetak ini dari halaman detail pesanan di panel admin Anda
- File-file tersebut dirender pada DPI yang Anda konfigurasikan untuk setiap permukaan

Untuk detail tentang penyelesaian pesanan yang dikustomisasi, lihat [Menyelesaikan Pesanan Produk yang Dapat Dikustomisasi](/admin/orders/).

## Tips

- Mulailah dengan produk sederhana (satu permukaan, seperti poster) untuk mempelajari proses pengaturan sebelum menangani produk multi-permukaan seperti kaos.
- Unggah gambar mockup berkualitas tinggi — mereka adalah hal pertama yang dilihat pelanggan dan menetapkan ekspektasi kualitas untuk seluruh pengalaman.
- Buat 3-5 template desain untuk setiap produk untuk mengurangi ketakutan "kanvas kosong" dan menginspirasi pelanggan.
- Gunakan pembatas per-permukaan untuk mengontrol apa yang dapat dilakukan pelanggan di setiap permukaan. Misalnya, izinkan hanya unggah logo kecil di lengan kaos sementara memungkinkan kebebasan desain penuh di bagian depan.
- Tetapkan persyaratan DPI minimum yang sesuai dengan metode cetak Anda — 150 DPI untuk cetak sablon, 300 DPI untuk cetak digital berkualitas tinggi.
- Uji alur pelanggan penuh (desain, simpan, tambahkan ke keranjang, checkout) sebelum mempublikasikan produk yang dapat dikustomisasi.
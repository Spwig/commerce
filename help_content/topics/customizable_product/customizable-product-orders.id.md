---
title: Memenuhi Pesanan Produk yang Dapat Disesuaikan
---

Ketika seorang pelanggan merancang sebuah produk dan memesan, desain mereka dibekukan dan disimpan bersama dengan pesanan. Panduan ini menjelaskan bagaimana desain kustom mengalir melalui siklus pesanan dan bagaimana mengakses file siap cetak yang Anda butuhkan untuk pemenuhan pesanan.

## Siklus Desain

Desain pelanggan melalui beberapa tahap dari pembuatan hingga pemenuhan:

### 1. Pembuatan Desain

Pelanggan menggunakan editor visual di toko online untuk membuat desain mereka. Saat mereka bekerja, kemajuan mereka disimpan secara otomatis di browser. Pelanggan yang terdaftar juga dapat menyimpan desain ke akun mereka untuk diedit nanti.

### 2. Draf Desain

Ketika pelanggan mengklik **Tambah ke Keranjang**, keadaan desain saat ini disimpan sebagai **draf desain**. Draf ini mencakup:

- Keadaan lengkap kanvas untuk setiap permukaan (posisi elemen, konten teks, gambar yang diunggah, clipart, gaya)
- Breakdown harga yang menunjukkan semua biaya desain yang berlaku
- Preview mini dari setiap permukaan

Draf terkait dengan item keranjang melalui token unik. Ini memastikan desain yang dibuat pelanggan tetap terjaga bahkan jika mereka terus berbelanja sebelum menyelesaikan pembayaran.

**Kadaluarsa Draf:** Draf desain secara otomatis kadaluarsa setelah 7 hari jika pelanggan tidak menyelesaikan pesanan. Ini mencegah akumulasi desain yang ditinggalkan.

### 3. Snapshot Desain

Ketika pelanggan menyelesaikan checkout dan pesanan ditempatkan, draf desain dikonversi menjadi **snapshot desain yang tidak dapat diubah**. Ini adalah catatan permanen dari desain:

- Snapshot tidak dapat diubah oleh pelanggan setelah pembelian
- Mengandung data desain yang sama persis dengan draf
- Secara permanen terkait dengan item pesanan tertentu

Ketidakberubahannya penting — ini memastikan bahwa apa yang dipesan pelanggan adalah tepat apa yang Anda produksi dan kirim, tanpa kemungkinan perubahan setelah pembayaran.

### 4. Rendering File Pemenuhan

Setelah pesanan ditempatkan, sistem secara otomatis menghasilkan **file pemenuhan resolusi tinggi** untuk setiap permukaan desain. Ini adalah gambar komposit yang menggabungkan semua elemen desain (teks, gambar, clipart) menjadi satu file siap cetak pada DPI yang dikonfigurasikan untuk setiap permukaan.

Rendering terjadi secara asinkron di latar belakang. Untuk sebagian besar desain, rendering selesai dalam beberapa detik. Status **Rendered** dari snapshot menunjukkan apakah file pemenuhan sudah siap.

## Mengakses Data Desain dalam Pesanan

### Halaman Detail Pesanan

Ketika Anda melihat pesanan yang berisi produk yang dapat disesuaikan di panel admin:

1. Navigasikan ke **Orders > All Orders**
2. Buka pesanan yang berisi produk yang disesuaikan
3. Item pesanan untuk produk yang dapat disesuaikan menampilkan informasi desain, termasuk preview permukaan dan tautan ke snapshot desain

### Daftar Snapshot Desain

Anda juga dapat menelusuri semua snapshot desain secara langsung:

1. Navigasikan ke **Customizable Products > Design Snapshots**
2. Daftar menampilkan semua snapshot yang terkait dengan item pesanan
3. Klik snapshot untuk melihat data desain lengkap, gambar yang dirender, dan file pemenuhan

Setiap snapshot menampilkan:

| Field | Description |
|-------|-------------|
| **Order Item** | Tautan ke item pesanan terkait |
| **Design Data** | Keadaan kanvas lengkap (JSON) |
| **Rendered Images** | Preview mini per permukaan |
| **Fulfillment Files** | File komposit resolusi tinggi untuk pencetakan |
| **Rendered** | Apakah rendering selesai |
| **Render Completed At** | Tanda waktu ketika file dihasilkan |

## Mendownload File Pemenuhan

File pemenuhan adalah file yang Anda kirim ke penyedia cetak Anda atau gunakan dalam proses produksi Anda.

**Untuk pesanan kemeja kustom:**
- Unduh file permukaan **Depan** (misalnya, gambar PNG komposit 300 DPI)
- Unduh file permukaan **Belakang**
- Unduh file permukaan **Lengan** (jika dirancang)
- Kirim semua file ke printer layar Anda atau printer DTG (direct-to-garment) Anda


**Untuk pesanan poster khusus:**
- Unduh file permukaan **Front** tunggal dengan resolusi cetak
- File ini mencakup area bleed jika bleed dikonfigurasikan untuk permukaan tersebut
- Kirimkan ke printer poster/kartu Anda

Setiap file adalah satu gambar komposit yang berisi semua elemen desain yang digabungkan, ditampilkan dengan DPI yang Anda konfigurasikan untuk permukaan tersebut.

## Desain yang disimpan

Pelanggan terdaftar dapat menyimpan desain mereka ke akun mereka untuk diedit nanti. Sebagai penjual, Anda dapat melihat desain yang disimpan ini dalam daftar hanya untuk dibaca:

1. Navigasikan ke **Produk Kustomisasi > Desain yang Disimpan**
2. Daftar menampilkan semua desain yang disimpan oleh pelanggan dengan nama pelanggan, produk, nama desain, dan tanggal

Desain yang disimpan adalah:
- **Milik pelanggan** — Mereka termasuk dalam akun pelanggan
- **Hanya untuk dibaca oleh penjual** — Anda dapat melihatnya tetapi tidak dapat mengubahnya
- **Terpisah dari pesanan** — Sebuah desain yang disimpan hanya menjadi pesanan ketika pelanggan menambahkannya ke keranjang dan menyelesaikan pembelian
- **Dapat digunakan kembali** — Pelanggan dapat memuat ulang desain yang disimpan, memodifikasinya, dan memesan beberapa kali

## Alur pemenuhan pesanan

### Alur kerja standar

1. **Menerima pesanan** — Pesanan muncul di daftar pesanan Anda dengan item kustomisasi
2. **Memverifikasi rendering** — Periksa bahwa snapshot desain menunjukkan **Rendered: Yes**. Jika rendering belum selesai, tunggu beberapa saat dan segarkan
3. **Unduh file** — Unduh file pemenuhan untuk setiap permukaan yang didesain
4. **Periksa kualitas** — Buka file dan verifikasi desain memenuhi standar kualitas cetak Anda (periksa DPI, posisi elemen, dan keterbacaan teks)
5. **Kirim ke produksi** — Kirimkan file ke penyedia cetak atau tim produksi Anda
6. **Kirim dan selesaikan** — Setelah produksi, kirimkan produk dan tandai pesanan sebagai selesai

### Contoh pemenuhan kaos

1. Pesanan diterima: "Custom Team T-shirt" dengan desain di depan dan belakang
2. Buka pesanan → lihat snapshot desain
3. Unduh `front.png` (300 DPI, 300x400mm) dan `back.png` (300 DPI, 300x400mm)
4. Kirimkan kedua file ke printer DTG Anda dengan warna pakaian dan ukuran dari pilihan variasi pesanan
5. Setelah dicetak dan diperiksa kualitas, kirimkan ke pelanggan

### Contoh pemenuhan poster

1. Pesanan diterima: "Custom A4 Poster" dengan satu permukaan yang didesain
2. Buka pesanan → lihat snapshot desain
3. Unduh `front.png` (300 DPI, 210x297mm dengan 3mm bleed)
4. Kirimkan ke layanan cetak poster Anda
5. Setelah dicetak dan dipotong, kirimkan ke pelanggan

## Penyelesaian masalah

**Masalah:** Snapshot desain menunjukkan "Rendered: No" dan rendering belum selesai

- **Penyebab:** Tugas rendering latar belakang mungkin gagal atau masih dalam proses
- **Solusi:** Tunggu beberapa menit. Jika rendering tidak selesai, periksa log tugas latar belakang. Anda juga dapat melihat data desain secara langsung dalam snapshot untuk memastikan desain pelanggan tetap terjaga

**Masalah:** File pemenuhan tampak berkualitas lebih rendah dari yang diharapkan

- **Penyebab:** Pelanggan mungkin mengunggah gambar resolusi rendah
- **Solusi:** Periksa pengaturan DPI permukaan. Jika peringatan DPI minimum dikonfigurasikan, pelanggan akan diberi peringatan selama proses desain. Untuk produk masa depan, pertimbangkan untuk meningkatkan persyaratan DPI minimum

**Masalah:** Pelanggan meminta perubahan pada desain mereka setelah memesan

- **Solusi:** Snapshot desain dirancang untuk tidak dapat diubah. Jika pelanggan membutuhkan perubahan, mereka harus membuat pesanan baru dengan desain yang diperbarui. Jika Anda setuju untuk membuat pengecualian, pelanggan dapat menggunakan desain yang disimpan mereka (jika mereka menyimpan satu) sebagai titik awal untuk pesanan baru

## Tips

- Selalu verifikasi bahwa rendering selesai sebelum memulai produksi.

Periksa bidang **Rendered** pada snapshot desain.
- Pertahankan pengaturan DPI yang sesuai dengan metode cetak Anda.

DPI yang lebih tinggi menghasilkan kualitas yang lebih baik tetapi ukuran file yang lebih besar. 300 DPI adalah standar untuk sebagian besar produk cetak profesional.
- Dorong pelanggan untuk menyimpan desain mereka sebelum memesan.

Simpan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

Jika terjadi masalah produksi dan pesanan perlu dibuat ulang, desain yang disimpan membuat pengorderingan ulang menjadi mudah.
- Buat buffer dalam jadwal produksi Anda untuk produk yang dapat dikustomisasi.

Berbeda dengan produk standar, setiap item memerlukan penanganan file secara individual.
- Jika Anda memproses volume pesanan yang tinggi yang dapat dikustomisasi, pertimbangkan untuk mengotomatisasi langkah unduh file dengan mengintegrasikan API penyedia cetak Anda.
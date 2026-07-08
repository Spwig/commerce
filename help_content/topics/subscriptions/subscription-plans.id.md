---
title: Rencana Langganan
---

Rencana langganan memungkinkan Anda menawarkan pembayaran berulang untuk produk Anda — ideal untuk barang konsumsi, layanan, kotak terpilih, atau produk apa pun yang dibeli pelanggan secara berulang. Panduan ini menjelaskan cara membuat dan mengonfigurasi rencana, menetapkan tingkatan harga, menambahkan masa uji coba, dan menambahkan opsi tambahan yang opsional.

## Memulai

Navigasikan ke **Langganan > Rencana Langganan** di bilah sisi admin. Daftar rencana menampilkan semua rencana Anda dengan model harganya, jumlah pelanggan aktif, dan status visibilitas.

Untuk membuat rencana baru, klik tombol **+ Tambah Rencana Langganan** — ini membuka wizard pembuatan rencana, yang memandu Anda melalui pengaturan langkah demi langkah.

![Daftar rencana langganan](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Informasi Rencana

Bagian pertama menangkap identitas inti dari rencana Anda.

- **Nama Rencana** — Nama yang dilihat pelanggan saat berlangganan. Klik ikon globe untuk menambahkan terjemahan untuk bahasa toko lain.
- **Slug** — Identifikasi yang ramah URL yang dihasilkan secara otomatis dari nama (misalnya, `premium-plan`). Ini digunakan secara internal dan dalam integrasi.
- **Deskripsi** — Teks opsional yang menggambarkan apa yang termasuk dalam rencana ini. Mendukung terjemahan.

## Model Harga

Pilih cara struktur harga untuk rencana ini:

| Model Harga | Terbaik Untuk |
|---------------|----------|
| **Harga Berlapis** | Menawarkan opsi komitmen bulanan, kuartalan, dan tahunan dengan diskon untuk masa yang lebih lama |
| **Berdasarkan Kuantitas** | Harga per tempat duduk atau per pengguna di mana totalnya berkembang seiring kuantitas (misalnya, lisensi tim) |
| **Harga Tetap** | Harga tetap tunggal tanpa variasi |

Untuk rencana **Berdasarkan Kuantitas**, tetapkan **Kuantitas Minimum** (jumlah tempat duduk minimum yang diperlukan) dan secara opsional **Kuantitas Maksimum** untuk membatasi jumlah tempat duduk yang dapat dibeli pelanggan.

## Tingkatan Harga

Tingkatan harga mendefinisikan frekuensi pembayaran dan opsi diskon yang tersedia bagi pelanggan di rencana ini. Tambahkan mereka di bagian **Tingkatan Harga** di bawah formulir utama.

Setiap tingkatan memiliki bidang berikut:

- **Nama Tingkatan** — Label yang ditampilkan kepada pelanggan (misalnya, `Bulanan`, `Tahunan — Hemat 20%`). Mendukung terjemahan.
- **Siklus Pembayaran** — Seberapa sering pelanggan dikenakan biaya: Harian, Mingguan, Bulanan, Kuartalan, Setengah Tahunan, atau Tahunan.
- **Interval Pembayaran** — Pengali untuk siklus pembayaran. Tetapkan ke `2` dengan Bulanan untuk menagih setiap 2 bulan.
- **Persentase Diskon** — Diskon yang diterapkan pada harga produk untuk tingkatan ini. Tetapkan ke `0` untuk harga penuh, atau `20` untuk memberikan diskon 20%. Diskon ini ditumpuk di atas harga penjualan apa pun pada produk itu sendiri.
- **Tingkatan Default** — Tandai satu tingkatan sebagai default untuk memilih secara otomatis saat pelanggan melihat opsi langganan.

### Contoh: rencana berlapis dengan tiga opsi

Untuk rencana langganan "Coffee Club":

| Nama Tingkatan | Siklus Pembayaran | Diskon |
|-----------|---------------|----------|
| Bulanan | Bulanan | 0% |
| Kuartalan — Hemat 10% | Kuartalan | 10% |
| Tahunan — Hemat 20% | Tahunan | 20% |

## Masa Uji Coba

Masa uji coba memungkinkan pelanggan mencoba langganan Anda sebelum pembayaran penuh pertama mereka. Konfigurasikan ini di bagian **Masa Uji Coba**:

- **Masa Uji Coba (Hari)** — Jumlah hari uji coba gratis. Tetapkan ke `0` untuk menonaktifkan uji coba. Maksimum 365 hari.
- **Harga Uji Coba** — Harga tereduksi opsional selama masa uji coba (misalnya, $1 untuk bulan pertama). Biarkan kosong untuk uji coba sepenuhnya gratis.

## Kebijakan Pembatalan

Kontrol cara pelanggan dapat membatalkan langganan mereka di bagian **Kebijakan Pembatalan**:

| Kebijakan | Deskripsi |
|--------|-------------|
| **Batal Kapan Saja** | Pelanggan dapat membatalkan segera kapan saja |
| **Batal di Akhir Periode** | Pembatalan berlaku di akhir periode berbayar — pelanggan tetap memiliki akses hingga berakhir |
| **Komitmen Minimum Diperlukan** | Pelanggan harus menyelesaikan jumlah siklus pembayaran minimum sebelum membatalkan |

Pengaturan tambahan:

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- **Minimum Commitment (Cycles)** — Ketika menggunakan kebijakan komitmen, tetapkan jumlah siklus pembayaran yang diperlukan (misalnya, `3` untuk komitmen minimum 3 bulan).
- **Grace Period (Days)** — Hari akses terus-menerus setelah kegagalan pembayaran sebelum langganan dibatasi.

Setel ke `0` untuk pembatasan segera.
- **Reactivation Period (Days)** — Hari setelah pembatalan selama pelanggan dapat mengaktifkan kembali langganan mereka tanpa perlu mendaftar ulang dari awal.

## Perilaku perubahan rencana

Ketika pelanggan meningkatkan atau menurunkan antar rencana, Anda dapat mengontrol kapan perubahan berlaku:

- **Upgrade Behavior** — Setel ke **Immediate** (tagih jumlah prorata sekarang) atau **At Renewal** (ubah pada tanggal pembayaran berikutnya).
- **Downgrade Behavior** — Setel ke **Immediate** (terapkan kredit ke tagihan berikutnya) atau **At Renewal** (ubah pada tanggal pembayaran berikutnya).

## Batasan dan pembatasan

- **Maximum Billing Cycles** — Jumlah total siklus pembayaran sebelum langganan berakhir secara otomatis. Biarkan kosong untuk pembayaran berulang tanpa batas. Berguna untuk rencana cicilan atau langganan berbatas waktu.
- **Setup Fee** — Biaya satu kali yang dikumpulkan saat langganan pertama kali dibuat (misalnya, biaya onboarding atau aktivasi). Setel ke `0.00` untuk tidak ada biaya setup.

## Add-on rencana

Add-on adalah tambahan opsional yang dapat pelanggan lampirkan ke rencana mereka. Tambahkan di bagian **Plan Add-ons**:

- **Add-on Name** — Nama yang ditampilkan kepada pelanggan. Mendukung terjemahan.
- **Description** — Apa yang ditawarkan oleh add-on.
- **Price** — Biaya add-on.
- **Billing Frequency** — Apakah add-on dikenakan **Per Billing Cycle** (berulang) atau **One-Time** saat awal langganan.
- **Allow Quantity** — Aktifkan untuk memungkinkan pelanggan membeli beberapa unit add-on.
- **Required** — Centang untuk secara otomatis menyertakan add-on pada semua langganan baru. Add-on yang diperlukan tidak dapat dihapus oleh pelanggan.

## Visibilitas dan status

- **Active** — Nonaktifkan untuk menonaktifkan rencana sehingga tidak ada langganan baru yang dapat dibuat. Langganan yang sudah ada tidak terpengaruh.
- **Public** — Nonaktifkan untuk menyembunyikan rencana dari halaman pelanggan (berguna untuk rencana internal atau lama yang tetap digunakan oleh pelanggan yang sudah berlangganan).
- **Sort Order** — Mengontrol urutan tampilan pada halaman pemilihan langganan. Angka yang lebih rendah muncul lebih dulu.

## Tips

- Gunakan **periode uji coba** untuk mengurangi keraguan — bahkan uji coba gratis singkat selama 7 hari dapat meningkatkan signifikan tingkat konversi pada produk langganan.
- Atur **tiga tingkat harga** (bulanan, kuartalan, tahunan) dengan diskon yang meningkat untuk mendorong komitmen tahunan dan meningkatkan aliran kas Anda.
- Untuk langganan berbasis layanan, atur **Kebijakan Pembatalan** ke **Cancel at Period End** sehingga pelanggan tetap memiliki akses selama periode yang telah dibayar — ini terasa adil dan mengurangi pembatalan pembayaran.
- Pertahankan **Grace Period** selama 3–7 hari untuk kegagalan pembayaran. Ini memberi pelanggan waktu untuk memperbarui metode pembayaran sebelum kehilangan akses.
- Gunakan bendera **Required** pada add-on secara jarang — hanya gunakan untuk hal-hal yang benar-benar wajib (misalnya, perjanjian layanan), bukan sebagai cara untuk memperbesar harga.
- Nonaktifkan rencana yang tidak memiliki pelanggan daripada menghapusnya — ini mempertahankan data historis untuk pelanggan yang sebelumnya berlangganan.
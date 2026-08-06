---
title: Rencana Langganan
---

Rencana langganan memungkinkan Anda menawarkan pembayaran berulang untuk produk Anda — idealnya untuk barang habiskan, layanan, kotak yang dikuratori, atau produk apa pun yang pelanggan beli berulang kali. Panduan ini menjelaskan cara membuat dan mengkonfigurasi rencana, menyiapkan tingkatan harga, menambahkan periode percobaan, dan menghubungkan tambahan opsional.

## Mulai dari awal

Navigasi ke **Langganan > Rencana Langganan** di bilah sisi admin. Daftar rencana menunjukkan semua rencana Anda dengan model harga, jumlah pelanggan aktif, dan status visibilitasnya.

Untuk membuat rencana baru, klik tombol **+ Tambahkan Rencana Langganan** — ini membuka wizard pembuatan rencana, yang memandu Anda melalui langkah-langkah pemasangan secara bertahap.

![Daftar rencana langganan](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Sebuah rencana sendiri tidak bisa dibeli — ini adalah template. Setelah Anda membangunnya di sini, sertakan dalam satu atau beberapa produk dari tab **Langganan** produk (hanya produk Sederhana, Variabel, dan Digital) agar pelanggan sebenarnya dapat berlangganan. Lihat [Penjualan Produk sebagai Langganan](/help/selling-products-as-subscriptions) untuk langkah tersebut.

## Informasi Rencana

Bagian pertama ini menangkap identitas inti dari rencana Anda.

- **Nama Rencana** — Nama yang dilihat pelanggan saat berlangganan. Klik ikon globe untuk menambahkan terjemahan untuk bahasa toko lainnya.
- **Slug** — Identifikasi yang ramah URL yang dihasilkan secara otomatis dari nama (misalnya, `premium-plan`). Ini digunakan secara internal dan dalam integrasi.
- **Deskripsi** — Teks opsional yang menjelaskan apa saja yang termasuk dalam rencana ini. Mendukung terjemahan.

## Model Harga

Pilih bagaimana struktur harga untuk rencana ini:

| Model Harga | Paling Cocok untuk |
|---------------|----------|
| **Harga Tiered** | Menawarkan opsi komitmen bulanan, kuartalan, dan tahunan dengan diskon untuk jangka yang lebih lama |
| **Berdasarkan Jumlah** | Harga per kursi atau pengguna di mana totalnya meningkat sesuai jumlah (misalnya, lisensi tim) |
| **Tarif Tetap** | Harga tetap tunggal tanpa variasi |

Untuk rencana **Berdasarkan Jumlah**, tetapkan **Jumlah Minimum** (jumlah kursi minimal yang diperlukan) dan secara opsional **Jumlah Maksimum** untuk membatasi jumlah kursi yang dapat dibeli oleh pelanggan.

## Tingkatan Harga

Tingkatan harga menentukan frekuensi pembayaran dan opsi diskon yang tersedia bagi pelanggan pada rencana ini. Tambahkan di bagian **Tingkatan Harga** di bawah formulir utama.

Setiap tingkatan memiliki bidang berikut:

- **Nama Tingkatan** — Label yang ditampilkan kepada pelanggan (misalnya, `Bulanan`, `Tahunan — Hemat 20%`). Mendukung terjemahan.
- **Siklus Pembayaran** — Seberapa sering pelanggan dibebankan: Harian, Mingguan, Bulanan, Kuartalan, Semi-Annual, atau Tahunan.
- **Interval Pembayaran** — Pengali untuk siklus pembayaran. Atur ke `2` dengan Bulanan untuk menagih setiap 2 bulan.
- **Persentase Diskon** — Diskon yang diterapkan pada harga produk untuk tingkatan ini. Atur ke `0` untuk harga penuh, atau `20` untuk memberi diskon 20%. Diskon ini ditambahkan pada harga penjualan apa pun pada produk itu sendiri.
- **Tingkatan Default** — Tandai satu tingkatan sebagai default untuk memilihnya secara otomatis bagi pelanggan saat mereka melihat opsi langganan.

Diskon berlaku sejak siklus pembayaran pertama pelanggan, bukan hanya pada pembaruan — tingkatan dengan diskon 20% membebankan 20% diskon sejak hari pertama (atau dari pembayaran pertama setelah percobaan, jika rencana memiliki satu).

### Contoh: rencana tiered dengan tiga opsi

Untuk rencana langganan "Kopi Club":

| Nama Tingkatan | Siklus Pembayaran | Diskon |
|-----------|---------------|----------|
| Bulanan | Bulanan | 0% |
| Kuartalan — Hemat 10% | Kuartalan | 10% |
| Tahunan — Hemat 20% | Tahunan | 20% |

## Masa Percobaan

Masa percobaan memungkinkan pelanggan mencoba langganan Anda sebelum pembayaran penuh pertama mereka. Atur ini di bagian **Masa Percobaan**:

- **Masa Percobaan (Hari)** — Jumlah hari percobaan gratis. Atur ke `0` untuk menonaktifkan percobaan. Maksimalnya 365 hari.
- **Harga Percobaan** — Harga yang direduksi secara opsional selama masa percobaan (misalnya, $1 untuk bulan pertama). Biarkan kosong untuk uji coba sepenuhnya gratis.

## Kebbijakan Pembatalan

Atur bagaimana pelanggan dapat membatalkan langganan mereka di bagian **Kebijakan Pembatalan**:

| Kebijakan | Deskripsi |
|--------|-------------|
| **Batalkan Kapan Saja** | Pelanggan dapat membatalkan kapan saja |
| **Batalkan di Akhir Masa** | Pembatalan berlaku di akhir periode berbayar — pelanggan tetap memiliki akses hingga masa berlaku berakhir |
| **Kewajiban Minimal Dibutuhkan** | Pelanggan harus menyelesaikan jumlah siklus pembayaran minimal sebelum membatalkan |

Tambahan pengaturan:

- **Kewajiban Minimal (Siklus)** — Ketika menggunakan kebijakan kewajiban, tetapkan jumlah siklus pembayaran yang diperlukan (misalnya, `3` untuk kewajiban minimal 3 bulan).
- **Masa Percaya (Hari)** — Hari akses berkelanjutan setelah kegagalan pembayaran sebelum langganan dihentikan. Atur menjadi `0` untuk penghentian segera.
- **Masa Aktif Kembali (Hari)** — Hari setelah pembatalan selama pelanggan dapat mengaktifkan ulang langganan mereka tanpa harus berlangganan dari awal.

## Perilaku Perubahan Rencana

Ketika pelanggan meningkatkan atau menurunkan rencana, Anda dapat mengontrol kapan perubahan tersebut berlaku:

- **Perilaku Peningkatan** — Atur menjadi **Langsung** (menebus jumlah yang sesuai sekarang) atau **Pada Saat Perpanjangan** (berpindah pada tanggal pembayaran berikutnya).
- **Perilaku Penurunan** — Atur menjadi **Langsung** (menerapkan kredit pada tagihan berikutnya) atau **Pada Saat Perpanjangan** (berpindah pada tanggal pembayaran berikutnya).

## Batasan dan keterbatasan

- **Jumlah Siklus Pembayaran Maksimal** — Jumlah total siklus pembayaran sebelum langganan berakhir secara otomatis. Biarkan kosong untuk pembayaran berulang tak terbatas. Berguna untuk rencana cicilan atau langganan berdurasi terbatas.
- **Biaya Pemasangan** — Biaya satu kali yang dikumpulkan ketika langganan dibuat pertama kali (misalnya, biaya onboarding atau aktivasi). Atur menjadi `0.00` untuk tidak ada biaya pemasangan.

## Tambahan Rencana

Tambahan adalah ekstra opsional yang dapat ditambahkan pelanggan ke rencana mereka. Tambahkan di bagian **Tambahan Rencana**:

- **Nama Tambahan** — Nama yang ditampilkan kepada pelanggan. Mendukung terjemahan.
- **Deskripsi** — Apa yang ditawarkan tambahan tersebut.
- **Harga** — Biaya tambahan tersebut.
- **Frekuensi Pembayaran** — Apakah tambahan dikenakan biaya **Per Siklus Pembayaran** (berulang) atau **Satu Kali** saat pendaftaran.
- **Izinkan Jumlah** — Aktifkan untuk memungkinkan pelanggan membeli beberapa unit tambahan.
- **Wajib** — Centang ini untuk secara otomatis termasuk tambahan pada semua langganan baru. Tambahan yang wajib tidak dapat dihapus oleh pelanggan.

## Visibilitas dan status

- **Aktif** — Nonaktifkan untuk menonaktifkan rencana sehingga tidak ada langganan baru yang dapat dibuat. Langganan yang sudah ada tidak terpengaruh.
- **Umum** — Nonaktifkan untuk menyembunyikan rencana dari halaman yang terlihat pelanggan (berguna untuk rencana internal atau lama yang tetap diikuti pelanggan saat ini).
- **Urutan Pemesanan** — Mengontrol urutan tampilan pada halaman pemilihan langganan. Angka yang lebih rendah muncul lebih dulu.

## Saran

- Gunakan **masa percobaan** untuk mengurangi keraguan — bahkan masa percobaan 7 hari singkat pun dapat meningkatkan tingkat konversi secara signifikan pada produk langganan.
- Atur **tiga tingkatan harga** (bulanan, kuartalan, tahunan) dengan diskon yang meningkat untuk mendorong komitmen tahunan dan meningkatkan aliran kas Anda.
- Untuk langganan berbasis layanan, tetapkan **Kebijakan Pembatalan** menjadi **Batalkan di Akhir Masa** agar pelanggan tetap memiliki akses hingga masa berbayar mereka — ini terasa adil dan mengurangi klaim pembatalan pembayaran.
- Pertahankan **Masa Percaya** pada 3–7 hari untuk kegagalan pembayaran. Hal ini memberi waktu kepada pelanggan untuk memperbarui metode pembayaran mereka sebelum kehilangan akses.
- Gunakan bendera **Wajib** pada tambahan secara terbatas — hanya gunakan untuk hal-hal yang benar-benar wajib (misalnya, perjanjian layanan), bukan sebagai cara untuk menaikkan harga.
- Nonaktifkan rencana yang tidak memiliki pelanggan alih-alih menghapusnya — ini mempertahankan data historis untuk pelanggan mana pun yang pernah berlangganan.
---
title: Menjual Produk sebagai Langganan
---

Setiap produk Sederhana, Variabel, atau Digital kini dapat dijual secara berulang, baik bersamaan — atau sebagai pengganti — pembelian sekali bayar. Panduan ini mencakup cara mengaktifkan langganan untuk produk, memilih rencana mana yang dapat dipilih pelanggan, dan apa yang sebenarnya dilihat oleh pelanggan saat membeli.

## Jenis produk apa saja yang dapat dijual sebagai langganan

Langganan hanya tersedia untuk jenis produk berikut:

| Memenuhi syarat | Tidak memenuhi syarat |
|----------|---------------|
| Produk Sederhana | Paket Produk |
| Produk Variabel | Kartu Hadiah |
| Produk Digital | Produk yang Dapat Disesuaikan |
| | Produk Konfigurabel |
| | Produk Pemesanan |

Alasannya adalah pengiriman, bukan harga: langganan mengenakan biaya ulang kepada pelanggan setiap siklusnya dan mengirim ulang produk melalui pesanan baru setiap kalinya. Spwig tahu bagaimana mengirim ulang produk Sederhana atau Variabel dan mengizinkan ulang unduhan atau lisensi produk Digital setiap kali berlangganan — tetapi tidak dapat menjalankan ulang pemberian kartu hadiah, paket komponen ganda, penyesuaian pengguna yang disimpan, bangunan konfigurator, atau slot pemesanan secara berkala secara aman. Memungkinkan jenis-jenis ini dijual sebagai langganan akan berisiko mengambil uang pelanggan pada siklus kedua tanpa dapat mengirimkan apapun.

Centang **Aktifkan Langganan** sendiri tidak disembunyikan atau dilemahkan untuk jenis yang tidak memenuhi syarat — Anda secara teknis dapat mengeceknya pada setiap produk. Jika Anda mencoba menyimpan produk Kartu Hadiah, Paket, yang Dapat Disesuaikan, Konfigurabel, atau Pemesanan dengan langganan yang diaktifkan, Spwig akan menolak penyimpanan dengan pesan kesalahan validasi yang menjelaskan bahwa jenis produk ini tidak dapat dijual sebagai langganan. Ubah dulu **Jenis Produk** (tab Informasi Dasar), atau nonaktifkan langganan untuk produk tersebut.

## Mengaktifkan langganan pada produk

1. Navigasi ke **Produk > Semua Produk** dan buka produk yang ingin Anda jual sebagai langganan (atau buat yang baru).
2. Pastikan **Jenis Produk** pada tab Informasi Dasar adalah Sederhana, Variabel, atau Digital.
3. Klik tab **Langganan**.
4. Centang **Aktifkan Langganan**.
5. Pada bidang **Rencana Langganan**, pilih satu atau lebih rencana yang ingin produk ini tawarkan. Anda hanya dapat memilih rencana yang sudah ada — jika Anda belum membuatnya, lihat [Rencana Langganan](/help/subscription-plans) terlebih dahulu.
6. Atur dua kotak centang mode pembelian (di bawahnya).
7. Klik **Simpan**.

![Tab Langganan dari formulir edit produk: Centang **Aktifkan Langganan**, rencana dipilih di daftar Rencana Langganan, dan kotak centang **Izinkan Pembelian Sekali Bayar** dan **Default ke Langganan**](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Menghubungkan rencana langganan

Sebuah **Rencana Langganan** adalah template yang dapat digunakan kembali — opsi siklus pembayaran, uji coba, biaya pemasangan, aturan pembatalan — yang Anda buat sekali dan dapat Anda hubungkan ke berbagai produk yang memenuhi syarat. Kolom **Rencana Langganan** pada tab Langganan produk adalah tempat Anda menghubungkan produk dengan rencana yang ingin dijualnya.

Anda dapat menghubungkan lebih dari satu rencana ke produk yang sama. Hal ini berguna ketika, misalnya, Anda ingin menawarkan tingkatan berlangganan "Standar" dan "Premi" untuk item yang sama — setiap rencana dapat membawa kebijakan harga, uji coba, dan pembatalan yang berbeda. Ketika produk memiliki lebih dari satu rencana yang terhubung, pelanggan melihat pemilih rencana di halaman produk sebelum memilih frekuensi pembayaran.

## Mengontrol pembelian sekali bayar vs. langganan

Dua kotak centang di tab Langganan mengontrol bagaimana pelanggan dapat membeli produk:

- **Izinkan Pembelian Sekali Bayar** — Aktif secara default.

Jika dicentang, pelanggan memilih antara pembelian sekali bayar biasa dan berlangganan.

Nonaktifkan untuk membuat produk menjadi khusus langganan — setiap pembelian menjadi pesanan berulang, dan tidak ada opsi sekali bayar yang ditampilkan sama sekali.
- **Default ke Langganan** — Memilih opsi langganan (dan rencana/tier default) ketika halaman produk dimuat, alih-alih membuat pelanggan memilihnya secara aktif.

Ini hanya berdampak ketika **Izinkan Pembelian Sekali** dicentang — jika pembelian sekali di nonaktifkan, produk hanya berlangganan terlepas dari pengaturan ini.

Gunakan **Default ke Berlangganan** untuk produk di mana pengiriman berulang adalah harapan alami (kopi, suplemen, barang habiskan) — hal ini mengurangi satu klik dan membantu pelanggan menuju opsi yang membuat mereka kembali membeli, tanpa menghilahkan kemampuan mereka untuk membeli sekali saja.

## Yang dilihat pelanggan

### Di halaman produk

Ketika produk memiliki langganan yang diaktifkan dan setidaknya satu rencana yang aktif dan umum, selector mode pembelian muncul di halaman produk:

![Selector pembelian toko dengan "Langganan & Hemat" dipilih: tombol "Pembelian Sekali" vs "Langganan & Hemat" di atas daftar frekuensi pengiriman yang menunjukkan tingkat tahunan (Hemat 20%), bulanan, dan kuartalan (Hemat 10%) dengan harga, ditambah uji coba, pembatalan, dan catatan pembayaran](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- Jika pembelian sekali diperbolehkan, pelanggan melihat pilihan **"Pembelian Sekali"** vs **"Langganan & Hemat"**, yang defaultnya sesuai dengan mode yang Anda konfigurasi.
- Jika produk memiliki lebih dari satu rencana yang terpasang, pengatur rencana muncul ketika "Langganan & Hemat" dipilih.
- Untuk rencana yang dipilih, pelanggan melihat daftar **frekuensi pengiriman** yang dibangun dari tingkat harga rencana tersebut (misalnya, Bulanan, Kuartalan, Tahunan), masing-masing menunjukkan harganya dan **label "Hemat X%"** ketika tingkat tersebut memiliki diskon.
- Durasi uji coba, biaya pemasangan, dan kebijakan pembatalan rencana (misalnya, "Batal kapan saja") ditampilkan bersama daftar tingkat, beserta catatan bahwa metode pembayaran ditambahkan saat checkout.

### Di keranjang belanja dan saat checkout

Baris langganan di keranjang belanja memiliki **label Langganan**, cadence pembayaran (misalnya, "Setiap bulan"), dan catatan uji coba jika berlaku, sehingga pelanggan tahu baris mana yang berulang. Saat checkout, pelanggan memilih penyedia pembayaran seperti biasa — inilah metode pembayaran yang akan dicicil pada peninjauan berikutnya.

> **Keterbatasan yang diketahui:** Menyimpan kartu pelanggan secara otomatis untuk peninjauan langganan di masa depan saat checkout masih dalam proses koneksi untuk beberapa penyedia pembayaran. Hingga penyedia tertentu mendukung ini, langganan yang ditempatkan melalui penyedia tersebut mungkin memerlukan tindak lanjut tambahan (misalnya, menghubungi pelanggan untuk detail pembayaran yang diperbarui sebelum peninjauan) daripada sepenuhnya tanpa tindakan sejak awal. Periksa pengaturan penyedia pembayaran Anda jika Anda melihat peninjauan tidak menarik secara otomatis untuk langganan.

## Tips

- Buat dan uji rencana langganan terlebih dahulu (tingkat harga, uji coba, kebijakan pembatalan), lalu sertakan dalam produk — lebih mudah untuk mendapatkan rencana yang benar daripada memperbaikinya di beberapa produk nanti.
- Biarkan **Izinkan Pembelian Sekali** dicentang untuk sebagian besar produk. Sisihkan produk yang hanya berlangganan untuk kasus di mana pembelian sekali memang tidak masuk akal bagi bisnis Anda.
- Jika Anda mengubah produk best-seller lama menjadi opsi langganan, nonaktifkan **Default ke Berlangganan** terlebih dahulu agar tidak mengganggu pelanggan yang terbiasa membelinya sekali — aktifkan nanti setelah Anda melihat bagaimana respons pelanggan berlangganan.
- Produk digital adalah pilihan yang sangat baik untuk langganan (lisensi perangkat lunak, keanggotaan konten) karena peninjauan mengaktifkan akses secara otomatis tanpa pengiriman.
- Jika Anda membutuhkan jenis produk yang tidak memenuhi syarat (misalnya, paket atau barang yang dapat disesuaikan) untuk dijual secara berkala, pertimbangkan apakah versi sederhana atau digital yang setara bisa membawa langganan alih-alihnya.

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.
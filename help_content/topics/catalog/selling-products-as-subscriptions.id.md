---
title: Menjual Produk sebagai Langganan
---

Setiap produk Sederhana, Variabel, atau Digital kini dapat dijual secara berkala, sejalan — atau sebagai pengganti — pembelian sekali waktu. Panduan ini mencakup cara mengaktifkan langganan untuk produk, memilih rencana mana yang pelanggan bisa pilih, dan apa yang sebenarnya dilihat pelanggan saat membeli.

<!-- screenshots-needed:
- url: /admin/catalog/product/{id}/change/
  filename: subscriptions-tab.webp
  description: Form edit produk dengan tab Langganan aktif, menunjukkan
    Centang Enable Subscription, satu atau lebih rencana yang dipilih di bidang Rencana Langganan, dan kotak centang Allow One-Time Purchase / Default to Subscription
    terlihat.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
- url: (storefront) halaman detail produk untuk produk yang diaktifkan langganan
  filename: subscribe-and-save-selector.webp
  description: Pemilih "Pembelian Sekali waktu" vs "Langganan & Hemat" yang diperluas,
    menunjukkan daftar tingkat frekuensi pengiriman dengan badge "Hemat X%" pada tingkat yang didiskon.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
  notes: Membutuhkan produk yang diaktifkan langganan dengan setidaknya satu rencana aktif
    publik dan tingkatan harga, dilihat dari toko (bukan admin).
-->

## Jenis produk apa saja yang bisa dijual sebagai langganan

Langganan hanya tersedia untuk jenis produk berikut:

| Memenuhi syarat | Tidak memenuhi syarat |
|----------|---------------|
| Produk Sederhana | Bundle Produk |
| Produk Variabel | Kartu Hadiah |
| Produk Digital | Produk yang Dapat Disesuaikan |
| | Produk Konfigurabel |
| | Produk Pemesanan |

Alasannya adalah pelayanan, bukan harga: langganan mengenakan biaya ulang kepada pelanggan setiap siklus dan mengirim ulang produk melalui pesanan baru setiap kalinya. Spwig tahu cara mengirim ulang produk Sederhana atau Variabel dan mengizinkan ulang unduhan atau lisensi produk Digital setiap kali berlangganan — tetapi tidak bisa secara aman menjalankan kembali pemberian kartu hadiah, bundle komponen multi, penyesuaian pengguna yang disimpan, bangunan konfigurator, atau slot pemesanan secara berkala. Memungkinkan jenis-jenis ini dijual sebagai langganan akan berisiko mengambil uang pelanggan di siklus 2 tanpa dapat mengirimkan apa pun.

Centang **Aktifkan Langganan** sendiri tidak disembunyikan atau dilemahkan untuk jenis yang tidak memenuhi syarat — Anda secara teknis bisa mengeceknya pada setiap produk. Jika Anda mencoba menyimpan produk Kartu Hadiah, Bundle, yang Dapat Disesuaikan, Konfigurabel, atau Pemesanan dengan langganan yang diaktifkan, Spwig akan menolak penyimpanan dengan pesan kesalahan validasi yang menjelaskan bahwa jenis produk ini tidak bisa dijual sebagai langganan. Ubah dulu **Jenis Produk** (tab Informasi Dasar), atau biarkan langganan dimatikan untuk produk tersebut.

## Mengaktifkan langganan pada produk

1. Navigasi ke **Produk > Semua Produk** dan buka produk yang ingin Anda jual sebagai langganan (atau buat yang baru).
2. Pastikan **Jenis Produk** pada tab Informasi Dasar adalah Sederhana, Variabel, atau Digital.
3. Klik tab **Langganan**.
4. Centang **Aktifkan Langganan**.
5. Di bidang **Rencana Langganan**, pilih satu atau lebih rencana yang ingin produk ini tawarkan. Anda hanya bisa memilih rencana yang sudah ada — jika Anda belum membuatnya, lihat [Rencana Langganan](/help/subscription-plans) terlebih dahulu.
6. Konfigurasikan dua kotak centang mode pembelian (di bawahnya).
7. Klik **Simpan**.

## Menambahkan rencana langganan

Sebuah **Rencana Langganan** adalah template yang dapat digunakan kembali — opsi siklus pembayaran, uji coba, biaya pemasangan, aturan pembatalan — yang Anda buat sekali dan bisa Anda sertakan pada sejumlah produk yang memenuhi syarat. Kolom **Rencana Langganan** pada tab Langganan produk adalah tempat Anda menghubungkan produk dengan rencana yang ingin dijual.

Anda dapat menambahkan lebih dari satu rencana ke produk yang sama.

Ini berguna ketika, misalnya, Anda ingin menawarkan tingkatan berlangganan "Standar" dan "Premi" untuk item yang sama — setiap rencana dapat membawa kebijakan harga sendiri, uji coba, dan pembatalan.


Ketika sebuah produk memiliki lebih dari satu rencana yang terkait, pelanggan akan melihat pilihan rencana di halaman produk sebelum memilih frekuensi pembayaran.

## Mengontrol pembelian sekali bayar vs langganan

Dua kotak centang di tab Subscriptions mengontrol bagaimana pelanggan dapat membeli produk:

- **Izinkan Pembelian Sekali Bayar** — Aktif secara default. Ketika dicentang, pelanggan memilih antara pembelian sekali bayar biasa dan berlangganan. Nonaktifkan untuk membuat produk menjadi khusus berlangganan — setiap pembelian menjadi pesanan berulang, dan tidak ada opsi sekali bayar sama sekali.
- **Default ke Langganan** — Memilih opsi langganan secara default (dan tingkat rencananya) ketika halaman produk dimuat, alih-alih membuat pelanggan memilih secara aktif. Hal ini hanya berdampak ketika **Izinkan Pembelian Sekali Bayar** juga dicentang — jika pembelian sekali bayar dimatikan, produk menjadi khusus berlangganan terlepas dari pengaturan ini.

Gunakan **Default ke Langganan** untuk produk di mana pengiriman berulang adalah harapan alami (kopi, suplemen, produk habiskan) — ini menghilangkan satu klik dan mengarahkan pelanggan ke opsi yang membuat mereka kembali, tanpa menghilangkan kemampuan mereka untuk membeli sekali saja.

## Yang dilihat pelanggan

### Di halaman produk

Ketika produk memiliki langganan yang diaktifkan dan setidaknya satu rencana aktif, pilihan mode pembelian muncul di halaman produk:

- Jika pembelian sekali bayar diizinkan, pelanggan melihat pilihan **"Pembelian Sekali Bayar"** vs **"Langganan & Hemat"**, defaultnya sesuai mode yang Anda konfigurasi.
- Jika produk memiliki lebih dari satu rencana yang terkait, pengganti rencana muncul setelah **"Langganan & Hemat"** dipilih.
- Untuk rencana yang dipilih, pelanggan melihat daftar **frekuensi pengiriman** yang dibangun dari tingkat harga rencana tersebut (misalnya, Bulanan, Kuartalan, Tahunan), masing-masing menunjukkan harganya dan **label "Hemat X%"** ketika tingkat tersebut memiliki diskon.
- Durasi percobaan, biaya pemasangan, dan kebijakan pembatalan rencana (misalnya, "Batal kapan saja") ditampilkan bersama daftar tingkat, serta catatan bahwa metode pembayaran ditambahkan saat checkout.

### Di keranjang belanja dan saat checkout

Baris langganan di keranjang belanja memiliki label **"Langganan"**, frekuensi pembayaran (misalnya, "Setiap bulan"), dan catatan percobaan jika berlaku, sehingga pelanggan tahu mana baris yang berulang. Saat checkout, pelanggan memilih penyedia pembayaran seperti biasa — inilah metode pembayaran yang akan dicicil pada penyelesaian berikutnya.

> **Keterbatasan yang diketahui:** Menyimpan kartu pelanggan secara otomatis untuk penyelesaian langganan berikutnya masih dalam proses koneksi untuk beberapa penyedia pembayaran. Hingga penyedia tertentu mendukung ini, langganan yang ditempatkan melalui penyedia tersebut mungkin memerlukan tindak lanjut tambahan (misalnya, menghubungi pelanggan untuk detail pembayaran yang diperbarui sebelum penyelesaian) daripada sepenuhnya bebas masalah sejak awal. Periksa penyiapan penyedia pembayaran Anda jika Anda melihat penyelesaian tidak menarik secara otomatis untuk langganan.

## Tips

- Buat dan uji rencana langganan terlebih dahulu (tingkat harga, masa percobaan, kebijakan pembatalan), lalu sertakan dalam produk — lebih mudah untuk mendapatkan rencana yang benar daripada memperbaikinya di beberapa produk nanti.
- Biarkan **Izinkan Pembelian Sekali Bayar** dicentang untuk sebagian besar produk. Sisihkan produk khusus berlangganan untuk kasus di mana pembelian sekali bayar benar-benar tidak masuk akal bagi bisnis Anda.
- Jika Anda mengubah produk best-seller lama menjadi opsi langganan, pertahankan **Default ke Langganan** dimatikan terlebih dahulu agar tidak mengganggu pelanggan yang terbiasa membelinya sekali — nyalakan nanti setelah Anda melihat bagaimana respons pelanggan berlangganan.
- Produk digital adalah pilihan yang sangat baik untuk langganan (lisensi perangkat lunak, keanggotaan konten) karena penyelesaian ulang secara otomatis memberi akses kembali tanpa ada pengiriman yang terlibat.
- Jika Anda membutuhkan jenis produk yang tidak memenuhi syarat (misalnya, paket atau item yang dapat disesuaikan) untuk dijual secara berulang, pertimbangkan apakah versi sederhana atau digital yang setara bisa membawa langganan alih-alihnya.
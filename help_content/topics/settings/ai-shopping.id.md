---
title: Belanja AI
---

Belanja AI memungkinkan asisten belanja AI menemukan produk Anda, dan, ketika Anda mengizinkannya, membeli dari toko Anda atas nama pelanggan. Fitur ini **dimatikan secara default** — mengaktifkannya adalah pilihan yang disengaja, dan hingga Anda melakukannya, toko Anda tidak menampilkan apa pun kepada asisten-asisten ini.

## Mengaktifkannya

Buka **Pengaturan → Belanja AI** dan aktifkan **Agentic commerce**. Sejak saat itu, asisten-asisten yang mendukung Protokol Perdagangan Universal dapat menemukan toko Anda dan membaca daftar produk Anda. Tidak ada yang berubah pada toko fisik biasa Anda.

## Dashboard kesiapan

Bagian atas halaman Belanja AI menjawab satu pertanyaan dalam satu kalimat: **Apakah asisten AI sebenarnya bisa membeli dari toko Anda sekarang?**

- **"Asisten AI dapat membeli dari toko Anda"** — segala sesuatu yang diperlukan untuk pembelian sudah tersedia.
- **"Asisten AI dapat menjelajahi toko Anda, tetapi belum bisa membeli"** — toko Anda dapat ditemukan, tetapi sesuatu yang hilang sebelum pembelian dapat selesai (biasanya penyedia pembayaran yang terhubung).
- **"Stop darurat aktif"** atau **"Agentic commerce dimatikan"** — tidak ada yang diberikan kepada asisten.

Di bawah keputusan tersebut, Anda akan melihat daftar periksa singkat — penyedia pembayaran terhubung, pengiriman dapat ditawarkan, produk terlihat oleh asisten — dengan petunjuk di samping apa pun yang masih memerlukan perhatian. Pengecekan menunjukkan berapa banyak produk yang dapat dijual asisten, berapa banyak yang telah Anda sembunyikan dari mereka, berapa banyak asisten yang mengunjungi, dan berapa banyak yang telah Anda blokir.

Daftar periksa mencerminkan pengaturan **live** Anda: sambungkan penyedia pembayaran atau tambahkan metode pengiriman, dan keputusan akan diperbarui ketika Anda membuka halaman berikutnya.

## Stop darurat

**Stop darurat** adalah saklar terpisah dari yang utama. Gunakan untuk menghentikan aktivitas asisten kapan pun — misalnya jika sesuatu terlihat salah — tanpa mengubah konfigurasi Anda. Bersihkan untuk melanjutkan. Pikirkan saklar utama sebagai "apakah fitur ini dikonfigurasi" dan stop darurat sebagai "hentikan semuanya sekarang".

## Apa yang dapat dilakukan asisten

Dua tingkat akses, dikendalikan secara terpisah:

- **Membaca** (penemuan dan penjelajahan) adalah risiko yang lebih rendah. Seorang asisten dapat menemukan toko Anda dan membaca detail produk.
- **Pemesanan** (membeli sebenarnya) adalah tingkat yang lebih tinggi dan tetap tertutup bagi asisten yang belum diverifikasi kecuali Anda mengizinkannya.

Sebuah toko dapat ditemukan tanpa dapat dibeli — cara yang berguna untuk memulai.

## Menyembunyikan produk tertentu

Setiap produk memiliki pengaturan **Dapat Dilihat oleh Agen Belanja AI** (aktif secara default). Matikan untuk menjaga produk tertentu dari asisten sambil tetap berada di toko Anda — berguna untuk barang-barang yang lebih baik Anda jual hanya melalui situs web Anda sendiri.

## Mengelola asisten individual

Ketika seorang asisten pertama kali membeli — atau mencoba membeli — Spwig mencatatnya di bawah **Belanja AI → Identitas Agen**. Setiap entri menunjukkan rumah yang diverifikasi asisten (direktori di mana ia menandatangani), tingkat kepercayaannya, dan berapa banyak permintaan yang telah dibuatnya. Nama dan logo yang ditampilkan asisten hanya ditunjukkan sebagai detail yang *diklaim* — anggap sebagai label, bukan bukti identitas; bagian rumah yang diverifikasi adalah bagian yang dapat dipercaya.

Setiap asisten berada dalam salah satu dari tiga tingkat kepercayaan:

| Tingkat kepercayaan | Artinya |
|---|---|
| **Dibatasi (terverifikasi, terbatas)** | Default untuk asisten baru. Spwig telah mencatat identitasnya, dan ia membawa batasan nilai pesanan, batasan pengeluaran, dan pembatasan pembayaran yang ditetapkan dalam kebijakannya (lihat di bawah). |
| **Diverifikasi (batasan dihapus)** | Keputusan yang disengaja oleh Anda untuk mempercayai asisten ini sepenuhnya. Batasan nilai pesanan dan pengeluaran harian dihapus.
| **Diblokir** | Asisten tidak lagi dapat membeli dari toko Anda. Pemesanan yang sedang berlangsung berakhir, meskipun pembayaran yang telah diambil sebelumnya tetap tidak berubah.

Untuk menghentikan seorang asisten, pilih di daftar dan pilih **Blokir asisten yang dipilih**. **Buka kembali asisten yang dipilih** selalu mengembalikannya ke **Dibatasi** — tidak pernah langsung ke **Diverifikasi** — karena mengangkat batasan adalah langkah terpisah, yang disengaja.

Untuk mengangkat seluruh batasan seorang asisten, pilih dan pilih **Tingkatkan menjadi diverifikasi (hapus batasan)**.

Ini menghapus nilai pesanan maksimal dan batas pengeluaran harian, lalu memindahkan asisten ke status Terverifikasi.

Asisten yang diblokir dilewati — unblokir terlebih dahulu, lalu tingkatkan statusnya.

Anggaplah ini sebagai keputusan kepercayaan nyata: hanya tingkatkan asisten yang Anda percayai, karena verifikasi menghilangkan pembatasan yang dimiliki asisten baru.

## Menetapkan batasan asisten

Buka halaman detail asisten dan gunakan bagian **Kebbijakan (batasan & penawaran yang diperbolehkan)** untuk menentukan apa yang boleh dilakukan oleh asisten tersebut:

| Kolom | Apa yang dikendalikan |
|---|---|
| **Nilai pesanan maksimal** | Pesanan terbesar yang dapat ditempatkan oleh asisten ini. Biarkan kosong jika tidak ada batas. |
| **Batas pengeluaran harian** | Jumlah maksimal yang dapat dikeluarkan asisten ini untuk semua pesanan dalam sehari. Biarkan kosong jika tidak ada batas. |
| **Izinkan kode diskon** | Apakah asisten boleh menerapkan kode voucher saat checkout. |
| **Izinkan kartu hadiah** | Apakah asisten boleh menebus kartu hadiah. |
| **Izinkan barang digital** | Apakah asisten boleh membeli produk digital. |
| **Batas permintaan (per menit)** | Berapa banyak permintaan yang dapat dilakukan asisten ini ke toko Anda per menit. |

Asisten baru dimulai dengan batasan nilai pesanan dan pengeluaran yang jelas, serta diskon kode, kartu hadiah, dan barang digital dimatikan — default yang sengaja konservatif. Ubah salah satu kolom ini dan simpan; setiap perubahan akan ditulis ke **Agent Events** dengan nilai sebelum dan sesudahnya, sehingga Anda selalu memiliki catatan siapa yang mengubah apa, dan kapan. Meningkatkan status asisten menjadi Terverifikasi akan menghapus nilai pesanan maksimal dan batas pengeluaran harian asisten tersebut untuk Anda — Anda tidak perlu mengosongkan keduanya secara manual terlebih dahulu.

## Catatan aktivitas

**AI Shopping → Agent Events** adalah catatan yang tidak dapat diubah tentang apa yang dilakukan asisten — setiap permintaan yang diverifikasi, setiap upaya yang diblokir, setiap perubahan yang Anda buat. Ini bersifat baca saja dan tidak dapat diedit atau dihapus, sehingga menjadi jejak bukti Anda jika suatu pembelian oleh asisten pernah dipersoalkan.

## Catatan mengenai platform asisten

Perusahaan yang menjalankan asisten ini (dan aturan untuk muncul di dalamnya) baru dan sering berubah. Beberapa membutuhkan Anda untuk mendaftar atau memenuhi kondisi regional sebelum produk Anda dapat dibeli melalui mereka. Spwig membuat toko Anda siap; apakah asisten tertentu mendaftarkan Anda tergantung pada asisten tersebut.

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.
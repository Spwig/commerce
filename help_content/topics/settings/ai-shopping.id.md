---
title: Pembelian dengan AI
---

Pembelian dengan AI memungkinkan asisten pembelian AI menemukan produk Anda, dan ketika Anda mengizinkannya, membeli dari toko Anda atas nama pelanggan. Fitur ini **dimatikan secara default** — mengaktifkannya adalah pilihan sadar, dan sampai Anda melakukannya, toko Anda tidak menampilkan apa pun kepada asisten tersebut.

## Mengaktifkannya

Buka **Pengaturan → Pembelian dengan AI** dan nyalakan **Komersial Agensif Dikaktifkan**. Dari titik ini, asisten yang mendukung Protokol Komersial Universal dapat menemukan toko Anda dan membaca katalog Anda. Tidak ada perubahan pada toko Anda yang biasa.

## Dashboard Kesiapan

Bagian atas halaman Pembelian dengan AI menjawab satu pertanyaan dalam satu kalimat: **apakah asisten AI benar-benar dapat membeli dari toko Anda saat ini?**

- **"Asisten AI dapat membeli dari toko Anda"** — segala sesuatu yang diperlukan untuk pembelian sudah siap.
- **"Asisten AI dapat menjelajahi toko Anda, tetapi belum bisa membeli"** — toko Anda dapat ditemukan, tetapi masih ada sesuatu yang kurang sebelum pembelian dapat diselesaikan (biasanya penyedia pembayaran yang terhubung).
- **"Penghentian darurat aktif"** atau **"Komersial agensif dimatikan"** — tidak ada yang disajikan kepada asisten.

Di bawah penilaian tersebut, Anda akan melihat daftar singkat pemeriksaan: penyedia pembayaran terhubung, pengiriman dapat dikutip, produk terlihat oleh asisten — dengan petunjuk di samping hal-hal yang masih memerlukan perhatian. Angka-angka menunjukkan berapa banyak produk yang dapat dijual oleh asisten, berapa banyak yang Anda sembunyikan dari mereka, berapa banyak asisten yang telah mengunjungi, dan berapa banyak yang Anda blokir.

Daftar pemeriksaan mencerminkan konfigurasi **aktif** Anda: terhubungkan penyedia pembayaran atau tambahkan metode pengiriman dan penilaian akan diperbarui saat Anda membuka halaman berikutnya.

## Penghentian Darurat

**Penghentian darurat** adalah saklar terpisah dari utama. Gunakan untuk menghentikan semua aktivitas asisten secara segera — misalnya jika sesuatu terlihat tidak benar — tanpa mengubah konfigurasi Anda. Bersihkan untuk melanjutkan. Pikirkan saklar utama sebagai "apakah fitur ini dikonfigurasi" dan penghentian darurat sebagai "hentikan segalanya sekarang".

## Apa yang Bisa Dilakukan Asisten

Dua tingkat akses, dikontrol secara terpisah:

- **Membaca** (penemuan dan menjelajah) berisiko lebih rendah. Seorang asisten dapat menemukan toko Anda dan membaca detail produk.
- **Checkout** (pembelian sebenarnya) lebih berisiko dan tetap tertutup bagi asisten yang belum diverifikasi kecuali Anda mengizinkannya.

Sebuah toko dapat ditemukan tanpa bisa dibeli — cara yang berguna untuk memulai.

## Menyembunyikan Produk Tertentu

Setiap produk memiliki pengaturan **Tampak untuk Agen Pembelian AI** (aktif secara default). Matikan untuk menjaga produk tertentu dari asisten sementara tetap muncul di toko Anda — berguna untuk barang yang lebih baik dijual hanya melalui situs Anda sendiri.

## Mengelola Asisten Individual

Ketika asisten pertama kali membeli — atau mencoba — Spwig mencatatnya di bawah **Pembelian dengan AI → Identitas Agen**. Setiap entri menunjukkan rumah terverifikasi asisten (direktori yang mereka tanda tangani dengan) dan jumlah permintaan yang telah mereka buat. Nama dan logo yang ditampilkan oleh asisten hanya ditampilkan sebagai *detail yang dinyatakan* — perlakukan sebagai label, bukan bukti identitas; rumah terverifikasi adalah bagian yang dapat dipercaya.

Asisten baru mulai **dibatasi**: mereka dapat melakukan transaksi, tetapi dalam batas tertentu. Untuk menghentikan satu, pilih dan pilih **Blokir asisten yang dipilih** — checkout terbuka berakhir dan asisten tidak dapat membeli lagi, sementara pembayaran yang sudah diterima tetap tidak tersentuh. **Buka kembali asisten yang dipilih** mengembalikannya ke keadaan terbatas (tidak langsung ke tak terbatas — mengangkat batasan selalu merupakan langkah terpisah, sadar).

## Rekam Aktivitas

**Pembelian dengan AI → Acara Agen** adalah catatan yang dapat dibuktikan bahwa asisten melakukan — setiap permintaan terverifikasi, setiap upaya yang diblokir, setiap perubahan yang Anda lakukan. Ini hanya dapat dilihat dan tidak dapat diedit atau dihapus, sehingga menjadi bukti Anda jika pembelian yang dilakukan oleh asisten pernah diperdebatkan.

## Catatan tentang Platform Asisten

Perusahaan yang menjalankan asisten ini (dan aturan untuk muncul di dalamnya) baru dan sering berubah.

Beberapa memerlukan Anda untuk mengajukan atau memenuhi kondisi regional sebelum produk Anda dapat dibeli melalui mereka.

Spwig membuat toko Anda siap; apakah asisten tertentu memasukkan Anda atau tidak tergantung pada asisten tersebut.
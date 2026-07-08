---
title: Kotak Keluar Email
---

Kotak Keluar Email adalah catatan lengkap dari setiap email yang telah dikirim atau dicoba dikirim oleh toko Anda — konfirmasi pesanan, pembaruan pengiriman, laporan admin, dan semua pesan transaksional lainnya. Gunakan untuk memverifikasi pengiriman, menyelidiki kegagalan, dan mengelola antrian email.

Navigasikan ke **Sistem Email > Kotak Keluar Email** untuk melihat log email.

![Daftar Kotak Keluar Email dengan badge status](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Membaca kotak keluar

Baris ringkasan di bagian atas menampilkan jumlah untuk setiap kategori status. Daftar di bawah menampilkan email individu dengan:

- **Subjek** — baris subjek email
- **Untuk** — alamat email penerima
- **Dari** — alamat pengirim yang digunakan
- **Status** — status pengiriman saat ini
- **Diantrikan Pada** — kapan email masuk ke antrian
- **Dikirim Pada** — kapan email dikirim ke penyedia
- **Jumlah Pengulangan** — berapa kali pengiriman telah dicoba

## Status email

| Status | Arti |
|--------|---------|
| Diantrikan | Email sedang menunggu di antrian untuk dikirim |
| Sedang Dikirim | Email sedang dikirim ke penyedia |
| Dikirim | Penyedia menerima email |
| Dihentikan | Email dihentikan dan tidak akan dikirim sampai dilepaskan |
| Dicatat | Email dicatat tetapi tidak dikirim (mode uji atau pengaturan hanya pencatatan) |
| Gagal | Penyedia menolak atau tidak dapat mengirimkan email |
| Dibalas Kembali | Email dikirim tetapi dikembalikan oleh server email penerima |
| Dilewati | Pengiriman dilewati karena alasan sistem |

## Melihat detail email

Klik email apa pun dalam daftar untuk melihat detail lengkap:

- **Tubuh HTML** dan **Tubuh Teks** lengkap dari email
- **ID Pesan Penyedia** — referensi dari penyedia email Anda (gunakan ini saat menghubungi dukungan penyedia)
- **Pesan Kesalahan** — pesan kesalahan yang tepat untuk email yang gagal atau dikembalikan
- **Jumlah Pengulangan** dan **Maksimal Pengulangan** — berapa kali pengiriman telah dicoba
- Semua timestamp: dibuat, diantrikan, dikirim, dan gagal

## Memfilter kotak keluar

Gunakan filter di sebelah kanan untuk menyempitkan tampilan Anda:

- **Status** — tampilkan email dengan status pengiriman tertentu
- **Tanggal** — filter berdasarkan kapan email dibuat atau dikirim
- **Jenis Template** — tampilkan hanya email dengan jenis notifikasi tertentu (misalnya, hanya konfirmasi pesanan)

Kotak pencarian di bagian atas mencari berdasarkan subjek, alamat penerima, alamat pengirim, atau ID pesan penyedia.

## Melepaskan email yang dihentikan

Email dengan status **Dihentikan** sedang dihentikan — mereka tidak akan dikirim sampai Anda melepaskannya. Sebuah email mungkin dihentikan jika toko Anda berada dalam mode perawatan saat dibuat, atau jika tindakan admin menempatkannya dalam status dihentikan.

Untuk melepaskan email yang dihentikan:
1. Pilih email yang ingin Anda lepaskan (centang kotak di sebelah kiri)
2. Pilih **Lepaskan email yang dihentikan untuk pengiriman** dari dropdown **Tindakan**
3. Klik **Lanjutkan**

Email yang dilepaskan berpindah ke status **Diantrikan** dan dikirim pada siklus pemrosesan antrian berikutnya.

## Email yang dijadwalkan

Beberapa email dijadwalkan untuk dikirim pada waktu tertentu di masa depan — laporan ringkasan mingguan, misalnya, dijadwalkan untuk dikirim pada hari dan waktu tertentu. Navigasikan ke **Sistem Email > Email yang Dijadwalkan** untuk melihat pengiriman yang akan datang.

Daftar email yang dijadwalkan menampilkan:

- **Jenis Template** — jenis email yang dijadwalkan
- **Email Penerima** — alamat yang akan dikirimkan
- **Dijadwalkan Pada** — tanggal dan waktu yang dijadwalkan untuk dikirim
- **Status** — Menunggu (belum dikirim), Dikirim, atau Gagal

Email yang dijadwalkan diproses secara otomatis saat waktunya tiba — tidak diperlukan tindakan manual.

## Menangani pengiriman yang gagal

Jika email menunjukkan status **Gagal**, klik untuk melihat pesan kesalahan dan ikuti langkah-langkah berikut:

### Penyebab umum dan solusi

| Gejala | Penyebab kemungkinan | Yang harus dilakukan |
|---------|-------------|------------|
| "Autentikasi gagal" | Kredensial penyedia email tidak valid | Perbarui kredensial di **Sistem Email > Akun Email** |
| "Koneksi ditolak" / "Kadaluarsa" | Server email Anda tidak dapat dijangkau | Periksa halaman status penyedia email; uji koneksi di **Akun Email** |
| "Penerima tidak valid" | Alamat email pelanggan tidak valid | Periksa akun pelanggan dan perbaiki email mereka |
| Email yang dikembalikan | Server email penerima menolak email | Alamat mungkin tidak ada atau kotak masuknya penuh; jangan coba terlalu sering |
| Tingkat kegagalan tinggi tiba-tiba | Masalah penyedia atau kredensial telah kedaluarsa | Periksa status penyedia; uji koneksi kembali di **Akun Email** |

### Memeriksa koneksi akun email Anda

Jika banyak email gagal, uji akun email Anda:

1. Navigasikan ke **Sistem Email > Akun Email**
2. Cari akun aktif Anda dan periksa status **Koneksi**-nya
3. Jika koneksi menunjukkan kesalahan, klik akun tersebut dan gunakan opsi **Uji Koneksi** untuk mendiagnosis masalah

### Perilaku pengulangan

Spwig secara otomatis mencoba mengirim ulang email yang gagal hingga batas **Maksimal Pengulangan**. Jumlah pengulangan yang ditampilkan pada setiap email memberi tahu Anda berapa kali upaya telah dilakukan. Setelah batas pengulangan tercapai, email tetap berada dalam status **Gagal** dan tidak ada pengulangan otomatis lebih lanjut.

## Email yang dikembalikan

Email **Dikembalikan** telah dikirim tetapi dikembalikan oleh server email penerima. Ada dua jenis pengembalian:

- **Pengembalian keras** — alamat email tidak valid atau domain tidak menerima email. Jangan coba pengembalian keras; alamat tersebut tidak valid
- **Pengembalian lunak** — masalah sementara (kotak masuk penuh, server sementara tidak tersedia). Mungkin berhasil saat dicoba kembali

Pengembalian berulang ke alamat yang sama dapat merusak reputasi pengirim Anda dengan penyedia email. Jika Anda melihat pengembalian berulang ke alamat pelanggan yang sama, perbarui atau hapus alamat tersebut dari akun pelanggan.

## Tips

- Periksa kotak keluar setelah acara besar seperti penjualan cepat atau peluncuran produk besar untuk memastikan semua email konfirmasi pesanan telah dikirim dengan sukses
- Jika seorang pelanggan mengatakan mereka tidak menerima email, cari kotak keluar berdasarkan alamat email mereka untuk melihat apakah email tersebut dikirim, gagal, atau dilewati
- Kenaikan mendadak dalam kegagalan biasanya menunjukkan masalah kredensial atau akun — periksa **Akun Email** segera
- Status **Ditahan** bukanlah kegagalan — hanya berarti email sedang menunggu. Lepaskan email yang ditahan saat Anda siap mengirimkannya
- Gunakan filter **Jenis Template** untuk dengan cepat meninjau semua email satu jenis — misalnya, periksa bahwa semua konfirmasi pesanan dalam 7 hari terakhir memiliki status **Dikirim**
- Navigasi hierarki tanggal (hari / bulan / tahun) di bagian atas daftar berguna untuk meninjau kotak keluar untuk periode tertentu
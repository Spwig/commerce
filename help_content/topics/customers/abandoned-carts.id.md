---
title: Keranjang yang Ditinggalkan
---

Keranjang yang ditinggalkan dibuat ketika seorang pelanggan yang sudah masuk menambahkan barang ke keranjangnya tetapi tidak menyelesaikan proses checkout dalam 24 jam. Spwig secara otomatis melacak keranjang-keranjang ini sehingga Anda dapat memahami pendapatan yang hilang, mengidentifikasi pola mengapa pelanggan meninggalkan keranjang, dan mengambil tindakan untuk memulihkan penjualan.

Navigasikan ke **Pelanggan > Keranjang yang Ditinggalkan** untuk melihat semua peninggalkan yang tercatat.

## Apa yang dapat Anda lihat dalam daftar keranjang yang ditinggalkan

Tampilan daftar menampilkan setiap keranjang yang ditinggalkan dengan informasi berikut ini secara sekilas:

| Kolom | Deskripsi |
|---|---|
| **Pelanggan** | Nama dan alamat email pelanggan |
| **Ditinggalkan Pada** | Tanggal dan waktu keranjang ditandai sebagai ditinggalkan |
| **Nilai Total** | Nilai moneter barang dalam keranjang pada saat ditinggalkan |
| **Jumlah Item** | Jumlah item dalam keranjang |
| **Alasan Diperkirakan** | Perkiraan Spwig mengenai alasan keranjang ditinggalkan |
| **Status Pemulihan** | Apakah keranjang ini sudah dipulihkan (dijadikan pesanan yang selesai) |
| **Hari Sejak Ditinggalkan** | Seberapa lama keranjang ditinggalkan |

### Memfilter keranjang yang ditinggalkan

Gunakan filter di sisi kanan untuk menyempitkan daftar:

- **Alasan Diperkirakan** — filter berdasarkan alasan peninggalkan (misalnya, tampilkan hanya keranjang di mana alasan diperkirakan adalah biaya pengiriman yang tinggi)
- **Dipulihkan** — filter untuk menampilkan hanya keranjang yang sudah dipulihkan atau belum dipulihkan
- **Ditinggalkan Pada** — filter berdasarkan rentang tanggal untuk fokus pada peninggalkan terbaru atau periode kampanye tertentu

## Memahami alasan peninggalkan

Spwig mencatat alasan diperkirakan untuk setiap peninggalkan. Alasan-alasan ini berdasarkan sinyal yang tertangkap selama proses checkout dan tidak dijamin akurat, tetapi mereka memberikan titik awal yang berguna untuk mendiagnosis pola peninggalkan.

| Alasan | Apa yang mungkin menunjukkan |
|---|---|
| **Tidak Diketahui** | Tidak ada sinyal spesifik yang tertangkap — alasan paling umum |
| **Biaya Pengiriman yang Tinggi** | Pelanggan mungkin terhalang oleh biaya pengiriman yang ditampilkan saat checkout |
| **Total Terlalu Tinggi** | Total pesanan secara keseluruhan mungkin lebih tinggi dari yang diperkirakan |
| **Masalah Checkout** | Pelanggan mengalami masalah selama proses checkout |
| **Pembayaran Gagal** | Upaya pembayaran dilakukan tetapi gagal |
| **Banding Harga** | Pelanggan kemungkinan besar mengunjungi untuk membandingkan harga |
| **Disimpan untuk Nanti** | Pelanggan sengaja menyimpan barang untuk kunjungan di masa depan |

Jika Anda melihat proporsi besar keranjang dengan alasan yang sama — misalnya, kluster besar peninggalkan dengan alasan "Biaya Pengiriman yang Tinggi" — itu adalah sinyal yang layak diteliti dalam pengaturan pengiriman atau presentasi checkout Anda.

## Melihat keranjang yang ditinggalkan secara individual

Klik baris apa pun dalam daftar untuk membuka tampilan detail. Anda akan melihat:

- **Detail Peninggalkan** — pelanggan, referensi keranjang, kapan keranjang ditinggalkan, dan alasan diperkirakan
- **Ringkasan Keranjang** — jumlah item dan nilai total saat peninggalkan
- **Pelacakan Pemulihan** — apakah keranjang sudah dipulihkan, kapan keranjang dipulihkan, dan pesanan mana yang dihasilkan

Laporan **Keranjang** mengarah langsung ke catatan keranjang yang mendasarinya, sehingga Anda dapat melihat secara tepat produk apa yang ada dalam keranjang.

## Alur kerja pemulihan

Spwig melacak apakah setiap keranjang yang ditinggalkan akhirnya berubah menjadi pesanan yang selesai. Ketika pelanggan kembali dan menyelesaikan pembelian dari keranjang yang ditinggalkan, catatan secara otomatis ditandai sebagai **Dipulihkan** dan pesanan yang dihasilkan dikaitkan.

Penghitung **Email Pemulihan yang Dikirim** menunjukkan jumlah email pemulihan otomatis yang telah dikirim ke pelanggan untuk keranjang ini. Hal ini membantu Anda memahami apakah kampanye email Anda mendorong pelanggan untuk kembali.

### Tindakan pemulihan manual

Tampilan keranjang yang ditinggalkan hanya untuk baca — ini adalah catatan dari apa yang terjadi, bukan alat untuk mengedit isi keranjang. Untuk bertindak terhadap keranjang yang ditinggalkan:

1.

Catat alamat email pelanggan dari catatan keranjang yang ditinggalkan
2.

Gunakan sistem email atau alat pemasaran Anda untuk mengirim pesan pribadi
3.

Pertimbangkan untuk melampirkan kode kupon untuk memberikan insentif kepada pelanggan untuk menyelesaikan pembelian
4.

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

Pantau status **Recovered** selama beberapa hari berikutnya untuk melihat apakah outreach yang dilakukan berhasil

## Menganalisis tren peninggalan keranjang

Lihat daftar keranjang yang ditinggalkan secara teratur sebagai pemeriksaan kesehatan pada proses checkout Anda:

- Lonjakan mendadak dalam peninggalan mungkin menunjukkan masalah teknis dengan checkout atau pembayaran
- Nilai keranjang yang konsisten tinggi dalam keranjang yang tidak pulih mewakili segmen pemulihan dengan peluang tertinggi
- Bandingkan rasio keranjang yang pulih terhadap keranjang yang tidak pulih seiring waktu untuk mengukur efektivitas email pemulihan Anda

Bagian **Customer Analytics** dari setiap profil pelanggan juga menampilkan tingkat peninggalan keranjang pribadi mereka, sehingga Anda dapat mengidentifikasi pelanggan yang sering menambahkan ke keranjang tetapi jarang menyelesaikan pembelian.

## Tips

- Urutkan berdasarkan **Total Value** (menurun) untuk mengidentifikasi keranjang bernilai tertinggi yang perlu diprioritaskan untuk outreach pribadi
- Gunakan filter **Abandoned At** untuk meninjau peninggalan dari kampanye atau periode promosi tertentu — lonjakan selama penjualan flash mungkin berarti promosi Anda menarik pengunjung daripada pembeli
- Pasangkan data keranjang yang ditinggalkan dengan kampanye voucher: kirimkan kode diskon berbatas waktu kepada pelanggan dengan keranjang bernilai tinggi yang belum pulih untuk menciptakan rasa mendesak
- Keranjang yang ditinggalkan selama lebih dari 7 hari tidak mungkin pulih sendiri — jika email pemulihan diaktifkan, ini adalah keranjang yang membutuhkan perhatian paling banyak
- Pelanggan tamu tidak muncul dalam keranjang yang ditinggalkan — pelacakan ini hanya berlaku untuk pelanggan dengan akun yang terdaftar
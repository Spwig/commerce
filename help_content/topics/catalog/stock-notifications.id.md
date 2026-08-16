---
title: Pemberitahuan Stok
---

Pemberitahuan stok memungkinkan pelanggan untuk mendaftar agar menerima email ketika produk yang kehabisan stok kembali tersedia. Pengaturan tampilan stok mengontrol apa yang dilihat pelanggan di halaman produk — seperti label status stok, peringatan stok rendah, dan apa yang terjadi ketika produk kehabisan stok.

## Pengaturan tampilan stok

Pengaturan tampilan stok adalah pengaturan default untuk seluruh toko yang berlaku untuk semua produk kecuali diatur ulang di tingkat kategori atau produk.

Navigasi ke **Katalog > Pengaturan Tampilan Stok** untuk mengkonfigurasi opsi ini. Ada satu catatan pengaturan untuk toko Anda — klik untuk diedit.

### Penampilan status stok

| Pengaturan | Keterangan |
|---------|-------------|
| **Tampilkan Status Stok** | Menampilkan label "Tersedia" atau "Habis" di halaman produk |
| **Tampilkan Peringatan Stok Rendah** | Menampilkan pesan "Hanya X tersisa" ketika stok mulai habis |
| **Ambang Batas Stok Rendah** | Jumlah di mana peringatan stok rendah muncul (default: 5) |
| **Tampilkan Jumlah Pasti** | Menampilkan jumlah tersisa yang tepat (misalnya, "Hanya 3 tersisa!") daripada peringatan umum |

### Perilaku stok habis

Pengaturan **Tindakan Stok Habis** menentukan apa yang dilihat pelanggan ketika produk kehabisan stok:

| Tindakan | Yang dilihat pelanggan |
|--------|-------------------|
| **Sembunyikan dari daftar** | Produk dihapus dari halaman kategori dan hasil pencarian |
| **Tampilkan sebagai tidak tersedia** | Produk terlihat tetapi tidak dapat ditambahkan ke keranjang |
| **Tampilkan tombol "Beritahu Saya"** | Pelanggan dapat mendaftarkan alamat email mereka untuk menerima pemberitahuan ketika stok kembali |
| **Izinkan pesanan kembali** | Pelanggan dapat membeli produk tersebut meskipun stok nol |

Atur **Pesan Stok Habis** untuk menyesuaikan teks yang ditampilkan ketika produk tidak tersedia (default: `Habis Stok`).

Atur **Pesan Pesanan Kembali** untuk menyesuaikan teks yang ditampilkan untuk produk yang dapat dipesan kembali (default: `Tersedia untuk pesanan kembali`).

### Penampilan pengiriman dan pengiriman

| Pengaturan | Keterangan |
|---------|-------------|
| **Tampilkan lokasi "Dikirim dari"** | Menampilkan nama gudang di halaman produk |
| **Tampilkan Pengiriman Terkira** | Menampilkan tanggal pengiriman terkira yang dihitung dari lokasi gudang |

### Izinkan pesanan kembali (seluruh situs)

Centang **Izinkan Pesanan Kembali** untuk memungkinkan pelanggan membeli produk yang kehabisan stok secara default. Produk dan kategori individu dapat mengganti pengaturan ini.

## Pemberitahuan kembali stok

Ketika Anda mengatur tindakan stok habis menjadi **Tampilkan tombol "Beritahu Saya"**, pelanggan dapat memasukkan alamat email mereka di halaman produk untuk menerima email ketika produk tersebut kembali tersedia.

### Melihat permintaan pemberitahuan

Navigasi ke **Katalog > Pemberitahuan Stok** untuk melihat semua permintaan pemberitahuan pelanggan. Setiap catatan menunjukkan:
- Alamat email pelanggan
- Produk dan variasi (jika berlaku)
- Gudang pilihan (jika pelanggan memilih preferensi regional)
- Kapan permintaan dibuat
- Kapan pemberitahuan dikirim (kosong jika belum dikirim)

### Kapan pemberitahuan dikirim

Spwig mengirim email kembali stok secara otomatis ketika tingkat stok produk melebihi nol. Kolom **Diberitahukan Pada** mencatat kapan email dikirim.

Pelanggan menerima satu email pemberitahuan. Setelah diberitahu, mereka perlu mendaftar kembali jika produk habis stok untuk kedua kalinya.

### Menyaring permintaan pemberitahuan

Gunakan filter admin untuk menemukan:
- Permintaan untuk produk tertentu
- Permintaan yang sudah diberitahukan (untuk melihat siapa yang telah dihubungi)
- Permintaan yang masih menunggu (pelanggan yang menunggu restok)

## Pengaturan tingkat produk

Pengaturan tampilan stok seluruh situs dapat diatur ulang per produk atau kategori. Pada formulir edit produk, carilah bagian **Stok** di mana Anda dapat menyetel **Tindakan Stok Habis** yang spesifik untuk produk tersebut yang berbeda dari default global.

Ini berguna ketika Anda ingin sebagian besar produk mengizinkan pesanan kembali tetapi menjaga beberapa produk tetap diatur menjadi "Beritahu Saya" — atau ketika produk tertentu harus disembunyikan ketika habis stok.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Atur **Ambang Batas Stok Rendah** ke titik pemesanan ulang yang biasanya Anda gunakan, sehingga pelanggan diberi tahu tentang ketersediaan yang terbatas sebelum stok benar-benar habis.
- Gunakan opsi **Tampilkan tombol "Beri Tahu Saya"** daripada menyembunyikan produk yang kehabisan stok — pelanggan yang mendaftar menunjukkan permintaan nyata yang dapat membenarkan pesanan ulang.
- Aktifkan **Tampilkan Jumlah yang Tepat** secara hati-hati.

Untuk sebagian besar toko, menampilkan "Hanya tersisa 3!" lebih baik daripada menampilkan jumlah yang tepat, karena menciptakan rasa urgensi tanpa mengungkap gambaran lengkap stok Anda.
- Periksa daftar pemberitahuan stok sebelum memesan pesanan baru — jumlah permintaan pemberitahuan yang tertunda memberi tahu Anda seberapa besar permintaan yang ada untuk produk tersebut.
- Jika Anda menggunakan pesanan terlebih dahulu, perbarui **Pesan Pesanan Terlebih Dahulu** untuk menetapkan ekspektasi yang akurat (misalnya, "Dikirim dalam 2-3 minggu — pesan sekarang untuk memesan tempat Anda").
- Gabungkan pemberitahuan kehabisan stok dengan pemasaran email: ketika Anda stok kembali untuk produk yang populer, kirim kampanye kepada semua orang yang mendaftar, bukan hanya email pemberitahuan otomatis saja.
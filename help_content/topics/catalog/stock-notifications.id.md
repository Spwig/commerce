---
title: Pemberitahuan Stok
---

Pemberitahuan stok memungkinkan pelanggan untuk mendaftar agar menerima email ketika produk yang kehabisan stok kembali tersedia. Pengaturan tampilan stok mengontrol apa yang dilihat pelanggan di halaman produk — seperti label status stok, peringatan stok rendah, dan apa yang terjadi ketika produk kehabisan stok.

## Pengaturan tampilan stok

Pengaturan tampilan stok adalah pengaturan default untuk seluruh toko yang berlaku untuk semua produk kecuali diubah di tingkat kategori atau produk.

Navigasi ke **Katalog > Pengaturan Tampilan Stok** untuk mengkonfigurasi opsi ini. Ada satu catatan pengaturan untuk toko Anda — klik untuk diedit.

### Penampilan status stok

| Pengaturan | Keterangan |
|---------|-------------|
| **Tampilkan Status Stok** | Menampilkan label "Tersedia" atau "Habis" di halaman produk |
| **Tampilkan Peringatan Stok Rendah** | Menampilkan pesan "Hanya X tersisa" ketika stok habis |
| **Ambang Batas Stok Rendah** | Jumlah di mana peringatan stok rendah muncul (default: 5) |
| **Tampilkan Jumlah Pasti** | Menampilkan jumlah tersisa yang tepat (misalnya, "Hanya 3 tersisa!") daripada peringatan umum |

### Perilaku habis stok

Pengaturan **Tindakan Stok Habis** menentukan apa yang dilihat pelanggan ketika produk kehabisan stok:

| Tindakan | Yang dilihat pelanggan |
|--------|-------------------|
| **Sembunyikan dari daftar** | Produk dihapus dari halaman kategori dan hasil pencarian |
| **Tampilkan sebagai tidak tersedia** | Produk terlihat tetapi tidak dapat ditambahkan ke keranjang |
| **Tampilkan tombol "Beritahu Saya"** | Pelanggan dapat mendaftarkan alamat email mereka untuk menerima pemberitahuan ketika stok kembali |
| **Izinkan pemesanan kembali** | Pelanggan dapat membeli produk tersebut meskipun stok nol |

Atur **Pesan Stok Habis** untuk menyesuaikan teks yang ditampilkan ketika produk tidak tersedia (default: `Habis Stok`).

Atur **Pesan Pemesanan Kembali** untuk menyesuaikan teks yang ditampilkan untuk produk yang dapat dipesan kembali (default: `Tersedia untuk pemesanan kembali`).

### Penampilan pengiriman dan pengiriman

| Pengaturan | Keterangan |
|---------|-------------|
| **Tampilkan lokasi "Dikirim dari"** | Menampilkan nama gudang di halaman produk |
| **Tampilkan Pengiriman yang Diperkirakan** | Menampilkan tanggal pengiriman yang diperkirakan yang dihitung dari lokasi gudang |

### Izinkan pemesanan kembali (seluruh situs)

Centang **Izinkan Pemesanan Kembali** untuk memungkinkan pelanggan membeli produk yang kehabisan stok secara default. Produk dan kategori individu dapat mengganti pengaturan ini.

## Pemberitahuan kembali tersedia

Ketika Anda mengatur tindakan stok habis menjadi **Tampilkan tombol "Beritahu Saya"**, pelanggan dapat memasukkan alamat email mereka di halaman produk untuk menerima email ketika produk kembali tersedia.

### Melihat permintaan pemberitahuan

Navigasi ke **Katalog > Pemberitahuan Stok** untuk melihat semua permintaan pemberitahuan pelanggan. Setiap catatan menunjukkan:
- Alamat surel pelanggan
- Produk dan variasi (jika berlaku)
- Gudang pilihan (jika pelanggan memilih preferensi regional)
- Kapan permintaan dibuat
- Kapan pemberitahuan dikirim (kosong jika belum dikirim)

### Kapan pemberitahuan dikirim

Spwig mengirim email kembali tersedia secara otomatis ketika tingkat stok produk melebihi nol. Kolom **Diberitahukan Pada** mencatat kapan email dikirim.

Pelanggan menerima satu email pemberitahuan. Setelah diberitahu, mereka perlu mendaftar kembali jika produk habis stok untuk kedua kalinya.

Jika Anda lebih suka mengirim lebih dari sekadar pemberitahuan sederhana — misalnya, menampilkan produk yang kembali tersedia dengan blok konten **Produk Unggulan**, atau mengikuti sehari kemudian — bangunlah **Perjalanan Kembali Tersedia** di **Campaign Studio > Journeys** dan atur **Aktif**. Setelah perjalanan itu ada, pelanggan yang menunggu akan masuk ke dalamnya alih-alih menerima email satu kali; dengan tidak adanya perjalanan yang aktif, email satu kali ini terus dikirim sesuai yang dijelaskan di atas. Lihat [Jalur Terpicu](/bantuan/jalur-terpicu) untuk bagaimana perilaku pemicu bekerja.

### Memfilter permintaan pemberitahuan

Gunakan filter admin untuk menemukan:
- Permintaan untuk produk tertentu
- Permintaan yang sudah diberitahukan (untuk melihat siapa yang telah dihubungi)
- Permintaan yang masih menunggu (pelanggan yang menunggu restok)


## Penimpaan tingkat produk

Pengaturan tampilan stok se-website dapat ditimpa per produk atau kategori. Pada formulir edit produk, cari bagian **Stok** di mana Anda dapat mengatur **Tindakan Stok Habis** khusus produk yang berbeda dari default global.

Ini berguna ketika Anda ingin sebagian besar produk mengizinkan pesanan lanjutan (backorder) tetapi mempertahankan beberapa produk diatur ke "Beri Tahu Saya" — atau ketika produk tertentu harus disembunyikan saat stok habis.

## Tips

- Atur **Ambang Batas Stok Rendah** ke titik pemesanan ulang yang biasanya Anda gunakan, sehingga pelanggan diberi peringatan tentang ketersediaan terbatas sebelum stok benar-benar habis.
- Gunakan opsi **Tampilkan tombol "Beri Tahu Saya"** alih-alih menyembunyikan produk yang stoknya habis — pelanggan yang mendaftar mewakili permintaan nyata yang dapat membenarkan pesanan restock.
- Aktifkan **Tampilkan Jumlah Persis** secara hemat. Untuk sebagian besar toko, menampilkan "Sisa 3 saja!" bekerja lebih baik daripada menampilkan angka persis, karena menciptakan urgensi tanpa mengungkapkan gambaran inventaris lengkap Anda.
- Periksa daftar notifikasi stok sebelum melakukan pesanan baru — jumlah permintaan notifikasi yang tertunda memberi tahu Anda berapa banyak permintaan yang ada untuk produk tersebut.
- Jika Anda menggunakan pesanan lanjutan (backorder), perbarui **Pesan Pesanan Lanjutan** Anda untuk menetapkan ekspektasi yang akurat (misalnya, "Dikirim dalam 2-3 minggu — pesan sekarang untuk memesan tempat Anda").
- Gabungkan notifikasi stok habis dengan pemasaran email: ketika Anda melakukan restock produk populer, kirim kampanye ke semua orang yang mendaftar, bukan hanya email notifikasi otomatis.
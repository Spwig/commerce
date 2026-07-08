---
title: Pemberitahuan Stok
---

Pemberitahuan stok memungkinkan pelanggan mendaftar untuk menerima email ketika produk yang habis stok kembali tersedia. Pengaturan tampilan stok mengontrol apa yang pelanggan lihat di halaman produk — seperti label status stok, peringatan stok rendah, dan apa yang terjadi ketika produk habis.

## Pengaturan Tampilan Stok

Pengaturan tampilan stok adalah pengaturan default toko yang berlaku untuk semua produk kecuali diubah di tingkat kategori atau produk.

Navigasikan ke **Katalog > Pengaturan Tampilan Stok** untuk mengonfigurasi opsi ini. Ada satu catatan pengaturan untuk toko Anda — klik untuk mengedit.

### Tampilan Status Stok

| Pengaturan | Deskripsi |
|---------|-------------|
| **Tampilkan Status Stok** | Tampilkan label "Tersedia" atau "Habis" di halaman produk |
| **Tampilkan Peringatan Stok Rendah** | Tampilkan pesan "Hanya tersisa X" ketika stok sedang rendah |
| **Ambang Batas Stok Rendah** | Jumlah stok di mana atau di bawahnya peringatan stok rendah muncul (default: 5) |
| **Tampilkan Jumlah Persis** | Tampilkan jumlah yang tersisa secara spesifik (misalnya, "Hanya tersisa 3!") alih-alih peringatan umum |

### Perilaku Produk Habis Stok

Pengaturan **Tindakan Habis Stok** menentukan apa yang pelanggan lihat ketika produk tidak memiliki stok yang tersedia:

| Tindakan | Apa yang pelanggan lihat |
|--------|-------------------|
| **Sembunyikan dari daftar** | Produk dihilangkan dari halaman kategori dan hasil pencarian |
| **Tampilkan sebagai tidak tersedia** | Produk terlihat tetapi tidak dapat ditambahkan ke keranjang |
| **Tampilkan tombol "Beritahu Saya"** | Pelanggan dapat mendaftarkan alamat email mereka untuk diberitahu ketika stok kembali |
| **Izinkan pemesanan ulang** | Pelanggan dapat membeli produk meskipun stok sedang habis |

Atur **Pesan Habis Stok** untuk menyesuaikan teks yang ditampilkan ketika produk tidak tersedia (default: `Habis Stok`).

Atur **Pesan Pemesanan Ulang** untuk menyesuaikan teks yang ditampilkan untuk produk yang dapat dipesan ulang (default: `Tersedia untuk pemesanan ulang`).

### Tampilan Pengiriman dan Pengiriman

| Pengaturan | Deskripsi |
|---------|-------------|
| **Tampilkan Lokasi "Dikirim Dari"** | Tampilkan nama gudang di halaman produk |
| **Tampilkan Estimasi Pengiriman** | Tampilkan tanggal estimasi pengiriman yang dihitung dari lokasi gudang |

### Izinkan Pemesanan Ulang (Seluruh Situs)

Centang **Izinkan Pemesanan Ulang** untuk memungkinkan pelanggan membeli produk yang habis stok secara default. Produk dan kategori individu dapat mengubah pengaturan ini.

## Pemberitahuan Kembali Tersedia

Ketika Anda mengatur tindakan habis stok menjadi **Tampilkan tombol "Beritahu Saya"**, pelanggan dapat memasukkan alamat email mereka di halaman produk untuk menerima email ketika produk kembali tersedia.

### Melihat Permintaan Pemberitahuan

Navigasikan ke **Katalog > Pemberitahuan Stok** untuk melihat semua permintaan pemberitahuan pelanggan. Setiap catatan menampilkan:
- Alamat email pelanggan
- Produk dan variasi (jika berlaku)
- Gudang yang dipilih (jika pelanggan memilih preferensi regional)
- Kapan permintaan dibuat
- Kapan pemberitahuan dikirim (kosong jika belum dikirim)

### Kapan Pemberitahuan Dikirim

Spwig mengirimkan email kembali tersedia secara otomatis ketika tingkat stok produk naik di atas nol. Bidang **Diberitahu Pada** mencatat kapan email dikirim.

Pelanggan menerima satu email pemberitahuan. Setelah diberitahu, mereka perlu mendaftar kembali jika produk kembali habis stok untuk kedua kalinya.

### Memfilter Permintaan Pemberitahuan

Gunakan filter admin untuk menemukan:
- Permintaan untuk produk tertentu
- Permintaan yang sudah diberitahu (untuk melihat siapa yang sudah dihubungi)
- Permintaan yang masih menunggu (pelanggan yang menunggu restok)

## Pengaturan Per Produk

Pengaturan tampilan stok seluruh situs dapat diubah per produk atau kategori. Di formulir pengeditan produk, cari bagian **Stok** tempat Anda dapat mengatur **Tindakan Habis Stok** yang berbeda dari pengaturan default global.

Ini berguna ketika Anda ingin sebagian besar produk mengizinkan pemesanan ulang tetapi menjaga beberapa produk tetap diatur ke "Beritahu Saya" — atau ketika produk tertentu harus disembunyikan ketika habis stok.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.


- Atur **Low Stock Threshold** ke titik reorder yang biasanya Anda gunakan, sehingga pelanggan diingatkan tentang ketersediaan terbatas sebelum Anda habis sepenuhnya.
- Gunakan opsi **Show "Notify Me" button** alih-alih menyembunyikan produk yang habis — pelanggan yang mendaftar mewakili permintaan nyata yang dapat membenarkan pesanan restok.
- Aktifkan **Show Exact Quantity** secara terbatas.

Untuk sebagian besar toko, menampilkan "Hanya tersisa 3!" bekerja lebih baik daripada menampilkan jumlah yang tepat, karena menciptakan urgensi tanpa mengungkap gambaran inventaris penuh Anda.
- Periksa daftar notifikasi stok sebelum menempatkan pesanan baru — jumlah permintaan notifikasi yang tertunda memberi tahu Anda seberapa besar permintaan untuk produk tersebut.
- Jika Anda menggunakan backorders, perbarui **Backorder Message** Anda untuk menetapkan ekspektasi yang akurat (misalnya, "Dikirim dalam 2-3 minggu — pesan sekarang untuk memesan tempat Anda").
- Gabungkan notifikasi produk habis dengan pemasaran email: ketika Anda menambah stok produk populer, kirimkan kampanye kepada semua orang yang telah mendaftar, bukan hanya email notifikasi otomatis.
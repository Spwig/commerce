---
title: Memparkir dan Melanjutkan Transaksi POS
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/parkedcart/
  filename: parked-cart-list.webp
  description: Tampilan daftar keranjang yang diparkir (mungkin kosong pada instalasi baru — tetap ambil screenshot)
  save-to: core/static/core/admin/img/help/pos/
-->

Keranjang yang diparkir memungkinkan kasir Anda menghentikan transaksi dan segera melayani pelanggan berikutnya tanpa kehilangan satupun barang atau diskon. Ketika Anda siap, keranjang asli akan dikembalikan tepat seperti semula dan penjualan dilanjutkan dari titik yang ditinggalkan.

## Apa yang dilakukan memparkir keranjang

Ketika kasir mengetuk **Park** di register POS, Spwig menyimpan snapshot lengkap dari keranjang saat ini ke server. Register kemudian dibersihkan sehingga transaksi baru dapat dimulai segera. Keranjang yang diparkir disimpan dan terikat ke terminal tempat keranjang tersebut dibuat.

Tidak ada yang terhilang dalam snapshot. Keranjang yang diparkir mempertahankan:

- Setiap barang dan jumlahnya
- Pelanggan yang terikat ke penjualan
- Diskon manual yang diterapkan pada keranjang atau barang individu

Keranjang yang diparkir tetap tersedia di terminal yang sama selama **24 jam**. Setelah itu, Spwig secara otomatis menghapusnya. Keranjang yang telah dikembalikan akan dihapus segera setelah dikembalikan dan tidak dihitung dalam jendela 24 jam.

## Cara memparkir transaksi

Anda harus memiliki setidaknya satu barang di keranjang sebelum memparkir. Keranjang kosong tidak dapat diparkir.

1. Saat transaksi sedang berlangsung, ketuk tombol **Park** di register POS.
2. Spwig menyimpan keranjang dan membersihkan register. Anda akan melihat konfirmasi dan jumlah keranjang di area keranjang yang diparkir akan diperbarui.
3. Mulai transaksi pelanggan berikutnya di register yang sekarang kosong.

Jika pelanggan telah terikat ke penjualan sebelum diparkir, nama mereka akan muncul di daftar keranjang yang diparkir untuk identifikasi yang mudah.

## Cara melanjutkan transaksi yang diparkir

1. Ketuk area atau ikon **Keranjang yang Diparkir** di register POS. Anda akan melihat daftar semua keranjang yang sedang diparkir di terminal ini, menampilkan nama pelanggan (jika ada), jumlah barang, total jumlah, kasir yang memparkirnya, dan waktu pemarkiran.
2. Ketuk keranjang yang ingin dilanjutkan.
3. Jika register saat ini memiliki barang di dalamnya, POS akan membersihkan barang tersebut sebelum mengembalikan keranjang yang diparkir. Pastikan Anda telah menyelesaikan atau memparkir transaksi saat ini sebelum melanjutkan transaksi lain.
4. Barang, ikatan pelanggan, dan diskon manual dari keranjang yang diparkir semuanya dikembalikan. Penjualan dilanjutkan seperti biasa.

## Visibilitas keranjang yang diparkir

Keranjang yang diparkir **terikat ke terminal** tempat mereka dibuat. Setiap kasir yang masuk ke terminal yang sama dapat melihat dan melanjutkan keranjang yang diparkir di terminal tersebut — tidak ada pembatasan per-kasir mengenai siapa yang dapat mengambil keranjang yang diparkir.

Keranjang yang diparkir di terminal lain, bahkan di lokasi toko yang sama, tidak terlihat di terminal saat ini.

## Membatalkan keranjang yang diparkir dari POS

Kasir dapat menghapus keranjang yang diparkir secara langsung dari daftar keranjang yang diparkir di terminal — ketuk keranjang dan gunakan opsi hapus atau buang. Keranjang yang diparkir yang dihapus dihapus secara permanen dan tidak dapat dipulihkan.

## Kadaluarsa otomatis dan pembersihan

Setiap keranjang yang diparkir kadaluarsa **24 jam setelah diparkir**. Spwig menjalankan tugas latar belakang yang menghapus keranjang yang kadaluarsa dan tidak pernah dikembalikan. Tidak ada yang perlu Anda lakukan — pembersihan terjadi secara otomatis.

Jika Anda perlu membersihkan keranjang yang diparkir sebelum jendela 24 jam, kasir dapat menghapusnya satu per satu dari daftar keranjang yang diparkir di terminal.

## Shift dan keranjang yang diparkir

Tidak ada tautan keras antara keranjang yang diparkir dan shift yang sedang terbuka saat keranjang tersebut diparkir. Menutup shift **tidak** secara otomatis menghapus atau membatalkan keranjang yang diparkir di terminal tersebut. Keranjang yang diparkir bertahan melalui perubahan shift dan tetap tersedia untuk jendela 24 jam penuh.

Ini berarti:

- Keranjang yang diparkir di akhir shift pagi dapat dilanjutkan oleh kasir di shift berikutnya.
- Jika Anda tidak ingin keranjang yang diparkir berpindah antar shift, mintalah kasir membersihkan daftar keranjang yang diparkir sebelum menutup shift mereka.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Parkirkan keranjang saat pelanggan mengatakan "Saya hanya perlu mengambil satu barang lagi" — ini lebih cepat daripada meminta mereka menunggu antrian lagi atau menambahkan barang secara manual.
- Jika daftar keranjang yang diparkir semakin panjang, periksa apakah kasir sebelumnya meninggalkan transaksi yang belum terselesaikan di akhir shift mereka dan bersihkan keranjang yang sudah tidak relevan.
- Tambahkan nama pelanggan ke dalam penjualan sebelum memarkir keranjang — nama mereka akan muncul dalam daftar, sehingga jauh lebih mudah menemukan keranjang yang tepat saat mereka kembali.
- Keranjang yang diparkir akan kedaluwarsa setelah 24 jam, sehingga tidak cocok untuk menahan transaksi selama lebih dari satu hari bisnis.
- Ingat bahwa melanjutkan keranjang yang diparkir akan mengosongkan apa pun yang saat ini ada di kasir.

Selesaikan atau parkirkan transaksi aktif sebelum mengambil keranjang yang diparkir yang berbeda.
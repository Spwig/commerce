---
title: Tindakan Massal Produk
---

Daftar **Produk** memungkinkan Anda melakukan tindakan pada banyak produk sekaligus, alih-alih membuka masing-masing produk secara terpisah. Dari **Tindakan Massal** di bagian bawah bilah alat di atas grid produk, Anda dapat menerbitkan atau tidak menerbitkan produk, menghadirkan atau tidak menghadirkan mereka, mengekspor data ke CSV, memeriksa mana produk yang siap untuk pengiriman internasional, atau menghapusnya — semuanya dalam satu langkah.

Navigasi ke **Produk > Semua Produk** untuk menggunakan tindakan ini.

![Toolbar daftar produk dengan tiga kartu produk yang dipilih dan kotak centang Tindakan Massal menunjukkan setiap opsi, termasuk Ekspor Data Kepabeanan (CSV) dan Periksa Kesiapan Pengiriman Internasional](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Menjalankan Tindakan Massal

1. Gunakan panel filter atau kotak **Pencarian** untuk menyempitkan produk yang ingin Anda pilih, jika diperlukan
2. Centang kotak di sudut kiri atas setiap kartu produk yang ingin Anda masukkan — **Bilah Tindakan Massal** menunjukkan jumlah produk yang dipilih secara berjalan
3. Pilih tindakan dari **Tindakan Massal**
4. Klik **Terapkan**

Tindakan yang mengubah atau mengekspor data berjalan segera; **Hapus yang Dipilih** meminta Anda untuk memverifikasi terlebih dahulu, karena ini satu-satunya tindakan di sini yang tidak mudah dibatalkan dari daftar itu sendiri.

## Tindakan yang Tersedia

| Tindakan | Apa yang dilakukannya |
|--------|---------------|
| **Tandai sebagai Diterbitkan** | Menetapkan status produk yang dipilih menjadi Diterbitkan sehingga terlihat di toko. |
| **Tandai sebagai Draf** | Menetapkan status produk yang dipilih menjadi Draf, menyembunyikan mereka dari toko sambil Anda terus mengedit. |
| **Tandai sebagai Unggulan** | Mengaktifkan **Apakah Unggulan** pada produk yang dipilih. |
| **Hapus Unggulan** | Menonaktifkan **Apakah Unggulan** pada produk yang dipilih. |
| **Ekspor ke CSV** | Mengunduh CSV dari ID, nama, SKU, status, tanda unggulan, dan harga produk yang dipilih. |
| **Ekspor Data Kepabeanan (CSV)** | Mengunduh CSV informasi kepabeanan untuk produk yang dipilih. Lihat di bawah ini. |
| **Periksa Kesiapan Pengiriman Internasional** | Menampilkan ringkasan mana produk yang dipilih memiliki data kepabeanan yang dibutuhkan untuk pengiriman internasional. Lihat di bawah ini. |
| **Hapus yang Dipilih** | Memindahkan produk yang dipilih ke tempat sampah, setelah prompt konfirmasi. |

## Ekspor Data Kepabeanan (CSV)

Gunakan ini ketika Anda membutuhkan formulir pernyataan kepabeanan untuk diberikan kepada pihak pengiriman, kurir, atau broker kepabeanan — misalnya, sebelum pengiriman internasional besar, atau ketika menyiapkan pengirim baru yang meminta kode HS dan data asal secara langsung.

Pilih produknya, pilih **Ekspor Data Kepabeanan (CSV)** dari kotak centang, lalu klik **Terapkan**. Spwig mengunduh file bernama `product_customs_data.csv` dengan satu baris per produk dan kolom-kolom berikut:

| Kolom | Sumber |
|--------|--------|
| **SKU** | SKU produk |
| **Nama** | Nama produk |
| **Kode HS** | Kode klasifikasi Sistem Harmonisasi |
| **Negara Asal** | Di mana produk diproduksi |
| **Harga Unit Kepabeanan** | Nilai yang dinyatakan per unit untuk kepabeanan |
| **Lisensi Ekspor** | Nomor lisensi ekspor, jika produk membutuhkannya |
| **Masa Berlaku Lisensi** | Tanggal kedaluwarsa lisensi ekspor, jika ditetapkan |
| **Siap Internasional** | `Ya` atau `Tidak` — apakah produk memiliki data minimum yang diperlukan untuk pengiriman internasional (lihat di bawah ini) |

Bidang-bidang ini berasal dari bagian **Pengiriman Internasional / Kepabeanan** formulir produk. Jika produk kehilangan satu, kolomnya kosong dalam ekspor — isi data yang hilang pada produk sebelum Anda mengandalkan file ini untuk pengiriman nyata.

## Periksa Kesiapan Pengiriman Internasional

Gunakan ini untuk meninjau sejumlah produk sebelum Anda memulai pengiriman internasional, tanpa membuka masing-masing produk secara terpisah atau menunggu ekspor CSV penuh.

Pilih produknya, pilih **Periksa Kesiapan Pengiriman Internasional**, lalu klik **Terapkan**. Spwig memeriksa setiap produk yang dipilih terhadap tiga bidang yang diperlukan — **Kode HS**, **Negara Asal**, dan **Harga Unit Kepabeanan** — dan menampilkan notifikasi ringkasan hasilnya:

- Jika setiap produk yang dipilih memiliki ketiga kolom tersebut terisi, Anda akan melihat konfirmasi bahwa semuanya sudah siap.
- Jika beberapa di antaranya kekurangan data, notifikasi akan melaporkan berapa banyak yang siap dan berapa yang tidak, serta mendaftar setiap produk yang tidak siap beserta bidang apa saja yang hilang (misalnya, "Blue Ceramic Mug (tidak ada: hs_code, country_of_origin)").

Jika lebih dari 10 produk yang kekurangan data, notifikasi akan mendaftar 10 yang pertama dan memberi tahu Anda berapa banyak lagi yang tersisa.

Tindakan ini hanya membaca data — tidak mengubah apa pun pada produk, jadi aman untuk dijalankan sebanyak apa pun selama Anda mengisi informasi bea cukai di seluruh katalog Anda.

**Nomor Sertifikat Ekspor** dan **Tanggal kedaluwarsa Sertifikat Ekspor** bukan bagian dari pemeriksaan kesiapan. Mereka hanya berlaku untuk barang yang dikendalikan atau dibatasi, jadi produk bisa saja "siap" untuk pengiriman internasional tanpa keduanya.

## Tips

- Jalankan **Periksa Kesiapan Pengiriman Internasional** pada keseluruhan katalog Anda (atau kategori per kategori) sebelum pesanan internasional pertama — ini jauh lebih cepat daripada menemukan kode HS yang hilang saat pengiriman sudah di perbatasan.
- Pertahankan **Ekspor Data Bea Cukup (CSV)** untuk diserahkan kepada pialang dan pengangkut, serta **Periksa Kesiapan Pengiriman Internasional** untuk daftar periksa internal Anda — CSV adalah catatan, sedangkan pemeriksaan kesiapan adalah daftar tugas.
- Isi **Kode HS**, **Negara Asal**, dan **Harga Unit Bea Cukup** pada formulir produk (di bawah **Pengiriman Internasional / Bea Cukup**) saat menambahkan produk baru, sehingga Anda tidak sampai-sampai melakukannya secara massal nanti hari.
- Grid produk memuat lebih banyak produk secara otomatis saat Anda menggulir (infinite scroll), dan pilihan kotak centang Anda tetap terjaga saat produk baru muncul — jadi Anda bisa menggulir untuk membangun pilihan yang besar sebelum menerapkan tindakan. Namun, mengubah filter atau memuat ulang halaman akan menghapus pilihan Anda, jadi terapkan tindakan sebelum Anda menyesuaikan filter.
- **Tandai sebagai Draft** adalah cara cepat untuk menarik beberapa produk dari toko sekaligus — misalnya, menjelang pengecekan stok — tanpa mengubah hal lain tentang produk tersebut.
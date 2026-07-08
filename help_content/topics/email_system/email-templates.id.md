---
title: Sampul Email
---

Sampul email mengontrol desain dan konten dari setiap email otomatis yang toko Anda kirimkan ke pelanggan dan ke Anda — konfirmasi pesanan, pembaruan pengiriman, pengaturan ulang kata sandi, pemberitahuan pengembalian dana, dan masih banyak lagi. Mengedit sebuah sampul akan mengubah semua email masa depan dari jenis tersebut; email sebelumnya yang sudah ada di antrean tidak terpengaruh.

Navigasikan ke **Sistem Email > Sampul Email** untuk melihat dan mengelola sampul Anda.

![Daftar sampul email](/static/core/admin/img/help/email-templates/templates-list.webp)

## Jenis Sampul

Toko Anda memiliki sampul untuk berbagai acara. Mereka dikelompokkan berdasarkan kategori:

### Email pesanan yang ditujukan ke pelanggan
| Sampul | Dikirim saat |
|----------|-----------|
| Konfirmasi Pesanan | Seorang pelanggan menyelesaikan pembelian |
| Konfirmasi Pembayaran | Pembayaran berhasil diproses |
| Pesanan Dikirim | Pesanan ditandai sebagai dikirim |
| Konfirmasi Pengiriman | Nomor pelacakan pengiriman ditambahkan |
| Konfirmasi Pengiriman | Pesanan ditandai sebagai telah terkirim |
| Pesanan Dibatalkan | Pesanan dibatalkan |
| Pemberitahuan Keterlambatan Pesanan | Keterlambatan dicatat pada pesanan |
| Pemberitahuan Pengembalian Dana | Pengembalian dana dikeluarkan |

### Email Akun
| Sampul | Dikirim saat |
|----------|-----------|
| Selamat Datang di Akun | Seorang pelanggan membuat akun |
| Undangan Akun | Anda mengundang pelanggan untuk membuat akun |
| Verifikasi Email | Seorang pelanggan memverifikasi alamat email mereka |
| Atur Ulang Kata Sandi | Seorang pelanggan meminta pengaturan ulang kata sandi |

### Pengembalian
| Sampul | Dikirim saat |
|----------|-----------|
| Pengembalian: Permintaan Diterima | Seorang pelanggan mengajukan permintaan pengembalian |
| Pengembalian: Disetujui | Permintaan pengembalian disetujui |
| Pengembalian: Ditolak | Permintaan pengembalian ditolak |
| Pengembalian: Paket Diterima | Barang yang dikembalikan tiba di lokasi Anda |
| Pengembalian: Pengembalian Dana Dikirimkan | Pengembalian dana untuk pengembalian dikeluarkan |

### Pemberitahuan Admin (dikirim ke Anda)
| Sampul | Dikirim saat |
|----------|-----------|
| Admin: Pesanan Baru | Pesanan baru ditempatkan |
| Admin: Pembayaran Gagal | Upaya pembayaran gagal |
| Admin: Laporan Penjualan Harian | Ringkasan penjualan harian dihasilkan |
| Admin: Peringatan Stok Rendah | Produk turun di bawah ambang batas stoknya |
| Admin: Ringkasan Mingguan | Ringkasan toko mingguan dihasilkan |

Sampul tambahan mencakup pencapaian pelacakan pengiriman, aktivitas program afiliasi, konfirmasi pemesanan (jika fitur pemesanan diaktifkan), dan acara program loyalitas.

## Mengedit Sampul

1. Navigasikan ke **Sistem Email > Sampul Email**
2. Cari sampul yang ingin Anda edit. Anda dapat menyaring berdasarkan **Jenis Sampul**, **Bahasa**, atau **Status** menggunakan filter di sebelah kanan
3. Klik sampul untuk membukanya
4. Edit baris **Subjek** (judul email yang ditampilkan di kotak masuk pelanggan)
5. Edit **Konten HTML** untuk versi desain penuh email
6. Secara opsional, edit **Konten Teks** — versi teks biasa sebagai cadangan untuk klien email yang tidak mendukung HTML
7. Klik **Simpan**

> **Email HTML:** Bidang konten HTML menerima HTML standar termasuk CSS inline. Spwig merender ini menjadi email yang diformat dengan benar. Jika Anda menggunakan markup MJML, ini akan dikompilasi secara otomatis saat disimpan.

## Melihat Pratinjau Sampul

Sebelum menyimpan, Anda dapat melihat pratinjau bagaimana sampul akan terlihat di klien email:

1. Buka sampul yang ingin Anda lihat pratinjau
2. Klik tombol **Pratinjau** (terlihat di daftar sampul atau di halaman detail sampul)
3. Pratinjau akan terbuka di tab browser baru yang menampilkan email yang telah dirender

Ini memungkinkan Anda memeriksa tata letak, format, dan penampilan variabel tempat penampung sebelum sampul diluncurkan.

## Variabel Sampul

Variabel adalah tempat penampung di sampul Anda yang diganti oleh Spwig dengan data nyata saat email dikirim. Mereka ditulis sebagai `{{ nama_variabel }}`.

Variabel umum yang tersedia di sebagian besar sampul:

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Variabel | Diganti dengan |
|----------|---------------|
| `{{ customer_name }}` | Nama lengkap pelanggan |
| `{{ order_number }}` | Nomor referensi pesanan |
| `{{ order_total }}` | Jumlah total pesanan |
| `{{ store_name }}` | Nama toko Anda |
| `{{ store_url }}` | Alamat web toko Anda |
| `{{ tracking_number }}` | Nomor pelacakan pengiriman |
| `{{ tracking_url }}` | Tautan klik untuk melacak pengiriman |

Variabel yang tersedia secara eksak tergantung pada jenis template. Variabel yang relevan untuk template terkait pesanan (seperti `{{ order_number }}`) tidak tersedia dalam template akun (seperti Reset Kata Sandi). Jika Anda menyertakan variabel yang tidak berlaku, maka akan muncul kosong atau tidak diganti.

## Dukungan bahasa

Setiap jenis template dapat memiliki versi untuk setiap bahasa yang didukung toko Anda. Bidang **Bahasa** pada setiap template mengontrol versi bahasa yang aktif.

Spwig secara otomatis memilih versi bahasa yang benar berdasarkan preferensi bahasa pelanggan saat mengirim. Jika tidak ada template yang ada untuk bahasa pelanggan, Spwig akan kembali ke versi bahasa Inggris.

Untuk menambahkan template untuk bahasa baru:
1. Buka template yang sudah ada
2. Klik **Clone Template** dari menu **Actions**
3. Tetapkan **Language Code** pada salinan ke bahasa baru
4. Terjemahkan konten
5. Aktifkan template yang dikloning

## Mengklon, mengaktifkan, dan menonaktifkan template

### Mengklon template

Mengklon membuat salinan persis dari template — berguna untuk membuat variasi bahasa atau menguji versi berbeda tanpa memengaruhi template yang sedang berjalan.

1. Pilih satu atau beberapa template dalam daftar
2. Pilih **Clone selected templates** dari dropdown **Actions**
3. Salinan dibuat dalam keadaan tidak aktif — edit dan aktifkan saat siap

### Mengaktifkan dan menonaktifkan template

Sebuah template harus **Aktif** untuk digunakan dalam pengiriman. Hanya satu template aktif per jenis dan kombinasi bahasa yang digunakan sekaligus.

Untuk mengaktifkan atau menonaktifkan secara massal:
1. Pilih template yang diinginkan
2. Pilih **Activate selected templates** atau **Deactivate selected templates** dari dropdown **Actions**

Atau buka template individu dan ubah kotak centang **Active**.

## Template sistem

Template yang ditandai dengan badge **System** adalah template default yang disediakan oleh Spwig. Mereka tidak dapat dihapus. Anda dapat mengeditnya langsung atau mengklonnya untuk membuat versi kustom.

## Tips

- Selalu pratinjau template setelah mengedit untuk menangkap masalah pemformatan sebelum pelanggan melihatnya
- Pertahankan subjek yang pendek dan spesifik — `Pemesanan #10045 Anda telah dikirim` bekerja lebih baik daripada subjek umum seperti `Pembaruan dari toko kami`
- Edit konten teks biasa juga — beberapa klien email hanya menampilkan versi teks biasa, dan beberapa pelanggan lebih memilihnya
- Klone versi Inggris dari template sebagai titik awal sebelum membuat versi terjemahan
- Jika Anda ingin menguji perubahan tanpa memengaruhi email yang sedang berjalan, klone template, edit salinan, dan biarkan kedua versi aktif sementara saat Anda memverifikasi pratinjau — kemudian nonaktifkan versi asli
- Template notifikasi admin (seperti **Admin: Pesanan Baru**) dikirim ke alamat email admin toko Anda — pastikan alamat email tersebut benar dalam pengaturan toko Anda
---
title: Dompet Pelanggan
---

Dompet pelanggan adalah buku besar kredit toko yang melacak saldo berjalan untuk setiap pelanggan. Kredit toko dapat ditambahkan sebagai hasil dari pengembalian dana, hadiah afiliasi, kampanye promosi, atau penyesuaian manual yang dilakukan oleh tim Anda.

> **Saldo dompet dapat digunakan saat checkout.** Seorang pelanggan yang sudah masuk dan memiliki kredit toko akan melihatnya pada langkah pembayaran dan dapat menggunakannya dengan satu klik. Kredit akan dikurangi dari total tagihan — setelah pajak dan pengiriman — dan sisa yang ada akan dibebankan ke kartu mereka seperti biasa. Jika kredit mencakup seluruh pesanan, tidak diperlukan kartu sama sekali. Kredit akan dibekukan saat digunakan dan hanya benar-benar dikurangi setelah pembayaran dikonfirmasi, sehingga checkout yang dibatalkan tidak akan memakan biaya apa pun bagi pelanggan.

Navigasikan ke **Pelanggan > Dompet Pelanggan** untuk melihat dan mengelola dompet.

## Memahami saldo dompet

Setiap dompet pelanggan menampilkan empat angka saldo:

| Saldo | Deskripsi |
|---|---|
| **Saldo Tersedia** | Kredit saat ini yang dapat digunakan oleh pelanggan — ini akan menjadi jumlah yang dapat digunakan saat checkout setelah fitur tersebut diluncurkan |
| **Saldo Tertunda** | Kredit yang belum masuk ke saldo tersedia — contohnya, pengembalian dana yang masih dalam jendela konfirmasi |
| **Total Kredit Seumur Hidup** | Total jumlah yang pernah dikreditkan ke dompet ini, termasuk semua kredit sebelumnya |
| **Total Penggunaan Seumur Hidup** | Total jumlah yang pernah dikurangi dari dompet ini |

Saldo tersedia adalah angka yang akan penting setelah fitur pengeluaran checkout diluncurkan. Kredit tertunda akan masuk ke sana setelah periode tertunda berakhir.

## Melihat dompet pelanggan

1. Navigasikan ke **Pelanggan > Dompet Pelanggan**
2. Gunakan bidang pencarian untuk menemukan pelanggan berdasarkan nama atau email
3. Klik entri dompet untuk membuka tampilan detail

Tampilan detail menampilkan saldo saat ini di bagian atas dan riwayat transaksi lengkap di bawahnya. Timestamp **Terakhir Dikreditkan Pada** dan **Terakhir Digunakan Pada** memberi tahu kapan dompet terakhir kali aktif.

### Memfilter daftar dompet

Gunakan filter **Aktif** untuk memisahkan dompet yang aktif dari yang beku. Dompet yang ditandai sebagai tidak aktif adalah dompet yang beku — tidak ada kredit atau debet yang dapat dicatat terhadapnya, meskipun saldo tetap terjaga.

## Membaca riwayat transaksi

Setiap perubahan pada saldo dompet dicatat sebagai transaksi individual. Riwayat transaksi adalah buku besar lengkap dan permanen — transaksi tidak pernah diedit atau dihapus. Jika ada kesalahan yang perlu diperbaiki, transaksi kompensasi baru akan ditambahkan.

Setiap transaksi menampilkan:

| Bidang | Deskripsi |
|---|---|
| **Jenis** | Kredit, Debit, Pengembalian, Penyesuaian, atau Pembatalan |
| **Jumlah** | Nilai transaksi ini (selalu ditampilkan sebagai angka positif) |
| **Saldo Setelah** | Saldo dompet segera setelah transaksi ini diterapkan |
| **Sumber** | Tempat kredit atau debet berasal |
| **Status** | Selesai, Tertunda, atau Dibatalkan |
| **Deskripsi** | Penjelasan singkat tentang transaksi |
| **ID Referensi** | Tautan ke catatan asal (misalnya, nomor pesanan atau ID hadiah) |
| **Dibuat Pada** | Kapan transaksi dicatat |

### Penjelasan jenis transaksi

- **Kredit** — dana yang ditambahkan ke dompet (dari pengembalian, promosi, atau penyesuaian manual)
- **Debit** — dana yang dikurangi dari dompet. Setelah fitur pengeluaran checkout diluncurkan ini akan berarti "dibayarkan untuk pesanan" — untuk saat ini satu-satunya cara debit terjadi adalah melalui penyesuaian manual
- **Pengembalian** — kredit yang ditambahkan secara khusus sebagai hasil dari pesanan yang dikembalikan atau dibatalkan
- **Penyesuaian** — perbaikan manual yang dilakukan oleh tim Anda
- **Pembatalan** — transaksi yang membatalkan entri sebelumnya

### Penjelasan sumber transaksi

- **Pengembalian Pesanan** — kredit yang diberikan saat pesanan dikembalikan ke dompet
- **Hadiah Afiliasi** — kredit yang diperoleh melalui program afiliasi
- **Promosi** — kredit yang diberikan sebagai bagian dari kampanye pemasaran
- **Penyesuaian Manual** — kredit yang ditambahkan atau dikurangi secara langsung oleh staf
- **Pembayaran Pesanan** — dana yang digunakan saat checkout untuk membayar pesanan. Belum digunakan — disisihkan untuk saat fitur pengeluaran dompet checkout diluncurkan

## Penyesuaian dompet secara manual

Anda tidak dapat menambah atau mengurangi dana dari panel admin — transaksi dompet hanya dibuat oleh proses yang mengelolanya: pengembalian pesanan, hadiah loyalitas, dan hadiah referensi. Ini adalah kebijakan sengaja. Setiap pergerakan memiliki referensi kembali ke penyebabnya, dan pemeriksaan malam hari memverifikasi saldo setiap dompet terhadap sejarahnya sendiri; baris yang dimasukkan secara manual yang memecah rantai tersebut.

Untuk kredit kebaikan — keluhan layanan, tindakan setelah masalah — keluarkan **kartu hadiah** secara manual alih-alih (lihat topik bantuan **Kartu Hadiah**). Kartu hadiah dirancang untuk persis ini: Anda mengontrol nilai, pelanggan menerima kode melalui email, dan dapat digunakan saat checkout dengan cara yang sama seperti kredit toko.

## Memblokir dompet

Jika Anda perlu mencegah pelanggan menggunakan saldo dompet mereka — misalnya, selama penyelidikan penipuan — Anda dapat menonaktifkannya tanpa menghapusnya atau menghilangkan saldo.

1. Buka tampilan detail dompet pelanggan
2. Nonaktifkan toggle **Aktif**
3. Klik **Simpan**

Saldo tetap dipertahankan dan dompet dapat diaktifkan kapan saja. Selama tidak aktif, tidak ada kredit atau debet baru — manual atau lainnya — dapat dicatat terhadap dompet.

## Melihat semua transaksi

Untuk tampilan toko-wide aktivitas dompet, navigasikan ke **Pelanggan > Transaksi Dompet**. Daftar ini menampilkan setiap transaksi di semua dompet pelanggan, dengan filter untuk:

- **Jenis Transaksi** — filter berdasarkan kredit, debet, penyesuaian, dll.
- **Sumber** — filter berdasarkan tempat transaksi berasal
- **Status** — filter berdasarkan selesai, menunggu, atau dibatalkan
- **Tanggal** — gunakan hierarki tanggal di bagian atas untuk menelusuri hari, bulan, atau tahun tertentu

Daftar transaksi hanya untuk dibaca — transaksi tidak dapat diedit atau dihapus dari tampilan ini.

## Tips

- Periksa **Kredited Seumur Hidup** versus **Digunakan Seumur Hidup** untuk memahami seberapa aktif pelanggan menggunakan kredit toko mereka — saldo besar yang tidak digunakan mungkin menunjukkan pelanggan lupa bahwa kredit tersebut ada
- Jika pelanggan melaporkan bahwa saldonya terlihat salah, tinjau sejarah transaksi lengkap untuk melacak persis bagaimana saldo berubah seiring waktu; kolom **Saldo Setelah** pada setiap entri membuat ini mudah
- Saldo besar yang belum digunakan layak untuk dikirimkan pesan — pelanggan melihat kredit toko mereka di dashboard akun dan di langkah pembayaran saat checkout, tetapi email singkat yang menunjukkannya sering mengubahnya menjadi pesanan
- Dompet yang dibekukan tetap mempertahankan saldonya secara permanen; tidak ada masa kedaluwarsa — jika Anda menonaktifkan dompet sementara, ingat untuk mengaktifkannya kembali ketika masalahnya selesai
- **ID Referensi** pada setiap transaksi menghubungkannya kembali ke catatan asal, membuatnya mudah untuk memverifikasi mengapa kredit atau debet diterapkan tanpa harus mencari di tempat lain
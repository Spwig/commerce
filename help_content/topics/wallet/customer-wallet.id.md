---
title: Dompet Pelanggan
---

Dompet pelanggan adalah sistem kredit toko yang memberikan pelanggan saldo yang dapat mereka gunakan untuk pesanan masa depan. Kredit toko dapat ditambahkan sebagai hasil dari pengembalian dana, hadiah referral, kampanye promosi, atau penyesuaian manual yang dilakukan oleh tim Anda. Pelanggan kemudian dapat menerapkan saldo dompet mereka saat checkout untuk mengurangi jumlah yang mereka bayar.

Navigasikan ke **Pelanggan > Dompet Pelanggan** untuk melihat dan mengelola dompet.

## Memahami saldo dompet

Setiap dompet pelanggan menampilkan empat angka saldo:

| Saldo | Deskripsi |
|---|---|
| **Saldo Tersedia** | Jumlah yang dapat dibelanjakan oleh pelanggan saat ini saat checkout |
| **Saldo Tertunda** | Kredit yang belum dapat digunakan — contohnya, pengembalian dana yang masih dalam jendela konfirmasi |
| **Total Kredit Seumur Hidup** | Total jumlah yang pernah dikreditkan ke dompet ini, termasuk semua kredit masa lalu |
| **Total Penggunaan Seumur Hidup** | Total jumlah yang telah dibelanjakan oleh pelanggan dari dompet mereka di semua pesanan |

Saldo tersedia adalah satu-satunya angka yang penting saat checkout. Kredit tertunda menjadi tersedia setelah periode tertunda berakhir.

## Melihat dompet pelanggan

1. Navigasikan ke **Pelanggan > Dompet Pelanggan**
2. Gunakan bidang pencarian untuk menemukan pelanggan berdasarkan nama atau email
3. Klik entri dompet untuk membuka tampilan detail

Tampilan detail menampilkan saldo saat ini di bagian atas dan riwayat transaksi lengkap di bawahnya. Timestamp **Terakhir Dikreditkan Pada** dan **Terakhir Digunakan Pada** memberi tahu kapan dompet terakhir kali aktif.

### Memfilter daftar dompet

Gunakan filter **Aktif** untuk memisahkan dompet yang aktif dari yang beku. Dompet yang ditandai sebagai tidak aktif tidak dapat digunakan saat checkout meskipun memiliki saldo positif.

## Membaca riwayat transaksi

Setiap perubahan pada saldo dompet dicatat sebagai transaksi individual. Riwayat transaksi adalah buku besar lengkap dan permanen — transaksi tidak pernah diedit atau dihapus. Jika ada kesalahan yang perlu diperbaiki, transaksi kompensasi baru ditambahkan sebagai gantinya.

Setiap transaksi menampilkan:

| Bidang | Deskripsi |
|---|---|
| **Jenis** | Kredit, Debit, Pengembalian, Penyesuaian, atau Pembatalan |
| **Jumlah** | Nilai transaksi ini (selalu ditampilkan sebagai angka positif) |
| **Saldo Setelah** | Saldo dompet segera setelah transaksi ini diterapkan |
| **Sumber** | Di mana kredit atau debet berasal |
| **Status** | Selesai, Tertunda, atau Dibatalkan |
| **Deskripsi** | Penjelasan singkat tentang transaksi |
| **ID Referensi** | Tautan ke catatan asal (misalnya, nomor pesanan atau ID hadiah) |
| **Dibuat Pada** | Kapan transaksi dicatat |

### Penjelasan jenis transaksi

- **Kredit** — dana yang ditambahkan ke dompet (dari pengembalian, promosi, atau penyesuaian manual)
- **Debit** — dana yang dibelanjakan saat checkout
- **Pengembalian** — kredit yang ditambahkan secara khusus sebagai hasil dari pesanan yang dikembalikan atau dibatalkan
- **Penyesuaian** — penyesuaian manual yang dilakukan oleh tim Anda
- **Pembatalan** — transaksi yang membatalkan entri sebelumnya

### Penjelasan sumber transaksi

- **Pengembalian Pesanan** — kredit yang diberikan saat pesanan dikembalikan ke dompet
- **Hadiah Referral** — kredit yang diperoleh melalui program referral
- **Promosi** — kredit yang diberikan sebagai bagian dari kampanye pemasaran
- **Penyesuaian Manual** — kredit yang ditambahkan atau dikurangi secara langsung oleh staf
- **Pembayaran Pesanan** — dana yang dibelanjakan saat checkout untuk membayar pesanan

## Penyesuaian dompet manual

Anda tidak dapat menambahkan atau mengurangi dana secara langsung dari tampilan detail dompet — transaksi dompet dibuat melalui proses yang relevan (pengembalian, hadiah, promosi). Namun, staf dengan izin yang sesuai dapat membuat transaksi penyesuaian manual melalui bagian **Transaksi Dompet**.

Navigasikan ke **Pelanggan > Transaksi Dompet** dan gunakan **+ Tambahkan Transaksi Dompet** jika Anda perlu menerapkan kredit yang tidak cocok dengan sumber lain — contohnya, kredit kebaikan setelah keluhan layanan.

Ketika membuat penyesuaian manual:

1.

Pilih **Dompet** yang sedang disesuaikan (cari berdasarkan email pelanggan)
2.


Setel **Jenis Transaksi** menjadi `Adjustment`
3.

Setel **Sumber** menjadi `Manual Adjustment`
4.

Masukkan **Jumlah** — selalu dalam bentuk angka positif terlepas dari arahnya
5.

Setel **Status** menjadi `Completed` untuk kredit segera
6.

Tambahkan **Deskripsi** yang jelas yang menjelaskan alasan — ini terlihat dalam riwayat transaksi
7.

Klik **Simpan**

> **Catatan:** Karena transaksi dompet tidak dapat diubah, pastikan kembali jumlah dan dompet sebelum menyimpan. Jika Anda membuat kesalahan, Anda akan perlu membuat transaksi pembalikan untuk memperbaikinya.

## Memblokir dompet

Jika Anda perlu mencegah pelanggan menggunakan saldo dompet mereka — misalnya, selama penyelidikan penipuan — Anda dapat menonaktifkannya tanpa menghapusnya atau menghilangkan saldo.

1. Buka tampilan detail dompet pelanggan
2. Nonaktifkan toggle **Aktif**
3. Klik **Simpan**

Saldo tetap terjaga dan dompet dapat diaktifkan kapan saja. Selama tidak aktif, pelanggan tidak dapat menggunakan saldo dompet saat checkout.

## Melihat semua transaksi

Untuk tampilan menyeluruh transaksi dompet, navigasikan ke **Pelanggan > Transaksi Dompet**. Daftar ini menampilkan setiap transaksi di semua dompet pelanggan, dengan filter untuk:

- **Jenis Transaksi** — filter berdasarkan kredit, debet, penyesuaian, dll.
- **Sumber** — filter berdasarkan tempat transaksi berasal
- **Status** — filter berdasarkan selesai, menunggu, atau dibatalkan
- **Tanggal** — gunakan hierarki tanggal di bagian atas untuk menelusuri hari, bulan, atau tahun tertentu

Daftar transaksi hanya untuk dibaca — transaksi tidak dapat diedit atau dihapus dari tampilan ini.

## Tips

- Periksa **Kredited Seumur Hidup** versus **Digunakan Seumur Hidup** untuk memahami seberapa aktif pelanggan menggunakan kredit toko mereka — saldo yang besar dan tidak digunakan mungkin menunjukkan pelanggan lupa bahwa kredit tersebut ada
- Jika pelanggan melaporkan bahwa saldo terlihat salah, tinjau riwayat transaksi lengkap untuk melacak secara tepat bagaimana saldo berubah seiring waktu; kolom **Saldo Setelah** pada setiap entri membuat ini mudah
- Gunakan kredit dompet sebagai alat retensi pelanggan — kredit kebaikan setelah pengalaman pemesanan yang sulit dapat lebih murah daripada pengembalian dana sambil tetap mempertahankan pelanggan berbelanja di toko Anda
- Dompet yang dibekukan tetap mempertahankan saldonya secara permanen; tidak ada masa kedaluwarsa — jika Anda menonaktifkan dompet sementara, ingatlah untuk mengaktifkannya kembali ketika masalah selesai
- **ID Referensi** pada setiap transaksi terkait dengan catatan asalnya, sehingga memudahkan untuk memverifikasi mengapa kredit atau debet diterapkan tanpa harus mencari di tempat lain
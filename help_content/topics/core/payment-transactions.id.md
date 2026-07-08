---
title: Transaksi Pembayaran
---

Transaksi pembayaran adalah catatan lengkap dari setiap kejadian pembayaran yang diproses melalui toko Anda — tagihan, pengembalian dana, otorisasi, dan lainnya. Bagian ini juga mencakup log webhook dari penyedia pembayaran Anda dan niat pembayaran yang dibuat selama proses checkout.

## Transaksi Pembayaran

Beralih ke **Pembayaran > Transaksi Pembayaran** untuk melihat setiap transaksi yang telah diproses toko Anda.

### Jenis Transaksi

| Jenis | Artinya |
|------|--------------|
| **Tagihan** | Pembayaran langsung — dana dikumpulkan saat transaksi |
| **Otorisasi** | Dana dipegang di kartu pelanggan tetapi belum dikumpulkan |
| **Pengambilan** | Mengumpulkan dana dari otorisasi sebelumnya |
| **Batal** | Membatalkan otorisasi sebelum diambil |
| **Pengembalian Dana** | Mengembalikan pembayaran ke pelanggan |

### Status Transaksi

| Status | Artinya |
|--------|--------------|
| **Menunggu** | Transaksi telah dimulai tetapi belum diproses |
| **Diproses** | Sedang diproses oleh penyedia pembayaran |
| **Diorisasi** | Dana dipegang — menunggu pengambilan |
| **Selesai** | Pembayaran berhasil |
| **Gagal** | Pembayaran ditolak atau terjadi kesalahan |
| **Dibatalkan** | Otorisasi dibatalkan sebelum diambil |
| **Dikembalikan** | Pengembalian penuh telah dikeluarkan |
| **Dikembalikan Sebagian** | Sebagian dari pembayaran telah dikembalikan |

### Apa yang dapat Anda lihat pada catatan transaksi

Setiap transaksi menampilkan:
- **ID Transaksi** — Referensi internal Spwig
- **ID Transaksi Penyedia** — Referensi dari penyedia pembayaran Anda (misalnya, ID tagihan Stripe)
- **Jumlah** — Jumlah transaksi dan mata uang
- **Status** dan **Jenis**
- **Email Pelanggan** dan **Nama Pelanggan**
- **Metode Pembayaran** — Jenis (kartu kredit, transfer bank, dll.) dan 4 digit terakhir
- **Pemesanan** — Pesanan yang transaksi ini termasuk dalam
- **Akun Penyedia** — Penyedia pembayaran yang memprosesnya
- **Respons Penyedia** — Respons teknis mentah dari penyedia pembayaran
- **Pesan Kesalahan** — Jika transaksi gagal, alasan yang diberikan oleh penyedia
- Timestamp untuk pembuatan, pembaruan terakhir, dan penyelesaian

### Memfilter transaksi

Gunakan filter admin untuk menyempitkan transaksi berdasarkan:
- Status (misalnya, tampilkan hanya transaksi yang gagal)
- Jenis (misalnya, tampilkan hanya pengembalian dana)
- Akun penyedia
- Rentang tanggal

Ini berguna untuk rekonsiliasi akhir hari atau menyelidiki sejarah pembayaran pelanggan tertentu.

### Kapan transaksi dapat dikembalikan?

Transaksi dapat dikembalikan ketika:
- Statusnya adalah **Selesai**
- Jenisnya adalah **Tagihan** atau **Pengambilan**

Untuk mengeluarkan pengembalian dana, gunakan aksi **Pengembalian Dana** dari halaman detail pesanan. Pengembalian dana yang diproses melalui pesanan membuat catatan transaksi baru dengan jenis **Pengembalian Dana**.

### Alur Otorisasi dan Pengambilan

Beberapa metode pembayaran (dan beberapa penyedia pembayaran) mendukung otorisasi dan pengambilan terpisah. Ini berguna jika Anda ingin memverifikasi pembayaran sebelum pengiriman:

1. **Otorisasi** — Dana dipegang di kartu pelanggan (status: `Diorisasi`)
2. **Pengambilan** — Dicetuskan ketika pesanan dikirim atau selesai
3. Jika tidak diambil dalam jendela otorisasi, pegangan **berakhir** secara otomatis

Bidang **Berakhir Pada** pada transaksi menunjukkan kapan otorisasi akan berakhir.

## Webhook Pembayaran

Penyedia pembayaran mengirimkan acara webhook untuk memberi tahu toko Anda tentang perubahan status pembayaran — misalnya, ketika pembayaran berhasil, gagal, atau sengketa muncul. Spwig mencatat semua webhook yang masuk.

Beralih ke **Pembayaran > Webhook Pembayaran** untuk melihat log.

### Apa yang ditampilkan oleh catatan webhook


| Field | Description |
|-------|-------------|
| **Provider** | Which payment provider sent the webhook |
| **Event ID** | The provider's unique event identifier |
| **Event Type** | The type of event (e.g., `payment_intent.succeeded`, `charge.refunded`) |
| **Processed** | Whether Spwig has acted on this webhook |
| **Signature Verified** | Whether the webhook's security signature was valid |
| **Payload** | The full data sent by the provider |
| **Processing Result** | What Spwig did in response |
| **Processing Error** | Any error that occurred during processing |
| **Received At** | When the webhook arrived |

### Menggunakan log webhook untuk penyelesaian masalah

Jika pembayaran tampak macet atau status pesanan tidak diperbarui setelah pembayaran:

1. Navigasikan ke **Payments > Payment Webhooks**
2. Filter berdasarkan penyedia dan cari acara terbaru
3. Periksa kolom **Processed** — webhook yang belum diproses mungkin menunjukkan masalah pengiriman
4. Periksa **Signature Verified** — tanda tangan yang gagal mungkin berarti webhook secret Anda dikonfigurasi dengan salah
5. Tinjau **Processing Error** untuk pesan kesalahan apa pun

Acara duplikat ditangani secara otomatis — kombinasi `Event ID` dan penyedia adalah unik, sehingga webhook yang sama tidak dapat diproses dua kali.

## Payment intents

A payment intent melacak siklus hidup pembayaran checkout dari saat pelanggan memulai proses pembayaran hingga hasil akhir. Payment intents dibuat secara otomatis ketika pelanggan mencapai langkah pembayaran di checkout.

Navigasikan ke **Payments > Payment Intents** untuk melihat daftarnya.

### Payment intent statuses

| Status | Meaning |
|--------|---------|
| **Created** | Intent telah dibuat, menunggu metode pembayaran |
| **Requires Payment Method** | Menunggu pelanggan memasukkan detail kartu mereka |
| **Requires Confirmation** | Detail pembayaran telah dimasukkan, menunggu konfirmasi |
| **Requires Action** | Pelanggan perlu menyelesaikan tindakan (misalnya, otentikasi 3D Secure) |
| **Processing** | Pembayaran sedang diproses |
| **Succeeded** | Pembayaran selesai dengan sukses |
| **Canceled** | Pembayaran dibatalkan atau dibatalkan |
| **Failed** | Upaya pembayaran gagal |

### Alur payment intent ke pesanan

1. Pelanggan mencapai langkah pembayaran checkout → Spwig membuat **Payment Intent** dan **Order** draft (belum dibayar)
2. Pelanggan memasukkan detail pembayaran dan mengonfirmasi
3. Penyedia pembayaran memproses pembayaran
4. Pada keberhasilan, Order diperbarui menjadi **Paid** dan Payment Intent berpindah ke **Succeeded**
5. Catatan **Payment Transaction** dibuat dengan detail tagihan akhir

Payment intent menghubungkan sesi checkout, akun penyedia, dan pesanan — memberi Anda gambaran lengkap tentang perjalanan checkout pelanggan.

### Menggunakan payment intents untuk dukungan

Jika pelanggan melaporkan bahwa mereka telah membayar tetapi pesanan menunjukkan sebagai belum dibayar:

1. Cari pesanan pelanggan di **Orders**
2. Navigasikan ke **Payments > Payment Intents** dan cari intents yang terkait dengan pesanan tersebut
3. Periksa status intent — jika statusnya **Succeeded**, periksa transaksi yang terkait
4. Jika intentnya **Requires Action**, pelanggan mungkin belum menyelesaikan otentikasi 3D Secure
5. Jika intentnya **Failed**, detail kesalahan menjelaskan mengapa pembayaran ditolak

## Tips

- Tinjau transaksi yang gagal setiap hari — pola kegagalan (misalnya, metode pembayaran atau negara tertentu) mungkin menunjukkan masalah konfigurasi atau upaya penipuan.
- Log webhook sangat berharga saat menyelidiki ketidaksesuaian pembayaran.

Jika pesanan telah dibayar tetapi tidak dikonfirmasi, log webhook biasanya akan memberi tahu Anda apa yang salah.
- Penahanan otorisasi berakhir secara otomatis — jika Anda menggunakan authorise-then-capture, pastikan proses penyelesaian Anda menangkap dana sebelum jendela kedaluwarsa berakhir (biasanya 7 hari untuk sebagian besar penyedia).
- Bidang **Provider Response** pada transaksi berisi data mentah dari penyedia pembayaran.

Bagikan ini dengan tim dukungan penyedia Anda jika Anda membutuhkan bantuan untuk menyelesaikan masalah transaksi tertentu.
- Gagal verifikasi tanda tangan pada webhooks harus segera diselidiki — mereka mungkin menunjukkan webhook secret yang dikonfigurasi dengan salah atau upaya untuk mengirimkan acara webhook penipuan ke toko Anda.
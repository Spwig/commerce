---
title: Mengelola Langganan Pelanggan
---

Bagian langganan pelanggan memberi Anda pandangan lengkap mengenai semua langganan berulang yang aktif, dijeda, dan dibatalkan di toko Anda. Dari sini Anda dapat memantau kesehatan pembayaran, melihat detail langganan individu, dan mengambil tindakan ketika ada masalah.

## Melihat langganan pelanggan

Navigasikan ke **Langganan > Langganan Pelanggan** untuk melihat daftar lengkap langganan dari semua pelanggan.

![Daftar langganan pelanggan](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

Daftar ini menampilkan pelanggan, nama rencana, status saat ini, tanggal pembayaran berikutnya, dan jumlah siklus pembayaran yang telah selesai untuk setiap langganan.

### Memfilter dan mencari

Gunakan panel filter di sebelah kanan untuk menyaring langganan berdasarkan:

- **Status** — Saring berdasarkan Aktif, Uji Coba, Terlambat, Dijeda, Dibatalkan, atau Berakhir
- **Rencana** — Lihat langganan untuk rencana tertentu
- **Mode Pemasok** — Bawaan (Dikelola oleh Stripe/PayPal) atau Cadangan (pembayaran internal)

Gunakan bilah pencarian untuk mencari langganan berdasarkan alamat email pelanggan.

## Status langganan

Memahami setiap status membantu Anda mengidentifikasi langganan yang memerlukan perhatian:

| Status | Artinya |
|--------|---------------|
| **Uji Coba** | Pelanggan sedang dalam periode uji coba gratis atau harga yang lebih rendah |
| **Aktif** | Langganan sehat — pembayaran saat ini dan akses aktif |
| **Terlambat** | Upaya pembayaran gagal — sistem sedang mencoba kembali. Pelanggan tetap memiliki akses selama periode grasi |
| **Dijeda** | Langganan sementara ditangguhkan — tidak ada pembayaran, tidak ada akses |
| **Dibatalkan** | Permohonan pembatalan telah diajukan. Pelanggan mungkin masih memiliki akses hingga tanggal akhir periode |
| **Berakhir** | Langganan telah berakhir sepenuhnya — uji coba berakhir, jumlah siklus pembayaran maksimum tercapai, atau periode pembatalan telah berlalu |

Langganan yang **Terlambat** memerlukan perhatian paling besar — jika pembayaran terus gagal dan periode grasi berakhir, langganan akan ditangguhkan.

## Melihat detail langganan

Klik pada langganan apa pun untuk membuka tampilan detail. Ini menampilkan:

### Periode pembayaran saat ini

- **Awal / Akhir Periode Saat Ini** — Tanggal jendela pembayaran aktif
- **Tanggal Pembayaran Berikutnya** — Kapan upaya pembayaran berikutnya akan dilakukan
- **Tanggal Pembayaran Terakhir** dan **Status Pembayaran Terakhir** — Hasil upaya pembayaran terbaru
- **Jumlah Siklus Pembayaran** — Berapa banyak siklus pembayaran yang berhasil selesai

### Informasi langganan

- **Rencana** dan **Tingkat Harga** — Rencana dan frekuensi pembayaran yang digunakan pelanggan
- **Produk / Varian** — Produk katalog yang terkait dengan langganan ini (jika berlaku)
- **Jumlah** — Jumlah kursi atau unit (untuk rencana berbasis kuantitas)
- **Token Pembayaran** — Metode pembayaran yang disimpan yang digunakan untuk pembayaran berulang

### Detail uji coba

Jika langganan sedang dalam uji coba, **Tanggal Akhir Uji Coba** menunjukkan kapan uji coba pelanggan berakhir dan pembayaran penuh dimulai.

### Detail pembatalan

Untuk langganan yang dibatalkan, Anda dapat melihat:

- **Jenis Pembatalan** — Apakah pembatalan dilakukan segera, pada akhir periode, atau dijadwalkan
- **Dibatalkan Pada** — Kapan pembatalan diajukan
- **Alasan Pembatalan** — Catatan mengenai alasan pelanggan membatalkan (jika dicatat)
- **Tanggal Batas Pembaruan** — Tanggal terakhir pelanggan dapat membarui tanpa mendaftar ulang dari awal

### Periode grasi dan komitmen

- **Tanggal Akhir Periode Grasi** — Jika pembayaran gagal, ini menunjukkan tanggal batas sebelum akses ditangguhkan
- **Tanggal Akhir Komitmen Minimum** — Untuk rencana dengan komitmen minimum, tanggal pembatalan tercepat

## Menjeda langganan

Langganan yang dijeda menghentikan pembayaran sementara sekaligus menangguhkan akses. Ini berguna untuk pelanggan yang ingin beristirahat tanpa membatalkan sepenuhnya.

Untuk melihat langganan yang dijeda, saring berdasarkan **Status: Dijeda**. Tampilan detail menampilkan:

- **Dijeda Pada** — Kapan penjedaan dimulai
- **Alasan Penjedaan** — Catatan mengenai alasan penjedaan
- **Tanggal Pemulihan Otomatis** — Jika diatur, tanggal langganan akan secara otomatis melanjutkan pembayaran dan akses


Langganan akan dilanjutkan pada tanggal auto-resume atau ketika pelanggan secara manual mengaktifkan kembali.

## Riwayat siklus pembayaran

Setiap upaya pembayaran — berhasil atau gagal — dicatat dalam riwayat siklus pembayaran. Navigasikan ke **Subscriptions > Billing Cycle Logs** untuk melihat riwayat ini.

![Billing cycle log list](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Membaca entri riwayat siklus pembayaran

Setiap entri log mencatat:

- **Subscription** — Langganan pelanggan mana upaya pembayaran ini termasuk
- **Cycle Number** — Siklus pembayaran berurutan (Cycle 1 = pembayaran pertama setelah masa uji coba)
- **Billing Date** — Kapan pembayaran dicoba
- **Status** — Menunggu, Diproses, Berhasil, Gagal, atau Dicoba Kembali
- **Amount breakdown**:
  - **Base Amount** — Harga rencana sebelum setiap penyesuaian
  - **Quantity Amount** — Biaya tambahan untuk jumlah kursi/unit
  - **Add-ons Amount** — Total biaya dari add-ons aktif
  - **Discount Amount** — Total diskon yang diterapkan
  - **Total Amount** — Jumlah akhir yang dibebankan (atau dicoba)
- **Payment Method** — Kartu atau metode pembayaran yang digunakan
- **Provider Transaction ID** — Nomor referensi dari penyedia pembayaran (berguna untuk pencarian pengembalian dana)
- **Failure Reason** — Jika pembayaran gagal, mengapa pembayaran gagal (misalnya, kartu ditolak, dana tidak cukup)

### Diagnosa kegagalan pembayaran

Jika pelanggan menghubungi Anda mengenai masalah pembayaran, cari langganan mereka dan periksa riwayat siklus pembayaran. Bidang **Failure Reason** menjelaskan apa yang salah. Alasan kegagalan umum meliputi:

- **Card declined** — Kartu pelanggan ditolak oleh bank mereka
- **Insufficient funds** — Saldo akun terlalu rendah saat pembayaran
- **Card expired** — Metode pembayaran yang disimpan sudah kedaluwarsa
- **Network error** — Masalah sementara koneksi dengan penyedia pembayaran — biasanya teratasi saat dicoba kembali

Untuk kegagalan yang terus-menerus, arahkan pelanggan untuk memperbarui metode pembayaran mereka di pengaturan akun mereka.

## Tips

- Periksa filter **Past Due** setiap minggu untuk menangkap langganan yang berisiko churn. Email cepat ke pelanggan sering kali menyelesaikan masalah pembayaran sebelum masa grasi berakhir.
- Riwayat siklus pembayaran hanya bisa dibaca — mereka dibuat secara otomatis dan tidak dapat diubah. Ini memastikan jejak audit yang andal.
- Jika langganan pelanggan menunjukkan **Past Due** tetapi mereka sudah memperbarui metode pembayaran mereka, percobaan otomatis berikutnya akan mengambil kartu baru. Percobaan mengikuti jadwal masa grasi yang dikonfigurasikan dalam rencana.
- Langganan yang **Expired** tidak dihapus — mereka tetap terlihat untuk pelaporan. Gunakan filter tanggal untuk fokus pada langganan aktif saat ini.
- Untuk langganan dalam **Trial**, periksa **Trial End Date** untuk memprediksi pembayaran pertama yang akan datang dan secara proaktif menangani masalah metode pembayaran.
---
title: Mengelola Langganan Pelanggan
---

Bagian langganan pelanggan memberi Anda pandangan lengkap tentang semua langganan berulang yang aktif, tertunda, dan dibatalkan di toko Anda. Di sini Anda dapat memantau kesehatan pembayaran, melihat detail langganan individu, dan mengambil tindakan ketika terjadi masalah.

## Melihat langganan pelanggan

Navigasi ke **Langganan > Langganan Pelanggan** untuk melihat daftar lengkap langganan di seluruh pelanggan.

![Daftar langganan pelanggan](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

Daftar menunjukkan pelanggan, nama rencana, status saat ini, tanggal pembayaran berikutnya, dan jumlah siklus pembayaran yang selesai untuk setiap langganan.

### Menyaring dan mencari

Gunakan panel penyaring di sebelah kanan untuk menyempitkan langganan berdasarkan:

- **Status** — Saring berdasarkan Aktif, Uji coba, Tenggat waktu, Ditangguhkan, Dibatalkan, atau Kedaluwarsa
- **Rencana** — Lihat langganan untuk rencana tertentu
- **Mode Penyedia** — Asli (dikelola Stripe/PayPal) atau Cadangan (pembayaran internal)

Gunakan bilah pencarian untuk menemukan langganan berdasarkan alamat surel pelanggan.

## Status langganan

Memahami setiap status membantu Anda mengidentifikasi langganan yang memerlukan perhatian:

| Status | Artinya |
|--------|-----------|
| **Uji coba** | Pelanggan dalam masa uji coba gratis atau harga berkurang |
| **Aktif** | Langganan sehat — pembayaran saat ini dan akses aktif |
| **Tenggat waktu** | Upaya pembayaran gagal — sistem sedang mencoba ulang. Pelanggan tetap memiliki akses selama masa tenggat |
| **Ditangguhkan** | Langganan ditangguhkan sementara — tidak ada pembayaran, tidak ada akses |
| **Dibatalkan** | Permintaan pembatalan telah diajukan. Pelanggan mungkin masih memiliki akses hingga tanggal akhir periode |
| **Kedaluwarsa** | Langganan telah berakhir sepenuhnya — masa uji coba habis, siklus pembayaran maksimum tercapai, atau periode pembatalan berlalu |

Langganan yang **Tenggat waktu** memerlukan perhatian paling banyak — jika pembayaran terus gagal dan masa tenggat habis, langganan akan ditangguhkan.

## Melihat detail langganan

Klik pada langganan apa pun untuk membuka tampilan detail. Ini menunjukkan:

### Siklus pembayaran saat ini

- **Mulai Siklus Saat Ini / Akhir** — Tanggal jendela pembayaran aktif
- **Tanggal Pembayaran Berikutnya** — Kapan penagihan berikutnya akan dicoba
- **Tanggal Pembayaran Terakhir** dan **Status Pembayaran Terakhir** — Hasil dari upaya pembayaran terbaru
- **Jumlah Siklus Pembayaran** — Berapa banyak siklus pembayaran yang berhasil selesai

### Informasi langganan

- **Rencana** dan **Tingkat Harga** — Rencana dan frekuensi pembayaran yang digunakan pelanggan
- **Produk / Variasi** — Produk katalog yang terkait dengan langganan ini (jika berlaku)
- **Jumlah** — Jumlah kursi atau unit (untuk rencana berbasis jumlah)
- **Token Pembayaran** — Metode pembayaran yang disimpan yang digunakan untuk pembayaran berulang

### Detail uji coba

Jika langganan dalam masa uji coba, **Tanggal Berakhirnya Uji Coba** menunjukkan kapan masa uji coba pelanggan berakhir dan pembayaran penuh dimulai.

### Detail pembatalan

Untuk langganan yang dibatalkan, Anda dapat melihat:

- **Jenis Pembatalan** — Apakah pembatalan dilakukan secara langsung, pada akhir periode, atau dijadwalkan
- **Dibatalkan Pada** — Kapan pembatalan diajukan
- **Alasan Pembatalan** — Catatan tentang mengapa pelanggan membatalkan (jika dicatat)
- **Tenggat Waktu Pemulihan** — Tanggal terakhir pelanggan dapat memulihkan tanpa harus berlangganan dari awal

### Masa tenggat dan komitmen

- **Tanggal Berakhirnya Masa Tenggat** — Jika pembayaran gagal, ini menunjukkan tenggat waktu sebelum akses ditangguhkan
- **Tanggal Berakhirnya Komitmen Minimum** — Untuk rencana dengan komitmen minimum, tanggal pembatalan terdini

## Menonaktifkan langganan

Langganan yang ditangguhkan menghentikan pembayaran secara sementara sambil juga menangguhkan akses. Ini berguna bagi pelanggan yang ingin berhenti sejenak tanpa sepenuhnya membatalkannya.

Untuk melihat langganan yang ditangguhkan, saring berdasarkan **Status: Ditangguhkan**. Tampilan detail menunjukkan:

- **Ditangguhkan Pada** — Kapan penangguhan dimulai
- **Alasan Penangguhan** — Catatan mengapa ditangguhkan
- **Tanggal Pemulihan Otomatis** — Jika diatur, tanggal ketika langganan akan secara otomatis melanjutkan pembayaran dan akses

Langganan dilanjutkan pada tanggal auto-resume atau ketika pelanggan secara manual mengaktifkan kembali langganan tersebut.

## Catatan siklus pembayaran

Setiap upaya pembayaran — berhasil atau gagal — dicatat dalam catatan siklus pembayaran. Navigasi ke **Langganan > Catatan Siklus Pembayaran** untuk melihat riwayat ini.

![Daftar catatan siklus pembayaran](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Membaca entri catatan siklus pembayaran

Setiap entri catatan mencatat:

- **Langganan** — Langganan pelanggan mana yang termasuk dalam upaya pembayaran ini
- **Nomor Siklus** — Siklus pembayaran berurutan (Siklus 1 = tagihan pertama setelah percobaan)
- **Tanggal Pembayaran** — Kapan tagihan dilakukan
- **Status** — Tertunda, Sedang Diproses, Berhasil, Gagal, atau Sedang Diulang
- **Pemecahan Jumlah**:
  - **Jumlah Dasar** — Harga rencana sebelum penyesuaian apa pun
  - **Jumlah Kuantitas** — Biaya tambahan untuk jumlah kursi/unit
  - **Jumlah Tambahan** — Total biaya tambahan yang aktif
  - **Jumlah Diskon** — Total diskon yang diterapkan
  - **Jumlah Total** — Jumlah yang dibebankan (atau dicoba)
- **Metode Pembayaran** — Kartu atau metode pembayaran yang digunakan
- **ID Transaksi Penyedia** — Nomor referensi penyedia pembayaran (berguna untuk pencarian refund)
- **Alasan Kegagalan** — Jika pembayaran gagal, mengapa gagal (misalnya, kartu ditolak, dana tidak cukup)

### Mendiagnosis kegagalan pembayaran

Jika seorang pelanggan menghubungi Anda tentang masalah pembayaran, temukan langganan mereka dan periksa catatan siklus pembayaran. Kolom **Alasan Kegagalan** menjelaskan apa yang salah. Alasan kegagalan umum termasuk:

- **Kartu ditolak** — Kartu pelanggan ditolak oleh bank mereka
- **Dana tidak cukup** — Saldo rekening terlalu rendah saat pembayaran dilakukan
- **Kartu kedaluwarsa** — Metode pembayaran yang disimpan telah kedaluwarsa
- **Kesalahan jaringan** — Masalah koneksi sementara dengan penyedia pembayaran — biasanya terselesaikan saat dicoba ulang

Untuk kegagalan yang berkelanjutan, arahkan pelanggan untuk memperbarui metode pembayaran mereka di pengaturan akun mereka.

## Bagaimana langganan diaktifkan kembali

Setiap tagihan ulang yang berhasil menciptakan pesanan yang dibayar baru untuk siklus pembayaran tersebut — bukan hanya catatan pembayaran. Pesanan ini melewati proses pemenuhan normal Anda, persis seperti pesanan yang dipesan saat checkout:

- **Produk fisik** — Pesanan ulang memasuki antrian pemenuhan biasa Anda untuk pemilihan, pengemasan, dan pengiriman. Tidak secara otomatis dialokasikan stok saat kartu dicicil, jadi kekurangan stok sementara tidak pernah menghalangi pembayaran yang berhasil — Anda akan melihat pesanan tersebut dan dapat memenuhinya sesuai dengan stok yang tersedia.
- **Produk digital** — Akses (tautan unduh, kunci lisensi) diberikan kembali secara otomatis segera setelah pesanan ulang dibuat, sama seperti halnya untuk pembelian pertama.

Pesanan ulang menyalin detail pengiriman dan pembayaran dari pesanan yang memulai langganan, jadi Anda tidak perlu memasukkan apa pun lagi. Mereka tidak memiliki badge khusus di daftar **Pesanan** Anda, tetapi Anda selalu dapat melacak siklus tertentu kembali ke pesanannya: buka **Langganan > Catatan Siklus Pembayaran**, klik entri catatan untuk siklus tersebut, dan kolom **Pesanan** langsung mengarah ke pesanan tersebut.

## Email langganan otomatis

Spwig mengirim email siklus langganan secara otomatis — Anda tidak perlu memicu ini secara manual. Email yang paling sering ditanyakan oleh pedagang:

| Email | Kapan dikirim |
|-------|----------------|
| **Peringatan ulang** | Sebelum tagihan ulang yang akan datang |
| **Akhir percobaan** | Sebelum masa percobaan gratis atau harga rendah berubah menjadi pembayaran penuh |
| **Pembayaran gagal** | Langsung setelah tagihan ulang gagal, dan lagi sebagai pemberitahuan terakhir jika masa tenggang akan segera berakhir (dunning) |
| **Konfirmasi pembatalan** | Ketika langganan dibatalkan |

Spwig juga mengirim email selamat datang, sukses pembayaran, jeda/aktif kembali, kedaluwarsa, aktif kembali, perubahan rencana, dan kedaluwarsa metode pembayaran pada titik yang sesuai dalam siklus hidup langganan.

Semua ini adalah template email biasa — lihat [Template Email](/bantuan/template-email) untuk meninjau atau mempersonalisasi isinya dan memastikan mereka aktif.

## Layanan pelanggan sendiri pengguna

Pelanggan tidak perlu menghubungi Anda untuk perubahan langganan rutin — mereka dapat mengelola langganan mereka sendiri dari akun mereka: melihat detail dan riwayat pembayaran, menunda, melanjutkan, menghapus, dan memperbarui metode pembayaran yang tersimpan. Ini mencakup sebagian besar hal yang sebelumnya akan masuk ke antrian dukungan Anda, jadi ketika pelanggan menghubungi tentang langganan mereka, penting untuk terlebih dahulu memeriksa apakah mereka telah mencoba halaman akun mereka sebelum Anda membuat perubahan untuk mereka di admin.

## Tips

- Periksa filter **Tenggat** secara berkala untuk menangkap langganan yang berisiko hilang. Email singkat kepada pelanggan sering kali menyelesaikan masalah pembayaran sebelum masa grace period berakhir.
- Catatan siklus pembayaran bersifat baca saja — mereka dibuat secara otomatis dan tidak dapat diubah. Hal ini memastikan jejak audit yang dapat diandalkan.
- Jika langganan pelanggan menunjukkan **Tenggat** tetapi mereka telah memperbarui metode pembayaran mereka, pembaruan berikutnya akan mengambil kartu baru tersebut. Pembaruan ulang mengikuti jadwal grace period yang dikonfigurasi dalam rencana.
- Langganan **Kadaluarsa** tidak dihapus — tetap terlihat untuk pelaporan. Gunakan filter tanggal untuk fokus pada langganan yang sedang aktif saat ini.
- Untuk langganan dalam **Masa Percobaan**, periksa **Tanggal Berakhirnya Masa Percobaan** untuk memprediksi tagihan pertama yang akan datang dan secara proaktif menangani masalah metode pembayaran apa pun.
- Jika seorang pelanggan mengatakan bahwa pembaruan fisik "tidak juga dikirim", periksa antrian pemenuhan biasa Anda daripada catatan langganan — pesanan pembaruan dipenuhi dengan cara yang sama seperti pesanan lainnya dan tidak melompat antrian.
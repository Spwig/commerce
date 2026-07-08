---
title: Payout Processing
---

Pengolahan pembayaran memungkinkan Anda membayar afiliasi untuk komisi yang disetujui mereka. Panduan ini menunjukkan cara membuat, mengelola, dan memproses pembayaran melalui PayPal atau penyedia transfer bank.

![Daftar Pembayaran](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Ringkasan Pembayaran

Pembayaran adalah batch pembayaran yang mengelompokkan beberapa komisi yang disetujui untuk satu afiliasi. Bayangkan sebagai menulis cek untuk semua pendapatan yang belum dibayar.

Ciri khas utama:
- **Memuat beberapa komisi** — Satu pembayaran dapat mencakup puluhan komisi yang disetujui
- **Memerlukan ambang minimum** — Kebanyakan program memiliki jumlah pembayaran minimum ($50-$100 umum)
- **Diproses melalui penyedia** — PayPal atau Airwallex menangani transfer uang sebenarnya
- **Memiliki siklus hidup** — Menunggu → Diproses → Selesai (atau Gagal)

## Alur Pembayaran

Proses pembayaran lengkap mengikuti enam langkah:

1. **Afiliasi memperoleh komisi** — Penjualan yang diatribusikan ke tautan pelacakan afiliasi
2. **Pemilik toko menyetujui komisi** — Tinjau dan setujui komisi yang menunggu
3. **Saldo mencapai ambang minimum** — Saldo afiliasi yang disetujui mencapai ambang program
4. **Afiliasi meminta pembayaran** — Afiliasi mengajukan permintaan pembayaran di dasbor mereka
5. **Pemilik toko memproses pembayaran** — Anda membuat dan memproses pembayaran
6. **Pembayaran selesai** — Penyedia mengirim dana, komisi ditandai sebagai telah dibayar

## Melihat Pembayaran

Navigasikan ke **Program Afiliasi > Pembayaran** untuk mengakses dasbor manajemen pembayaran.

Panel statistik menampilkan:
- **Menunggu** — Pembayaran yang dibuat tetapi belum diproses
- **Diproses** — Saat ini dikirim ke penyedia pembayaran
- **Selesai** — Berhasil dibayar
- **Gagal** — Pembayaran gagal (memerlukan perhatian)

Tampilan daftar menampilkan:
- Nama dan kode afiliasi
- Jumlah pembayaran
- Metode pembayaran (PayPal atau Transfer Bank)
- Badge status
- Tanggal pembuatan dan penyelesaian
- Tombol aksi

Gunakan filter untuk menyempitkan berdasarkan:
- Afiliasi
- Metode pembayaran
- Status
- Rentang tanggal

## Membuat Pembayaran

Ikuti langkah-langkah berikut untuk membuat pembayaran baru:

1. **Navigasikan** ke **Program Afiliasi > Pembayaran**
2. **Klik** tombol **+ Tambahkan Pembayaran**
3. **Pilih afiliasi** dari dropdown
4. **Lihat komisi yang disetujui** — Sistem menampilkan semua komisi yang belum dibayar dan disetujui untuk afiliasi ini
5. **Pilih komisi yang akan dimasukkan** — Centang kotak untuk komisi yang akan dibayar (biasanya semua)
6. **Verifikasi jumlah total** — Sistem menghitung jumlah secara otomatis
7. **Pilih metode pembayaran** — PayPal atau Transfer Bank (berdasarkan preferensi afiliasi)
8. **Pilih akun penyedia** — Pilih akun PayPal/Airwallex yang akan digunakan
9. **Tambahkan catatan** (opsional) — Catatan internal untuk catatan
10. **Klik Simpan** — Pembayaran dibuat dengan status "Menunggu"

Pembayaran sekarang siap diproses.

## Memproses Pembayaran

Anda memiliki dua opsi untuk memproses pembayaran: manual atau berbasis penyedia.

### Memproses Manual

Gunakan pemrosesan manual ketika Anda menangani pembayaran di luar sistem (cek, transfer kabel, dll.):

1. Pilih pembayaran dalam daftar
2. Klik tindakan **Tandai sebagai Diproses**
3. Selesaikan pembayaran melalui metode eksternal Anda
4. Kembali ke pembayaran
5. Klik tindakan **Tandai sebagai Selesai**
6. Komisi secara otomatis diperbarui menjadi status "Telah Dibayar"

Pemrosesan manual memberikan fleksibilitas tetapi memerlukan lebih banyak pekerjaan administratif.

### Memproses Berbasis Penyedia (Direkomendasikan)

Pemrosesan penyedia memproses pembayaran secara otomatis melalui PayPal atau Airwallex:

1. **Pilih pembayaran (pembayaran)** dalam daftar (Anda dapat memproses beberapa pembayaran)
2. **Klik** tindakan **Proses dengan Penyedia**
3. **Konfirmasi** dalam dialog
4. **Sistem mengantre tugas** — Pekerja Celery menangani panggilan API
5. **Penyedia memproses pembayaran**:
   - **PayPal**: Mengelompokkan hingga 15.000 pembayaran per permintaan
   - **Airwallex**: Transfer bank individu
6. **Webhook memperbarui status** — Penyedia mengonfirmasi penyelesaian
7. **Komisi ditandai sebagai telah dibayar** — Sistem memperbarui semua komisi yang termasuk

Pemrosesan penyedia lebih cepat, lebih dapat diandalkan, dan menciptakan jejak audit otomatis.

## Metode Pembayaran

Spwig mendukung dua metode pembayaran dengan persyaratan yang berbeda:

| Metode | Penyedia | Persyaratan | Waktu Pemrosesan | Biaya | Terbaik Untuk |
|--------|----------|--------------|-----------------|------|----------|
| **PayPal** | PayPal Payouts | Afiliasi harus memiliki `payment_email` yang valid | 1-2 hari kerja | ~2% atau $0,25-$1,00 | Sebagian besar afiliasi, jangkauan global |
| **Transfer Bank** | Airwallex | Detail rekening bank (nomor rekening, routing, SWIFT) | 2-5 hari kerja | Berbeda tergantung negara | Afiliasi internasional, jumlah besar |

Afiliasi mengatur metode pembayaran dan detailnya di dasbor mereka. Sistem secara otomatis memilih penyedia yang sesuai berdasarkan preferensi mereka.

### Logika Pemilihan Metode Pembayaran

Ketika memproses pembayaran, Spwig memilih penyedia sebagai berikut:

1. Periksa metode pembayaran yang dipilih afiliasi (PayPal atau Transfer Bank)
2. Cocokkan dengan akun penyedia yang dikonfigurasi (PayPal → PayPal, Bank → Airwallex)
3. Jika preferensi tidak tersedia, beralih ke penyedia yang tersedia pertama
4. Tampilkan kesalahan jika tidak ada penyedia yang dikonfigurasi

## Alur Status Pembayaran

Memahami status pembayaran membantu Anda melacak kemajuan pembayaran:

| Status | Arti | Tindakan Berikutnya |
|--------|---------|-------------|
| **Menunggu** | Dibuat tetapi belum dikirim ke penyedia | Proses dengan penyedia atau tandai sebagai diproses |
| **Diproses** | Dikirim ke penyedia pembayaran, menunggu konfirmasi | Tunggu webhook atau periksa dasbor penyedia |
| **Selesai** | Pembayaran berhasil, dana dikirim | Tidak ada — komisi ditandai sebagai telah dibayar |
| **Gagal** | Pembayaran gagal (lihat detail kesalahan) | Periksa kesalahan, perbaiki masalah, coba lagi atau batalkan |
| **Dibatalkan** | Dibatalkan secara manual sebelum penyelesaian | Tidak ada — komisi tetap tidak dibayar |

### Jalur Sukses

Menunggu → Diproses → Selesai

Ini adalah jalur yang ideal. Webhook penyedia secara otomatis memperbarui status saat pembayaran berlangsung.

### Jalur Gagal

Menunggu → Diproses → Gagal

Ketika pembayaran gagal, status pembayaran berubah menjadi Gagal dan Anda harus menyelidiki.

## Menangani Pembayaran yang Gagal

Pembayaran yang gagal memerlukan intervensi manual. Alasan kegagalan umum:

| Penyebab | Kesalahan Penyedia | Solusi |
|-------|----------------|----------|
| Akun tidak valid | "Akun penerima tidak ditemukan" | Verifikasi email pembayaran afiliasi atau detail rekening bank |
| Saldo tidak cukup | "Dana tidak cukup" | Tambahkan dana ke akun penyedia Anda |
| Kesalahan detail rekening bank | "Nomor routing tidak valid" | Minta afiliasi memperbarui informasi rekening bank |
| Batasan akun | "Penerima tidak dapat menerima pembayaran" | Hubungi afiliasi untuk menyelesaikan status akun mereka |
| Masalah penyedia | "Layanan sementara tidak tersedia" | Tunggu dan coba lagi setelah beberapa jam |

### Cara Mencoba Ulang Pembayaran yang Gagal

1. **Lihat pembayaran yang gagal** — Klik pembayaran tersebut dalam daftar
2. **Baca pesan kesalahan** — Periksa bidang **Respons Penyedia** untuk detail
3. **Perbaiki masalah mendasar** — Perbarui detail afiliasi, tambahkan dana penyedia, dll.
4. **Atur ulang status** — Ubah status kembali ke Menunggu (formulir edit)
5. **Proses ulang** — Gunakan tindakan **Proses dengan Penyedia**

### Cara Membatalkan dan Membuat Ulang

Jika mencoba ulang tidak berhasil:

1. **Buka pembayaran yang gagal**
2. **Ubah status menjadi Dibatalkan**
3. **Simpan pembayaran**
4. **Buat pembayaran baru** — Ikuti langkah pembuatan ulang
5. **Proses pembayaran baru**

Pembayaran yang dibatalkan tidak menandai komisi sebagai telah dibayar, sehingga tetap layak untuk pembayaran baru.

## Integrasi Penyedia Pembayaran

Pemrosesan pembayaran memerlukan akun penyedia pembayaran yang dikonfigurasi. Spwig terintegrasi dengan:

- **PayPal Payouts API** — Untuk pembayaran PayPal
- **Airwallex** — Untuk transfer bank internasional

### Persyaratan Pengaturan

Sebelum memproses pembayaran:
1. Konfigurasikan setidaknya satu penyedia di **Pengaturan > Penyedia Pembayaran**
2. Tambahkan kredensial API (ID Klien, Rahasia, Kunci API)
3. Atur ke mode produksi (sandbox untuk pengujian)
4. Konfigurasikan URL webhook di dasbor penyedia
5. Verifikasi koneksi dengan pembayaran uji

Lihat panduan [Pengaturan Penyedia Pembayaran](#) untuk instruksi konfigurasi yang rinci.

### Pemilihan Penyedia oleh Afiliasi

Afiliasi memilih metode pembayaran yang dipilih mereka di dasbor mereka:
- PayPal: Masukkan `payment_email`
- Transfer Bank: Masukkan detail rekening bank

Sistem secara otomatis mengarahkan pembayaran ke penyedia yang sesuai.

## Rekomendasi Jadwal Pembayaran

Buat jadwal pembayaran teratur untuk membangun kepercayaan dengan afiliasi:

| Jadwal | Frekuensi | Beban Kerja | Kepuasan Afiliasi | Direkomendasikan Untuk |
|----------|-----------|----------|------------------------|-----------------|
| Mingguan | Setiap Jumat | Tinggi | Excellent | Program baru, volume tinggi |
| Setiap dua minggu | 1st dan 15th | Medium | Baik | Program volume sedang |
| Bulanan | 1st bulan | Rendah | Diterima | Program yang sudah mapan |
| Setiap tiga bulan | Setiap 3 bulan | Sangat rendah | Buruk | Tidak direkomendasikan |

Pertimbangkan ukuran program Anda dan kapasitas administratif saat memilih jadwal.

## Rekomendasi Pemrosesan

Ikuti panduan berikut untuk operasi pembayaran yang lancar:

- **Kelompokkan pembayaran berdasarkan jadwal** — Proses semua pembayaran yang layak pada hari yang sama setiap minggu/bulan
- **Verifikasi detail sebelum pemrosesan** — Periksa ulang informasi pembayaran afiliasi, terutama untuk jumlah besar
- **Pantau saldo penyedia** — Pastikan dana cukup di akun PayPal/Airwallex Anda
- **Tetapkan ambang minimum yang jelas** — Komunikasikan batas pembayaran dalam ketentuan program ($50-$100 umum)
- **Dokumentasikan jadwal Anda** — Tambahkan jadwal pembayaran ke ketentuan afiliasi dan pengaturan portal
- **Gunakan pemrosesan penyedia** — Hindari pemrosesan manual kecuali sangat diperlukan
- **Periksa pembayaran yang gagal segera** — Alamatkan kegagalan dalam 24 jam
- **Pastikan webhook penyedia dikonfigurasi** — Webhook memungkinkan pembaruan status otomatis
- **Unduh laporan pembayaran secara berkala** — Unduh laporan bulanan untuk akuntansi

## Catatan Pembayaran dan Pelaporan

Setiap pembayaran menciptakan catatan yang tidak dapat diubah dengan:
- Informasi afiliasi
- ID komisi yang termasuk
- Jumlah total
- Metode dan penyedia pembayaran
- Tanda waktu pembuatan dan penyelesaian
- ID transaksi penyedia (setelah diproses)
- Data respons penyedia (untuk debugging)
- Catatan internal

Akses data ini dengan mengklik pembayaran apa pun dalam daftar. Gunakan fitur ekspor antarmuka admin untuk mengunduh laporan pembayaran untuk keperluan akuntansi atau pajak.

## Tips

- Proses pembayaran pada jadwal tetap (misalnya, setiap Jumat pukul 2 siang) agar afiliasi tahu kapan mereka dapat mengharapkan pembayaran.
- Selalu gunakan pemrosesan penyedia daripada pemrosesan manual — lebih cepat, lebih dapat diandalkan, dan menciptakan jejak audit yang lebih baik.
- Tetapkan ambang pembayaran minimum dalam program Anda untuk mengurangi beban administratif — $50 atau $100 adalah standar.
- Pantau saldo akun penyedia sebelum memproses batch besar untuk menghindari kegagalan.
- Uji integrasi pembayaran Anda dalam mode sandbox sebelum meluncurkan pembayaran nyata.
- Tambahkan catatan ke setiap pembayaran yang menjelaskan periode yang dicakup (misalnya, "Komisi untuk Januari 2026").
- Periksa pembayaran yang gagal segera — penundaan menyebabkan kekecewaan afiliasi dan merusak kepercayaan.
- Komunikasikan penundaan secara proaktif — jika Anda tidak dapat memproses sesuai jadwal, beri tahu afiliasi yang terkena sebelumnya.

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis persis seperti yang ditunjukkan dalam aturan preservasi.
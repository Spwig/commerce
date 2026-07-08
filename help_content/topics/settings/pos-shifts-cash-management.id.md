---
title: Pergantian POS dan Manajemen Kas
---

Pergantian POS melacak periode kerja kasir dan memastikan akuntansi kas yang akurat. Setiap shift mewakili waktu seorang kasir di terminal—dari membuka laci kas dengan jumlah kas awal hingga menutup shift dengan jumlah akhir dan rekonsiliasi. Sistem secara otomatis menghitung jumlah kas yang diharapkan berdasarkan penjualan kas aktual dan membandingkannya dengan jumlah fisik, menyoroti ketidaksesuaian untuk diselidiki. Pergerakan kas selama shift (penambahan uang kembalian, penarikan uang kecil) dilacak dengan alasan untuk menciptakan jejak audit yang lengkap.

Navigasi ke **POS > Shifts** untuk melihat semua shift, memantau shift aktif, meninjau laporan rekonsiliasi kas, dan mengaudit aktivitas historis.

![Shift List](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## Memahami Pergantian POS

Sebuah shift adalah periode kerja selama satu kasir mengoperasikan satu terminal. Shift memaksa akuntabilitas kas—setiap kasir bertanggung jawab atas uang di laci mereka selama shift mereka.

**Siklus Hidup Shift**:
1. **Membuka** - Kasir memulai shift, menghitung uang awal, mencatat jumlah
2. **Selama Shift** - Memproses penjualan, menerima pembayaran, memberikan pengembalian
3. **Menutup** - Kasir menghitung uang, mencatat jumlah penutupan, sistem menghitung ketidaksesuaian
4. **Rekonsiliasi** - Shift ditutup dan dikunci untuk tujuan audit

**Metrik Utama yang Ditrack**:
- **Uang Awal** - Jumlah uang di laci saat awal shift
- **Uang Penutupan** - Uang fisik di laci saat akhir shift
- **Uang yang Diharapkan** - Dihitung: Uang awal + penjualan uang tunai - pengembalian uang tunai + pergerakan uang tunai
- **Perbedaan Uang** - Ketidaksesuaian: Uang penutupan - uang yang diharapkan (positif = kelebihan, negatif = kekurangan)
- **Total Penjualan** - Jumlah semua transaksi penjualan selama shift
- **Total Pengembalian** - Jumlah semua transaksi pengembalian selama shift
- **Jumlah Transaksi** - Jumlah pesanan yang diproses

## Tampilan Daftar Shift

Daftar shift menampilkan semua shift dengan informasi kunci:

**Status Shift**:
- **Terbuka** (label hijau) - Shift aktif saat ini
- **Tutup** (label abu-abu) - Shift yang selesai
- **Rekonsiliasi** (label biru) - Shift yang ditutup dan dikunci untuk audit

**Terminal** - Terminal POS mana shift dilakukan

**Kasir** - Staf yang menangani shift

**Uang Awal** - Jumlah uang awal

**Uang Penutupan** - Jumlah uang akhir (kosong jika shift masih terbuka)

**Uang yang Diharapkan** - Jumlah yang diharapkan dihitung oleh sistem berdasarkan transaksi

**Perbedaan Uang** - Ketidaksesuaian (ditekankan dalam merah jika negatif, hijau jika positif, hitam jika nol)

**Durasi** - Panjang shift (waktu mulai ke waktu selesai)

**Total Penjualan** - Pendapatan yang dihasilkan selama shift

Gunakan filter untuk melihat:
- Hanya shift terbuka (memantau terminal aktif)
- Shift dengan ketidaksesuaian (perbedaan uang ≠ 0)
- Shift berdasarkan rentang tanggal (laporan rekonsiliasi harian)
- Shift berdasarkan kasir (audit kinerja)

## Membuka Shift

Kasir membuka shift langsung dari terminal POS (tidak dapat dibuka dari admin). Alur kerja di terminal:

1. **Staf Masuk** - Memasukkan kredensial untuk mengakses terminal

2. **Menghitung Uang Awal** - Secara fisik menghitung semua uang di laci (uang kertas dan koin)

3. **Memasukkan Jumlah Awal** - Mencatat jumlah yang dihitung dalam aplikasi POS

4. **Shift Dimulai** - Terminal siap memproses penjualan

**Panduan Uang Awal**:
- Uang awal standar (uang kembalian) biasanya $100-$300 tergantung ukuran toko
- Hitung dua kali untuk memastikan akurasi—kesalahan saat membuka akan berdampak pada ketidaksesuaian saat menutup
- Jika laci kosong, uang awal adalah $0.00 (uang kembalian ditambahkan melalui pergerakan uang)
- Dokumentasikan uang besar (> $50) secara terpisah untuk melacak pergerakannya

![Shift Add Form](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## Selama Shift

Saat shift terbuka, sistem secara otomatis melacak:

**Penjualan Uang Tunai** - Setiap transaksi di mana pelanggan membayar dengan uang tunai (menambahkan ke uang yang diharapkan)

**Pengembalian Uang Tunai** - Setiap pengembalian dalam bentuk uang tunai (mengurangi dari uang yang diharapkan)

**Penjualan Kartu** - Transaksi kartu kredit/debit (tidak memengaruhi uang tunai)

**Pembayaran Gabungan** - Bagian uang tunai + bagian kartu (hanya bagian uang tunai yang memengaruhi uang yang diharapkan)

**Kartu Hadiah & Voucher** - Metode pembayaran non-uang tunai (tidak memengaruhi uang tunai)

Kasir terus memproses penjualan secara normal. Sistem mempertahankan perhitungan uang yang diharapkan secara otomatis di belakang layar.

## Pergerakan Uang Tunai

Pergerakan uang tunai adalah penyesuaian laci uang selama shift:

**Penambahan Uang Kembalian** - Menambahkan uang ke laci:
- Alasan: "Menambahkan uang kembalian untuk uang besar"
- Jumlah: +$100.00
- Uang yang diharapkan meningkat sebesar $100.00

**Penarikan Uang Kecil** - Menghilangkan uang untuk pengeluaran:
- Alasan: "Pembelian peralatan kantor"
- Jumlah: -$25.00
- Uang yang diharapkan berkurang sebesar $25.00

**Pengiriman ke Bank** - Menghilangkan uang berlebih untuk keamanan:
- Alasan: "Pengiriman ke amanah - lebih dari $500 di laci"
- Jumlah: -$300.00
- Uang yang diharapkan berkurang sebesar $300.00

**Merekam Pergerakan Uang di Terminal**:
1. Sentuh **Menu** > **Pergerakan Uang**
2. Pilih jenis: Tambahkan atau Hapus
3. Masukkan jumlah
4. Masukkan alasan (diperlukan untuk jejak audit)
5. Konfirmasi

Semua pergerakan uang tunai muncul dalam laporan detail shift dengan timestamp, jumlah, dan alasan.

## Menutup Shift

Ketika kasir selesai dengan periode kerjanya, mereka menutup shift:

1. **Sentuh Tutup Shift** - Di menu terminal

2. **Proses Transaksi yang Tersisa** - Selesaikan keranjang yang tertunda atau penjualan yang tertunda

3. **Menghitung Uang Penutupan** - Secara fisik menghitung semua uang di laci
   - Hitung uang kertas berdasarkan denominasi ($100s, $50s, $20s, $10s, $5s, $1s)
   - Hitung koin berdasarkan jenis (quarter, dimes, nickels, pennies)
   - Total = jumlah uang penutupan

4. **Masukkan Jumlah Penutupan** - Catat total yang dihitung

5. **Sistem Menghitung Ketidaksesuaian**:
   - Uang yang diharapkan = Uang awal + penjualan uang tunai - pengembalian uang tunai + pergerakan uang tunai
   - Perbedaan uang = Uang penutupan - uang yang diharapkan
   - Contoh: Uang penutupan $485.00 - Uang yang diharapkan $480.00 = +$5.00 kelebihan

6. **Tinjau Ketidaksesuaian** - Terminal menampilkan perbedaan:
   - **Sempurna ($0.00)** - Rekonsiliasi sempurna
   - **Kelebihan kecil (+$1 hingga +$5)** - Pembulatan yang diterima atau tip pelanggan
   - **Kekurangan kecil (-$1 hingga -$5)** - Kesalahan penghitungan kecil, diterima
   - **Ketidaksesuaian besar (>$5)** - Diperlukan penghitungan ulang

7. **Hitung ulang jika diperlukan** - Jika ketidaksesuaian besar (>$10), kasir harus menghitung ulang uang penutupan sebelum menyelesaikan

8. **Tutup Shift** - Konfirmasi jumlah penutupan, status shift berubah menjadi "Tutup"

9. **Cetak Laporan Shift** - Terminal mencetak bukti rekonsiliasi kas untuk catatan kasir

![Shift Detail](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Rumus Rekonsiliasi Kas

Sistem menghitung uang yang diharapkan menggunakan rumus ini:

```
Uang yang Diharapkan = Uang Awal
                + Penjualan Uang Tunai
                - Pengembalian Uang Tunai
                + Penambahan Uang (pergerakan)
                - Pengurangan Uang (pergerakan)
```

**Contoh**:
- Uang Awal: $200.00
- Penjualan Uang Tunai: $450.00 (dari 15 transaksi)
- Pengembalian Uang Tunai: -$30.00 (1 pengembalian)
- Penambahan Uang: +$100.00 (uang kembalian ditambahkan di tengah shift)
- Pengurangan Uang: -$50.00 (penarikan uang kecil)
- **Uang yang Diharapkan: $200 + $450 - $30 + $100 - $50 = $670.00**

Jika kasir menghitung $675.00 saat penutupan:
- Perbedaan Uang: $675.00 - $670.00 = **+$5.00 kelebihan**

## Pelaporan dan Audit Shift

Laporan shift menyediakan informasi rekonsiliasi yang rinci:

**Bagian Ringkasan**:
- Uang awal dan penutupan
- Perhitungan uang yang diharapkan
- Perbedaan uang (kelebihan/kekurangan)
- Total penjualan dan pengembalian
- Jumlah transaksi
- Durasi shift

**Detail Transaksi**:
- Semua penjualan selama shift (ID pesanan, jumlah, metode pembayaran)
- Semua pengembalian yang diberikan
- Timestamp setiap transaksi

**Log Pergerakan Uang**:
- Semua penambahan dan pengurangan
- Alasan yang diberikan
- Timestamp

**Kasus Penggunaan**:
- **Rekonsiliasi harian** - Tinjau semua shift di akhir hari bisnis
- **Kinerja kasir** - Identifikasi pola ketidaksesuaian berdasarkan staf
- **Deteksi pencurian** - Kekurangan besar dan konsisten mungkin menunjukkan pencurian
- **Kebutuhan pelatihan** - Ketidaksesuaian kecil yang sering menunjukkan masalah akurasi penghitungan
- **Jejak audit** - Catatan lengkap untuk keperluan akuntansi dan pajak

## Manajemen Kas untuk Multi-Terminal

Untuk toko dengan beberapa terminal yang menjalankan shift bersamaan:

**Laci Terpisah**: Setiap terminal memiliki laci kas sendiri—shift bersifat independen. Kasir A di Terminal 1 dan Kasir B di Terminal 2 menjalankan shift terpisah dengan rekonsiliasi terpisah.

**Laci Bersama**: Beberapa toko berbagi satu laci kas di beberapa terminal (tidak disarankan). Jika melakukannya:
- Hanya satu shift yang dapat terbuka per laci kas bersama
- Kasir harus menutup shift saat menyerahkan ke kasir berikutnya
- Pergerakan kas melacak semua penambahan/pengurangan selama penyerahan
- Ketidaksesuaian lebih sulit dihubungkan dengan kasir tertentu

**Praktik Terbaik**: Satu laci kas per terminal, satu shift per kasir per sesi. Ini memastikan akuntabilitas yang jelas dan rekonsiliasi yang disederhanakan.

## Menangani Ketidaksesuaian

Ketika uang penutupan tidak cocok dengan uang yang diharapkan:

**Ketidaksesuaian Kecil (<$5)**:
- Diterima karena pembulatan, kesalahan penghitungan, atau tip pelanggan
- Dokumentasikan dalam catatan shift
- Tidak diperlukan tindakan lebih lanjut kecuali pola muncul

**Ketidaksesuaian Sedang ($5-$20)**:
- Hitung ulang uang sebelum menutup shift
- Tinjau log transaksi untuk kesalahan (uang kembalian yang salah diberikan, transaksi yang dibatalkan tidak diproses)
- Dokumentasikan situasi dalam catatan shift
- Disarankan tinjauan manajer

**Ketidaksesuaian Besar (>$20)**:
- Penghitungan ulang wajib
- Persetujuan manajer diperlukan untuk menutup shift
- Tinjau semua transaksi dan pergerakan uang
- Selidiki penyebab potensial (pencurian, pencetakan laci, uang awal yang salah)
- Mungkin memerlukan tindakan disipliner tergantung pada situasi

**Kekurangan Konsisten**:
- Pola ketidaksesuaian negatif dari kasir yang sama = masalah pelatihan atau pencurian
- Terapkan pengawasan tambahan (manajer memeriksa secara acak selama shift)
- Tinjau prosedur pelatihan POS
- Pertimbangkan pembaruan kebijakan pengelolaan uang tunai

## Tips

- **Hitung uang awal dua kali** - Kesalahan saat membuka akan berdampak pada ketidaksesuaian saat menutup; akurasi di awal mencegah masalah di akhir
- **Catat pergerakan uang segera** - Jangan menunggu hingga menutup untuk mendokumentasikan penambahan uang kembalian atau penarikan uang kecil
- **Selalu berikan alasan pergerakan** - "Menambahkan $100" tidak berguna untuk audit; "Menambahkan $100 untuk uang kembalian (kurang uang $5)" adalah tindakan yang dapat diambil
- **Hitung ulang jika ketidaksesuaian >$10** - Jangan menutup shift dengan ketidaksesuaian besar tanpa menghitung ulang
- **Cetak laporan shift harian** - Lampirkan ke dokumen rekonsiliasi harian untuk akuntansi
- **Tinjau pola, bukan ketidaksesuaian individu** - Satu kekurangan -$3.00 adalah baik; lima kekurangan -$3.00 berturut-turut adalah masalah
- **Tutup shift di akhir hari** - Jangan biarkan shift terbuka semalaman; ketidaksesuaian lebih mudah diselidiki ketika baru
- **Latih kasir dalam penghitungan denominasi** - Sebagian besar kesalahan berasal dari penghitungan uang kertas yang salah (mengira uang $5 adalah $10)
- **Gunakan kemasan koin** - Koin yang dikemas sebelumnya mengurangi kesalahan penghitungan dan mempercepat rekonsiliasi


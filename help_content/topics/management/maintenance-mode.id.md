---
title: Mode Pemeliharaan
---

Mode pemeliharaan sementara menonaktifkan toko Anda dan menampilkan pesan "kami akan segera kembali" kepada pelanggan. Backend admin Anda tetap dapat diakses selama pemeliharaan — Anda dapat terus bekerja sementara pelanggan diarahkan ke halaman pemeliharaan.

Gunakan mode pemeliharaan sebelum membuat perubahan yang dapat menyebabkan keadaan tidak konsisten sementara, seperti menjalankan impor produk besar, menerapkan desain ulang tema besar, atau menunggu operasi pemulihan selesai.

![Pengaturan mode pemeliharaan di dashboard sistem](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Mengaktifkan mode pemeliharaan

1. Navigasikan ke **Manajemen > Metrik Sistem**
2. Klik **Dashboard Sistem** dari bilah alat
3. Di panel **Status Toko**, klik **Aktifkan Mode Pemeliharaan**
4. Secara opsional masukkan **Alasan** — ini untuk referensi Anda sendiri dan tidak ditampilkan kepada pelanggan (misalnya, `Pembaruan katalog produk sedang berlangsung`)
5. Konfirmasi dengan mengklik **Aktifkan**

Toko Anda segera mulai menampilkan halaman pemeliharaan kepada semua pengunjung. Backend admin tidak terpengaruh dan Anda dapat terus bekerja secara normal.

## Apa yang pelanggan lihat

Ketika mode pemeliharaan aktif, setiap halaman toko Anda (toko, halaman produk, checkout, dan halaman akun) menampilkan pesan pemeliharaan yang didaur ulang. Pesan tersebut memberi tahu pelanggan bahwa toko sementara tidak tersedia dan mendorong mereka untuk kembali sebentar lagi.

Pelanggan yang sedang dalam sesi atau checkout saat mode pemeliharaan diaktifkan juga akan melihat halaman pemeliharaan pada permintaan berikutnya mereka. Tidak ada pesanan yang sedang berlangsung yang hilang — data tetap ada ketika Anda menonaktifkan mode pemeliharaan.

## Menonaktifkan mode pemeliharaan

1. Navigasikan ke **Manajemen > Metrik Sistem**
2. Klik **Dashboard Sistem**
3. Di panel **Status Toko**, Anda akan melihat banner yang mengonfirmasi bahwa mode pemeliharaan aktif
4. Klik **Nonaktifkan Mode Pemeliharaan**
5. Konfirmasi ketika diminta

Toko kembali online secara langsung. Pelanggan dapat menjelajahi dan membeli seperti biasa.

## Ketika Spwig mengaktifkan mode pemeliharaan secara otomatis

Beberapa operasi sistem mengaktifkan mode pemeliharaan secara otomatis dan mengaktifkan kembali toko ketika selesai:

- **Pembaruan platform** — proses pembaruan mengaktifkan mode pemeliharaan sebelum menerapkan perubahan dan menonaktifkannya ketika pembaruan selesai
- **Operasi pemulihan** — memulihkan dari cadangan menempatkan toko dalam mode pemeliharaan selama operasi pemulihan

Jika operasi otomatis berakhir secara tidak terduga, mode pemeliharaan mungkin tetap aktif. Dalam kasus tersebut, ikuti langkah-langkah di atas untuk menonaktifkannya secara manual.

## Tips

- Selalu beri tahu tim Anda sebelum mengaktifkan mode pemeliharaan — ini memengaruhi setiap pengunjung toko Anda
- Pertahankan jendela pemeliharaan sependek mungkin; bahkan beberapa menit offline dapat memengaruhi kepercayaan pelanggan
- Gunakan bidang alasan sebagai pengingat bagi diri Anda sendiri mengapa mode pemeliharaan diaktifkan — ini muncul dalam log sistem
- Jika Anda menyadari mode pemeliharaan aktif tetapi tidak mengaktifkannya sendiri, periksa log sistem untuk operasi otomatis yang mungkin memicunya
- Rencanakan jendela pemeliharaan selama periode lalu lintas rendah (malam hari atau pagi awal) untuk meminimalkan dampak pada penjualan


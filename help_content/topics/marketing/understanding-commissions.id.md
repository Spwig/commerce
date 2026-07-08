---
title: Memahami Komisi
---

Komisi adalah catatan pendapatan yang dibuat ketika afiliasi berhasil mendorong penjualan ke toko Anda. Setiap komisi terkait dengan pesanan, afiliasi, dan program tertentu, dan melewati siklus hidup dari menunggu hingga dibayar. Panduan ini menjelaskan bagaimana komisi bekerja, bagaimana mereka dihitung, dan bagaimana mengelolanya secara efektif.

## Apa Itu Komisi?

Komisi merepresentasikan jumlah yang terutang kepada afiliasi untuk mereferensikan pelanggan yang menyelesaikan pembelian. Ketika pelanggan mengklik tautan referensi afiliasi dan melakukan pemesanan dalam jendela waktu cookie, Spwig secara otomatis membuat catatan komisi.

Setiap komisi berisi:
- **Afiliasi** — Mitra yang mereferensikan pelanggan
- **Program** — Program afiliasi yang mendefinisikan aturan komisi
- **Pesanan** — Pesanan yang menghasilkan komisi
- **Jumlah** — Nilai komisi yang dihitung
- **Status** — Tahap saat ini dalam siklus hidup komisi
- **Tanggal** — Tanggal dibuat, tanggal disetujui/ditolak, dan tanggal dibayar

## Perhitungan Komisi

Komisi dihitung secara otomatis berdasarkan jenis komisi dan tingkat program.

| Jenis Komisi | Perhitungan | Contoh |
|-----------------|-------------|---------|
| **Persentase** | Total Pesanan × Persentase Komisi ÷ 100 | Pesanan: $200, Tingkat: 10% → **Komisi $20** |
| **Tetap** | Jumlah tetap per pesanan | Tingkat: $15 → **Komisi $15** (tidak peduli nilai pesanan) |

### Contoh Perhitungan

**Komisi Persentase (10%)**:
- Pelanggan melakukan pesanan $50 → $5 komisi
- Pelanggan melakukan pesanan $150 → $15 komisi
- Pelanggan melakukan pesanan $300 → $30 komisi

**Komisi Tetap ($20)**:
- Pelanggan melakukan pesanan $50 → $20 komisi
- Pelanggan melakukan pesanan $150 → $20 komisi
- Pelanggan melakukan pesanan $300 → $20 komisi

Komisi dihitung berdasarkan **subtotal pesanan** (sebelum biaya pengiriman dan pajak) dan dibuat secara langsung ketika pesanan ditempatkan.

## Siklus Hidup Komisi

Setiap komisi melewati serangkaian status dari pembuatan hingga pembayaran:

```
Menunggu → Disetujui → Dibayar
   ↓
Ditolak
```

### Definisi Status

| Status | Deskripsi | Terjadi Apa |
|--------|-------------|--------------|
| **Menunggu** | Pesanan ditempatkan, komisi menunggu tinjauan | Komisi dibuat tetapi belum dikonfirmasi. Afiliasi dapat melihatnya tetapi tidak dapat menarik dana. |
| **Disetujui** | Penjual mengonfirmasi penjualan valid | Komisi diverifikasi dan ditambahkan ke saldo tersedia afiliasi. Layak untuk pembayaran. |
| **Ditolak** | Penjual menolak komisi | Komisi ditolak (misalnya, pesanan dikembalikan, penipuan, atau melanggar ketentuan). Tidak layak untuk pembayaran. |
| **Dibayar** | Komisi termasuk dalam pembayaran yang selesai | Afiliasi telah dibayar. Komisi selesai dan tidak dapat diubah. |

![Daftar Komisi](/static/core/admin/img/help/commission-management/commission-list.webp)

## Kapan Komisi Dibuat

Komisi dibuat secara otomatis sesuai urutan berikut:

1. **Pelanggan mengklik tautan afiliasi** — URL referensi berisi kode pelacakan unik afiliasi (misalnya, `?ref=JOHNSMITH`)
2. **Cookie disetel** — Cookie pelacakan disimpan di browser pelanggan dengan kode afiliasi
3. **Pembelian dalam jangka waktu cookie** — Pelanggan menyelesaikan pesanan sebelum cookie kedaluwarsa (default: 30 hari)
4. **Sistem mengatribusikan pesanan** — Spwig memeriksa cookie pelacakan aktif dan mengidentifikasi afiliasi yang merujuk
5. **Komisi dibuat secara otomatis** — Catatan komisi dibuat dengan status **Menunggu**

Komisi dibuat **segera** ketika pesanan ditempatkan, bahkan sebelum pembayaran dikonfirmasi. Hal ini memungkinkan penjual untuk meninjau komisi saat pesanan sedang diproses.

## Pelacakan & Atribusi

Spwig menggunakan **model atribusi klik terakhir** untuk menentukan afiliasi mana yang harus menerima kredit untuk penjualan.

### Cara Atribusi Bekerja

- **Model klik terakhir** — Tautan afiliasi terbaru yang diklik mendapatkan kredit (bahkan jika beberapa afiliasi mereferensikan pelanggan)
- **Pelacakan berbasis cookie** — Cookie menyimpan kode afiliasi di browser pelanggan
- **Jangka waktu cookie** — Menentukan jendela selama mana penjualan dapat diatribusikan (dikonfigurasi per program, biasanya 30 hari)
- **Pelacakan IP dan sesi** — Data tambahan membantu mengidentifikasi pola penipuan

### Contoh Atribusi

- Hari 1: Pelanggan mengklik tautan Afiliasi A → Cookie diatur untuk Afiliasi A
- Hari 5: Pelanggan mengklik tautan Afiliasi B → Cookie **diperbarui** ke Afiliasi B (klik terakhir menang)
- Hari 7: Pelanggan menempatkan pesanan → Komisi pergi ke **Afiliasi B**

Jika pelanggan kembali pada Hari 35 (setelah cookie 30 hari berakhir) dan menempatkan pesanan, **tidak ada komisi** yang dibuat karena jendela pelacakan telah ditutup.

## Detail Komisi

Navigasi ke **Pemasaran > Komisi** untuk melihat semua catatan komisi.

### Bidang Komisi

Setiap komisi menampilkan:

| Bidang | Deskripsi |
|-------|-------------|
| **Afiliasi** | Nama dan kode afiliasi |
| **Program** | Nama program afiliasi |
| **Pesanan** | Nomor pesanan (tautan klik untuk melihat detail pesanan lengkap) |
| **Jumlah** | Nilai komisi yang dihitung |
| **Status** | Tahap saat ini (Menunggu, Disetujui, Ditolak, Dibayar) |
| **Dibuat** | Kapan komisi dibuat |
| **Tanggal Disetujui/Ditolak** | Kapan status diperbarui |
| **Tanggal Dibayar** | Kapan pembayaran diproses |
| **Catatan** | Catatan internal tentang komisi |

### Melihat Detail Pesanan

Klik **nomor pesanan** dalam catatan komisi untuk melihat pesanan asli. Ini memungkinkan Anda memverifikasi:
- Total pesanan dan barang yang dibeli
- Informasi pelanggan
- Status pembayaran
- Status pengiriman
- Setiap pengembalian atau pengembalian dana

Konteks ini membantu Anda memutuskan apakah menyetujui atau menolak komisi.

## Mengelola Komisi

Meskipun panduan ini berfokus pada memahami komisi, langkah-langkah praktis untuk menyetujui, menolak, dan membayar komisi dibahas secara rinci dalam topik bantuan **Pengelolaan Komisi**.

### Ringkasan Cepat

- **Menyetujui** — Verifikasi pesanan sah dan konfirmasi komisi valid
- **Menolak** — Menolak komisi untuk pesanan penipuan, pengembalian dana, atau pelanggaran kebijakan
- **Menambahkan catatan** — Dokumentasikan alasan persetujuan atau penolakan untuk referensi masa depan
- **Memproses pembayaran** — Kelompokkan komisi yang disetujui menjadi pembayaran batch

Lihat topik bantuan terkait untuk instruksi langkah demi langkah untuk setiap tugas pengelolaan.

## Tips

- Tinjau komisi yang menunggu **setiap hari** selama bulan pertama untuk menetapkan ritme dan menangkap masalah pelacakan sejak dini
- Atur **notifikasi email** untuk memberi tahu Anda ketika komisi baru dibuat sehingga Anda dapat meninjau saat detail pesanan masih segar
- Setujui komisi **setelah penyelesaian pesanan** (bukan segera setelah pesanan ditempatkan) untuk mempertimbangkan pembatalan dan pengembalian dana
- Gunakan **bidang catatan** untuk mendokumentasikan keputusan, terutama untuk komisi yang ditolak, sehingga Anda memiliki catatan jika afiliasi bertanya
- Cari **pola penolakan** — jika satu afiliasi memiliki banyak komisi yang ditolak, mungkin menunjukkan penipuan atau kesalahpahaman tentang ketentuan program
- Pertimbangkan membuat **kebijakan persetujuan komisi** (misalnya, "disetujui setelah jendela pengembalian 14 hari") dan komunikasikan ke afiliasi untuk menetapkan harapan yang jelas

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis secara tepat seperti yang ditunjukkan dalam aturan preservasi.
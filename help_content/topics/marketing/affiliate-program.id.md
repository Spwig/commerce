---
title: Program Afiliasi
---

Program afiliasi memungkinkan Anda merekrut mitra yang mempromosikan produk Anda dan memperoleh komisi dari penjualan yang mereka hasilkan. Afiliasi berbagi tautan rujukan unik, dan Spwig secara otomatis melacak klik, menghubungkan pesanan, dan menghitung komisi.

![Program afiliasi](/static/core/admin/img/help/affiliate-program/program-list.webp)

## Cara Kerjanya

1. Anda membuat satu atau lebih **program afiliasi** dengan tingkat komisi dan aturan
2. Afiliasi **mendaftar** melalui portal umum atau ditambahkan secara manual
3. Setiap afiliasi mendapatkan **tautan rujukan unik** dengan kode pelacakan
4. Ketika seorang pelanggan mengklik tautan dan membuat pembelian, **komisi** dicatat
5. Anda meninjau dan menyetujui komisi, lalu memproses **pembayaran**

## Membuat Program

Navigasikan ke **Pemasaran > Program Afiliasi** dan klik **Tambah Program**.

### Pengaturan Program

| Pengaturan | Deskripsi |
|---------|-------------|
| **Nama** | Nama program yang terlihat oleh afiliasi (misalnya, "Program Mitra") |
| **Jenis Komisi** | **Persentase** dari total pesanan atau **Tetap** jumlah per penjualan |
| **Tingkat Komisi** | Persentase atau jumlah tetap yang diperoleh afiliasi |
| **Umur Cookie** | Berapa hari cookie pelacakan rujukan bertahan (default: 30 hari) |
| **Minimum Pembayaran** | Jumlah minimum pendapatan sebelum afiliasi dapat meminta pembayaran |
| **Otomatis Menyetujui Afiliasi** | Terima otomatis aplikasi afiliasi baru, atau memerlukan persetujuan manual |
| **Status** | Aktif, dijeda, atau ditutup |

### Jenis Komisi

- **Persentase** — Afiliasi memperoleh persentase dari subtotal setiap pesanan yang dirujuk (misalnya, 10% dari pesanan $100 = komisi $10)
- **Tetap** — Afiliasi memperoleh jumlah tetap per penjualan tanpa memandang nilai pesanan (misalnya, $5 per penjualan)

## Mengelola Afiliasi

Navigasikan ke **Pemasaran > Afiliasi** untuk melihat dan mengelola akun afiliasi.

### Detail Afiliasi

Setiap afiliasi memiliki:
- **Kode Afiliasi** — Kode unik yang digunakan dalam tautan rujukan (dibuat secara otomatis atau kustom)
- **Tautan Rujukan** — Tautan pelacakan lengkap yang dibagikan oleh afiliasi (misalnya, `yourstore.com/?ref=CODE`)
- **Status** — Menunggu, disetujui, atau ditolak
- **Metode Pembayaran** — Cara afiliasi menerima pembayaran (PayPal atau transfer bank)
- **Anggota Program** — Program mana yang dimiliki oleh afiliasi

### Menambahkan Afiliasi Secara Manual

1. Klik **Tambah Afiliasi**
2. Pilih akun pelanggan yang sudah ada atau buat yang baru
3. Tetapkan afiliasi ke satu atau beberapa program
4. Tetapkan kode afiliasi (atau biarkan kosong untuk dibuat secara otomatis)

### Portal Afiliasi

Afiliasi mengakses portal yang menghadap ke publik di mana mereka dapat:
- Melihat dashboard mereka dengan pendapatan dan statistik klik
- Salin tautan rujukan mereka
- Lacak sejarah komisi
- Meminta pembayaran

URL portal tersedia secara otomatis di `/affiliate/` pada toko Anda.

## Pelacakan dan Komisi

### Cara Kerja Pelacakan

1. Seorang pelanggan mengklik tautan rujukan afiliasi
2. Cookie pelacakan diatur di browser pelanggan (bertahan selama umur cookie yang dikonfigurasi)
3. Jika pelanggan membuat pesanan dalam masa berlaku cookie, pesanan tersebut dihubungkan ke afiliasi
4. Catatan komisi dibuat dengan status **Menunggu**

### Status Komisi

| Status | Deskripsi |
|--------|-------------|
| **Menunggu** | Komisi dicatat, menunggu tinjauan |
| **Disetujui** | Diverifikasi dan siap untuk pembayaran |
| **Ditolak** | Komisi ditolak (misalnya, pesanan curang atau barang dikembalikan) |
| **Dibayar** | Komisi termasuk dalam pembayaran yang selesai |

### Meninjau Komisi

Navigasikan ke **Pemasaran > Komisi** untuk meninjau komisi yang menunggu:

1. Periksa detail pesanan untuk memverifikasi penjualan tersebut sah
2. Klik **Setujui** untuk mengonfirmasi, atau **Tolak** dengan alasan
3. Komisi yang disetujui menumpuk menuju saldo pembayaran afiliasi

## Pembayaran

Ketika saldo komisi yang disetujui afiliasi mencapai ambang batas pembayaran minimum, Anda dapat memproses pembayaran.

### Memproses Pembayaran

1. Navigasikan ke **Pemasaran > Pembayaran**
2. Pilih afiliasi dengan saldo yang tersedia
3. Pilih metode pembayaran:
   - **PayPal** — Kirim dana langsung ke email PayPal afiliasi
   - **Transfer Bank** — Catat transfer bank manual
4. Konfirmasi dan proses pembayaran
5. Status pembayaran diperbarui menjadi **Selesai** dan komisi ditandai sebagai **Dibayar**

### Pemberi Pembayaran

Spwig terintegrasi dengan penyedia pembayaran untuk pembayaran otomatis:
- **PayPal** — Pembayaran massal otomatis melalui API PayPal
- **Airwallex** — Pembayaran internasional dengan kurs pertukaran kompetitif
- **Manual** — Catat pembayaran yang diproses di luar Spwig

## Tautan Rujukan

Setiap tautan rujukan afiliasi mengikuti pola ini:

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Afiliasi juga dapat membuat tautan ke produk atau kategori tertentu:

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

Parameter `ref` bekerja pada halaman mana pun — cookie pelacakan diatur tanpa memandang halaman tujuan.

## Analitik Program

Dashboard program afiliasi menampilkan:
- **Total Klik** — Berapa kali tautan rujukan diklik
- **Total Pesanan** — Pesanan yang dihubungkan ke afiliasi
- **Total Komisi** — Jumlah semua komisi (menunggu, disetujui, dan dibayar)
- **Afiliasi Aktif** — Jumlah afiliasi yang disetujui saat ini yang menghasilkan rujukan

## Tips

- Mulailah dengan **komisi berbasis persentase** (5–15%) — ini berkembang secara alami dengan nilai pesanan dan mudah dipahami oleh afiliasi.
- Tetapkan **umur cookie 30 hari** sebagai dasar — ini memberi pelanggan waktu untuk kembali dan menyelesaikan pembelian mereka sementara penjualan masih dihubungkan ke afiliasi.
- Aktifkan **otomatis menyetujui** untuk program umum untuk mengurangi hambatan, atau gunakan persetujuan manual untuk program undangan pribadi di mana Anda ingin memverifikasi setiap afiliasi.
- Tetapkan **minimum pembayaran** yang masuk akal (misalnya, $25–$50) untuk menghindari memproses banyak transaksi kecil.
- Kustomisasi **portal afiliasi** agar sesuai dengan merek Anda — afiliasi lebih mungkin mempromosikan toko Anda ketika pengalaman terasa profesional.
- Pantau komisi secara teratur untuk **pola penipuan** seperti rujukan diri sendiri, tingkat pengembalian yang tidak biasa, atau volume klik yang mencurigakan.
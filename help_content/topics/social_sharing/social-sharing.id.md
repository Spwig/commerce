---
title: Berbagi Sosial
---

Tombol berbagi sosial memungkinkan pelanggan berbagi produk, posting blog, dan halaman Anda ke jaringan sosial langsung dari toko online Anda. Anda mengontrol platform mana yang muncul, bagaimana tombol tersebut terlihat, di mana mereka ditempatkan, dan apakah aktivitas berbagi dilacak dan dihitung.

## Mengonfigurasi pengaturan berbagi sosial

Semua perilaku berbagi sosial dikontrol dari satu halaman pengaturan. Navigasikan ke **Pemasaran > Pengaturan Berbagi Sosial** (halaman ini secara otomatis dialihkan ke formulir pengaturan — hanya ada satu catatan pengaturan).

### Penempatan: di mana tombol muncul

Bagian **Penempatan** mengontrol jenis konten mana yang menampilkan tombol berbagi secara otomatis.

| Pengaturan | Deskripsi |
|---------|-------------|
| **Aktifkan pada Produk** | Tampilkan tombol berbagi pada halaman detail produk |
| **Aktifkan pada Kategori** | Tampilkan tombol berbagi pada halaman daftar kategori |
| **Aktifkan pada Posting Blog** | Tampilkan tombol berbagi pada halaman posting blog |
| **Aktifkan pada Halaman Kustom** | Tampilkan tombol berbagi pada halaman toko kustom |

Centang jenis konten di mana Anda ingin tombol muncul. Anda dapat mengaktifkan kombinasi apa pun — misalnya, hanya produk dan posting blog.

**Posisi Penempatan** mengontrol di mana tombol ditampilkan pada halaman:

| Opsi | Deskripsi |
|--------|-------------|
| **Di Bawah Konten** (default) | Ditampilkan setelah konten utama |
| **Di Atas Konten** | Ditampilkan sebelum konten utama |
| **Sidebar** | Ditampilkan di sidebar halaman |
| **Melayang (sticky)** | Menempel di sisi viewport saat pengunjung menggulir |

### Tampilan: bagaimana tombol terlihat

Bagian **Tampilan** mengontrol platform mana yang ditampilkan dan bagaimana tombol tersebut bergaya.

**Platform yang Diaktifkan** — biarkan kosong untuk menampilkan semua platform yang didukung, atau masukkan array JSON untuk membatasi platform yang muncul:

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Platform yang didukung: `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Gaya Tombol** opsi:

| Gaya | Deskripsi |
|-------|-------------|
| **Ikon Saja** (default) | Menampilkan hanya ikon platform |
| **Ikon + Label** | Menampilkan ikon dan nama platform |
| **Label Saja** | Menampilkan hanya nama platform sebagai teks |

**Ukuran Tombol** — pilih **Kecil**, **Sedang** (default), atau **Besar** untuk cocok dengan desain toko online Anda.

**Arah Tata Letak** — susun tombol **Mendatar** (default, berdampingan) atau **Vertikal** (berjejer).

**Tampilkan Judul** — ketika dicentang, judul "Berbagi" muncul di atas grup tombol.

**Keterlihatan di Perangkat Mobile** mengontrol tampilan tombol di layar kecil:

| Opsi | Deskripsi |
|--------|-------------|
| **Selalu Tampilkan** (default) | Tombol terlihat di semua perangkat |
| **Sembunyikan di Perangkat Mobile** | Tombol disembunyikan di perangkat mobile |
| **Hanya di Perangkat Mobile** | Tombol hanya ditampilkan di perangkat mobile |

### Pengaturan pelacakan

**Tampilkan Jumlah Berbagi** — ketika dicentang, badge jumlah muncul di setiap tombol menunjukkan berapa kali platform tersebut telah dibagikan. Jumlah diperbarui secara real time saat berbagi dicatat.

**Lacak Berbagi** — ketika dicentang, setiap klik berbagi dicatat dalam analitik berbagi. Menonaktifkan ini menghentikan catatan baru dari disimpan tetapi tidak menghapus data yang sudah ada. Pelacakan juga memberikan badge loyalitas kepada pelanggan yang berbagi (jika program loyalitas aktif).

Klik **Simpan** di bagian bawah formulir untuk menerapkan perubahan Anda. Pengaturan berlaku segera.

## Melihat aktivitas berbagi

### Acara berbagi individu

Navigasikan ke **Pemasaran > Berbagi Sosial** untuk melihat log setiap acara berbagi yang dicatat. Setiap entri menampilkan:

- **Platform** — jaringan sosial yang digunakan (ditampilkan sebagai badge berwarna)
- **Konten yang Dibagikan** — jenis dan nama konten yang dibagikan (misalnya, `produk: Blue Widget`)
- **Pengguna** — pelanggan yang berbagi, atau "Anonim" untuk pengunjung yang tidak masuk
- **Jenis Perangkat** — desktop, mobile, atau tablet
- **Dibagikan Pada** — tanggal dan waktu berbagi

Log berbagi hanya untuk dibaca — entri dibuat secara otomatis saat pelanggan mengklik tombol berbagi.

Gunakan filter **Platform** dan **Jenis Perangkat** untuk mengeksplorasi pola berbagi, dan hierarki tanggal untuk melihat periode waktu tertentu.

### Jumlah berbagi berdasarkan konten

Beralih ke **Pemasaran > Jumlah Berbagi** untuk melihat total berbagi yang telah diagregasi, dikelompokkan berdasarkan item konten dan platform. Tampilan ini memudahkan Anda mengidentifikasi produk dan postingan yang paling sering dibagikan.

Setiap entri menampilkan:
- **Konten** — jenis dan nama item (misalnya, `produk: Blue Widget`)
- **Platform** — jaringan sosial
- **Jumlah Berbagi** — total berbagi yang tercatat di platform tersebut
- **Terakhir Diperbarui** — kapan jumlah tersebut terakhir dihitung ulang

Daftar ini diurutkan berdasarkan jumlah berbagi secara menurun, sehingga konten yang paling viral akan muncul di bagian atas. Jumlah berbagi diperbarui secara otomatis setiap kali acara berbagi baru tercatat — tidak perlu memperbarui secara manual.

## Memahami cara pelacakan berbagi

Ketika pelanggan mengklik tombol berbagi, Spwig mencatat:

1. Platform mana yang digunakan untuk berbagi
2. Konten apa yang dibagikan (produk, posting blog, halaman, dll.)
3. Apakah mereka masuk (jika ya, berbagi tersebut terkait dengan akun mereka untuk integrasi loyalitas)
4. Jenis perangkat mereka
5. URL yang dibagikan

Jumlah berbagi untuk platform dan item konten tersebut kemudian ditingkatkan secara otomatis. Jika **Tampilkan Jumlah Berbagi** diaktifkan, jumlah yang diperbarui akan muncul di tombol berikutnya saat halaman dimuat ulang.

## Integrasi loyalitas

Jika program loyalitas Anda aktif dan **Lacak Berbagi** diaktifkan, pelanggan yang masuk akan mendapatkan badge loyalitas saat mereka berbagi konten. Badge berbagi sosial adalah bagian dari aturan program loyalitas berbasis aksi.

Untuk mengatur poin hadiah berdasarkan berbagi, beralih ke **Pelanggan > Aturan Loyalitas** dan cari aturan dengan tipe **Berbasis Aksi** dan tipe aksi **Berbagi Sosial**.

## Tips

- Aktifkan berbagi pada produk dan posting blog terlebih dahulu — ini adalah jenis konten yang paling mungkin dibagikan secara organik oleh pelanggan
- Pinterest sangat bernilai untuk kategori produk visual seperti fashion, dekorasi rumah, dan makanan — prioritaskan platform ini dalam daftar `enabled_platforms` untuk toko-toko tersebut
- Berbagi melalui WhatsApp mendorong konversi yang kuat dari rujukan hangat, terutama di perangkat mobile; pertimbangkan untuk menggunakan mode tampilan **Hanya Mobile** untuk WhatsApp sementara mempertahankan platform lainnya terlihat di semua perangkat
- Jika Anda melihat jumlah berbagi terlalu tinggi, periksa apakah lalu lintas uji (dari sesi admin) dihitung sebelum bendera **Apakah Lalu Lintas Admin** berfungsi sepenuhnya — Anda dapat mereset jumlah dengan menghapus entri dari analitik berbagi
- Tinjau daftar Jumlah Berbagi setiap bulan untuk mengidentifikasi produk yang paling sering dibagikan dan tampilkan lebih menonjol di halaman utama atau dalam email pemasaran Anda
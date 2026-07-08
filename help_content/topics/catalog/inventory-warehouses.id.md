---
title: Persediaan & Gudang
---

Sistem gudang memungkinkan Anda mengelola persediaan di beberapa lokasi, menetapkan prioritas pemenuhan pesanan, dan melacak tingkat stok secara real time. Navigasikan ke **Pengaturan > Manajemen Lisensi** di bilah samping, atau akses gudang dari tab inventaris produk.

![Daftar gudang](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Gudang

### Daftar Gudang

Halaman gudang menampilkan semua lokasi inventaris Anda sebagai kartu dengan:

- **Nama dan kode** — Identifikasi gudang (misalnya, "Main Warehouse", kode "MAIN-WH")
- **Wilayah penjualan** — Penugasan wilayah geografis
- **Lencana status** — Aktif/tidak aktif, lokasi ritel
- **Statistik** — Produk yang disimpan, prioritas pemenuhan, persentase buffer persediaan
- **Lokasi** — Kota dan negara
- **Terakhir diperbarui** — Kapan tingkat stok terakhir kali dimodifikasi

### Membuat Gudang

1. Klik **+ Tambah Gudang**
2. Isi detail gudang:
   - **Nama** — Label deskriptif (misalnya, "US East Warehouse")
   - **Kode** — Identifikasi unik pendek (misalnya, "US-EAST")
   - **Wilayah Penjualan** — Tetapkan ke wilayah geografis untuk routing pemenuhan
   - **Alamat** — Alamat lengkap gudang untuk perhitungan pengiriman
3. Konfigurasikan pengaturan:
   - **Aktif** — Aktifkan untuk termasuk dalam pemenuhan pesanan
   - **Lokasi Ritel** — Tandai jika gudang ini juga berfungsi sebagai toko fisik
   - **Prioritas Pemenuhan** — Angka lebih tinggi = prioritas pemenuhan pesanan lebih tinggi
   - **Buffer Persediaan** — Persentase stok yang disisihkan sebagai buffer keamanan
4. Klik **Simpan**

### Prioritas Pemenuhan

Ketika pesanan masuk, sistem memilih gudang terbaik berdasarkan:

1. **Nilai prioritas** — Gudang dengan prioritas lebih tinggi lebih disukai
2. **Ketersediaan stok** — Harus memiliki stok yang cukup
3. **Pemetaan wilayah** — Gudang di wilayah pelanggan lebih disukai

Contoh, jika Anda memiliki gudang AS (prioritas 100) dan gudang Eropa (prioritas 60), pesanan AS akan dipenuhi dari gudang AS terlebih dahulu.

### Buffer Persediaan

Buffer persediaan menyisihkan persentase inventaris yang tidak akan dijual secara online. Ini berguna untuk:
- Toko ritel fisik yang memerlukan stok di lantai
- Stok cadangan untuk mencegah penjualan berlebihan
- Persediaan yang dicadangkan untuk pesanan grosir

10% buffer dari 100 unit berarti hanya 90 unit yang tersedia untuk pesanan online.

## Item Persediaan

Item persediaan merepresentasikan inventaris aktual dari produk tertentu di gudang tertentu.

### Melihat Tingkat Persediaan

1. Klik ikon **persediaan** di kartu gudang mana pun untuk melihat item persediaannya
2. Atau navigasikan ke tab **Inventaris** produk untuk melihat persediaan di semua gudang

Setiap item persediaan menampilkan:
- **Nama produk** dan variasi (jika berlaku)
- **Di tangan** — Total inventaris fisik
- **Telah dialokasikan** — Kuantitas yang dicadangkan untuk pesanan yang sedang diproses
- **Tersedia** — Di tangan dikurangi dialokasikan (apa yang bisa dijual)

### Menambahkan Persediaan

1. Dari tampilan persediaan gudang, klik **Tambah Item Persediaan**
2. Pilih produk dan variasi
3. Masukkan kuantitas **di tangan**
4. Simpan

### Pergerakan Persediaan

Setiap perubahan pada inventaris dilacak sebagai **pergerakan persediaan**:

| Jenis Pergerakan | Deskripsi |
|------------------|-----------|
| **Penerimaan** | Stok baru diterima dari pemasok |
| **Penjualan** | Stok dikurangi untuk pesanan yang telah dipenuhi |
| **Pengembalian** | Stok dikembalikan oleh pelanggan |
| **Penyesuaian** | Koreksi manual (ketidaksesuaian perhitungan) |
| **Pemindahan** | Dipindahkan antar gudang |
| **Pemesanan Sementara** | Dihold sementara untuk keranjang aktif |

Pergerakan persediaan menyediakan jejak audit lengkap dari perubahan inventaris.

## Pelacakan Persediaan pada Produk

### Mematikan Pelacakan Persediaan

Di tab **Inventaris** produk:

1. Nyalakan **Lacak Persediaan** untuk mengaktifkan manajemen stok
2. Tetapkan **Ambang Batas Persediaan Rendah** — memicu peringatan saat persediaan berada di bawah tingkat ini
3. Konfigurasikan **Izinkan Pemesanan Kembali** jika Anda ingin menerima pesanan saat stok habis

### Persediaan Multi-Gudang

Ketika pelacakan persediaan diaktifkan, tab Inventaris menampilkan tingkat persediaan di semua gudang dalam tabel ringkasan:

- Total di tangan di semua lokasi
- Pemecahan per gudang
- Kuantitas tersedia setelah reservasi dan alokasi

## Peringatan Persediaan Rendah

Sistem secara otomatis memantau tingkat persediaan dan memperingatkan Anda saat:
- Produk berada di bawah **ambang batas persediaan rendah**
- Produk mencapai **stok tersedia nol**

Peringatan persediaan rendah muncul di:
- **Dashboard Toko** di bagian **Tindakan yang Diperlukan**
- Daftar produk dengan indikator visual

## Tips

- Mulailah dengan satu gudang dan tambahkan lebih banyak saat bisnis Anda berkembang.
- Tetapkan prioritas pemenuhan berdasarkan kecepatan pengiriman dan biaya ke setiap wilayah.
- Gunakan buffer persediaan untuk lokasi ritel untuk memastikan ketersediaan stok di lantai.
- Periksa pergerakan persediaan secara teratur untuk mengidentifikasi penyusutan atau ketidaksesuaian.
- Tetapkan ambang batas persediaan rendah berdasarkan waktu pembaruan pesanan Anda — jika memerlukan 2 minggu untuk restok, tetapkan ambang batas untuk menutupi 2 minggu penjualan.
- Aktifkan pelacakan persediaan sebelum diluncurkan untuk menghindari penjualan berlebihan.
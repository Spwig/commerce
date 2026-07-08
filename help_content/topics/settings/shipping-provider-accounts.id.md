---
title: Akun Penyedia Pengiriman
---

Akun penyedia pengiriman menghubungkan toko Anda ke API penyedia (FedEx, UPS, DHL) untuk perhitungan tarif real-time dan pembelian label otomatis. Setiap akun menyimpan kredensial API yang dienkripsi, memantau kesehatan koneksi, dan terhubung ke metode pengiriman real-time. Penyedia mengambil tarif langsung saat checkout berdasarkan dimensi paket, berat, asal, dan tujuan—menghilangkan perawatan tabel tarif manual dan memastikan harga penyedia yang akurat.

Gunakan akun penyedia saat Anda membutuhkan tarif pengiriman yang dihitung oleh penyedia atau pembuatan label otomatis alih-alih pembuatan pengiriman manual.

## Penyedia Pengiriman yang Didukung

Spwig mendukung penyedia utama melalui komponen penyedia yang dapat diinstal:

### FedEx

**Layanan**: Ground, Express, International
**API**: FedEx Web Services
**Fitur**: Tarif real-time, pembelian label, pelacakan, dokumen bea cukai internasional

### UPS

**Layanan**: Ground, Air, Worldwide
**API**: UPS Developer API
**Fitur**: Tarif real-time, pembuatan label, pelacakan, validasi alamat

### DHL

**Layanan**: Express, eCommerce, International
**API**: DHL Express API
**Fitur**: Tarif internasional, dokumen bea cukai, pelacakan

### Penyedia Tambahan

Pasang dari pasar komponen sesuai kebutuhan (USPS, Canada Post, Australia Post, dll.)

---

## Konfigurasi Akun Penyedia

Setiap akun penyedia memerlukan:

### Informasi Dasar

- **Nama Tampilan**: Cara akun muncul di admin (misalnya, "Akun Produksi FedEx")
- **Penyedia**: Pilih komponen penyedia yang terinstal dari dropdown
- **Aktif**: Toggle untuk mengaktifkan/menonaktifkan tanpa menghapus kredensial
- **Default**: Tetapkan sebagai akun default untuk penyedia ini (hanya satu default per penyedia)

### Kredensial API (Dienkripsi)

**Bervariasi berdasarkan penyedia**, biasanya mencakup:

**FedEx**:
- Nomor Akun
- Nomor Meter
- API Key
- API Secret

**UPS**:
- Nomor Lisensi Akses
- ID Pengguna
- Kata Sandi
- Nomor Akun

**DHL**:
- ID Situs
- Kata Sandi
- Nomor Akun

**Semua kredensial dienkripsi dalam penyimpanan** dan hanya didekripsi saat membuat panggilan API.

### Alamat Asal

- **Alamat Kirim Default**: Gudang/alamat asal untuk perhitungan tarif
- Beberapa penyedia memerlukan pengaturan asal tertentu di dashboard mereka

### Pengaturan

Opsi khusus penyedia (bervariasi berdasarkan penyedia):

- **Mode Uji**: Gunakan akhir uji/sandbox penyedia
- **Tarif yang Dibicarakan**: Gunakan tarif yang dinegosiasikan dengan penyedia (jika tersedia)
- **Sertakan Asuransi**: Tawarkan asuransi secara otomatis dalam tarif
- **Biaya Pengiriman untuk Rumah Tangga**: Terapkan biaya pengiriman untuk pengiriman ke alamat rumah tangga
- **Tanda Tangan Diperlukan**: Persyaratan tanda tangan default

---

## Membuat Akun Penyedia

**Proses Pengaturan 6 Langkah**:

**Langkah 1: Dapatkan Akses API Penyedia**
1. Buat akun dengan penyedia (FedEx.com, UPS.com, DHL.com)
2. Ajukan akses API/Pengembang
3. Lengkapi onboarding API penyedia (mungkin memakan waktu 1-3 hari kerja)
4. Terima kredensial API melalui email atau portal pengembang

**Langkah 2: Pasang Komponen Penyedia** (jika belum dipasang sebelumnya)
1. Pergi ke **Pengaturan > Komponen > Pasar Komponen**
2. Cari nama penyedia (misalnya, "FedEx")
3. Pasang komponen penyedia pengiriman
4. Tunggu hingga pemasangan selesai

**Langkah 3: Buat Akun Penyedia di Spwig**
1. Navigasi ke **Pengaturan > Pengiriman > Akun Penyedia**
2. Klik "Tambahkan Akun Penyedia"
3. Pilih penyedia dari dropdown
4. Masukkan nama tampilan

**Langkah 4: Masukkan Kredensial API**
1. Isi bidang kredensial (bervariasi berdasarkan penyedia)
2. Kredensial dienkripsi secara otomatis saat disimpan
3. Opsional: Aktifkan mode uji untuk pengujian awal

**Langkah 5: Uji Koneksi**
1. Klik tombol "Uji Koneksi"
2. Sistem mencoba panggilan API ke penyedia
3. Verifikasi status "Terhubung" muncul
4. Periksa tanda waktu last_tested_at

**Langkah 6: Hubungkan ke Metode Pengiriman**
1. Buat atau edit metode pengiriman (**Pengaturan > Keranjang > Metode Pengiriman**)
2. Setel method_type = "Real-Time"
3. Pilih akun penyedia dari dropdown
4. Simpan metode

---

## Pemantauan Status Koneksi

Akun penyedia melacak kesehatan koneksi:

### Nilai Status

**Tidak diketahui** (abu-abu): Pernah diuji atau belum terhubung

**Terhubung** (hijau): Panggilan API terakhir berhasil, kredensial valid

**Kesalahan** (merah): Panggilan API terakhir gagal, kredensial mungkin tidak valid

### Terakhir Diuji

- **Timestamp**: Kapan koneksi terakhir diverifikasi
- **Auto-updates**: Setiap kali penyedia digunakan (pencarian tarif, pembelian label)
- **Uji manual**: Klik tombol "Uji Koneksi" kapan saja

### Menyelesaikan Koneksi yang Gagal

**Penyebab Umum**:
- Kredensial API salah (ejaan salah, disalin dengan spasi tambahan)
- Kunci API penyedia sudah kedaluwarsa atau dicabut
- Mode uji diaktifkan tetapi menggunakan kredensial produksi (atau sebaliknya)
- Alamat IP tidak diizinkan oleh penyedia
- Penyedia API sedang mengalami gangguan

**Langkah Solusi**:
1. Verifikasi kredensial cocok dengan dashboard penyedia secara tepat
2. Periksa pengaturan mode uji cocok dengan jenis kredensial
3. Periksa halaman status API penyedia untuk gangguan
4. Hubungi dukungan penyedia untuk verifikasi akun

---

## Alur Pencarian Tarif

Bagaimana tarif real-time bekerja saat checkout:

**1. Pelanggan Memasukkan Alamat**
- Alamat pengiriman dimasukkan
- Keranjang menghitung total berat + dimensi

**2. Sistem Menyiapkan Permintaan Tarif**
- Mengambil kredensial akun penyedia (didekripsi)
- Menghitung dimensi paket dari item keranjang (menggunakan paket pengiriman jika didefinisikan)
- Menyiapkan permintaan API dengan asal, tujuan, paket

**3. API Penyedia Dipanggil**
- Permintaan dikirim ke API penyedia dengan kredensial otentikasi
- Penyedia menghitung tarif berdasarkan zona, berat, dimensi
- Respons mencakup opsi layanan (Ground, Express, dll.)

**4. Tarif Ditampilkan**
- Sistem memparse respons penyedia
- Menormalkan ke format standar
- Markup opsional diterapkan (jika dikonfigurasi)
- Tarif ditampilkan kepada pelanggan saat checkout

**5. Pelanggan Memilih Layanan**
- Pelanggan memilih opsi yang diinginkan
- Tarif yang dipilih disimpan ke pesanan

**Alur API Contoh**:
```
Permintaan ke API FedEx:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // gram
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

Respons FedEx:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Pembelian Label (Opsional)

Jika penyedia mendukung pembuatan label:

**Alur Kerja**:
1. Pelanggan menyelesaikan pesanan
2. Penjual membuat pengiriman (**Pesanan > Detail Pesanan > Buat Pengiriman**)
3. Pilih akun penyedia + layanan
4. Sistem memanggil API label penyedia
5. PDF label dibuat dan dilampirkan ke pengiriman
6. Nomor pelacakan diisi secara otomatis
7. Label siap dicetak

**Manfaat**:
- Tidak perlu login ke situs web penyedia secara manual
- Pelacakan disinkronkan secara otomatis
- Formulir bea cukai dihasilkan secara otomatis (internasional)
- Pembuatan label dalam batch mungkin

---

## Markup Tarif

Tambahkan markup penjual ke tarif penyedia:

**Konfigurasi** (di metode pengiriman, bukan akun penyedia):
- **Jenis Markup**: Persentase atau Tetap
- **Jumlah Markup**: contoh, 15% atau $2.50

**Contoh**:
```
Tarif Penyedia: $12.50
Markup: 15%
Pelanggan Membayar: $14.38

ATAU

Tarif Penyedia: $12.50
Markup: $2.50 (tetap)
Pelanggan Membayar: $15.00
```

**Kasus Penggunaan**:
- Tutup biaya kemasan/pengelolaan
- Tambahkan margin keuntungan untuk pengiriman
- Menutup biaya kartu kredit pada pengiriman

---

## Akun Penyedia Banyak

Anda dapat membuat beberapa akun untuk penyedia yang sama:

**Kasus Penggunaan**:
1. **Uji vs Produksi**
   - Akun Uji: Kredensial sandbox penyedia
   - Akun Produksi: Kredensial live

2. **Banyak Gudang**
   - Akun Gudang A: Asal = Los Angeles
   - Akun Gudang B: Asal = New York

3. **Tarif yang Dinegosiasikan Berbeda**
   - Akun A: Tarif standar
   - Akun B: Tarif diskon volume

**Setiap akun dapat terhubung ke metode pengiriman berbeda** untuk konfigurasi fleksibel.

---

## Tips

- **Uji di sandbox terlebih dahulu** - Gunakan kredensial uji penyedia sebelum pergi live
- **Pantau status koneksi** - Periksa dashboard untuk status kesalahan secara teratur
- **Definisikan paket pengiriman** - Dimensi yang akurat meningkatkan kutipan tarif
- **Gunakan tarif yang dinegosiasikan** - Aktifkan jika Anda memiliki diskon volume dengan penyedia
- **Atur asal yang realistis** - Gunakan alamat asal yang sebenarnya untuk zona yang akurat
- **Jaga kredensial aman** - Jangan pernah berbagi kunci API, rotasi secara berkala
- **Punya metode cadangan** - Pertahankan metode flat-rate aktif jika API penyedia gagal
- **Pantau batas API penyedia** - Beberapa penyedia membatasi panggilan API per hari
- **Perbarui kredensial segera** - Saat penyedia memutar kunci, perbarui segera
- **Gunakan nama deskriptif** - "FedEx LA Warehouse" lebih baik daripada "FedEx 1"
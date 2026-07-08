---
title: Permintaan Pengembalian & Pemrosesan
---

Permintaan pengembalian melacak pengembalian pelanggan dari awal hingga penyelesaian pengembalian—pelanggan memilih barang yang dikembalikan dengan alasan, pedagang menyetujui atau menolak permintaan, menghasilkan label pengembalian, memeriksa barang yang dikembalikan, dan memproses pengembalian. Alur kerja berlangsung melalui 9 tahap status (menunggu → disetujui → label_dikirim → dalam_perjalanan → diterima → diperiksa → selesai/ditolak/dibatalkan) dengan alasan pengembalian per barang, catatan pemeriksaan, dan biaya restocking opsional.

Gunakan halaman admin ini untuk meninjau, menyetujui, dan memproses permintaan pengembalian pelanggan secara efisien.

## Alur Kerja Permintaan Pengembalian

**Proses 9 Tahap**:

### 1. Menunggu (Diatas Inisiatif Pelanggan)

Pelanggan mengirimkan permintaan pengembalian:
- Memilih barang dari pesanan
- Memberikan alasan pengembalian per barang
- Catatan pelanggan opsional
- Status: `menunggu`

### 2. Disetujui/Ditolak (Pemeriksaan oleh Pedagang)

Pedagang meninjau permintaan:
- **Setujui**: Pengembalian diperbolehkan, lanjutkan ke pembuatan label
- **Tolak**: Pengembalian ditolak dengan alasan penolakan
- Status: `disetujui` atau `ditolak`

### 3. Label Dikirim (Pengiriman Pengembalian)

Label pengembalian dibuat:
- Pedagang membuat pengiriman pengembalian (opsional)
- Label pengembalian dikirim ke pelanggan melalui email
- Pelanggan mengirimkan barang kembali
- Status: `label_dikirim`

### 4. Dalam Perjalanan (Pelanggan Mengirim)

Pelanggan mengirim barang:
- Pelacakan menunjukkan pergerakan
- Pembaruan status otomatis dari webhook penyedia
- Status: `dalam_perjalanan`

### 5. Diterima (Tiba di Gudang)

Barang tiba:
- Gudang memindai pengiriman
- Barang diperiksa masuk
- Status: `diterima`

### 6. Diperiksa (Pemeriksaan Kualitas)

Pedagang memeriksa barang:
- Catat kondisi barang (sangat baik/baik/terimaable/berlumur/bercacat)
- Tambahkan catatan pemeriksaan
- Terapkan biaya restocking jika berlaku
- Status: `diperiksa`

### 7. Selesai (Pengembalian Diproses)

Pengembalian dikeluarkan:
- Buat pengembalian terkait
- Pembayaran diproses
- Pengembalian ditutup
- Status: `selesai`

**Hasil Alternatif**:
- **Dibatalkan**: Pelanggan membatalkan sebelum pengiriman
- **Ditolak**: Pedagang menolak setelah tinjauan

---

## Pemrosesan Permintaan Pengembalian

**Langkah demi Langkah**:

**Langkah 1: Tinjau Permintaan yang Menunggu**
- Navigasi ke Pesanan > Permintaan Pengembalian
- Filter berdasarkan status = "Menunggu"
- Klik permintaan untuk melihat detail

**Langkah 2: Evaluasi Permintaan**
- Tinjau detail pesanan
- Periksa alasan pengembalian
- Verifikasi kepatuhan terhadap kebijakan pengembalian (dalam jangka pengembalian, barang layak)

**Langkah 3: Setujui atau Tolak**
- Klik "Setujui" untuk menerima pengembalian
- ATAU klik "Tolak" dan masukkan alasan penolakan
- Simpan keputusan

**Langkah 4: Buat Label Pengembalian** (jika disetujui)
- Klik "Buat Pengiriman Pengembalian"
- Pilih penyedia/jasa
- Sistem menghasilkan label pengembalian
- Label dikirim otomatis ke pelanggan
- Status → `label_dikirim`

**Langkah 5: Pantau Perjalanan**
- Pembaruan pelacakan otomatis sinkron dari webhook penyedia
- Status otomatis maju ke `dalam_perjalanan` ketika penyedia memindai paket

**Langkah 6: Terima Barang**
- Ketika barang tiba, klik "Tandai sebagai Diterima"
- Status → `diterima`

**Langkah 7: Periksa Barang**
- Buka permintaan pengembalian
- Pilih kondisi barang dari dropdown:
  - Sangat Baik (seperti baru, dapat dijual kembali)
  - Baik (sedikit aus, dapat dijual kembali)
  - Terimaable (aus terlihat, dapat dijual kembali dengan diskon)
  - Rusak (tidak dapat dijual kembali)
  - Rusak Pabrik (cacat produksi)
- Tambahkan catatan pemeriksaan
- Opsional: Terapkan biaya restocking (persentase atau tetap)
- Status → `diperiksa`

**Langkah 8: Proses Pengembalian**
- Klik "Buat Pengembalian"
- Sistem menghitung jumlah pengembalian:
  - Harga barang asli
  - Kurangi biaya restocking (jika diterapkan)
  - Kurangi biaya pengiriman (jika tidak dapat dikembalikan)
- Buat pengembalian (terkait dengan permintaan pengembalian)
- Status → `selesai`

---

## Alasan Pengembalian Per Barang

Pelanggan memilih alasan per barang:

**Alasan Umum**:
- Barang yang salah diterima
- Barang rusak/cacat
- Berubah pikiran/tidak lagi diperlukan
- Barang tidak sesuai deskripsi
- Ditemukan harga yang lebih baik
- Pesanan oleh kesalahan
- Kualitas tidak sesuai harapan

**Gunakan Alasan Untuk**:
- Analitik (lacak penyebab pengembalian umum)
- Kontrol kualitas (identifikasi produk cacat)
- Peningkatan proses (kurangi pengembalian yang dapat dicegah)

---

## Biaya Restocking

Terapkan biaya untuk mengimbangi biaya pemrosesan pengembalian:

**Konfigurasi**:
- **Jenis**: Persentase (misalnya, 15%) atau Tetap (misalnya, $5)
- **Kapan Diterapkan**: Pengembalian non-cacat, barang terbuka, pesanan khusus

**Contoh**:
```
Belanja awal: $100
Biaya restocking: 15%
Jumlah pengembalian: $85
```

**Praktik Terbaik**:
- Komunikasikan kebijakan biaya restocking secara jelas
- Jangan terapkan untuk barang cacat
- Pertimbangkan untuk menghapus untuk pelanggan VIP

---

## Pedoman Pemeriksaan Pengembalian

Tetapkan kriteria pemeriksaan yang konsisten:

**Sangat Baik**:
- Kemasan asli belum terbuka
- Tidak ada tanda aus terlihat
- Semua aksesori termasuk
- Dapat dijual kembali dengan harga penuh

**Baik**:
- Terbuka tetapi penggunaan minimal
- Sedikit aus kemasan
- Semua komponen hadir
- Dapat dijual kembali dengan harga penuh

**Terimaable**:
- Tanda penggunaan/aus terlihat
- Kemasan rusak
- Hilang aksesori non-esensial
- Dapat dijual kembali dengan diskon

**Rusak**:
- Rusak fisik
- Komponen hilang
- Tidak dapat dijual kembali
- Diperlukan pembuangan atau perbaikan

**Rusak Pabrik**:
- Cacat produksi
- Gagal fungsional
- Klaim garansi
- Pengembalian ke pabrik

---

## Opsi Pengiriman Pengembalian

**Opsi 1: Pelanggan Bayar Pengiriman Pengembalian**
- Tidak ada label pengembalian yang diberikan
- Pelanggan memilih penyedia pengiriman sendiri
- Entri nomor pelacakan manual

**Opsi 2: Pedagang Sediakan Label yang Dibayar Sebelumnya**
- Buat label pengembalian melalui akun penyedia
- Biaya dikurangi dari pengembalian atau pedagang menyerapnya
- Pelacakan sinkron otomatis

**Opsi 3: Pengiriman Pengembalian Gratis**
- Pedagang menyerap biaya pengiriman pengembalian
- Meningkatkan kepuasan pelanggan
- Meningkatkan tingkat pengembalian (pertimbangkan trade-off)

---

## Penyaringan & Pelaporan

**Penyaring yang Berguna**:
- Status: Menunggu (butuh tindakan)
- Rentang Tanggal: 30 hari terakhir
- Pesanan: Pencarian pesanan spesifik
- Alasan: Lacak penyebab pengembalian

**Analitik Pengembalian**:
- Tingkat pengembalian berdasarkan produk
- Alasan pengembalian paling umum
- Rata-rata waktu pemrosesan (menunggu → selesai)
- Pendapatan biaya restocking

---

## Tips

- **Tetapkan kebijakan pengembalian yang jelas** - Komunikasikan jendela (30 hari), kondisi, biaya
- **Proses permintaan secara cepat** - Jawab permintaan yang menunggu dalam 24 jam
- **Periksa secara menyeluruh** - Dokumentasikan kondisi untuk menghindari sengketa
- **Lacak alasan pengembalian** - Gunakan data untuk meningkatkan produk/deskripsi
- **Otomatis sebanyak mungkin** - Webhook penyedia memperbarui status perjalanan secara otomatis
- **Komunikasikan dengan pelanggan** - Kirim email pembaruan pada setiap perubahan status
- **Adil dalam biaya restocking** - Terapkan secara konsisten, hapus untuk cacat
- **Pantau penipuan pengembalian** - Tandai pelanggan dengan pengembalian berlebihan
- **Perbaiki kemasan** - Kurangi pengembalian terkait kerusakan
- **Perbarui inventaris secara cepat** - Kembalikan stok setelah pemeriksaan
- **Pelajari dari pola** - Tingkat pengembalian tinggi untuk produk tertentu mungkin menunjukkan masalah kualitas

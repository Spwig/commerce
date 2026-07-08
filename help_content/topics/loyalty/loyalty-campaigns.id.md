---
title: Kampanye Keanggotaan
---

Kampanye keanggotaan memungkinkan Anda menjalankan promosi berbatas waktu dan hadiah otomatis yang melampaui aturan pengumpulan poin sehari-hari. Gunakan mereka untuk menjalankan akhir pekan poin ganda, memberi hadiah kepada pelanggan di hari ulang tahun mereka, memulihkan pelanggan yang tidak aktif, dan memberikan bonus terarah kepada kelompok anggota tertentu.

Setiap kampanye mendefinisikan pemicu atau jadwal, anggota yang berlaku, dan tindakan yang diambil. Setelah aktif, kampanye akan berjalan secara otomatis — Anda hanya perlu mengatur sekali dan Spwig akan menangani sisanya.

## Jenis kampanye

| Jenis | Kapan terpicu |
|------|---------------|
| **Berdasarkan Pemicu** | Ketika kejadian tertentu terjadi (misalnya, pesanan ditempatkan, ulang tahun terdeteksi) |
| **Jadwal** | Pada jadwal berulang (harian, mingguan, bulanan) |
| **Manual** | Hanya ketika Anda secara eksplisit menjalankannya dari admin |
| **Perilaku** | Ketika pelanggan cocok dengan pola perilaku (misalnya, menjelajah tanpa membeli) |

## Membuat kampanye

Navigasikan ke **Promosi > Kampanye Keanggotaan** dan klik **+ Tambahkan Kampanye Keanggotaan**.

### Langkah 1: informasi dasar

- **Nama** — nama yang jelas dan deskriptif yang hanya terlihat di admin (misalnya, `Bonus Ulang Tahun — 200 Poin`)
- **Slug** — dihasilkan secara otomatis dari nama; digunakan secara internal
- **Deskripsi** — catatan opsional tentang tujuan kampanye
- **Jenis Kampanye** — pilih jenis dari tabel di atas

### Langkah 2: pemicu atau jadwal

**Untuk kampanye berdasarkan pemicu**, atur **Peristiwa Pemicu** yang memicu kampanye. Pemicu yang tersedia meliputi:

| Pemicu | Deskripsi |
|---------|-------------|
| Pesanan Ditempatkan | Terpicu ketika anggota menyelesaikan pesanan |
| Pembelian Pertama | Terpicu pada pesanan pertama anggota |
| Ulang Tahun Pelanggan | Terpicu pada ulang tahun anggota |
| Perayaan Keanggotaan | Terpicu setiap tahun pada hari keanggotaan anggota |
| Keranjang Ditinggalkan | Terpicu ketika keranjang ditinggalkan tanpa checkout |
| Promosi Tingkat | Terpicu ketika anggota naik ke tingkat yang lebih tinggi |
| Poin Sebentar Lagi Kadaluarsa | Terpicu ketika anggota memiliki poin yang segera kadaluarsa |
| Tidak Aktif 90 Hari | Terpicu ketika anggota tidak melakukan pembelian dalam 90 hari |
| Ulasan Dikirim | Terpicu ketika anggota mengirim ulasan produk |
| Referensi Dikonversi | Terpicu ketika pelanggan yang direferensikan melakukan pembelian 

Anda dapat menambahkan **Kondisi Pemicu** sebagai objek JSON untuk menyaring lebih lanjut kapan kampanye terpicu. Sebagai contoh, untuk hanya memicu pesanan di atas $100:

```json
{
  "min_order_amount": 100
}
```

**Untuk kampanye jadwal**, atur **Jenis Jadwal** (Harian, Mingguan, Bulanan, atau Cron Kustom) dan konfigurasikan waktu dalam bidang **Konfigurasi Jadwal**:

```json
{
  "hour": 9,
  "minute": 0
}
```

### Langkah 3: tindakan

Bidang **Tindakan** mendefinisikan apa yang terjadi ketika kampanye terpicu. Masukkan array JSON dari objek tindakan. Tindakan paling umum adalah pemberian poin bonus:

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Bonus ulang tahun — terima kasih telah menjadi anggota!"
  }
]
```

Tindakan lain yang tersedia meliputi mengirimkan notifikasi email atau memberikan badge. Lihat dokumentasi komponen penyedia Anda untuk daftar lengkap.

### Langkah 4: penargetan

Kontrol anggota mana yang berlaku untuk kampanye menggunakan bidang penargetan:

- **Target Semua Anggota** — dicentang secara default; kampanye berlaku untuk setiap anggota keanggotaan aktif
- **Target Segmen** — batasi kampanye hanya untuk anggota dalam segmen tertentu (lihat [Segmen](#managing-member-segments) di bawah ini)
- **Target Tingkat** — batasi kampanye hanya untuk anggota dalam tingkat keanggotaan tertentu

### Langkah 5: batasan dan masa pendingin

- **Maksimal Pemicu per Anggota** — seberapa sering anggota yang sama dapat memperoleh manfaat dari kampanye ini. Tetapkan ke `1` untuk hadiah sekali pakai seperti hadiah ulang tahun. Biarkan kosong untuk tidak terbatas.
- **Hari Masa Pendingin** — hari minimum antara pemicu kampanye untuk anggota yang sama. Sebagai contoh, tetapkan ke `365` untuk mencegah kampanye ulang tahun dari terpicu lebih dari sekali per tahun.

### Langkah 6: tanggal kampanye

Atur **Tanggal Mulai** dan **Tanggal Berakhir** untuk membuat kampanye berbatas waktu. Biarkan keduanya kosong untuk kampanye yang berlangsung terus-menerus.

Kampanye dapat berada dalam salah satu status berikut:

| Status | Deskripsi |
|--------|-------------|
| **Draft** | Dibuat tetapi belum aktif; aman untuk dikonfigurasi dan diuji |
| **Aktif** | Berjalan dan akan berjalan ketika kondisi terpenuhi |
| **Dijeda** | Dihentikan sementara tanpa kehilangan konfigurasi |
| **Selesai** | Melebihi tanggal akhirnya; tidak lagi berjalan |
| **Diarsipkan** | Tersembunyi dari daftar aktif tetapi disimpan untuk catatan |

Setelah mengisi semua bidang, klik **Simpan**. Kemudian ubah status menjadi **Aktif** untuk memulai kampanye.

## Contoh praktis

### Contoh: double points weekend

**Skenario:** Berikan 2x poin pada semua pembelian yang ditempatkan selama akhir pekan tertentu.

| Bidang | Nilai |
|-------|-------|
| Nama | `Double Points Weekend — Maret` |
| Jenis Kampanye | Berbasis Pemicu |
| Acara Pemicu | Pesanan Ditempatkan |
| Tindakan | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| Tanggal Mulai | Malam Jumat |
| Tanggal Berakhir | Tengah malam Minggu |
| Target Semua Anggota | Dicentang |

### Contoh: bonus ulang tahun

**Skenario:** Berikan 200 poin bonus kepada setiap anggota loyalitas pada ulang tahun mereka.

| Bidang | Nilai |
|-------|-------|
| Nama | `Birthday Bonus` |
| Jenis Kampanye | Berbasis Pemicu |
| Acara Pemicu | Ulang Tahun Pelanggan |
| Tindakan | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Selamat ulang tahun dari kami!\"}"]` |
| Maksimal Pemicu per Anggota | 1 |
| Hari Pendinginan | 365 |
| Target Semua Anggota | Dicentang |

### Contoh: kampanye win-back

**Skenario:** Kirimkan 100 poin bonus kepada anggota yang belum membeli dalam 90 hari.

| Bidang | Nilai |
|-------|-------|
| Nama | `90-Day Win-Back Bonus` |
| Jenis Kampanye | Berbasis Pemicu |
| Acara Pemicu | Tidak Aktif 90 Hari |
| Tindakan | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"Kami merindukan Anda — berikut beberapa poin bonus\"}"]` |
| Maksimal Pemicu per Anggota | 1 |
| Hari Pendinginan | 180 |
| Target Semua Anggota | Dicentang |

## Mengelola segmen anggota

Segmen memungkinkan Anda menargetkan kampanye pada kelompok spesifik anggota loyalitas. Navigasikan ke **Promosi > Segmen Loyalitas** untuk mengelolanya.

### Jenis segmen

| Jenis | Deskripsi |
|------|-------------|
| **Berdasarkan Aturan** | Keanggotaan ditentukan oleh aturan (misalnya, anggota dengan lebih dari 1.000 poin) |
| **Perhitungan Dinamis** | Keanggotaan dihitung saat ini dari kriteria real-time |
| **Penugasan Manual** | Anggota ditambahkan ke segmen secara manual |

### Membuat segmen

1. Navigasikan ke **Promosi > Segmen Loyalitas** dan klik **+ Tambah Segmen Loyalitas**
2. Isi:
   - **Nama** — nama deskriptif (misalnya, `Pelanggan Berharga`, `Anggota Tier Perak`)
   - **Slug** — dihasilkan secara otomatis
   - **Jenis Kriteria** — cara keanggotaan ditentukan
   - **Konfigurasi Kriteria** — objek JSON yang mendefinisikan aturan keanggotaan
3. Klik **Simpan**

#### Contoh: segmen untuk anggota dengan 500+ poin

```json
{
  "min_available_points": 500
}
```

#### Contoh: segmen hanya untuk anggota tier emas

```json
{
  "tier_slugs": ["gold"]
}
```

Kolom **Jumlah Anggota** dalam daftar segmen menunjukkan berapa banyak anggota saat ini yang cocok. Klik segmen dan gunakan tindakan **Perbarui Jumlah Anggota** untuk menghitung ulang jika data Anda telah berubah.

## Melacak kinerja kampanye

### Riwayat eksekusi kampanye

Navigasikan ke **Promosi > Eksekusi Kampanye** untuk melihat catatan setiap kali kampanye berjalan untuk anggota mana pun. Setiap catatan eksekusi menunjukkan kampanye mana yang berjalan, anggota mana yang berjalan, dan hasilnya.

### Melihat jangkauan kampanye

Buka catatan kampanye apa pun untuk melihat jumlah **Kali Dipicu** dan kapan kampanye terakhir berjalan. Ini memberi Anda pandangan cepat tentang berapa banyak anggota yang telah memanfaatkan kampanye tersebut.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Buat kampanye dengan status **Draft** terlebih dahulu agar Anda dapat meninjau semua pengaturan sebelum kampanye tersebut diluncurkan
- Gunakan **Max Triggers Per Member** pada semua kampanye bonus sekali pakai (ulang tahun, pembelian pertama, pendaftaran) untuk mencegah pelanggan mendapatkan bonus lebih dari sekali
- Gabungkan **Target Segment** dengan kampanye berbasis pencetus untuk menjalankan promosi eksklusif tingkat — contohnya, poin ganda pada pembelian hanya untuk anggota Gold dan Platinum
- Tetapkan nilai **Cooldown Days** pada kampanye win-back agar anggota tidak terganggu jika mereka melakukan pembelian kecil dan kemudian menjadi tidak aktif lagi tidak lama setelahnya
- Daftar kampanye adalah alat terbaik Anda untuk melacak promosi yang saat ini aktif — tinjau daftar tersebut sebelum meluncurkan penawaran baru untuk memastikan kampanye tidak tumpang tindih secara tidak sengaja
- Arsipkan kampanye yang telah berakhir daripada menghapusnya agar Anda memiliki catatan sejarah dari promosi yang telah Anda lakukan dan kapan
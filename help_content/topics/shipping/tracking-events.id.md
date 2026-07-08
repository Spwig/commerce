---
title: Pemantauan Acara
---

Acara pemantauan mencatat titik-titik status pengiriman sepanjang siklus pengiriman—setiap acara menangkap status (dalam perjalanan, sedang dikirim, telah terkirim), tanda waktu, lokasi, deskripsi, dan data pengangkut mentah. Acara dibuat secara otomatis melalui notifikasi webhook pengangkut atau secara manual oleh pedagang. Pelanggan melihat riwayat acara pemantauan di akun mereka dan email konfirmasi pesanan, memberikan visibilitas pengiriman secara real-time.

Halaman admin ini menampilkan riwayat acara hanya baca untuk tujuan audit dan dukungan pelanggan.

## Struktur Acara Pemantauan

Setiap acara berisi:

**Informasi Status**:
- **Status**: dalam_perjalanan, sedang_dikirim, telah_terkirim, pengecualian, gagal, dikembalikan
- **Deskripsi**: Status yang dapat dibaca oleh manusia (misalnya, "Paket tiba di fasilitas pengurutan")
- **Kode Status Pengangkut**: Status pengangkut asli (misalnya, "DEP" untuk telah berangkat)

**Data Lokasi**:
- **Kota**: Kota lokasi acara
- **Negara Bagian**: Negara bagian/propinsi lokasi acara
- **Negara**: Negara lokasi acara
- **Kode Pos**: Kode pos/ZIP lokasi acara

**Tanda Waktu**:
- **Terjadi Pada**: Saat acara terjadi (waktu pengangkut)
- **Dibuat Pada**: Saat acara dicatat di Spwig (waktu sistem)

**Metadata**:
- **Data Mentah**: Respons JSON lengkap dari API pengangkut
- **Pengiriman**: ID pengiriman yang terkait

---

## Jenis Status Acara

**dalam_perjalanan**: Paket bergerak melalui jaringan pengangkut
- Contoh: "Paket telah berangkat dari fasilitas", "Tiba di pusat", "Dalam perjalanan ke fasilitas berikutnya"

**sedang_dikirim**: Paket di kendaraan pengiriman
- Contoh: "Sedang dikirim", "Di kendaraan pengiriman"

**telah_terkirim**: Paket berhasil dikirim
- Contoh: "Telah terkirim ke pintu depan", "Ditinggalkan di resepsionis", "Diberikan kepada penerima"

**pengecualian**: Masalah pengiriman yang memerlukan perhatian
- Contoh: "Keterlambatan cuaca", "Alamat salah", "Percobaan pengiriman gagal"

**gagal**: Pengiriman gagal secara permanen
- Contoh: "Tidak dapat dikirim ke alamat yang diberikan", "Ditolak oleh penerima"

**dikembalikan**: Paket sedang dikembalikan ke pengirim
- Contoh: "Pengembalian ke pengirim dimulai", "Paket dikembalikan"

---

## Cara Acara Pemantauan Dibuat

### Otomatis (Webhook Pengangkut)

**Alur Kerja**:
1. Pengangkut memindai paket (berangkat, tiba, dikirim)
2. Pengangkut mengirim webhook ke titik akhir webhook Spwig
3. Webhook dicatat dalam tabel WebhookLog
4. Sistem memparse payload webhook
5. Acara Pemantauan dibuat dengan data yang diekstrak
6. Notifikasi email pelanggan dikirim (jika dikonfigurasi)

**Manfaat**:
- Pembaruan real-time (tidak perlu polling)
- Tanda waktu akurat dari pengangkut
- Riwayat acara lengkap secara otomatis dipertahankan

### Manual (Pengisian Pedagang)

**Alur Kerja**:
1. Navigasi ke detail pengiriman
2. Klik "Tambahkan Acara Pemantauan"
3. Pilih status dari dropdown
4. Masukkan deskripsi
5. Opsional: Masukkan data lokasi
6. Tetapkan tanda waktu terjadi_pada
7. Simpan

**Kasus Penggunaan**:
- Pengangkut tanpa dukungan webhook
- Koreksi pengiriman manual
- Pengiriman lokal (non-pengangkut)
- Pembaruan status internal

---

## Urutan Tampilan Acara

Acara ditampilkan dalam **urutan kronologis terbalik** (terbaru terlebih dahulu):

**Contoh Tampilan**:
```
13 Feb 2026 10:30 AM - Telah Terkirim (Brooklyn, NY)
13 Feb 2026 08:15 AM - Sedang Dikirim (Brooklyn, NY)
12 Feb 2026 11:45 PM - Tiba di fasilitas lokal (Brooklyn, NY)
12 Feb 2026 06:30 PM - Dalam Perjalanan (Newark, NJ)
12 Feb 2026 02:15 PM - Berangkat dari asal (Philadelphia, PA)
12 Feb 2026 09:00 AM - Diambil (Philadelphia, PA)
```

---

## Visibilitas Pelanggan

Acara pemantauan ditampilkan kepada pelanggan dalam:

**Email Konfirmasi Pesanan**:
- Status acara terbaru
- Tanggal pengiriman yang diperkirakan
- Tautan pelacakan

**Akun Pelanggan > Detail Pesanan**:
- Timeline acara lengkap
- Deskripsi acara
- Riwayat lokasi
- Tanda waktu

**Halaman Pelacakan** (jika diaktifkan):
- URL pelacakan khusus
- Timeline visual
- Logo pengangkut
- Peta pengiriman (jika tersedia data lokasi)

---

## Penyaring Acara Pemantauan

**Penyaring yang Berguna**:
- **Pengiriman**: Lihat acara untuk pengiriman spesifik
- **Status**: Saring berdasarkan jenis acara (telah_terkirim, dalam_perjalanan, dll.)
- **Rentang Tanggal**: Acara dalam periode waktu
- **Lokasi**: Acara di kota/propinsi spesifik

**Kasus Penggunaan**:
- "Tampilkan semua pengiriman yang telah terkirim hari ini"
- "Cari semua pengecualian dalam seminggu terakhir"
- "Lacak pengiriman yang sedang dalam_perjalanan"

---

## Data Mentah (Pemecahan Masalah)

**Lokasi Data Mentah**:
- Menyimpan respons lengkap API pengangkut sebagai JSON
- Berguna untuk memperbaiki masalah webhook
- Mengandung metadata spesifik pengangkut

**Contoh Data Mentah** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "Sedang dikirim",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**Kapan Periksa Data Mentah**:
- Deskripsi acara tidak jelas
- Data lokasi hilang
- Kesalahan pemrosesan webhook
- Eskalasi dukungan pengangkut

---

## Waktu Acara

**Terjadi Pada** vs **Dibuat Pada**:

**Terjadi Pada**: Saat acara pengangkut terjadi
- Contoh: Paket dipindai pada pukul 10:30 AM

**Dibuat Pada**: Saat Spwig menerima webhook
- Contoh: Webhook diterima pada pukul 10:32 AM (keterlambatan 2 menit)

**Mengapa Berbeda?**:
- Latensi jaringan
- Pemrosesan pengangkut dalam batch
- Keterlambatan ulang webhook

**Gunakan Terjadi Pada untuk tampilan pelanggan** - lebih akurat mencerminkan kemajuan pengiriman sebenarnya.

---

## Tips

- **Acara hanya baca** - Tidak dapat diedit setelah dibuat (integritas audit)
- **Periksa data mentah untuk detail** - Lebih banyak informasi daripada bidang yang ditampilkan
- **Pantau keterlambatan webhook** - Keterlambatan besar antara occurred_at dan created_at menunjukkan masalah webhook
- **Gunakan untuk dukungan pelanggan** - Timeline acara membantu mendiagnosis masalah pengiriman
- **Lacak pola pengiriman** - Analisis waktu acara untuk kinerja pengangkut
- **Atur notifikasi** - Email otomatis ke pelanggan pada acara kunci (sedang_dikirim, telah_terkirim)
- **Jangan menghapus acara** - Pertahankan riwayat audit lengkap
- **Periksa WebhookLog untuk kegagalan** - Acara yang hilang mungkin menunjukkan kesalahan pemrosesan webhook
- **Data lokasi bervariasi berdasarkan pengangkut** - Beberapa pengangkut menyediakan data lokasi rinci, yang lain minimal
- **Acara pengecualian memerlukan perhatian** - Pantau dan tindak lanjuti acara pengecualian pengiriman
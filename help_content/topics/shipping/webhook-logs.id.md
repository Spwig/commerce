---
title: Log Webhook
---

Log webhook menyediakan jejak audit permanen dari semua permintaan webhook carrier yang masuk—menangkap metode permintaan, URL endpoint, header, payload, status pemrosesan (pending/proses/ gagal), dan respons. Setiap webhook dicatat sebelum diproses untuk memastikan tidak ada kejadian yang terlewat jika pemrosesan gagal. Log memungkinkan debugging masalah integrasi webhook, memantau keandalan API carrier, dan merekonstruksi timeline pengiriman untuk dukungan pelanggan.

Halaman admin hanya baca ini membantu menyelesaikan masalah webhook dan memverifikasi kesehatan integrasi carrier.

## Struktur Log Webhook

Setiap entri log mencatat:

**Detail Permintaan**:
- **Kunci Pemasok**: Carrier yang mengirim webhook (fedex, ups, dhl)
- **Endpoint**: Jalur URL webhook (misalnya, `/webhooks/shipping/fedex/`)
- **Metode**: Metode HTTP (biasanya POST)
- **Header**: Header permintaan (JSON)
- **Payload**: Tubuh permintaan (JSON)

**Pemrosesan**:
- **Status Pemrosesan**: pending, processed, failed
- **Pesan Kesalahan**: Alasan kegagalan (jika status=failed)
- **Respons**: Respons HTTP yang dikirim ke carrier
- **Kode Status Respons**: 200, 400, 500, dll.

**Timestamp**:
- **Diterima Pada**: Kapan webhook tiba
- **Diproses Pada**: Kapan pemrosesan selesai

---

## Nilai Status Pemrosesan

**pending**: Webhook diterima, menunggu pemrosesan
- Normal untuk sejenak setelah penerimaan
- Jika terjebak pending, menunjukkan antrean pemrosesan tertunda

**processed**: Webhook berhasil diproses
- TrackingEvent dibuat
- Pemberitahuan pelanggan dikirim (jika berlaku)
- Respons 200 dikirim ke carrier

**failed**: Pemrosesan webhook gagal
- Periksa error_message untuk alasan
- Penyebab umum: JSON tidak valid, pengiriman tidak dikenal, acara duplikat

---

## Alur Webhook

**Alur Kerja Normal**:
```
1. Carrier memindai paket
   ↓
2. Carrier mengirim POST ke titik akhir webhook Spwig
   ↓
3. Spwig membuat WebhookLog (status=pending)
   ↓
4. Worker latar belakang memproses webhook
   ↓
5. Parse payload JSON
   ↓
6. Cari pengiriman yang cocok (berdasarkan nomor pelacakan)
   ↓
7. Buat TrackingEvent
   ↓
8. Perbarui WebhookLog (status=processed)
   ↓
9. Kirim respons HTTP 200 ke carrier
```

**Skenario Gagal**:
- **JSON Tidak Valid**: Carrier mengirim data yang tidak valid → status=failed, error="kesalahan parsing JSON"
- **Pengiriman Tidak Dikenal**: Nomor pelacakan tidak cocok dengan pengiriman apa pun → status=failed, error="Pengiriman tidak ditemukan"
- **Duplikat**: Acara sudah ada → status=failed, error="Acara duplikat"

---

## Men-debug Gagal Webhook

**Langkah demi Langkah**:

**1. Saring dengan Status=Gagal**
- Navigasikan ke Pengiriman > Log Webhook
- Saring: Status Pemrosesan = "gagal"
- Tinjau kegagalan terbaru

**2. Periksa Pesan Kesalahan**
- Klik entri log
- Baca bidang error_message
- Kesalahan umum:
  - "Pengiriman tidak ditemukan" → ketidakcocokan nomor pelacakan
  - "Kesalahan decode JSON" → Carrier mengirim JSON tidak valid
  - "Field wajib hilang" → Payload kehilangan data yang diharapkan

**3. Periksa Payload**
- Lihat payload JSON mentah
- Verifikasi struktur cocok dengan format yang diharapkan
- Periksa field yang hilang (tracking_id, event_type, dll.)

**4. Verifikasi Pengiriman Ada**
- Ekstrak nomor pelacakan dari payload
- Cari pengiriman dengan nomor pelacakan
- Pastikan pengiriman ada dan menggunakan carrier yang benar

**5. Periksa Konfigurasi Pemasok**
- Pastikan akun pemasok aktif
- Konfirmasi URL titik akhir webhook benar
- Uji kredensial API pemasok

**6. Ulangi Pemrosesan** (jika berlaku)
- Beberapa pemroses webhook mendukung ulang manual
- Perbaiki masalah mendasar terlebih dahulu
- Ulangi webhook yang gagal

---

## Masalah Webhook Umum

**Masalah 1: "Pengiriman tidak ditemukan"**

**Penyebab**: Nomor pelacakan dalam webhook tidak cocok dengan pengiriman apa pun
- Kesalahan ketik saat membuat pengiriman
- Webhook untuk akun berbeda
- Pengiriman dihapus sebelum webhook diterima

**Solusi**:
- Verifikasi ejaan nomor pelacakan
- Periksa apakah carrier pengiriman cocok dengan pemasok webhook
- Buat ulang pengiriman jika diperlukan

---

**Masalah 2: "Kesalahan decode JSON"**

**Penyebab**: Carrier mengirim JSON yang rusak
- Langka, biasanya bug API carrier
- Masalah encoding karakter

**Solusi**:
- Hubungi dukungan carrier dengan payload mentah
- Periksa header untuk encoding karakter
- Verifikasi URL titik akhir di dashboard carrier

---

**Masalah 3: Webhook duplikat**

**Penyebab**: Carrier mengirim acara yang sama beberapa kali
- Logika ulang (carrier tidak menerima respons 200)
- Bug carrier

**Solusi**:
- Sistem menolak duplikat secara otomatis (perilaku normal)
- Verifikasi kode status respons adalah 200
- Jika terus-menerus, hubungi dukungan carrier

---

**Masalah 4: Webhook hilang**

**Penyebab**: Webhook yang diharapkan tidak pernah diterima
- Carrier tidak mengirim (pemindaian terlewat)
- Titik akhir webhook dikonfigurasi salah di dashboard carrier
- Firewall memblokir permintaan

**Solusi**:
- Periksa konfigurasi webhook di dashboard carrier
- Pastikan URL titik akhir publik dan dapat diakses
- Uji titik akhir dengan curl/Postman
- Periksa aturan firewall server

---

## Konfigurasi Titik Akhir Webhook

**URL Webhook Umum**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Setup Dashboard Carrier**:
1. Masuk ke portal pengembangan carrier
2. Navigasikan ke pengaturan webhook
3. Masukkan URL webhook Spwig
4. Pilih acara untuk berlangganan (update pelacakan, pengiriman, pengecualian)
5. Simpan konfigurasi
6. Uji webhook dengan alat uji carrier

**Keamanan**:
- Webhook memerlukan HTTPS (bukan HTTP)
- Beberapa carrier menandatangani permintaan (verifikasi tanda tangan)
- Daftar putih IP (jika carrier menyediakan IP statis)

---

## Memantau Kesehatan Webhook

**Metrik Kunci**:

**Lingkup Keberhasilan**:
```
Lingkup Keberhasilan = (Proses / Total) × 100%

Target: >98%
```

**Waktu Pemrosesan**:
```
Avg Time = Diproses Pada - Diterima Pada

Target: <2 detik
```

**Polanya Gagal**:
- Lonjakan mendadak dalam kegagalan → Perubahan atau kegagalan API carrier
- Konsisten "pengiriman tidak ditemukan" → Masalah sinkronisasi nomor pelacakan
- Semua webhook gagal → Masalah konfigurasi titik akhir

**Strategi Pemantauan**:
- Periksa tingkat kegagalan harian
- Beri peringatan jika tingkat kegagalan >5%
- Tinjau pesan kesalahan mingguan
- Bandingkan dengan halaman status carrier

---

## Retensi Webhook

**Log permanen** - tidak pernah dihapus otomatis

**Mengapa Permanen**:
- Kepatuhan audit
- Dukungan pelanggan (rekonstruksi timeline pengiriman)
- Penyelesaian sengketa
- Debugging webhook

**Penyimpanan**: Log disimpan secara efisien (JSON terkompresi)

---

## Tips

- **Webhook adalah log audit permanen** - Jangan pernah menghapus, bahkan jika diproses berhasil
- **Periksa webhook yang gagal setiap hari** - Tangkap masalah integrasi sejak dini
- **Pantau keterlambatan pemrosesan** - Keterlambatan panjang menunjukkan masalah kinerja
- **Simpan payload mentah** - Esensial untuk debugging perubahan API carrier
- **Uji konfigurasi titik akhir** - Gunakan alat uji carrier untuk memverifikasi pengaturan
- **Aktifkan tanda tangan webhook** - Verifikasi permintaan benar-benar dari carrier
- **Daftar putih IP carrier** - Jika carrier menyediakan rentang IP statis
- **Atur peringatan** - Beri tahu saat tingkat kegagalan melebihi ambang batas
- **Bandingkan dengan status carrier** - Celah webhook mungkin menunjukkan kegagalan carrier
- **Dokumentasikan format payload carrier** - Membantu saat carrier memperbarui API
- **Jaga URL webhook stabil** - Mengubah URL memerlukan pembaruan di dashboard carrier

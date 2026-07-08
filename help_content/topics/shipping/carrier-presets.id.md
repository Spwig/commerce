---
title: Preset Carrier
---

Preset carrier mendefinisikan pengiriman manual (DHL, FedEx, UPS, pengiriman khusus) untuk pengiriman yang dibuat tanpa integrasi API—setiap preset menyediakan logo carrier, template URL pelacakan, dan pengaturan tampilan. Preset sistem (DHL, FedEx, UPS, USPS) sudah dikonfigurasi sebelumnya dan tidak dapat dihapus, sedangkan preset khusus memungkinkan pedagang untuk menambahkan pengiriman regional atau spesialis. Preset terhubung dengan pengiriman manual di mana pedagang memasukkan nomor pelacakan secara manual alih-alih membeli label melalui API penyedia.

Gunakan preset carrier saat membuat pengiriman manual atau ketika Anda ingin tautan pelacakan tanpa integrasi API penuh.

## Preset Sistem vs Preset Khusus

**Preset Sistem** (Pre-installed):
- DHL, FedEx, UPS, USPS, Royal Mail, Canada Post, Australia Post
- Tidak dapat dihapus (is_system=True)
- Dapat mengganti URL pelacakan atau logo
- Template URL pelacakan default disediakan

**Preset Khusus** (Dibuat oleh pedagang):
- Pengiriman regional (OnTrac, LaserShip, pos regional)
- Pengiriman spesialis (freight, pengiriman white-glove)
- Dapat diedit atau dihapus
- Memerlukan template URL pelacakan manual

---

## Konfigurasi Preset Carrier

Setiap preset mendefinisikan:

**Pengaturan Dasar**:
- **Nama**: Nama tampilan carrier (contoh: "DHL Express", "Local Courier")
- **Kode**: Identifier internal (contoh: "dhl", "local_courier")
- **Logo**: Gambar logo carrier (opsional, menggunakan ikon jika tidak disediakan)
- **Ikon**: Ikon FontAwesome sebagai pengganti (contoh: "fa-truck")
- **Aktif**: Toggle visibilitas

**Pengaturan Pelacakan**:
- **Template URL Pelacakan**: Pola URL dengan placeholder {tracking_id}
- **URL Pelacakan Pengganti**: URL khusus (menggantikan template default)

**Pengaturan Sistem** (hanya untuk preset sistem):
- **Adalah Sistem**: Tidak dapat dihapus
- **Adalah Default**: Satu default per jenis carrier

---

## Template URL Pelacakan

URL pelacakan menggunakan placeholder {tracking_id}:

**Contoh**:

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

Khusus: `https://track.localcourier.com/tracking/{tracking_id}`

**Bagaimana Cara Kerjanya**:
1. Pedagang membuat pengiriman dengan nomor pelacakan "1234567890"
2. Sistem mengganti {tracking_id} dengan nomor aktual
3. Pelanggan mengklik tautan pelacakan → dialihkan ke situs carrier
4. Hasil: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## Membuat Preset Carrier Khusus

**Langkah demi Langkah**:

1. Navigasikan ke Pengaturan > Pengiriman > Carrier Preset
2. Klik "Tambahkan Preset Carrier"
3. Masukkan nama (contoh: "OnTrac")
4. Masukkan kode (slug: "ontrac")
5. Opsional: Unggah gambar logo
6. Pilih ikon (fa-truck, fa-shipping-fast, dll.)
7. Masukkan template URL pelacakan dengan {tracking_id}
8. Toggle aktif = Ya
9. Simpan

**Contoh - OnTrac**:
```
Nama: OnTrac
Kode: ontrac
URL Pelacakan: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
Ikon: fa-truck
Aktif: Ya
```

---

## Mengganti URL Pelacakan Preset Sistem

Preset sistem dapat memiliki pengganti URL pelacakan:

**Kasus Penggunaan**: Akun carrier Anda memiliki portal pelacakan khusus

**Cara Mengganti**:
1. Edit preset sistem (contoh: DHL)
2. Masukkan URL pengganti di bidang "URL Pelacakan Pengganti"
3. Pengganti akan mendahului template default
4. Simpan

**Contoh**:
```
Sistem: DHL
URL Default: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
URL Pengganti: https://track.dhl.com/special-account/{tracking_id}
Hasil: URL Pengganti digunakan untuk semua pengiriman DHL
```

---

## Logo Carrier

**Panduan Logo**:
- Format: PNG atau SVG (SVG disarankan untuk skalabilitas)
- Ukuran: Rekomendasi 200×60px
- Latar belakang: Transparan atau putih
- Warna: Branding penuh warna carrier

**Ikon Pengganti**:
Jika tidak ada logo yang diunggah, sistem menampilkan ikon FontAwesome:
- fa-truck (default)
- fa-shipping-fast (ekspres)
- fa-plane (freight udara)
- fa-box (kemasan)

---

## Menggunakan Preset Carrier dalam Pengiriman

Ketika membuat pengiriman manual:

1. Pesanan > Detail Pesanan > Buat Pengiriman
2. Pilih mode "Pengiriman Manual"
3. Pilih carrier dari dropdown preset
4. Masukkan nomor pelacakan
5. Opsional: Ganti URL pelacakan untuk pengiriman ini
6. Simpan

**Tampilan Pengiriman**:
- Logo carrier ditampilkan (atau ikon)
- Nomor pelacakan ditampilkan
- Tautan pelacakan yang dapat diklik (menggunakan template URL preset)

---

## Carrier Default

Satu preset dapat diatur sebagai default per sistem:

**Kasus Penggunaan**: Carrier yang paling umum digunakan secara otomatis dipilih saat membuat pengiriman

**Cara Menetapkan**:
1. Edit preset carrier
2. Centang "Adalah Default"
3. Simpan
4. Default sebelumnya (jika ada) secara otomatis dibatalkan

**Hanya satu default yang diperbolehkan** - menetapkan default baru menghapus status default sebelumnya.

---

## Tips

- **Gunakan nama yang deskriptif** - "DHL Express" lebih baik daripada "DHL"
- **Uji URL pelacakan** - Verifikasi template bekerja dengan nomor pelacakan nyata
- **Unggah logo carrier** - Tampilan profesional dalam email pelanggan
- **Jangan menghapus preset sistem** - Mereka sudah dikonfigurasi dengan benar
- **Gunakan pengganti secara terbatas** - Hanya ketika carrier mengubah sistem pelacakan
- **Tetapkan default untuk carrier utama** - Menghemat waktu saat membuat pengiriman
- **Jaga preset aktif** - Hanya nonaktifkan jika carrier berhenti beroperasi
- **Dokumentasikan carrier khusus** - Tambahkan catatan tentang carrier regional
---
title: Mengelola Terminal POS
---

Mengelola terminal POS adalah fondasi operasi ritel Anda. Setiap terminal mewakili perangkat fisik (tablet, komputer, atau perangkat keras POS khusus) di mana staf memproses penjualan. Konfigurasikan terminal dengan penugasan gudang, otorisasi staf, integrasi perangkat keras, dan pengaturan sinkronisasi offline. Pantau kesehatan terminal dengan pelacakan detak jantung secara real-time dan bongkar terminal secara jarak jauh ketika terjadi masalah. Manajemen terminal yang tepat memastikan operasi toko yang lancar dan mencegah konflik konfigurasi di seluruh lokasi.

Navigasikan ke **POS > Terminal** untuk mendaftarkan terminal baru, melihat status online/offline, dan mengelola semua pengaturan terminal.

![Daftar Terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Tampilan Daftar Terminal

Daftar terminal menampilkan semua terminal yang terdaftar dengan informasi status kunci:

**Nama Terminal** - Label deskriptif untuk terminal (misalnya, "Checkout 1", "Main Register", "Mobile Terminal")

**UUID** - Identifikasi unik yang dihasilkan secara otomatis saat pembuatan (digunakan secara internal untuk identifikasi perangkat)

**Gudang** - Lokasi fisik yang ditugaskan ke terminal ini (menentukan ketersediaan stok dan atribusi pesanan)

**Status Online** - Indikator langsung yang menunjukkan apakah terminal saat ini terhubung:
- **Titik hijau** - Online (detak jantung diterima dalam 5 menit terakhir)
- **Titik merah** - Offline (tidak ada detak jantung selama >5 menit)
- **Titik abu-abu** - Pernah dipasangkan (terminal dibuat tetapi perangkat tidak pernah terhubung)

**Terakhir Detak Jantung** - Tanda waktu dari ping terbaru dari terminal (diperbarui setiap 5 menit saat online)

**Kode Pasangan** - Kode alfanumerik 8 karakter yang digunakan untuk pasangan perangkat awal (tersembunyi setelah penggunaan pertama)

**Pengguna yang Ditetapkan** - Jumlah staf yang diizinkan menggunakan terminal ini

## Membuat Terminal Baru

Klik **+ Tambahkan Terminal** untuk mendaftarkan perangkat POS baru:

![Formulir Tambah Terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Konfigurasi Dasar

**Nama Terminal** - Pilih nama deskriptif yang menunjukkan:
- Lokasi fisik: "Register Masuk Utara"
- Fungsi: "Terminal Meja Pengembalian"
- Urutan: "Checkout 1", "Checkout 2", "Checkout 3"

Nama membantu staf mengidentifikasi terminal selama penugasan shift dan pemecahan masalah. Gunakan konvensi penamaan yang konsisten di semua lokasi.

**Gudang** - **DIPERLUKAN** - Pilih gudang yang digunakan terminal ini:
- Menentukan stok mana yang tersedia untuk dijual
- Pesanan yang ditempatkan di terminal ini diatribusikan ke gudang ini
- Pemesanan stok memeriksa ketersediaan di gudang yang ditugaskan
- **Tidak dapat memproses penjualan tanpa penugasan gudang**

Jika Anda memiliki beberapa lokasi ritel, buat gudang terpisah untuk setiap lokasi dan tetapkan terminal sesuai.

**Apakah Aktif** - Toggle untuk mengaktifkan/menonaktifkan terminal tanpa menghapus konfigurasi:
- Terminal tidak aktif tidak dapat dipasangkan
- Sesi yang ada di terminal tidak aktif segera berakhir
- Gunakan untuk sementara menonaktifkan terminal yang dicuri atau rusak

### Penugasan Staf

**Pengguna yang Ditetapkan** - Pilih staf mana yang dapat mengakses terminal ini:
- Hanya pengguna yang ditetapkan yang dapat masuk ke terminal
- Pengguna harus juga memiliki izin POS di peran staf mereka
- Menetapkan nol pengguna secara efektif mengunci terminal
- Pola umum: Tetapkan semua staf toko ke semua terminal toko

**Contoh Penggunaan**:
- **Toko Umum**: Tetapkan semua staf ke semua terminal (setiap kasir dapat bekerja di register mana pun)
- **Toko Departemen**: Tetapkan staf departemen tertentu ke terminal departemen
- **Multi-Lokasi**: Tetapkan staf lokasi tertentu ke terminal lokasi
- **Manajer**: Tetapkan manajemen ke semua terminal untuk akses pengawasan

Pengguna tanpa penugasan terminal melihat kesalahan "Tidak diizinkan untuk terminal ini" saat mencoba masuk.

### Konfigurasi Perangkat Keras

Bidang **Konfigurasi Perangkat Keras** adalah struktur JSON yang mendefinisikan perangkat peripheral:

**Printer Termal**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**Scanner Kode Batang USB**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Laci Kasir** (terhubung ke printer):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Contoh Lengkap**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Biarkan kosong jika terminal tidak memiliki perangkat peripheral (cocok untuk terminal mobile atau tablet tanpa printer/scanner).

### Pengaturan Cache Offline

Konfigurasikan seberapa banyak data yang dicache terminal untuk operasi offline:

**Hari Sinkronisasi Pesanan** (7-30 hari, default: 14):
- Jumlah hari pesanan terbaru yang dicache secara lokal
- Nilai yang lebih tinggi = akses data historis yang lebih baik secara offline
- Nilai yang lebih rendah = sinkronisasi yang lebih cepat, penggunaan penyimpanan yang lebih sedikit
- **Rekomendasi**: 7 hari untuk terminal dengan volume tinggi, 14 hari untuk penggunaan normal, 30 hari untuk operasi audit yang berat

**Batas Sinkronisasi Pesanan** (200-1000 pesanan, default: 500):
- Maksimum jumlah pesanan yang dicache tanpa memperhatikan rentang tanggal
- Mencegah penggunaan penyimpanan berlebihan pada terminal dengan volume tinggi
- **Rekomendasi**: 200 untuk tablet dengan penyimpanan terbatas, 500 untuk terminal standar, 1000 untuk perangkat POS khusus

**Kompromi**:
- **Pengaturan yang lebih tinggi**: Akses offline yang lebih baik ke data historis, sinkronisasi awal yang lebih lambat, penggunaan penyimpanan yang lebih besar
- **Pengaturan yang lebih rendah**: Sinkronisasi yang lebih cepat, penyimpanan yang lebih sedikit, sejarah offline yang terbatas

Terminal mengunduh X pesanan terbaru (dalam Y hari) pada setiap siklus sinkronisasi. Jika terminal memproses 50 pesanan/hari dan sync_days adalah 14, harapkan ~700 pesanan yang dicache (mungkin mencapai batas sync_limit).

## Alur Kerja Pasangan Terminal

Setelah membuat terminal, pasangkan perangkat fisik:

1. **Buat Kode Pasangan** - Dibuat secara otomatis saat Anda menyimpan terminal (8 karakter alfanumerik)

2. **Catat Kode** - Ditampilkan dalam daftar terminal dan tampilan detail (kadaluarsa setelah pasangan pertama yang berhasil)

3. **Navigasikan ke Perangkat Terminal** - Di perangkat fisik (tablet/komputer), buka browser dan pergi ke: `https://yourstore.com/pos/`

4. **Masukkan Kode Pasangan** - Ketikkan kode 8 karakter saat diminta

5. **Terminal Mendownload Konfigurasi** - Perangkat menerima:
   - Penugasan gudang
   - Konfigurasi perangkat keras (printer, scanner, laci)
   - Pengaturan cache offline
   - Daftar pengguna yang ditetapkan
   - Sinkronisasi katalog produk awal

6. **Prompt Masuk Muncul** - Terminal menampilkan layar masuk untuk pengguna yang ditetapkan

7. **Staf Masuk** - Masukkan kredensial untuk pengguna yang ditetapkan ke terminal ini

8. **Sinkronisasi Awal Selesai** - Terminal mengunduh:
   - Pesanan terbaru (sesuai sync_days dan sync_limit)
   - Katalog produk lengkap untuk gudang yang ditetapkan
   - Basis data pelanggan
   - Konfigurasi promosi

9. **Terminal Siap** - Tampilan "Siap untuk Menjual" muncul dengan bilah pencarian

10. **Kode Pasangan Digunakan** - Kode dihapus dari admin; buat kode baru jika pasangan ulang diperlukan

**Regenerasi Kode Pasangan**: Jika Anda perlu memasangkan ulang terminal (reset perangkat, cache browser dihapus, perangkat keras baru), gunakan aksi admin **Regenerate Pairing Code**. Ini membatalkan kode lama dan membuat kode baru.

## Memantau Status Terminal

### Sistem Detak Jantung

Terminal memancarkan sinyal detak jantung ke server setiap **5 menit** yang berisi:
- UUID terminal
- Tanda waktu saat ini
- Jumlah pengguna online
- Tanda waktu sinkronisasi terakhir
- Status Pekerja Layanan

**Indikator Status Online**:
- **Hijau** - Detak jantung diterima dalam 5 menit terakhir (terminal online dan beroperasi)
- **Merah** - Tidak ada detak jantung selama >5 menit (terminal offline atau terputus)
- **Abu-abu** - Terminal tidak pernah dipasangkan (tidak pernah menerima detak jantung)

**Penggunaan Kasus**:
- **Buka Harian**: Periksa semua terminal online sebelum toko dibuka
- **Pemecahan Masalah**: Identifikasi terminal yang mengalami masalah koneksi
- **Audit**: Verifikasi terminal aktif selama jam operasional

### Tanda Waktu Detak Jantung Terakhir

Menampilkan tanggal/waktu persis dari detak jantung terbaru. Gunakan ini untuk:
- Menentukan seberapa lama terminal telah offline
- Mengidentifikasi pola (misalnya, terminal offline setiap malam saat penutupan)
- Memverifikasi frekuensi sinkronisasi (seharusnya diperbarui setiap ~5 menit saat online)

## Fitur Buka Kunci Jarak Jauh

Ketika terminal menjadi tidak responsif atau terjebak di layar (kemacetan perangkat lunak, masalah timeout sesi, kemacetan browser), gunakan aksi admin **Buka Kunci Jarak Jauh**:

**Bagaimana Cara Kerjanya**:
1. Pilih terminal yang bermasalah dalam daftar admin
2. Pilih **Buka Kunci Jarak Jauh** dari dropdown aksi admin
3. Konfirmasi aksi
4. Server mengirimkan sinyal buka kunci melalui respons detak jantung
5. Terminal menerima sinyal pada siklus detak jantung berikutnya (<5 menit)
6. Terminal memaksa keluar pengguna saat ini dan kembali ke layar masuk

**Kapan Menggunakan**:
- Terminal terjebak di layar transaksi
- Staf tidak bisa keluar (tombol keluar tidak merespons)
- Sesi tampak aktif tetapi terminal tidak responsif
- Browser crash tetapi cookie sesi tetap ada

**Penting**: Buka kunci jarak jauh TIDAK merestart perangkat atau browser-nya hanya memaksa keluar dan membersihkan sesi. Jika terminal sepenuhnya terjebak, staf mungkin perlu merestart browser atau perangkat secara manual.

## Mengedit Konfigurasi Terminal

Klik terminal dalam daftar untuk mengedit konfigurasinya:

![Formulir Edit Terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**Aman untuk Mengubah Saat Terminal Online**:
- Nama terminal
- Pengguna yang ditetapkan
- Konfigurasi perangkat keras (berlaku setelah terminal merestart aplikasi)
- Pengaturan cache offline (berlaku pada sinkronisasi berikutnya)

**Memerlukan Pasangan Ulang**:
- Penugasan gudang (mengubah gudang memerlukan pasangan ulang untuk sinkronisasi inventaris baru)

**Tidak Bisa Diubah**:
- UUID (identifikasi unik yang tidak dapat diubah)

Perubahan pada kebanyakan pengaturan diterapkan pada siklus detak jantung/sinkronisasi berikutnya. Perubahan konfigurasi perangkat keras memerlukan staf untuk menutup dan membuka ulang aplikasi POS (atau memuat ulang browser).

## Menyelesaikan Masalah Umum

**Terminal Menampilkan "Tidak Diizinkan" Saat Masuk**:
- Verifikasi pengguna berada dalam daftar **Pengguna yang Ditetapkan** untuk terminal ini
- Verifikasi pengguna memiliki izin POS di **Staf & Izin > Peran**
- Periksa terminal ditandai **Apakah Aktif**

**Terminal Tidak Bisa Dipasangkan (Kode Tidak Valid)**:
- Kode pasangan kadaluarsa setelah penggunaan pertama—regenerasi jika diperlukan
- Kode bersifat sensitif huruf besar/kecil—verifikasi kapitalisasi
- Periksa terminal ditandai **Apakah Aktif**

**Terminal Menampilkan Offline (Titik Merah)**:
- Verifikasi perangkat memiliki koneksi internet
- Periksa terminal sebenarnya sedang berjalan (browser terbuka ke URL /pos/)
- Pastikan firewall tidak memblokir permintaan detak jantung
- Tunggu 5 menit untuk siklus detak jantung berikutnya

**Terminal Lambat Sinkronisasi**:
- Kurangi **Hari Sinkronisasi Pesanan** dari 30 menjadi 7
- Kurangi **Batas Sinkronisasi Pesanan** dari 1000 menjadi 200
- Periksa kecepatan jaringan di lokasi terminal
- Verifikasi server tidak sedang dalam beban berat

**Printer Tidak Berfungsi**:
- Verifikasi IP dan port printer di **Konfigurasi Perangkat Keras**
- Uji koneksi printer dari perangkat terminal (ping alamat IP)
- Periksa printer kompatibel dengan ESC/POS
- Verifikasi printer dalam kondisi menyala dan online

## Tips

- **Konvensi penamaan penting** - Gunakan penamaan konsisten (lokasi + nomor) untuk menyederhanakan manajemen pada skala besar
- **Selalu tetapkan gudang sebelum pasangan** - Terminal tidak dapat memproses penjualan tanpa penugasan gudang
- **Uji konfigurasi perangkat keras sebelum diterapkan** - Cetak struk uji untuk memverifikasi integrasi printer/laci
- **Pantau detak jantung harian** - Tetapkan rutinitas untuk memeriksa semua terminal online saat toko dibuka
- **Kurangi batas sinkronisasi untuk terminal mobile** - Tablet dan ponsel mendapat manfaat dari sync_days: 7, sync_limit: 200
- **Gunakan buka kunci jarak jauh secara jarang** - Keluar paksa mengganggu transaksi aktif; konfirmasi terminal benar-benar terjebak terlebih dahulu
- **Dokumentasikan kode pasangan** - Catat kode sebelum menempatkan terminal di lantai toko (jika setup memakan waktu lebih lama dari yang diperkirakan)
- **Tetapkan manajer ke semua terminal** - Pastikan supervisor dapat mengakses register mana pun untuk void, pengembalian, dan pemecahan masalah
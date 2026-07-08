---
title: Pemrosesan Pembayaran
---

Pemrosesan pembayaran memungkinkan penerimaan kartu kredit dan debit di terminal POS Anda. Stripe Terminal adalah penyedia utama yang didukung, menawarkan pembaca kartu modern (S700, WisePOS E, P400), tarif pemrosesan kompetitif, dan integrasi yang mulus. Konfigurasikan akun penyedia dengan kredensial API, pantau status koneksi secara real-time, dan kelola beberapa penyedia jika beroperasi di wilayah berbeda. Sistem penyedia dapat diperluas—prosesor pembayaran tambahan dapat diintegrasikan melalui kerangka kerja penyedia jika Stripe Terminal tidak beroperasi di pasar Anda.

Gunakan penyedia pembayaran untuk menerima pembayaran kartu secara aman, melacak status pemrosesan pembayaran, dan mengelola penugasan pembaca di seluruh terminal.

![Daftar Penyedia Pembayaran](/static/core/admin/img/help/payment-terminal-providers/provider-list.webp)

## Ringkasan Penyedia Pembayaran

Penyedia pembayaran adalah layanan pihak ketiga yang memproses pembayaran kartu atas nama bisnis Anda:

**Tanggung Jawab Penyedia**:
- Membuat transaksi kartu secara real-time
- Berkomunikasi dengan pembaca kartu fisik
- Menangani keamanan pembayaran (kepatuhan PCI, enkripsi)
- Memindahkan dana ke rekening bank Anda (penyelesaian)
- Menyediakan pelaporan transaksi dan manajemen sengketa

**Peran Spwig**:
- Mengarahkan permintaan pembayaran ke penyedia yang dikonfigurasikan
- Menyimpan kredensial penyedia yang dienkripsi
- Memantau status koneksi
- Menghubungkan pembaca dengan terminal
- Merekam hasil pembayaran dalam pesanan

## Stripe Terminal (Penyedia Utama)

Stripe Terminal adalah penyedia pembayaran yang disarankan untuk sebagian besar pedagang:

**Fitur**:
- Pembaca kartu chip EMV modern
- Dukungan pembayaran tanpa kontak (NFC) (Apple Pay, Google Pay, kartu tap-to-pay)
- Manajemen sengketa terintegrasi
- Otorisasi real-time
- API yang ramah pengembang
- Tersedia di 40+ negara

**Harga** (sebagai of 2024, verifikasi tarif saat ini):
- Biaya transaksi: 2,7% + $0,05 per transaksi langsung (AS)
- Tidak ada biaya bulanan, tidak ada biaya setup, tidak ada biaya kepatuhan PCI
- Perangkat pembaca kartu: Pembelian sekali saja ($59-$299 tergantung model)

**Wilayah yang Didukung**:
- Amerika Serikat, Kanada, Inggris Raya, Uni Eropa, Australia, Singapura, dan lainnya
- Periksa ketersediaan Stripe: https://stripe.com/terminal

**Pembaca yang Didukung**:
- BBPOS WisePOS E (terminal Android all-in-one)
- Pembaca Stripe S700 (pembaca meja)
- Verifone P400 (pembaca lama, masih didukung)

## Mengatur Stripe Terminal

**Langkah 1: Membuat Akun Stripe**
- Daftar di stripe.com
- Lengkapi verifikasi bisnis (rekening bank, ID pajak)
- Aktifkan pembayaran

**Langkah 2: Mengaktifkan Stripe Terminal**
- Di Dashboard Stripe, navigasikan ke **Produk > Terminal**
- Klik **Mulai**
- Terima ketentuan layanan Terminal

**Langkah 3: Membuat Lokasi**
- Stripe Terminal memerlukan "Lokasi" yang merepresentasikan situs ritel fisik Anda
- Navigasikan ke **Terminal > Lokasi**
- Klik **Buat Lokasi**
- Masukkan alamat toko dan detail
- Simpan ID lokasi (terlihat seperti `tml_1ABC123...`)

**Langkah 4: Membuat Kunci API**
- Navigasikan ke **Pengembang > Kunci API**
- Temukan **Kunci Rahasia** Anda (mulai dengan `sk_live_...` untuk produksi, `sk_test_...` untuk pengujian)
- Salin kunci rahasia (jangan bagikan secara publik)

**Langkah 5: Mengonfigurasi di Spwig**
- Navigasikan ke **POS > Penyedia Pembayaran**
- Klik **+ Tambah Penyedia Pembayaran**
- Pilih **Penyedia**: "Stripe Terminal"
- Masukkan **Kunci Rahasia API** (dari Langkah 4)
- Masukkan **ID Lokasi** (dari Langkah 3)
- Simpan

**Langkah 6: Menguji Koneksi**
- Setelah disimpan, status penyedia harus berubah menjadi "Terhubung" (hijau)
- Jika status menunjukkan "Kesalahan" (merah), verifikasi kunci API dan ID lokasi
- Periksa pesan kesalahan di tampilan detail penyedia

![Formulir Tambah Penyedia Pembayaran](/static/core/admin/img/help/payment-terminal-providers/provider-add-form.webp)

## Bidang Konfigurasi Penyedia

**Kunci Penyedia** - Pilih prosesor pembayaran:
- **stripe_terminal** - Stripe Terminal (disarankan)
- **manual** - Masukan pembayaran manual (hanya untuk pengujian, tanpa pemrosesan sebenarnya)
- Penyedia tambahan mungkin muncul jika diinstal melalui sistem komponen

**Kredensial (Dienkripsi)** - Struktur JSON yang berisi kredensial API:
- Dienkripsi secara otomatis sebelum disimpan
- Tidak pernah terlihat dalam teks biasa setelah disimpan
- Contoh struktur (Stripe Terminal):
```json
{
  "api_key": "sk_live_ABC123...",
  "location_id": "tml_1ABC123..."
}
```

**Pengaturan Penyedia** - Konfigurasi tambahan (spesifik penyedia):
- Deskripsi pernyataan (muncul di pernyataan kartu kredit pelanggan)
- Otorisasi otomatis (otorisasi pembayaran secara langsung vs penangkapan manual)
- Override mata uang (jika akun penyedia menggunakan mata uang berbeda dari toko)

**Status Koneksi** - Indikator status real-time:
- **Terhubung** (hijau) - Penyedia dapat dijangkau dan dikonfigurasikan dengan benar
- **Kesalahan** (merah) - Koneksi gagal atau kredensial tidak valid
- **Tidak diketahui** (abu-abu) - Belum diuji (segera setelah pembuatan)

**Terakhir Dites** - Tanda waktu dari uji koneksi terbaru
- Diperbarui secara otomatis saat transaksi diproses
- Trigger uji secara manual melalui tindakan admin **Uji Koneksi**

## Memantau Status Koneksi

Sistem memantau koneksi penyedia untuk memperingatkan Anda tentang masalah sebelum pelanggan mencoba pembayaran:

**Uji Otomatis**:
- Setiap transaksi pembayaran memicu uji koneksi (dengan keharusan)
- Tugas latar belakang menguji koneksi setiap 6 jam (pemantauan preventif)

**Arti Status**:

**Terhubung** - API penyedia dapat dijangkau, kredensial valid, siap memproses pembayaran

**Kesalahan** - Penyebab umum:
- Kunci API tidak valid (dibatalkan, kedaluwarsa, atau salah)
- ID lokasi tidak valid (lokasi dihapus di Stripe, ID yang salah dimasukkan)
- Masalah koneksi jaringan (firewall memblokir API Stripe)
- Gangguan layanan Stripe (langka)

**Tidak diketahui** - Penyedia belum pernah diuji (akun baru yang menunggu transaksi pertama)

**Menyelesaikan Status Kesalahan**:
1. Periksa pesan kesalahan di tampilan detail penyedia (menjelaskan masalah spesifik)
2. Verifikasi kunci API masih valid di Dashboard Stripe
3. Verifikasi ID lokasi masih ada di Dashboard Stripe
4. Uji koneksi secara manual melalui tindakan admin **Uji Koneksi**
5. Perbarui kredensial jika diperlukan

![Detail Penyedia Pembayaran](/static/core/admin/img/help/payment-terminal-providers/provider-detail.webp)

## Perbandingan Pembaca Kartu yang Didukung

Stripe Terminal menawarkan beberapa opsi perangkat keras pembaca:

| Model | Jenis | Metode Pembayaran | Tampilan | Terbaik Untuk | Harga |
|-------|------|-----------------|---------|----------|-------|
| **WisePOS E** | All-in-one | Chip EMV, NFC, swipe | Layar sentuh berwarna 5" | POS ritel yang lengkap | ~$299 |
| **S700** | Meja | Chip EMV, NFC, swipe | LCD monokrom | Checkout ritel standar | ~$249 |
| **P400** | Meja | Chip EMV, NFC, swipe | LCD monokrom | Penggunaan lama | ~$299 |

**Keunggulan WisePOS E**:
- Berbasis Android (menjalankan aplikasi, dapat menampilkan konten kustom)
- Layar sentuh berwarna (UX yang lebih baik untuk promp tip, penangkapan tanda tangan)
- Cetak struk terintegrasi (opsional)
- Kecepatan transaksi tercepat

**Keunggulan S700**:
- Biaya lebih rendah daripada WisePOS E
- Kaki yang lebih kecil
- Desain tahan percikan air

**P400** (model lama):
- Masih didukung tetapi tidak disarankan untuk penggunaan baru
- Proses chip kartu lebih lambat daripada S700/WisePOS E

Semua pembaca terhubung ke POS Spwig melalui API Stripe Terminal (tidak diperlukan koneksi USB/Bluetooth langsung ke perangkat POS).

## Pertimbangan Keamanan

**Enkripsi Kredensial**:
- Semua kredensial penyedia dienkripsi dalam penyimpanan database
- Enkripsi menggunakan kunci rahasia aplikasi (didefinisikan dalam pengaturan aplikasi)
- Kredensial tidak pernah muncul dalam log atau pesan kesalahan

**Izin Kunci API**:
- Gunakan **kunci API terbatas** dalam produksi (batasi izin hanya ke Terminal)
- Jangan gunakan kunci rahasia tidak terbatas (akses lebih luas dari yang diperlukan = risiko keamanan)
- Di Dashboard Stripe, buat kunci terbatas dengan hanya **Terminal** izin

**Kepatuhan PCI**:
- Stripe Terminal menangani kepatuhan PCI (data kartu tidak menyentuh server Spwig)
- Nomor kartu diproses sepenuhnya di perangkat keras pembaca → server Stripe → jaringan kartu
- Spwig hanya menyimpan hasil pembayaran (disetujui/ditolak), tidak pernah detail kartu

**Rotasi Kunci**:
- Rotasi kunci API setiap tahun sebagai praktik keamanan terbaik
- Saat merotasi, perbarui kredensial dalam konfigurasi penyedia
- Kunci lama dapat dibatalkan di Dashboard Stripe setelah memastikan kunci baru berfungsi

## Penyedia Multi

Beberapa pedagang memerlukan akun penyedia multi:

**Operasi Multi-Mata Uang**:
- Toko AS menggunakan akun Stripe AS (memproses USD)
- Toko Eropa menggunakan akun Stripe EU (memproses EUR)
- Konfigurasikan penyedia terpisah per mata uang

**Penyedia Cadangan**:
- Penyedia utama (Stripe Terminal)
- Penyedia cadangan (masukan manual) saat pembaca bermasalah
- Kasir memilih penyedia saat memulai pembayaran

**Pengujian vs Produksi**:
- Gunakan penyedia pengujian dengan kunci API `sk_test_...`
- Gunakan penyedia produksi dengan kunci API `sk_live_...`
- Ubah penyedia setelah fase pengujian

## Menyelesaikan Masalah Umum

**Masalah 1: Status menunjukkan "Kesalahan" dengan pesan "Kunci API tidak valid"**
- **Penyebab**: Kunci API dibatalkan atau salah dikopi
- **Solusi**: Buat kunci API baru di Dashboard Stripe, perbarui kredensial penyedia, uji koneksi

**Masalah 2: Pembaca tidak ditemukan saat pembayaran**
- **Penyebab**: Pembaca tidak terdaftar ke lokasi penyedia
- **Solusi**: Di Dashboard Stripe, verifikasi pembaca terdaftar ke lokasi ID yang sama yang digunakan dalam konfigurasi penyedia

**Masalah 3: Pembayaran ditolak meskipun kartu valid**
- **Penyebab**: Akun Stripe belum sepenuhnya diaktifkan (verifikasi sedang berlangsung)
- **Solusi**: Lengkapi verifikasi bisnis di Dashboard Stripe (rekening bank, ID pajak)

**Masalah 4: Status koneksi menunjukkan "Tidak diketahui" dan tidak pernah diperbarui**
- **Penyebab**: Penyedia belum pernah diuji (tidak ada transaksi yang dicoba)
- **Solusi**: Gunakan tindakan admin **Uji Koneksi** untuk memicu uji koneksi secara manual

## Tips

- **Mode pengujian sebelum produksi** - Gunakan kunci API pengujian Stripe (`sk_test_...`) untuk pengaturan awal dan pengujian
- **Satu penyedia per mata uang** - Jangan coba memproses EUR dengan akun Stripe berbasis USD; buat penyedia terpisah
- **Pantau status koneksi setiap minggu** - Pemantauan proaktif mencegah kegagalan pembayaran di kasir
- **Batasi izin kunci API** - Batasi kunci API Stripe hanya ke izin Terminal (prinsip akses minimum)
- **Dokumentasikan ID lokasi** - Catat ID Stripe yang sesuai dengan toko fisik mana
- **Uji penugasan pembaca** - Setelah pengaturan penyedia, uji pembayaran dengan pembaca kartu sebenarnya untuk memverifikasi alur end-to-end
- **Perbarui kontak Stripe** - Pastikan informasi kontak bisnis di Stripe sesuai dengan saat ini (penting untuk sengketa, kepatuhan)
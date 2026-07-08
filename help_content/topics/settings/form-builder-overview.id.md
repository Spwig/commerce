---
title: Panduan Form Builder
---

Form Builder membuat formulir kustom untuk pengumpulan data—formulir kontak, survei, aplikasi, pendaftaran, dan lainnya. Bangun formulir secara visual dengan drag-and-drop field, konfigurasikan aturan validasi, aktifkan alur kerja multi-langkah, dan kumpulkan respons dengan analitik terperinci. Formulir terintegrasi secara mulus dengan elemen Page Builder, dapat disisipkan di mana saja di situs Anda. Semua pengajuan disimpan di database dengan metadata lengkap (alamat IP, browser, waktu penyelesaian) untuk analisis dan ekspor.

Gunakan Form Builder ketika Anda perlu mengumpulkan data terstruktur dari pelanggan, baik informasi kontak sederhana atau aplikasi multi-halaman yang kompleks.

## Apa itu Form Builder?

Form Builder adalah alat drag-and-drop visual untuk membuat formulir kustom tanpa kode:

**Jenis Formulir yang Didukung**:
- Formulir kontak (nama, email, pesan)
- Survei pelanggan (peringkat, umpan balik, NPS)
- Pendaftaran produk (garansi, dukungan)
- Aplikasi pekerjaan (unggah CV, multi-langkah)
- Pendaftaran acara (informasi peserta, preferensi)
- Permintaan layanan (persyaratan rinci)
- Pendaftaran newsletter (dengan kotak centang untuk preferensi)

**Fitur Utama**:
- **22 jenis field** - Teks, email, telepon, unggah file, peringkat, pemilih produk, dan lainnya
- **Formulir multi-langkah** - Pecah formulir panjang menjadi langkah logis dengan pelacakan kemajuan
- **Logika kondisional** - Tampilkan/sembunyikan field berdasarkan respons pengguna
- **Aturan validasi** - Field wajib, panjang min/max, pola regex kustom
- **Proteksi spam** - Field honeypot atau Google reCAPTCHA v3
- **Analitik respons** - Lacak waktu penyelesaian, alamat IP, browser, pengarah
- **Ekspor CSV** - Unduh semua respons untuk analisis di Excel/Google Sheets
- **Multi-bahasa** - Terjemahkan label formulir dan pesan ke semua bahasa aktif

## Membuat Formulir Pertama Anda

Navigasikan ke **Pengaturan > Halaman > Formulir** untuk mengakses manajer formulir:

**Langkah 1: Buat Formulir Baru**
- Klik **+ Buat Formulir Baru**
- Masukkan nama formulir (identifikasi internal, tidak ditampilkan kepada pelanggan)
- Masukkan judul formulir (ditampilkan sebagai heading di atas formulir)
- Opsional: Tambahkan deskripsi (teks bantuan ditampilkan di bawah judul)

**Langkah 2: Tambahkan Field**
- Klik **Edit Desain Formulir** untuk membuka pembangun visual
- Drag field jenis dari sidebar kiri ke canvas
- Klik field untuk mengonfigurasinya di panel kanan
- Atur label, placeholder, teks bantuan
- Toggle status wajib
- Tambahkan aturan validasi

**Langkah 3: Konfigurasikan Pengaturan Formulir**
- Atur teks tombol submit (default: "Submit")
- Personalisasi pesan sukses (ditampilkan setelah pengajuan)
- Pilih proteksi spam (rekomendasi: honeypot)
- Toggle "Require Login" jika diperlukan
- Aktifkan "Formulir Multi-langkah" untuk formulir kompleks

**Langkah 4: Aktifkan Formulir**
- Toggle status **Aktif**
- Hanya formulir aktif yang menerima pengajuan
- Simpan formulir

**Langkah 5: Gunakan dalam Page Builder**
- Tambahkan elemen **Formulir** ke halaman mana pun
- Pilih formulir dari dropdown
- Formulir mewarisi gaya halaman
- Pengajuan dikirim ke backend secara otomatis

## Formulir Satu Halaman vs Multi-Langkah

**Formulir Satu Halaman** (default):
- Semua field ditampilkan sekaligus
- Gulir untuk melihat semua field
- Tombol submit di bagian bawah
- Terbaik untuk: Formulir kontak, survei pendek, pengumpulan data sederhana

**Formulir Multi-Langkah**:
- Field dikelompokkan ke dalam langkah bernomor
- Indikator kemajuan menunjukkan langkah saat ini
- Tombol navigasi Kembali/Maju
- Submit hanya pada langkah akhir
- Opsional: Simpan respons sebagian (mode draf)
- Terbaik untuk: Aplikasi pekerjaan, pendaftaran, survei kompleks, alur checkout

**Mengaktifkan Multi-Langkah**:
1. Toggle "Formulir Multi-langkah" di pengaturan formulir
2. Klik tab **Langkah** di panel kanan
3. Tambahkan langkah (misalnya, "Informasi Pribadi", "Detail Kontak", "Preferensi")
4. Assign field ke langkah menggunakan dropdown langkah saat mengedit field
5. Ubah urutan langkah dengan menyeret
6. Atur properti langkah: judul, deskripsi, dapat dilewati

**Manfaat Multi-Langkah**:
- Mengurangi peninggalkan formulir (psikologis: "hanya 3 pertanyaan di halaman ini")
- Pengelompokan logis meningkatkan UX
- Indikator kemajuan mendorong penyelesaian
- Simpan draf opsional untuk formulir panjang

## Penjelasan Pengaturan Formulir

**Pengaturan Dasar**:
- **Nama Internal** - Cara Anda mengidentifikasi formulir di admin (tidak terlihat oleh pelanggan)
- **Slug** - Identifikasi yang ramah URL (dihasilkan otomatis, digunakan dalam akhir titik API)
- **Judul Formulir** - Judul yang ditampilkan di atas formulir
- **Deskripsi** - Teks bantuan opsional yang ditampilkan di bawah judul
- **Teks Tombol Submit** - Personalisasi label tombol (misalnya, "Kirim Pesan", "Lamar Sekarang")

**Pesan**:
- **Pesan Sukses** - Ditampilkan setelah pengajuan berhasil (default: "Terima kasih atas pengajuan Anda!")
- **Pesan Kesalahan** - Ditampilkan jika pengajuan gagal (default: "Terjadi kesalahan. Silakan coba lagi.")

**Keamanan & Akses**:
- **Aktif** - Hanya formulir aktif yang menerima pengajuan (formulir tidak aktif menampilkan "Formulir tidak tersedia")
- **Harus Login** - Batasi hanya pengguna yang terautentikasi (pengguna anonim melihat prompt login)

**Proteksi Spam**:
- **Tidak Ada** - Tidak ada perlindungan (tidak disarankan, bot akan spam)
- **Field Honeypot** - Field tak terlihat menangkap bot (disarankan untuk sebagian besar pedagang)
- **Google reCAPTCHA v3** - Memerlukan kunci situs dan kunci rahasia dari Google (perlindungan terkuat)

**Fitur Lanjutan**:
- **Formulir Multi-langkah** - Aktifkan alur kerja langkah demi langkah
- **Simpan Respons Sebagian** - Izinkan pengguna menyimpan kemajuan dan melanjutkan nanti (hanya untuk formulir multi-langkah)

## Opsi Proteksi Spam

**Field Honeypot (Disarankan)**:
- Field tak terlihat ditambahkan ke formulir
- Bot mengisi field ini (pengguna manusia tidak bisa melihatnya)
- Pengajuan dengan field honeypot yang terisi ditolak
- Tidak memerlukan konfigurasi
- Tidak ada frustrasi CAPTCHA bagi pengguna
- Efektif terhadap 95%+ bot spam

**Google reCAPTCHA v3**:
- Skor latar belakang tak terlihat (0,0-1,0)
- Tidak ada tantangan "klik lampu lalu lintas"
- Memerlukan pengaturan:
  1. Buat akun di google.com/recaptcha/admin
  2. Hasilkan kunci situs dan kunci rahasia
  3. Masukkan kunci ke dalam pengaturan pembangun formulir
- Lebih kuat daripada honeypot
- Gunakan ketika honeypot tidak cukup

**Tidak Ada**:
- Tidak ada perlindungan spam
- Hanya gunakan untuk formulir internal atau pengujian
- Formulir publik akan diserang spam secara berat

## Mengelola Respons Formulir

Lihat semua pengajuan di **Pengaturan > Halaman > Formulir > [Nama Formulir] > Respons**:

**Tampilan Daftar Respons**:
- Status: draf, dikirim, selesai
- Pengajuan: email (jika masuk) atau "Anonim"
- Alamat IP dan lokasi (jika GeoIP diaktifkan)
- Tanggal dan waktu pengajuan
- Waktu penyelesaian (detik)

**Detail Respons**:
- Semua nilai field dengan label
- Metadata: browser, pengarah, bahasa
- Pelacakan kemajuan (multi-langkah): langkah saat ini, langkah selesai
- Hasil aksi (jika formulir memicu aksi)

**Penyaringan Respons**:
- Saring berdasarkan formulir, status, rentang tanggal
- Cari berdasarkan email pengajuan atau alamat IP
- Urutkan berdasarkan tanggal pengajuan, waktu penyelesaian

**Ekspor Respons**:
- Klik tombol **Ekspor ke CSV**
- Unduh `{form-slug}_responses_{date}.csv`
- Baris header: Submitted At, User, IP, Status, [Label Field]
- Satu respons per baris
- Buka di Excel, Google Sheets, atau alat analisis data

## Menggunakan Formulir dalam Halaman

**Menyisipkan Formulir**:
1. Buka halaman di Page Builder
2. Tambahkan elemen **Formulir** dari panel elemen
3. Pilih formulir dari dropdown
4. Personalisasi gaya kontainer formulir (latar belakang, padding, border)
5. Simpan dan publikasikan halaman

**Formulir Tampil Dengan**:
- Judul dan deskripsi formulir (dari pengaturan formulir)
- Semua field dalam urutan (satu halaman) atau langkah saat ini (multi-langkah)
- Tombol submit dengan teks kustom
- Pesan sukses/kesalahan setelah pengajuan

**Pewarisan Gaya**:
- Formulir mewarisi gaya tema halaman
- Tombol menggunakan gaya tombol tema
- Field input menggunakan gaya input tema
- Kelas CSS kustom dapat ditambahkan ke field untuk gaya tertentu

## Antarmuka Form Builder

**Sidebar Kiri - Perpustakaan Field**:
- Dikelompokkan berdasarkan kategori (Teks, Pemilihan, Peringkat, Lanjutan)
- Drag field ke canvas atau klik untuk menambahkan
- Cari untuk menemukan field jenis secara cepat

**Canvas Utama - Editor Field**:
- Handle drag (≡) untuk mengurutkan field
- Klik field untuk memilih dan mengedit
- Tombol hapus (×) pada setiap field
- Tampilan visual field sesuai konfigurasi
- Keadaan kosong dengan instruksi zona drag

**Sidebar Kanan - Panel Properti**:
- **Tab Pengaturan Formulir** - Info dasar, pesan, proteksi spam
- **Tab Pengaturan Field** - Konfigurasikan field yang dipilih (label, validasi, dll.)
- **Tab Langkah** - Kelola langkah (hanya untuk formulir multi-langkah)
- **Tab Aturan Kondisional** - Tambahkan logika tampilkan/sembunyikan berdasarkan respons

**Fitur Toolbar**:
- **Undo/Redo** - Riwayat edit lengkap
- **Preview** - Uji fungsi formulir
- **Save** - Simpan otomatis setiap 3 detik saat mengedit
- **Terjemahan** - Terjemahkan teks formulir ke bahasa lain

## Contoh Formulir Umum

**Formulir Kontak**:
- Field: Nama Lengkap (wajib), Email (wajib), Telepon, Pesan (wajib)
- Tombol submit: "Kirim Pesan"
- Sukses: "Terima kasih telah menghubungi kami! Kami akan membalas dalam 24 jam.

**Survei Umpan Balik Produk**:
- Langkah 1: Peringkat bintang, skala persetujuan Likert
- Langkah 2: Skor NPS, saran peningkatan
- Kondisional: Jika peringkat < 3, wajib umpan balik peningkatan

**Aplikasi Pekerjaan**:
- Langkah 1: Informasi pribadi (nama, email, telepon)
- Langkah 2: Pengalaman (unggah CV, tahun pengalaman, referensi)
- Langkah 3: Ketersediaan (tanggal mulai, ekspektasi gaji)
- Simpan sebagian diaktifkan (pencari kerja dapat melanjutkan nanti)

**Pendaftaran Newsletter dengan Preferensi**:
- Email (wajib)
- Kelompok kotak centang: Minat (Produk, Penjualan, Pembaruan Blog)
- reCAPTCHA diaktifkan (mencegah pendaftaran palsu)

## Tips

- **Mulai dengan satu halaman** - Tambahkan multi-langkah hanya jika formulir memiliki lebih dari 10 field
- **Gunakan honeypot terlebih dahulu** - Hanya naikkan ke reCAPTCHA jika spam masih terjadi
- **Uji sebelum menerbitkan** - Gunakan mode preview untuk memverifikasi validasi dan alur
- **Ekspor secara teratur** - Unduh CSV respons mingguan untuk cadangan
- **Pantau waktu penyelesaian** - Jika rata-rata >5 menit, formulir mungkin terlalu panjang
- **Gunakan logika kondisional** - Sembunyikan field yang tidak relevan untuk mengurangi persepsi panjang formulir
- **Aktifkan simpan sebagian untuk formulir panjang** - Mengurangi peninggalkan pada aplikasi multi-langkah
- **Terjemahkan label formulir** - Gunakan sistem terjemahan bawa-in untuk situs multi-bahasa
- **Wajib login untuk data sensitif** - Mencegah spam anonim, menghubungkan pengajuan ke akun pengguna
- **Jaga pesan sukses spesifik** - "Kami akan membalas dalam 24 jam" lebih baik daripada "Terima kasih"
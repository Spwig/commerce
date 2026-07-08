---
title: Bidang Pembangun Formulir dan Validasi
---

Bidang formulir adalah blok bangunan dari formulir Anda—setiap bidang mengumpulkan satu bagian data dari pengguna. Form Builder menawarkan 22 jenis bidang yang beragam, mulai dari input teks sederhana hingga skala penilaian lanjutan dan pemilih produk. Konfigurasikan setiap bidang dengan label, aturan validasi, teks bantuan, dan logika kondisional untuk membuat formulir dinamis yang beradaptasi berdasarkan respons pengguna. Bidang dapat wajib atau opsional, divalidasi dengan pola regex, dan didesain dengan kelas CSS kustom.

Gunakan panduan ini untuk memahami semua jenis bidang yang tersedia, kapan menggunakan masing-masing, dan cara mengonfigurasi validasi dan logika kondisional.

## Dasar Konfigurasi Bidang

Setiap bidang memiliki pengaturan umum berikut:

**Identitas**:
- **Nama Bidang** - Nama mesin untuk penyimpanan data (tanpa spasi, gunakan garis bawah: `email_address`)
- **Jenis Bidang** - Menentukan perilaku input dan rendering
- **Penugasan Langkah** - Langkah mana bidang ini termasuk (hanya untuk formulir multi-langkah)

**Tampilan**:
- **Label** - Pertanyaan atau petunjuk yang ditampilkan kepada pengguna (contoh: "Apa alamat email Anda?")
- **Placeholder** - Teks petunjuk di dalam input (contoh: "you@example.com")
- **Teks Bantuan** - Panduan tambahan di bawah bidang (contoh: "Kami tidak akan pernah berbagi email Anda")
- **Nilai Default** - Nilai yang diisi ulang (pengguna dapat mengubahnya)

**Tata Letak**:
- **Lebar** - Penuh (100%), Setengah (50%), atau Satu Per Tiga (33%) dari lebar formulir
- **Kelas CSS** - Kelas gaya tambahan untuk desain kustom
- **Urutan** - Posisi dalam langkah (seret untuk mengurutkan ulang)

**Validasi**:
- **Wajib** - Toggle status wajib (tanda bintang merah muncul di label)
- **Min/Max Panjang** - Batas karakter (bidang teks)
- **Min/Max Nilai** - Batas numerik (bidang angka)
- **Polanya Validasi** - Pola regex kustom untuk validasi kompleks
- **Pesan Kesalahan** - Teks kustom yang ditampilkan saat validasi gagal

## Bidang Input Teks

**Teks Satu Baris** (`text`):
- Input teks dasar untuk respons pendek
- Validasi: min/max panjang, pola regex
- Kasus penggunaan: Nama, alamat, kode produk, jawaban pendek
- Contoh: "Nama Lengkap", "Alamat Jalan", "Nama Perusahaan"

**Teks Multi-baris** (`textarea`):
- Area teks yang dapat diperluas untuk konten yang lebih panjang (3-10 baris)
- Validasi: min/max panjang
- Kasus penggunaan: Komentar, umpan balik, deskripsi rinci, pesan
- Contoh: "Beritahu kami tentang pengalaman Anda", "Catatan tambahan"

**Alamat Email** (`email`):
- Validasi khusus email (memerlukan @ dan domain)
- Papan ketik mobile menampilkan tombol @ secara menonjol
- Kasus penggunaan: Email kontak, pendaftaran newsletter, pembuatan akun
- Contoh: "Alamat Email", "Email Kerja"

**Nomor Telepon** (`phone`):
- Otomatis memformat nomor telepon
- Papan ketik mobile menampilkan tata letak numerik
- Validasi: pola yang dapat dikonfigurasi (format internasional didukung)
- Kasus penggunaan: Nomor telepon kontak, kontak darurat, jadwal janji temu
- Contoh: "Nomor Telepon", "Ponsel", "Nomor Kontak"

**Angka** (`number`):
- Input numerik dengan kontrol peningkatan/pengurangan
- Validasi: min/max nilai, peningkatan langkah
- Mengembalikan angka (bukan string) dalam respons
- Kasus penggunaan: Kuantitas, usia, tahun pengalaman, jumlah anggaran
- Contoh: "Berapa banyak karyawan yang Anda miliki?", "Usia Anda", "Tahun dalam bisnis"

**URL** (`url`):
- Validasi URL (memerlukan http:// atau https://)
- Papan ketik mobile menampilkan tombol .com
- Kasus penggunaan: Situs web, profil LinkedIn, tautan portofolio
- Contoh: "Situs Web Perusahaan", "URL Portofolio"

## Bidang Pemilihan

**Dropdown Pemilihan** (`select`):
- Pemilihan satu opsi dari menu dropdown
- Konfigurasi: array dari {value, label} opsi
- Mendukung pemilihan default
- Kasus penggunaan: Kategori, negara/daerah, pemilihan status
- Contoh: "Pilih negara Anda", "Departemen", "Bagaimana Anda mengetahui tentang kami?"
- Terbaik untuk: 5+ opsi (opsi lebih sedikit gunakan radio)

**Tombol Radio** (`radio`):
- Pemilihan tunggal dari opsi yang terlihat (semua opsi ditampilkan)
- Konfigurasi: array dari {value, label} opsi
- UX yang lebih baik daripada select untuk 2-4 opsi
- Kasus penggunaan: Pertanyaan ya/tidak, jenis kelamin, preferensi dengan sedikit pilihan
- Contoh: "Apakah Anda akan merekomendasikan kami?", "Metode kontak yang dipilih"

**Checkbox** (`checkbox`):
- Checkbox toggle tunggal (on/off)
- Mengembalikan true/false dalam respons
- Kasus penggunaan: Penerimaan ketentuan, kesepakatan, preferensi tunggal
- Contoh: "Saya setuju dengan ketentuan dan kondisi", "Langgani newsletter"

**Grup Checkbox** (`checkbox_group`):
- Pemilihan multi dari opsi (pengguna dapat memilih 0, 1, atau banyak)
- Konfigurasi: array dari {value, label} opsi
- Mengembalikan array nilai yang dipilih
- Kasus penggunaan: Preferensi multi-pemilihan, minat, fitur yang diperlukan
- Contoh: "Topik apa yang menarik Anda?", "Pilih semua yang berlaku"

## Bidang Penilaian

**Penilaian Bintang** (`rating_stars`):
- Skala penilaian visual berbentuk bintang (biasanya 1-5 bintang)
- Konfigurasi:
  - `max_stars`: 3-10 bintang (default: 5)
  - `allow_half`: true/false untuk penilaian setengah bintang
  - `icon`: fa-star (default) atau fa-heart
  - `color`: kode warna heksadesimal (default: #FFD700 emas)
- Kasus penggunaan: Penilaian produk, kualitas layanan, skor kepuasan
- Contoh: "Berikan penilaian pengalaman Anda", "Bagaimana layanan kami?"

**Skala Likert** (`rating_likert`):
- Skala penilaian pernyataan: sangat tidak setuju → sangat setuju
- Konfigurasi:
  - `scale_type`: 5_point (1-5) atau 7_point (1-7)
  - `labels`: kustomisasi teks ujung (kiri: "Sangat Tidak Setuju", kanan: "Sangat Setuju")
- Mengembalikan nilai numerik (1-5 atau 1-7)
- Kasus penggunaan: Pernyataan survei, skala persetujuan, pengukuran sentimen
- Contoh: "Produk memenuhi kebutuhan saya", "Layanan pelanggan membantu"

**Skor Promotor Netral (NPS)** (`rating_nps`):
- Skala 0-10: "Tidak sedikit pun mungkin" hingga "Sangat mungkin"
- Konfigurasi:
  - `low_label`: teks ujung kiri (default: "Tidak sedikit pun mungkin")
  - `high_label`: teks ujung kanan (default: "Sangat mungkin")
- Mengembalikan nilai 0-10 (0-6 = detraktor, 7-8 = pasif, 9-10 = promotor)
- Kasus penggunaan: Survei NPS, kemungkinan rekomendasi, pengukuran loyalitas
- Contoh: "Seberapa mungkin Anda merekomendasikan kami kepada teman?"

## Bidang Lanjutan


**Pengunggahan File** (`file`):
- Unggah satu atau beberapa file
- Konfigurasi:
  - `max_size_mb`: batas ukuran file per file (default: 5MB)
  - `allowed_types`: array ekstensi (misalnya, ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: jumlah maksimum file (1 untuk tunggal, 2+ untuk beberapa)
- Mengembalikan jalur file(s) dalam respons
- File disimpan di `/media/form_uploads/{form-slug}/`
- Penggunaan: Unggah CV, pengiriman dokumen, lampiran foto
- Contoh: "Unggah CV Anda", "Lampirkan dokumen pendukung"

**Pemilih Produk** (`product_select`):
- Pemilihan multi dari katalog produk Anda
- Konfigurasi:
  - `category_filters`: batasi ke kategori tertentu (array ID kategori)
  - `max_selections`: 1 untuk produk tunggal, 2+ untuk beberapa
  - `display_mode`: "list" (default) atau "grid" (dengan gambar mini)
- Mengembalikan ID/SKU produk dalam respons
- Penggunaan: Rekomendasi produk, daftar keinginan, survei umpan balik, paket
- Contoh: "Produk apa yang menarik minat Anda?", "Pilih item favorit Anda"

**Tanggal** (`date`):
- Antarmuka pemilih tanggal (popup kalender)
- Mengembalikan format ISO (YYYY-MM-DD)
- Validasi: tanggal minimum/maksimum
- Penggunaan: Tanggal lahir, tanggal acara, jadwal janji temu, tenggat waktu
- Contoh: "Tanggal Lahir", "Tanggal Janji Temu yang Diinginkan"

**Waktu** (`time`):
- Pemilih waktu (jam dan menit)
- Mengembalikan format waktu ISO (HH:MM)
- Penggunaan: Waktu janji temu, jendela ketersediaan
- Contoh: "Waktu yang Diinginkan", "Tersedia Setelah"

**Tanggal & Waktu** (`datetime`):
- Pemilih tanggal dan waktu yang digabungkan
- Mengembalikan datetime ISO lengkap
- Penggunaan: Jadwal acara, pemesanan janji temu
- Contoh: "Waktu Mulai Acara", "Jendela Pengiriman"

## Bidang Tata Letak (Non-Input)

**Judul Bagian** (`heading`):
- Teks judul untuk mengorganisir bagian formulir
- Konfigurasi: tingkat judul (h2, h3, h4)
- Tidak mengumpulkan data
- Penggunaan: Memecah formulir panjang menjadi bagian logis
- Contoh: "Informasi Pribadi", "Detail Kontak", "Preferensi"

**Paragraf Deskriptif** (`paragraph`):
- Blok teks kaya untuk instruksi atau informasi
- Tidak mengumpulkan data
- Mendukung format dasar (tebal, miring, tautan)
- Penggunaan: Instruksi langkah, pernyataan hukum, penjelasan
- Contoh: Pernyataan kebijakan privasi, penjelasan persetujuan GDPR

**Garis Pemisah** (`divider`):
- Garis horizontal visual pemisah
- Tidak mengumpulkan data
- Penggunaan: Organisasi visual antar bagian

**Bidang Tersembunyi** (`hidden`):
- Bidang tak terlihat dengan nilai programatis
- Konfigurasi: `default_value` (diperlukan)
- Tidak menampilkan label atau teks bantuan kepada pengguna
- Penggunaan: Parameter UTM, data pelacakan, ID sesi, kode referensi
- Contoh: Bidang tersembunyi dengan nilai dari parameter URL

## Aturan Validasi Bidang

**Bidang Wajib**:
- Centang kotak "Wajib" di pengaturan bidang
- Tanda bintang merah (*) muncul di sebelah label
- Formulir tidak dapat dikirim jika bidang wajib kosong
- Pesan kesalahan kustom: "Bidang ini wajib" (atau pesan kustom)

**Min/Max Panjang** (bidang teks):
- Tetapkan jumlah karakter minimum: mencegah respons terlalu pendek
- Tetapkan jumlah karakter maksimum: mencegah input berlebihan
- Contoh: Bidang pesan memerlukan min 10 karakter (mencegah respons "ok")

**Min/Max Nilai** (bidang angka):
- Tetapkan nilai minimum numerik: mencegah usia negatif, kuantitas
- Tetapkan nilai maksimum numerik: membatasi input ke rentang yang masuk akal
- Contoh: Bidang usia memerlukan min 18, max 120

**Polanya Validasi** (regex):
- Ekspresi reguler kustom untuk validasi kompleks
- Pola umum:
  - Kode pos: `^\d{5}(-\d{4})?$` (format AS)
  - Telepon: `^\(\d{3}\) \d{3}-\d{4}$` (format AS)
  - Kode produk: `^[A-Z]{2}\d{4}$` (2 huruf, 4 angka)
- Pesan kesalahan kustom diperlukan saat menggunakan pola

**Validasi File**:
- Ukuran file maksimum: mencegah unggah besar (default 5MB)
- Jenis yang diizinkan: daftar putih ekstensi tertentu (keamanan)
- Contoh: Bidang CV mengizinkan ["pdf", "doc", "docx"], maks 2MB

## Logika Kondisional

Buat formulir dinamis di mana bidang muncul/menghilang berdasarkan respons pengguna:

**Bagaimana Aturan Kondisional Bekerja**:
1. Pengguna menjawab "bidang sumber" (pemicu)
2. Sistem mengevaluasi aturan: operator + nilai perbandingan
3. Jika kondisi benar, aksi dieksekusi (tampilkan/sembunyikan/require bidang atau langkah)
4. Banyak aturan dapat berantai (aturan A memicu aturan B)

**Operator yang Tersedia**:
- **Sama Dengan** (`equals`): cocok tepat (misalnya, negara sama dengan "US")
- **Tidak Sama Dengan** (`not_equals`): segala sesuatu selain nilai
- **Mengandung** (`contains`): teks mencakup substring (tidak sensitif huruf)
- **Lebih Besar Dari** (`greater_than`): perbandingan numerik (misalnya, usia > 18)
- **Lebih Kecil Dari** (`less_than`): perbandingan numerik (misalnya, rating < 3)
- **Kosong** (`is_empty`): bidang tidak memiliki nilai
- **Tidak Kosong** (`is_not_empty`): bidang memiliki nilai apa pun
- **Dalam Daftar** (`in_list`): nilai adalah salah satu ["Opsi1", "Opsi2"]

**Aksi yang Tersedia**:
- **Tampilkan Bidang** - Tampilkan bidang tersembunyi
- **Sembunyikan Bidang** - Sembunyikan bidang (nilai dihapus jika tersembunyi)
- **Wajibkan Bidang** - Jadikan bidang wajib
- **Tidak Wajibkan Bidang** - Jadikan bidang opsional
- **Atur Nilai** - Isi bidang dengan nilai
- **Tampilkan Langkah** - Tampilkan langkah tersembunyi (hanya untuk multi-langkah)
- **Sembunyikan Langkah** - Sembunyikan langkah (hanya untuk multi-langkah)
- **Lewati ke Langkah** - Loncat ke langkah tertentu (hanya untuk multi-langkah)

**Contoh Aturan**:
- JIKA `contact_method` SAMA DENGAN "phone" MAKA tampilkan_field `phone_number`
- JIKA `rating` KURANG DARI "3" MAKA wajibkan_field `improvement_feedback`
- JIKA `country` DALAM DAFTAR ["US", "CA"] MAKA tampilkan_langkah `shipping_details`
- JIKA `budget` LEBIH BESAR DARI "10000" MAKA tampilkan_field `enterprise_features`

**Membuat Aturan Kondisional**:
1. Klik tab "Aturan Kondisional" di panel kanan
2. Klik "Tambah Aturan"
3. Pilih bidang sumber (pemicu)
4. Pilih operator (cara membandingkan)
5. Masukkan nilai perbandingan (apa yang dibandingkan)
6. Pilih aksi (apa yang dilakukan)
7. Pilih target (bidang atau langkah yang terpengaruh)
8. Opsional: Tetapkan prioritas (aturan dengan prioritas lebih tinggi dievaluasi lebih dulu)
9. Simpan aturan

**Prioritas Aturan**:
- Angka yang lebih tinggi dievaluasi terlebih dahulu (prioritas 100 sebelum prioritas 10)
- Gunakan prioritas saat aturan bertentangan atau berantai
- Contoh: Aturan A (prioritas 100) menampilkan bidang, Aturan B (prioritas 50) memerlukannya (A dieksekusi terlebih dahulu, lalu B)

## Pola Bidang Umum

**Formulir Kontak**:
- Nama Lengkap (teks, wajib)
- Email (email, wajib)
- Telepon (telepon)
- Subjek (pilihan dengan opsi: "Penjualan", "Dukungan", "Kemitraan")
- Pesan (textarea, wajib, minimal 10 karakter)

**Umpan Balik Produk**:
- Produk (product_select, pemilihan tunggal)
- Penilaian Secara Keseluruhan (rating_stars, 5 bintang)
- Kondisional: JIKA penilaian < 3 MAKA wajib "Apa yang bisa kita tingkatkan?" (textarea)
- Rekomendasi (rating_nps)

**Lamaran Pekerjaan**:
- Langkah 1: Pribadi (nama, email, telepon)
- Langkah 2: Riwayat Hidup (unggah file, izinkan ["pdf", "doc"], maks 2MB)
- Langkah 3: Ketersediaan (tanggal mulai, checkbox_group untuk hari kerja)
- Kondisional: JIKA "years_experience" > 5 MAKA tampilkan bidang "pengalaman_kepemimpinan"

## Tips

- **Gunakan jenis bidang yang sesuai** - Bidang email untuk alamat email (bukan teks), menyediakan validasi dan keyboard mobile yang lebih baik
- **Jaga label singkat** - Gunakan teks bantuan untuk detail, bukan label
- **Kelompokkan bidang yang terkait** - Gunakan judul dan pemisah untuk organisasi visual
- **Uji validasi** - Pratinjau formulir dan coba mengirimkan dengan data tidak valid
- **Batasi ukuran unggah file** - Maks 5MB mencegah kelebihan beban server dari file besar
- **Gunakan logika kondisional secara bijak** - Terlalu banyak aturan membingungkan pengguna; pertahankan formulir sederhana
- **Atur nilai maksimum yang realistis** - Maks usia 120, maks kuantitas 100 (mencegah kesalahan ketik seperti 1000)
- **Sediakan contoh pola** - Jika menggunakan validasi regex, tunjukkan contoh dalam teks bantuan
- **Buat bidang yang jelas wajib** - Nama dan email untuk formulir kontak, selalu wajib
- **Gunakan radio untuk 2-4 opsi** - Dropdown untuk 5+ opsi (meningkatkan UX)
- **Bidang setengah lebar untuk input pendek** - Telepon dan Kode Pos dapat setengah lebar, menghemat ruang vertikal
- **Pemilih produk untuk daftar keinginan** - Izinkan pelanggan memilih beberapa produk untuk rekomendasi
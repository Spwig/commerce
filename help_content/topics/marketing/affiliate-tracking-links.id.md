---
title: Pelacakan Afiliasi & Tautan
---

Pelacakan afiliasi memungkinkan sistem komisi berjalan dengan menghubungkan pembelian pelanggan dengan afiliasi yang merujuk mereka. Panduan ini menjelaskan bagaimana tautan pelacakan bekerja, data apa yang dicatat Spwig ketika pelanggan mengklik tautan tersebut, dan bagaimana sistem atribusi berbasis cookie menentukan afiliasi mana yang mendapatkan komisi.

Memahami mekanisme pelacakan membantu Anda menyelesaikan masalah atribusi, menganalisis kinerja tautan, dan mengajarkan afiliasi Anda bagaimana memaksimalkan konversi mereka.

## Apa itu Tautan Pelacakan?

Tautan pelacakan adalah URL unik yang mengarahkan pelanggan ke toko Anda sambil mencatat identitas afiliasi dalam cookie. Setiap afiliasi dapat membuat beberapa tautan pelacakan yang mengarah ke destinasi berbeda — halaman utama, produk spesifik, halaman koleksi, atau halaman landing.

Format tautan pelacakan contoh:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

Tautan ini mengarahkan ke destinasi sambil menyetel cookie pelacakan yang menghubungkan pembelian masa depan dengan afiliasi yang memiliki kode tautan `a2b7f8c4d1e9`.

Afiliasi menghasilkan tautan ini dari dashboard portal mereka. Mereka menyalin URL lengkap dan membagikannya dalam posting blog, media sosial, email, atau saluran lainnya di mana mereka menjangkau pelanggan potensial.

## Komponen Tautan Pelacakan

Setiap tautan pelacakan berisi elemen-elemen berikut:

| Komponen | Contoh | Deskripsi |
|-----------|---------|-------------|
| **URL Dasar** | `https://yourstore.com` | Domain toko Anda |
| **Path Pelacakan** | `/affiliate/track/` | Titik akhir pelacakan Spwig |
| **Kode Tautan** | `a2b7f8c4d1e9` | Identifikasi unik 12 karakter yang dihasilkan secara otomatis |
| **Destinasi** | Diatur saat tautan dibuat | Tempat pelanggan tiba setelah dialihkan (halaman utama, produk, dll.) |

Ketika afiliasi membuat tautan, Spwig menghasilkan kode unik 12 karakter secara otomatis. Afiliasi tidak pernah perlu membuat atau mengedit kode ini secara manual — mereka hanya memilih destinasi dan Spwig menangani sisanya.

### Label Tautan (Opsional)

Afiliasi dapat menambahkan label ke setiap tautan untuk organisasi mereka sendiri:
- "Tautan Bio Instagram"
- "Deskripsi YouTube"
- "Kampanye Email Black Friday"

Label membantu afiliasi melacak saluran promosi mana yang paling efektif. Mereka hanya terlihat oleh afiliasi dan Anda — pelanggan tidak pernah melihat label.

## Bagaimana Pelacakan Bekerja

Proses pelacakan dan atribusi mengikuti lima langkah dari klik hingga komisi:

### 1. Pelanggan Mengklik Tautan

Seorang pelanggan potensial mengklik tautan pelacakan afiliasi dari saluran promosi apa pun (pos media sosial, artikel blog, newsletter email).

### 2. Klik Dicatat

Titik akhir pelacakan Spwig mencatat detail klik:
- Alamat IP
- User agent (browser dan perangkat)
- HTTP referrer (dari mana klik berasal)
- Timestamp
- Identifier sesi

Data ini muncul di **Klik** admin di **Afiliasi > Klik** untuk analitik dan deteksi penipuan.

### 3. Cookie Disetel

Sistem pelacakan menyetel cookie di browser pelanggan sebelum mengarahkannya. Cookie ini berisi:
- ID afiliasi (siapa yang harus mendapatkan komisi)
- ID program (struktur komisi mana yang berlaku)
- Kode tautan (tautan spesifik mana yang diklik)

### 4. Pelanggan Membeli

Pelanggan menjelajahi toko Anda dan menyelesaikan pembelian. Ini bisa terjadi segera atau beberapa hari/minggu kemudian, selama mereka membeli dalam jendela waktu cookie.

### 5. Komisi Dibuat

Pada saat checkout, Spwig memeriksa cookie afiliasi. Jika ditemukan dan masih valid (dalam jangka waktu cookie), sistem membuat catatan komisi dengan status **Pending** yang terkait dengan afiliasi, program, dan pesanan.

## Atribusi Berbasis Cookie

Cookie pelacakan adalah mekanisme inti yang menghubungkan pembelian dengan afiliasi. Memahami bagaimana cookie bekerja membantu Anda menetapkan jendela atribusi optimal dan menyelesaikan masalah pelacakan.

### Struktur Cookie

| Properti | Nilai |
|----------|-------|
| **Nama** | `aff_{program_id}` (misalnya, `aff_7` untuk ID program 7) |
| **Nilai** | JSON yang berisi ID afiliasi, kode tautan, timestamp |
| **Domain** | Domain toko Anda |
| **Path** | `/` (akses situs-wide) |
| **Durasi** | Jangka waktu cookie program (1–365 hari) |
| **HttpOnly** | `true` (mencegah akses JavaScript untuk keamanan) |
| **SameSite** | `Lax` (memungkinkan pelacakan dari referrer eksternal) |
| **Secure** | `true` pada situs HTTPS (dianjurkan) |

### Jendela Waktu Cookie

Jangka waktu cookie menentukan seberapa lama pelanggan memiliki waktu untuk membuat pembelian setelah mengklik tautan afiliasi. Jendela ini ditetapkan per program di **Pemasaran > Program Afiliasi** saat Anda membuat atau mengedit program.

Jangka waktu cookie standar industri:
- **7 hari**: Produk keputusan cepat (makanan, tiket acara)
- **30 hari**: E-commerce standar (pengaturan paling umum)
- **60–90 hari**: Pembelian yang dipertimbangkan (perabot, elektronik, produk B2B)
- **365 hari**: Siklus penjualan panjang (barang mewah, layanan berbiaya tinggi)

Jika seorang pelanggan mengklik tautan afiliasi pada 1 Januari dan jangka waktu cookie Anda adalah 30 hari, pembelian apa pun yang mereka lakukan hingga 30 Januari akan memberi kredit afiliasi tersebut. Pembelian pada 31 Januari atau setelahnya tidak menghasilkan komisi karena cookie telah kedaluwarsa.

### Model Atribusi Last-Click

Spwig menggunakan model atribusi **last-click**: tautan afiliasi terbaru yang menang. Berikut cara kerjanya:

**Skenario**: Seorang pelanggan mengklik tautan afiliasi A pada hari Senin, lalu mengklik tautan afiliasi B pada hari Rabu, lalu membeli pada hari Jumat.

**Hasil**: Afiliasi B mendapatkan komisi karena tautan mereka adalah klik terbaru.

Cookie last-click menimpa cookie afiliasi sebelumnya. Model ini sederhana untuk dipahami dan mencegah komisi ganda, meskipun berarti hanya satu afiliasi yang mendapatkan kredit per pesanan (yang terakhir sebelum pembelian).

## Pencatatan Klik

Spwig mencatat setiap klik pada setiap tautan afiliasi untuk memberikan analitik bagi Anda dan afiliasi. Data klik membantu mengukur kinerja tautan, mendeteksi penipuan, dan mengoptimalkan strategi promosi.

### Data yang Dicatat per Klik

Navigasikan ke **Afiliasi > Klik** untuk melihat semua klik yang dicatat. Setiap entri berisi:

| Bidang | Deskripsi |
|-------|-------------|
| **Tautan** | Tautan pelacakan yang diklik |
| **Afiliasi** | Siapa yang memiliki tautan |
| **Alamat IP** | IP pelanggan (untuk deteksi penipuan) |
| **User Agent** | Informasi browser dan perangkat |
| **Referrer** | Halaman di mana pelanggan mengklik tautan (misalnya, "https://instagram.com") |
| **ID Sesi** | Identifikasi unik untuk sesi penjelajahan ini |
| **Timestamp** | Tanggal dan waktu persis dari klik |

### Batas Klik

Untuk mencegah penipuan klik dan penyalahgunaan bot, Spwig membatasi klik hingga **100 per menit per alamat IP**. Jika alamat IP yang sama melebihi ambang ini, klik tambahan diabaikan dan tidak meningkatkan jumlah klik.

Perlindungan ini mencegah pihak jahat dari memperbesar statistik klik tanpa memblokir lalu lintas sah. Pelanggan nyata hampir tidak pernah melebihi 100 klik per menit.

### Pertimbangan Privasi

Data klik berisi alamat IP dan user agent untuk tujuan deteksi penipuan. Pastikan kebijakan privasi Anda mengungkapkan bahwa Anda melacak rujukan afiliasi dan berbagi data kinerja anonim dengan afiliasi.

## Melihat Tautan Afiliasi

Semua tautan pelacakan yang dihasilkan oleh afiliasi muncul di panel admin Anda untuk pemantauan dan manajemen.

### Mengakses Daftar Tautan

Navigasikan ke **Afiliasi > Tautan** untuk melihat semua tautan pelacakan di semua afiliasi dan program. Tampilan daftar menampilkan:

- **Kode Tautan**: Identifikasi unik 12 karakter
- **Afiliasi**: Siapa yang membuat tautan
- **Program**: Struktur komisi mana yang berlaku
- **Label**: Deskripsi opsional yang diberikan oleh afiliasi
- **Destinasi**: Tempat tautan mengarahkan pelanggan
- **Total Klik**: Jumlah klik sepanjang masa
- **Status Aktif**: Apakah tautan saat ini sedang melacak

### Menyaring Tautan

Gunakan penyaring admin untuk menyempitkan daftar:
- **Oleh Afiliasi**: Lihat semua tautan untuk mitra tertentu
- **Oleh Program**: Lihat tautan yang mempromosikan struktur komisi tertentu
- **Oleh Status Aktif**: Temukan tautan yang dinonaktifkan

Penyaring ini membantu Anda menganalisis distribusi tautan di jaringan afiliasi Anda dan mengidentifikasi tautan terbaik.

## Statistik Tautan

Setiap tautan pelacakan mengumpulkan metrik kinerja yang membantu afiliasi mengoptimalkan strategi promosi mereka dan membantu Anda mengidentifikasi mitra terbaik.

### Klik pada catatan tautan untuk melihat statistik terperinci:

| Metrik | Deskripsi | Perhitungan |
|--------|-------------|-------------|
| **Total Klik** | Semua klik yang dicatat sejak pembuatan tautan | Jumlah catatan klik |
| **Klik (7 hari)** | Indikator aktivitas terbaru | Klik dalam 7 hari terakhir |
| **Konversi** | Pesanan yang diatribusikan ke tautan ini | Jumlah komisi dari kode tautan ini |
| **Tingkat Konversi** | Persentase klik yang menghasilkan pembelian | (Konversi ÷ Total Klik) × 100 |
| **Total Pendapatan** | Jumlah semua nilai pesanan dari tautan ini | Jumlah total pesanan untuk klik yang dikonversi |

### Menggunakan Statistik untuk Optimasi

**Untuk Afiliasi**: Angka-angka ini menunjukkan saluran promosi mana yang paling efektif. Jika tautan bio Instagram memiliki tingkat konversi 5% tetapi tautan artikel blog memiliki 15%, afiliasi sebaiknya fokus lebih pada konten blog.

**Untuk Pedagang**: Statistik tautan mengungkapkan afiliasi mana yang mengarahkan lalu lintas berkualitas. Jumlah klik tinggi dengan tingkat konversi rendah menunjukkan audiens afiliasi tersebut tidak cocok dengan produk Anda.

## Mengelola Tautan

Anda dapat mengelola tautan afiliasi dari panel admin untuk tujuan pemeliharaan dan penyelesaian masalah.

### Menonaktifkan Tautan

Untuk mencegah tautan tertentu dari melacak klik baru sambil mempertahankan data historis:

1. Navigasikan ke **Afiliasi > Tautan**
2. Klik tautan yang ingin Anda nonaktifkan
3. Hilangkan centang **Aktif**
4. Klik **Simpan**

Tautan yang dinonaktifkan tetap mengarahkan pelanggan ke destinasi, tetapi tidak menyetel cookie pelacakan atau mencatat klik. Ini berguna ketika afiliasi menjalankan kampanye sementara atau Anda perlu menonaktifkan saluran promosi tertentu.

### Mengedit Detail Tautan

Anda dapat memodifikasi:
- **Label**: Perbarui deskripsi yang diberikan oleh afiliasi
- **Destinasi**: Ubah tempat tautan mengarahkan (berguna jika Anda memindahkan halaman produk)
- **Status Aktif**: Aktifkan atau nonaktifkan pelacakan

Anda tidak dapat mengedit kode tautan — kode ini permanen dan terkait dengan semua data klik dan komisi historis.

### Menghapus Tautan Tidak Aktif

Hapus tautan yang tidak lagi digunakan dan tidak memiliki klik atau konversi historis. Ini menjaga daftar tautan Anda tetap bersih tanpa kehilangan data analitik yang berharga.

**Peringatan**: Menghapus tautan menghapus semua catatan klik yang terkait. Hanya hapus tautan dengan nol klik atau ketika Anda yakin 100% bahwa Anda tidak memerlukan data historis tersebut.

## Model Atribusi

Memahami logika atribusi Spwig membantu Anda menetapkan ekspektasi dengan afiliasi dan menyelesaikan sengketa komisi.

### Atribusi Last-Click

Seperti yang disebutkan sebelumnya, Spwig menggunakan atribusi last-click: jika seorang pelanggan mengklik beberapa tautan afiliasi sebelum membeli, hanya afiliasi terbaru yang mendapatkan komisi.

**Keuntungan**:
- Sederhana untuk dipahami dan dijelaskan
- Mencegah komisi ganda
- Memberi penghargaan kepada afiliasi yang menutup penjualan

**Kekurangan**:
- Afiliasi sebelumnya yang memperkenalkan pelanggan tidak mendapatkan kredit
- Tidak mencerminkan perjalanan pelanggan multi-sentuhan
- Mungkin memicu "link hijacking" (afiliasi menargetkan pelanggan dengan niat tinggi yang sudah dirujuk oleh orang lain)

### Jangka Waktu Cookie Menentukan Kelayakan

Hanya pembelian dalam jendela waktu cookie yang menghasilkan komisi. Jika cookie kedaluwarsa sebelum checkout, tidak ada komisi yang dibuat meskipun pelanggan kembali melalui bookmark.

**Contoh**: Jangka waktu cookie 30 hari
- Pelanggan mengklik tautan 1 Januari → Cookie disetel, kedaluwarsa 31 Januari
- Pelanggan membeli 25 Januari → Komisi dibuat
- Pelanggan membeli 5 Februari → Tidak ada komisi (cookie kedaluwarsa)

### Pelacakan Sesi

Selain cookie, Spwig melacak ID sesi untuk setiap klik. Ini memungkinkan atribusi multi-visit dalam sesi yang sama meskipun cookie diblokir atau dihapus.

Jika seorang pelanggan mengklik tautan, menjelajahi toko Anda memicu beberapa muat halaman, lalu membeli — semua dalam sesi yang sama — afiliasi mendapatkan kredit meskipun tidak ada cookie yang bertahan.

## Penyelesaian Masalah

Masalah pelacakan umum dan cara menyelesaikannya:

### Tautan Tidak Melacak Klik

**Gejala**: Jumlah klik tetap nol meskipun afiliasi melaporkan berbagi tautan.

**Penyebab dan solusi**:
1. **Tautan dinonaktifkan**: Periksa status **Aktif** di halaman detail tautan
2. **Program tidak aktif**: Navigasikan ke **Afiliasi > Program** dan verifikasi status program adalah **Aktif**
3. **Akun afiliasi dinonaktifkan**: Periksa status akun afiliasi di **Afiliasi > Afiliasi**
4. **Batas klik**: Periksa apakah alamat IP yang sama menghasilkan klik berlebihan (lalu lintas bot)

### Tingkat Konversi Rendah

**Gejala**: Jumlah klik tinggi tetapi sangat sedikit pesanan yang diatribusikan.

**Penyebab dan solusi**:
1. **Jangka waktu cookie terlalu pendek**: Tingkatkan jangka waktu cookie program jika produk Anda memerlukan penelitian dan pertimbangan
2. **Kualitas halaman tujuan**: Periksa halaman landing — apakah ramah mobile? Apakah memuat cepat? Apakah produk tersedia?
3. **Ketidakcocokan audiens**: Audiens afiliasi mungkin tidak cocok dengan produk Anda
4. **Browser memblokir cookie**: Beberapa alat privasi memblokir cookie pihak ketiga, meskipun Spwig menggunakan cookie pihak pertama yang kurang mungkin diblokir

### Catatan Klik Duplikat

**Gejala**: Pelanggan yang sama menghasilkan beberapa catatan klik secara berurutan yang cepat.

**Penyebab**: Ini adalah perilaku normal. Setiap muat halaman dari tautan pelacakan menciptakan catatan klik. Jika seorang pelanggan mengklik, halaman memuat lambat, dan mereka mengklik lagi, Anda akan melihat beberapa catatan.

**Solusi**: Tidak diperlukan tindakan. Penghambat klik mencegah penyalahgunaan (100 klik/menit/IP), dan klik duplikat dari sesi yang sama tidak memengaruhi atribusi — hanya satu cookie yang disetel.

## Tips

- **Uji pelacakan sebelum peluncuran** — Buat akun afiliasi uji, buat tautan pelacakan, klik tautan tersebut di browser incognito, dan selesaikan pembelian uji. Verifikasi komisi muncul dengan atribusi afiliasi yang benar.
- **Ajarkan afiliasi tentang jangka waktu cookie** — Pastikan afiliasi memahami bahwa mereka hanya mendapatkan komisi untuk pembelian dalam jangka waktu cookie. Ini membantu mereka menetapkan ekspektasi yang realistis dan fokus pada lalu lintas dengan niat tinggi.
- **Pantau pola klik untuk penipuan** — Jumlah klik yang tidak biasa tinggi dari satu IP atau klik tanpa string user agent mungkin menunjukkan lalu lintas bot. Periksa afiliasi ini secara hati-hati sebelum menyetujui komisi.
- **Gunakan label tautan secara konsisten** — Dorong afiliasi untuk memberi label tautan mereka berdasarkan saluran (Instagram, Blog, Email) sehingga Anda dan mereka dapat menganalisis saluran promosi mana yang menghasilkan konversi terbaik.
- **Pertimbangkan jangka waktu cookie yang lebih panjang untuk produk berharga tinggi** — Jika nilai pesanan rata-rata Anda tinggi dan pelanggan biasanya melakukan penelitian sebelum membeli, perpanjang jangka waktu cookie hingga 60–90 hari untuk menangkap konversi yang tertunda.
- **Periksa data referrer untuk wawasan saluran** — Bidang referrer menunjukkan dari mana klik berasal. Jika Anda melihat banyak klik dari "instagram.com" atau "youtube.com", Anda tahu saluran media sosial mana yang digunakan afiliasi Anda secara paling efektif.
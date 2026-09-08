---
title: Buku Panduan Pengiriman Email
---

Mengirim email *terkirim* itu mudah. Mendapatkan email tersebut ke kotak masuk alih-alih folder spam adalah pekerjaan sebenarnya — dan penyedia layanan kotak masuk seperti Gmail dan Yahoo sekarang menerapkan persyaratan teknis yang ketat sebelum mereka bahkan akan mempertimbangkannya. Buku panduan ini menjelaskan apa yang perlu dikonfigurasi, dalam urutan apa pun, agar pemberitahuan pesanan dan kampanye Anda sampai di mana pelanggan dapat melihatnya.

Tidak ada yang menjadi tugas satu kali. Pengiriman email adalah posisi yang Anda bangun seiring waktu dan bisa hilang dengan cepat — daftar periksa di akhir ini layak untuk dilihat kembali kapan saja ketika sesuatu terlihat tidak benar.

## Mengapa ini penting

Setiap penyedia kotak masuk utama menilai email masuk berdasarkan reputasi pengirim sebelum menentukan apakah akan menerimanya, menyimpannya ke folder spam, atau menolaknya secara langsung. Sejak 2024, Gmail dan Yahoo memformalkan ini menjadi **persyaratan pengirim massal** bagi siapa pun yang mengirim volume yang signifikan:

- **otentifikasi domain Anda** — catatan SPF, DKIM, dan DMARC yang valid.
- **Buatlah mudah untuk berhenti berlangganan** — opsi untuk berhenti berlangganan yang berfungsi dengan alur kerja rendah dalam setiap email pemasaran.
- **pertahankan keluhan spam yang rendah** — pengirim massal yang melebihi sekitar 0,3% keluhan berisiko menerima email ditolak atau dikirim ke folder massal; target yang paling aman adalah jauh di bawah 0,1%.

Gagal dalam hal ini bukan hanya kampanye pemasaran yang menderita — kerusakan reputasi domain bisa membawa email transaksional (pemberitahuan pesanan, reset kata sandi) ke folder spam juga, karena Gmail dan Yahoo semakin menilai reputasi pada tingkat domain pengirim, bukan hanya jenis pesan.

Langkah-langkah di bawah ini adalah cara Anda memenuhi ketiga hal tersebut.

## Langkah 1: Otentikasi domain pengiriman Anda

SPF, DKIM, dan DMARC adalah catatan TXT DNS yang membuktikan ke server email penerima bahwa email yang mengklaim berasal dari domain Anda benar-benar dikirim oleh Anda. Bagaimana Anda mengatur pengaturan ini tergantung pada mode pengiriman toko Anda — ketiga-tiganya dikonfigurasi di bawah **Konfigurasi Email** di bilah samping admin (ini membuka daftar akun email; lihat [Konfigurasi Email](email-configuration) untuk panduan pemasangan akun lengkap).

| Mode pengiriman | Bagaimana otentikasi bekerja |
|---|---|
| **SMTP Bawaan** (server email Spwig sendiri) | Spwig secara otomatis menghasilkan pasangan kunci DKIM untuk domain Anda. Tambahkan akun email, dan **Langkah 4** dari wizard penyiapan menunjukkan status SPF, DKIM, dan DMARC Anda serta catatan yang tepat untuk ditambahkan, dengan tombol salin ke papan klip dan petunjuk khusus penyedia untuk Cloudflare, GoDaddy, Namecheap, dan AWS Route 53. Catatan DKIM DNS yang sama juga ditampilkan di halaman admin akun itu sendiri nanti, di bawah **Kunci DKIM yang dikonfigurasi**, jika Anda perlu menemukannya lagi. |
| **SMTP Umum** (penyedia pihak ketiga seperti SendGrid, Mailgun, Amazon SES, atau Google Workspace, yang terhubung melalui kredensial SMTP) | Otentikasi terjadi sebagian di dashboard penyedia itu sendiri. Tahap DNS dari wizard penyiapan termasuk petunjuk berpita untuk Gmail, Outlook, SendGrid, Mailgun, dan Amazon SES secara khusus — masing-masing menjelaskan apa yang perlu dikonfigurasi di konsol penyedia (misalnya, memverifikasi domain pengiriman di SendGrid) dan catatan DNS mana yang perlu ditambahkan di host DNS Anda. |
| **Pintu gerbang email yang dikelola Spwig** | Tersedia pada rencana Spwig yang dikelola sebagai opsi pengiriman yang dikelola. Ini menandatangani email keluar dengan DKIM secara otomatis dan default mengirim dari alamat pada domain yang diverifikasi Spwig sendiri, jadi bekerja dengan nol penyiapan. Jika Anda ingin mengirim dari domain Anda sendiri melalui pintu gerbang ini, bicaralah dengan penyedia layanan hosting Anda tentang verifikasi domain — ini adalah layanan yang dikelola, bukan alur kerja DNS mandiri. |

![Langkah 4 dari wizard penyiapan akun email, menunjukkan validasi SPF/DKIM/DMARC, tab penyedia DNS, dan catatan DKIM yang diperluas yang siap disalin](/static/core/admin/img/help/deliverability/wizard-dns-step.webp)

![Panel kunci DKIM dari akun email SMTP bawaan yang sudah ada, dengan catatan TXT DNS dan tombol Salin Catatan DNS](/static/core/admin/img/help/deliverability/dkim-dns-record.webp)

Mode mana pun yang Anda gunakan, **menambahkan rekaman DNS itu sendiri selalu merupakan langkah eksternal** — Anda melakukannya di registrar domain atau host DNS Anda (Cloudflare, GoDaddy, Namecheap, Route 53, atau di mana pun nameserver domain Anda menunjuk), bukan di dalam Spwig.

Spwig dapat memberi tahu Anda persis apa yang harus ditambahkan dan memvalidasi bahwa rekaman tersebut sudah aktif, tetapi tidak dapat masuk ke registrar Anda untuk menambahkannya untuk Anda.

Beberapa hal yang perlu diketahui sebelum Anda memulai:

- **Perubahan DNS tidak instan.** Propagasi dapat memakan waktu dari beberapa menit hingga 48 jam. Langkah validasi wizard akan menampilkan rekaman sebagai gagal atau hilang sampai benar-benar terpropagasi — itu hal yang wajar, bukan tanda ada yang salah.
- **Hanya satu rekaman SPF yang diizinkan per domain.** Jika Anda sudah memilikinya (dari Google Workspace, pengirim lain, dll.), tambahkan pengirim baru Anda ke rekaman yang ada dengan `include:` alih-alih membuat rekaman TXT SPF kedua — dua rekaman SPF akan merusak autentikasi untuk semua orang.
- **DMARC membutuhkan SPF atau DKIM yang sudah lolos.** Atur ini terakhir, setelah SPF dan DKIM keduanya terverifikasi.

## Langkah 2: Gunakan identitas pengirim yang nyata

Setelah domain Anda terautentikasi, pastikan apa yang benar-benar dilihat penerima mendukungnya:

- **Alamat From** — gunakan alamat di domain terautentikasi Anda sendiri (`orders@yourstore.com`), jangan pernah gunakan alamat penyedia gratis (`yourstore@gmail.com`). Alamat From dari penyedia gratis tidak dapat diautentikasi sama sekali oleh rekaman SPF/DKIM/DMARC Anda, dan penyedia kotak masuk memperlakukannya sebagai sinyal spam yang kuat dari sebuah toko.
- **Nama From** — gunakan nama toko Anda yang mudah dikenali, bukan label generik seperti "Notifications" atau "No Reply."
- **Reply-to** — atur alamat yang dipantau. Alamat `noreply@` yang tidak dipantau dan memantulkan atau secara diam-diam membuang balasan itu sendiri merupakan sinyal reputasi ringan, dan menghalangi satu-satunya saluran yang dimiliki pelanggan untuk memberi tahu Anda jika ada yang salah.

Atur ketiga hal ini di bawah **Email Configuration > (akun Anda) > Sender Configuration** — lihat [Email Configuration](email-configuration) untuk penjelasan lengkap setiap bidang.

## Langkah 3: Lakukan pemanasan sebelum Anda memperluas skala

Domain atau IP tanpa riwayat pengiriman belum memiliki reputasi — baik atau buruk — dan penyedia kotak masuk bersikap hati-hati terhadap yang tidak diketahui. Mengirim ledakan besar pertama kali dari domain yang benar-benar baru secara statistik terlihat identik dengan spammer yang memulai kampanye baru, dan dapat masuk ke folder bulk meskipun semua kotak teknis sudah dicentang.

- Mulai lebih kecil. Kirim beberapa kampanye pertama Anda ke audiens yang paling terlibat dan paling mungkin membuka, bukan ke seluruh daftar Anda sekaligus — lihat [Audiences](audiences) untuk membangun segmen awal yang ditargetkan.
- Tingkatkan volume secara bertahap selama beberapa minggu pertama alih-alih langsung melompat ke pengiriman daftar penuh.
- Jika Anda memigrasikan daftar yang sudah ada dari platform lain, perlakukan itu sebagai hari pertama untuk keperluan reputasi juga — riwayat pengiriman platform lama Anda tidak berpindah bersama domain.

## Langkah 4: Jaga daftar Anda tetap bersih

Setiap keluhan atau pantulan mengorbankan reputasi Anda, dan keduanya sebagian besar merupakan fungsi dari siapa yang ada di daftar Anda dan bagaimana mereka sampai di sana:

- **Hanya kirim email kepada orang yang telah memberikan persetujuan.** Kontak yang diimpor, daftar yang dibeli, dan alamat yang dikumpulkan adalah cara tercepat untuk meningkatkan keluhan spam dan pantulan keras.
- **Gunakan double opt-in.** Alur persetujuan pemasaran Spwig memverifikasi alamat email pelanggan sebelum mengirim email pemasaran kepada mereka — lihat [Communication Preferences](communication-preferences) untuk cara ini dikonfigurasi.
- **Biarkan penekanan otomatis Spwig melakukan tugasnya.** Spwig memantau pantulan keras, keluhan spam, dan pantulan lunak berulang dan berhenti mengirim email ke alamat-alamat tersebut secara otomatis, tanpa perlu pengaturan — lihat [List Hygiene and Suppressions](list-hygiene) untuk persis bagaimana ini bekerja dan kapan (jarang) untuk menimpanya.
- **Potong pelanggan tidak aktif secara berkala** alih-alih mengirim email ke alamat yang tidak terlibat yang sama secara tak terbatas — daftar yang menyusut tetapi dibuka dan diklik lebih berharga untuk reputasi Anda daripada daftar besar yang tidak.

## Langkah 5: Pantau

Masalah ketercapaian (deliverability) terlihat dalam angka sebelum pelanggan memberi tahu Anda bahwa email tidak sampai.

Buka [Laporan](campaign-reports) kampanye setelah setiap pengiriman dan pantau:

| Metrik | Yang perlu diperhatikan |
|---|---|
| **Tingkat pantulan (bounce rate)** | Mayoritas pantulan lunak (soft bounce) adalah hal yang normal; peningkatan pangsa **pantulan keras (hard bounce)** berarti daftar Anda menumpuk alamat yang sudah kedaluwarsa atau tidak valid. |
| **Keluhan spam** | Seharusnya tetap mendekati nol pada setiap pengiriman. Jaga agar jauh di bawah ambang batas sekitar 0,3% yang memicu penegakan aturan pengirim massal di Gmail dan Yahoo — perlakukan bahkan lonjakan kecil sebagai hal yang perlu diselidiki segera. |
| **Tingkat pembukaan / tingkat klik-ke-pembukaan** | Penurunan tiba-tiba dan tidak terduga di seluruh pengiriman ke daftar yang sama (bukan hanya satu kampanye) bisa menjadi tanda awal bahwa email mendarat di folder spam alih-alih kotak masuk, bahkan sebelum angka pantulan atau keluhan bergerak. |

Periksa juga kartu **Alamat tertekan (Suppressed addresses)** di dasbor Campaign Studio secara berkala — aliran kecil yang stabil adalah peluruhan daftar yang normal, tetapi lonjakan tiba-tiba perlu diselidiki sebelum pengiriman berikutnya (lihat [Kebersihan Daftar](list-hygiene)).

![Kartu statistik Alamat tertekan di dasbor Campaign Studio](/static/core/admin/img/help/deliverability/suppressed-addresses-card.webp)

Jika ada yang melonjak: berhenti dan periksa apakah catatan DNS Anda masih valid terlebih dahulu (perpanjangan domain yang kedaluwarsa atau perubahan DNS yang tidak disengaja dapat merusak SPF/DKIM secara diam-diam), kemudian lihat apa yang berubah tentang konten atau audiens dari pengiriman yang memicu hal tersebut.

## Langkah 6: Kebersihan konten

Autentikasi dan kualitas daftar membuat Anda masuk pintu; konten tetap memengaruhi bagaimana Anda diperlakukan setelah berada di sana.

- **Hindari pola pemicu spam** di baris subjek — HURUF KAPITAL, tanda baca berlebihan ("!!!"), dan frasa seperti "bertindak sekarang" atau "uang gratis" tetap merugikan Anda di filter spam, bahkan dari domain yang terautentikasi.
- **Jangan mengirim email yang hanya berisi gambar.** Email yang berupa satu gambar tanpa teks asli adalah pola spam klasik; pertahankan jumlah konten teks yang bermakna di samping gambar apa pun.
- **Pratinjau sebelum mengirim.** Periksa bagaimana email sebenarnya dirender — termasuk di perangkat seluler — sebelum dikirim ke daftar lengkap Anda.
- **Tautan batal langganan sudah ditangani.** Spwig secara otomatis menambahkan tautan batal langganan yang berfungsi dan tidak memerlukan login ke bagian bawah setiap email pemasaran — Anda tidak perlu menambahkan tautan Anda sendiri (lihat [Preferensi Komunikasi](communication-preferences) untuk persis bagaimana alur itu bekerja). Jangan menghapus atau menyembunyikannya; tautan batal langganan yang hilang atau rusak sendiri merupakan pelanggaran kebijakan dengan aturan pengirim massal Gmail dan Yahoo, terlepas dari angka lainnya.

## "Email saya masuk ke spam" — daftar periksa pemecahan masalah

Lakukan ini secara berurutan:

1. **Periksa ulang catatan DNS Anda.** Buka langkah DNS wizard pengaturan akun (atau panel DKIM di halaman admin akun untuk SMTP bawaan) dan pastikan SPF, DKIM, dan DMARC semuanya masih menunjukkan lulus.

Perpanjangan domain, migrasi penyedia DNS, atau perubahan yang tidak terkait pada file zona Anda dapat merusak salah satu dari ini secara diam-diam.
2. **Periksa angka pantulan dan keluhan di laporan kampanye** untuk pengiriman yang terdampak — lihat [Laporan Kampanye](campaign-reports).


Lonjakan pada salah satu indikator menunjukkan masalah kualitas daftar atau konten, bukan masalah autentikasi.
3. **Periksa daftar Suppressions** ([List Hygiene](list-hygiene)) untuk lonjakan mendadak — jika sebagian besar daftar Anda telah gagal selama beberapa waktu, kemampuan pengiriman ke sisa daftar juga akan menurun.
4. **Pastikan alamat From Anda berada di domain yang terautentikasi**, bukan alamat penyedia gratis atau domain yang tidak cocok dengan yang telah diatur untuk SPF/DKIM/DMARC.
5. **Kirim email uji ke alamat Gmail dan Yahoo/Outlook yang Anda kendalikan** dan periksa folder sebenarnya tempat email tersebut mendarat, bukan hanya apakah email tersebut diterima.
6. **Jika Anda baru saja mengubah volume pengiriman atau audiens secara drastis,** perlakukan sebagai pemanasan baru — kurangi volume dan tingkatkan secara lebih bertahap.
7. **Jika semua hal di atas sudah benar dan masalah masih berlanjut,** ini mungkin merupakan pembatasan (throttling) yang spesifik pada penyedia, bukan kesalahan dalam pengaturan Anda — ini mungkin membutuhkan waktu untuk terselesaikan dengan sendirinya setelah penyebab utamanya (biasanya keluhan atau pantulan) diperbaiki.

## Tips

- Perbaiki autentikasi DNS sebelum memperbaiki hal lain — setiap tuas kemampuan pengiriman lainnya (konten, kebersihan daftar, pemanasan) menjadi kurang penting jika SPF/DKIM/DMARC tidak lolos.
- Perlakukan validasi DNS dari wizard pengaturan sebagai pemeriksaan pada waktu tertentu, bukan sekali saja — jalankan ulang setiap kali Anda memigrasikan penyedia DNS atau memperbarui domain melalui registrar yang berbeda.
- Daftar yang bersih dan dibuka serta diklik akan selalu lebih unggul daripada daftar yang lebih besar tetapi tidak — tahan godaan untuk mengimpor daftar lama yang tidak terverifikasi "hanya untuk berjaga-jaga."
- Perhatikan angka Anda relatif terhadap pengiriman masa lalu Anda sendiri, bukan benchmark industri generik — riwayat Anda sendiri adalah sinyal paling andal dari masalah nyata.
- Jika Anda menggunakan paket yang di-hosting oleh Spwig, penandatanganan DKIM dan manajemen reputasi dari gerbang email yang di-hosting ditangani untuk Anda — tanggung jawab Anda yang tersisa adalah kualitas daftar dan konten, bukan DNS.
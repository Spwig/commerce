---
title: Runbook Ketercapaian Email
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Step 4 (DNS Configuration) of the email account setup wizard for the built-in SMTP provider, showing the SPF/DKIM/DMARC validation one-liners and the DNS provider tabs (Cloudflare/GoDaddy/Namecheap/Route 53/Other) with at least one record's "Details" panel expanded so a copyable TXT record is visible.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: An existing built-in SMTP EmailAccount's change form scrolled to the "DKIM keys configured" panel, showing the DNS TXT record Name/Value and the Copy DNS Record button.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: The Campaign Studio dashboard's Suppressed addresses stat card, for the "monitor" section of this runbook.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Mengirim email *berhasil* itu mudah. Memastikan email masuk ke kotak masuk (inbox) dan bukan folder spam adalah pekerjaan sebenarnya — dan penyedia kotak masuk seperti Gmail dan Yahoo sekarang menerapkan persyaratan teknis yang ketat sebelum mereka mempertimbangkannya. Runbook ini membahas apa yang harus dikonfigurasi, dalam urutan apa, agar konfirmasi pesanan dan kampanye Anda sampai ke tempat yang bisa dilihat oleh pelanggan.

Tidak ada yang bersifat tugas sekali jalan di sini. Ketercapaian adalah reputasi yang Anda bangun seiring waktu dan bisa hilang dengan cepat — daftar periksa di akhir dokumen ini layak ditinjau kembali kapan pun ada sesuatu yang terlihat tidak beres.

## Mengapa ini penting

Setiap penyedia kotak masuk utama menilai email masuk berdasarkan reputasi pengirim sebelum memutuskan apakah akan mengirimkannya, melipatnya ke folder spam, atau menolaknya secara langsung. Sejak 2024, Gmail dan Yahoo telah memformalkan ini menjadi **persyaratan pengirim massal** yang eksplisit untuk siapa pun yang mengirim volume yang signifikan:

- **Autentikasi domain Anda** — catatan SPF, DKIM, dan DMARC yang valid.
- **Mudah untuk berhenti berlangganan** — opt-out yang berfungsi dan minim hambatan di setiap email pemasaran.
- **Jaga keluhan spam tetap rendah** — pengirim massal yang melampaui sekitar 0,3% keluhan berisiko memiliki email ditolak atau dipindahkan ke folder massal; target teraman adalah jauh di bawah 0,1%.

Gagal memenuhi ini tidak hanya memengaruhi kampanye pemasaran — reputasi domain yang rusak dapat menyeret email transaksional (konfirmasi pesanan, reset kata sandi) ke spam juga, karena Gmail dan Yahoo semakin menilai reputasi pada tingkat domain pengirim, bukan hanya per jenis pesan. Langkah-langkah di bawah ini adalah cara Anda memenuhi ketiga persyaratan tersebut.

## Langkah 1: Autentikasi domain pengirim Anda

SPF, DKIM, dan DMARC adalah catatan DNS TXT yang membuktikan kepada server email penerima bahwa email yang diklaim berasal dari domain Anda benar-benar dikirim oleh Anda. Cara Anda mengaturnya bergantung pada mode pengiriman yang digunakan oleh toko Anda — ketiganya dikonfigurasi di bawah **Email Configuration** di bilah sisi admin (ini membuka daftar Email Accounts; lihat [Email Configuration](email-configuration) untuk panduan lengkap pengaturan akun).

| Mode Pengiriman | Bagaimana otorisasi bekerja |
|---|---|
| **SMTP Bawaan** (server email milik Spwig sendiri) | Spwig secara otomatis menghasilkan pasangan kunci DKIM untuk domain Anda. Tambahkan akun email, dan **Langkah 4** wizard penyiapan menunjukkan status SPF, DKIM, dan DMARC Anda serta catatan yang tepat untuk ditambahkan, dengan salin-tempel dan petunjuk khusus penyedia untuk Cloudflare, GoDaddy, Namecheap, dan AWS Route 53. Catatan DKIM DNS yang sama juga ditampilkan di halaman admin sendiri dari akun tersebut nanti, di bawah **Kunci DKIM yang dikonfigurasi**, jika Anda perlu mencarinya lagi. |
| **SMTP Umum** (penyedia pihak ketiga seperti SendGrid, Mailgun, Amazon SES, atau Google Workspace, yang terhubung melalui kredensial SMTP) | Otorisasi terjadi sebagian di dashboard penyedia masing-masing. Tahap DNS wizard penyiapan termasuk petunjuk berpita untuk Gmail, Outlook, SendGrid, Mailgun, dan Amazon SES secara khusus — masing-masing menjelaskan apa yang perlu dikonfigurasi di konsol penyedia (misalnya, memverifikasi domain pengiriman di SendGrid) dan catatan DNS mana yang perlu ditambahkan di penyedia DNS Anda. |
| **Pintu masuk email yang dikelola oleh Spwig** | Tersedia pada rencana Spwig-hosted sebagai opsi pengiriman yang dikelola. Ini menandatangani email keluar dengan DKIM secara otomatis dan defaultnya mengirim dari alamat pada domain diverifikasi Spwig sendiri, jadi bekerja dengan nol penyiapan. Jika Anda ingin mengirim dari domain Anda sendiri melalui pintu masuk ini, bicaralah dengan penyedia layanan hosting Anda tentang verifikasi domain tersebut — ini adalah layanan yang dikelola, bukan alur DNS self-serve. |

Apapun mode yang Anda gunakan, **menambahkan catatan DNS itu sendiri selalu menjadi langkah eksternal** — Anda melakukannya di penyedia registrar domain atau DNS Anda (Cloudflare, GoDaddy, Namecheap, Route 53, atau mana pun domain Anda menunjuk ke nameserver-nya), bukan di dalam Spwig. Spwig dapat memberi tahu Anda secara tepat apa yang perlu ditambahkan dan memvalidasi bahwa catatan tersebut sudah aktif, tetapi tidak bisa mencapai ke penyedia registrasi Anda dan menambahkannya untuk Anda.

Beberapa hal yang patut diketahui sebelum memulai:

- **Perubahan DNS tidak instan.** Propagasi bisa memakan waktu dari beberapa menit hingga 48 jam. Tahap validasi wizard akan menunjukkan catatan sebagai gagal atau tidak ada sampai sebenarnya telah tersebar — ini wajar, bukan tanda sesuatu yang salah.
- **Hanya satu catatan SPF yang diizinkan per domain.** Jika Anda sudah memiliki satu (dari Google Workspace, pengirim lain, dll.), tambahkan pengirim baru ke catatan yang sudah ada dengan `include:` daripada membuat catatan TXT SPF kedua — dua catatan SPF akan merusak otorisasi untuk semua orang.
- **DMARC membutuhkan SPF atau DKIM yang sudah lulus.** Atur terakhir, setelah SPF dan DKIM keduanya diverifikasi.

## Langkah 2: Gunakan identitas pengiriman nyata

Setelah domain Anda diverifikasi, pastikan apa yang dilihat penerima benar-benar mendukungnya:

- **Alamat Pengirim** — gunakan alamat pada domain yang diverifikasi Anda (`orders@yourstore.com`), jangan pernah menggunakan alamat dari penyedia gratis (`yourstore@gmail.com`). Alamat pengirim dari penyedia gratis tidak dapat diverifikasi sama sekali oleh catatan SPF/DKIM/DMARC Anda, dan penyedia kotak masuk menganggapnya sebagai tanda spam kuat dari toko.
- **Nama Pengirim** — gunakan nama toko yang dikenali, bukan label umum seperti "Notifikasi" atau "Tidak Ada Balasan."
- **Balas ke** — atur alamat yang terpantau. Alamat `noreply@` yang tidak terpantau yang memantul atau secara diam-diam menghapus balasan itu sendiri merupakan indikasi reputasi yang rendah, dan menghalangi saluran satu-satunya pelanggan untuk memberi tahu Anda sesuatu yang salah.

Atur ketiga hal tersebut di bawah **Konfigurasi Email > (akun Anda) > Konfigurasi Pengirim** — lihat [Konfigurasi Email](email-configuration) untuk penjelasan lengkap mengenai bidang-bidangnya.

## Langkah 3: Panaskan sebelum memperluas

Domain atau IP dengan riwayat pengiriman tidak memiliki reputasi sama sekali — baik atau buruk — dan penyedia kotak masuk waspada terhadap yang tidak dikenal. Mengirimkan ledakan pertama yang besar dari domain baru terlihat statistik sama dengan penipu yang memulai kampanye baru, dan bisa masuk ke folder sampah bahkan meskipun semua kotak teknis sudah terisi dengan benar.

- Mulailah dengan ukuran yang lebih kecil.

Kirim beberapa kampanye pertama Anda ke audiens yang paling terlibat dan paling mungkin membuka email, bukan ke seluruh daftar sekaligus — lihat [Audiens](audiences) untuk membangun segmen awal yang ditargetkan.
- Tingkatkan volume secara bertahap selama beberapa minggu pertama, bukan langsung melompat ke pengiriman ke seluruh daftar.
- Jika Anda memigrasikan daftar yang sudah ada dari platform lain, perlakukan itu sebagai hari pertama untuk tujuan reputasi juga — riwayat pengiriman platform lama Anda tidak berpindah bersama domain.

## Langkah 4: Jaga daftar Anda tetap bersih

Setiap keluhan atau pantulan (bounce) merugikan reputasi Anda, dan keduanya sebagian besar bergantung pada siapa yang ada di daftar Anda dan bagaimana mereka masuk ke sana:

- **Hanya kirim email kepada orang yang telah memberikan persetujuan.** Kontak yang diimpor, daftar yang dibeli, dan alamat yang dikumpulkan secara paksa adalah cara tercepat untuk memicu lonjakan keluhan spam dan pantulan keras (hard bounces).
- **Gunakan double opt-in.** Alur persetujuan pemasaran Spwig memverifikasi alamat email pelanggan sebelum mengirimkan email pemasaran kepada mereka — lihat [Preferensi Komunikasi](communication-preferences) untuk cara konfigurasinya.
- **Biarkan penekanan otomatis (suppression) Spwig bekerja.** Spwig memantau pantulan keras, keluhan spam, dan pantulan lunak (soft bounces) yang berulang, lalu berhenti mengirimkan email ke alamat-alamat tersebut secara otomatis, tanpa perlu pengaturan — lihat [Kebersihan Daftar dan Penekanan](list-hygiene) untuk penjelasan tepat tentang cara kerjanya dan kapan (jarang) Anda perlu menimbulkannya.
- **Bersihkan pelanggan tidak aktif secara berkala** daripada terus-menerus mengirimkan email ke alamat yang tidak terlibat — daftar yang menyusut tetapi memiliki tingkat pembukaan dan klik yang tinggi lebih berharga bagi reputasi Anda daripada daftar besar yang tidak.

## Langkah 5: Pantau

Masalah keterjangkauan (deliverability) muncul dalam angka sebelum pelanggan memberi tahu Anda bahwa email tidak sampai.

Buka [Laporan](campaign-reports) kampanye setelah setiap pengiriman dan perhatikan:

| Metrik | Yang perlu diperhatikan |
|---|---|
| **Tingkat pantulan (Bounce rate)** | Sebagian besar pantulan lunak (soft bounces) adalah hal yang normal; peningkatan pangsa **pantulan keras (hard bounces)** berarti daftar Anda menumpuk alamat yang kedaluwarsa atau tidak valid. |
| **Keluhan spam** | Seharusnya tetap mendekati nol pada setiap pengiriman. Jaga agar jauh di bawah ambang batas sekitar 0,3% yang memicu penegakan aturan pengirim massal di Gmail dan Yahoo — perlakukan bahkan lonjakan kecil sebagai hal yang perlu diselidiki segera. |
| **Tingkat pembukaan / tingkat klik-ke-pembukaan** | Penurunan tiba-tiba dan tidak terduga di antara pengiriman ke daftar yang sama (bukan hanya satu kampanye) bisa menjadi tanda awal bahwa email mendarat di folder spam alih-alih kotak masuk, bahkan sebelum angka pantulan atau keluhan berubah. |

Periksa juga kartu **Alamat ditekan (Suppressed addresses)** di dasbor Campaign Studio secara berkala — aliran yang stabil adalah keausan daftar yang normal, tetapi lonjakan tiba-tiba perlu diselidiki sebelum pengiriman berikutnya (lihat [Kebersihan Daftar](list-hygiene)).

Jika sesuatu melonjak: jeda dan periksa apakah catatan DNS Anda masih valid terlebih dahulu (perpanjangan domain yang kedaluwarsa atau perubahan DNS yang tidak disengaja dapat merusak SPF/DKIM secara diam-diam), lalu lihat apa yang berubah tentang konten atau audiens pengiriman yang memicu hal tersebut.

## Langkah 6: Kebersihan konten

Autentikasi dan kualitas daftar membuat Anda masuk ke pintu; konten masih memengaruhi bagaimana Anda diperlakukan setelah di sana.

- **Hindari pola pemicu spam** di baris subjek — HURUF BESAR, tanda baca berlebihan ("!!!"), dan frasa seperti "bertindak sekarang" atau "uang gratis" masih merugikan Anda dengan filter spam, bahkan dari domain yang terautentikasi.
- **Jangan kirim email yang hanya berisi gambar.** Email yang berupa satu gambar tanpa teks asli adalah pola spam klasik; pertahankan jumlah konten teks yang bermakna di samping gambar apa pun.
- **Pratinjau sebelum mengirim.** Periksa bagaimana email sebenarnya dirender — termasuk di perangkat seluler — sebelum dikirim ke daftar lengkap Anda.
- **Tautan batal langganan sudah ditangani.** Spwig secara otomatis menambahkan tautan batal langganan yang berfungsi dan tidak memerlukan login ke bagian bawah setiap email pemasaran — Anda tidak perlu menambahkan tautan Anda sendiri (lihat [Preferensi Komunikasi](communication-preferences) untuk penjelasan tepat tentang cara kerja alur tersebut). Jangan menghapus atau menyembunyikannya; tautan batal langganan yang hilang atau rusak sendiri merupakan pelanggaran kebijakan dengan aturan pengirim massal Gmail dan Yahoo, terlepas dari angka lainnya.


## ''Email saya masuk ke kotak sampah'' — daftar periksa penyelesaian masalah

Lakukan langkah-langkah berikut secara berurutan:

1. **Periksa kembali catatan DNS Anda.** Buka wizard setup akun langkah DNS (atau panel DKIM pada halaman admin akun untuk SMTP bawaan) dan pastikan SPF, DKIM, dan DMARC semuanya masih menunjukkan status lulus. Pengecekan ulang domain, migrasi penyedia DNS, atau perubahan tidak terkait lainnya pada file zona Anda dapat secara diam-diam merusak salah satu dari tiga hal tersebut.
2. **Periksa jumlah bounce dan keluhan pada laporan kampanye** untuk pengiriman yang terkena dampak — lihat [Laporan Kampanye](campaign-reports). Lonjakan pada keduanya menunjukkan masalah kualitas daftar atau konten, bukan masalah otorisasi.
3. **Periksa daftar penangguhan** ([Kebersihan Daftar](list-hygiene)) untuk lonjakan tajam — jika sebagian besar daftar Anda gagal dalam jangka waktu lama, kinerja pengiriman ke yang lainnya juga akan menurun.
4. **Pastikan alamat From Anda berada pada domain yang diverifikasi**, bukan alamat dari penyedia gratis atau domain yang tidak sesuai dengan yang telah diatur untuk SPF/DKIM/DMARC.
5. **Kirimkan email uji ke alamat Gmail dan Yahoo/Outlook yang Anda kendalikan** dan periksa folder tempat email tersebut sampai, bukan hanya sekadar apakah email tersebut tiba.
6. **Jika Anda baru-baru ini mengubah volume pengiriman atau audiens secara tajam,** anggaplah ini sebagai pemanasan ulang — turunkan volume secara perlahan dan tingkatkan kembali secara bertahap.
7. **Jika semua di atas sudah dicek dan masalahnya tetap ada,** kemungkinan besar ini adalah pembatasan dari penyedia layanan, bukan kesalahan dalam setup Anda — hal ini bisa memakan waktu untuk diselesaikan sendiri setelah penyebab mendasar (biasanya keluhan atau bounce) telah diperbaiki.

## Tips

- Perbaiki otorisasi DNS sebelum memperbaiki hal lainnya — setiap opsi pengiriman lainnya (konten, kebersihan daftar, pemanasan) kurang penting jika SPF/DKIM/DMARC tidak lulus.
- Pertimbangkan validasi DNS wizard setup sebagai pemeriksaan titik waktu, bukan satu kali — jalankan kembali jika Anda bermigrasi ke penyedia DNS baru atau merekayasa ulang domain melalui pendaftar yang berbeda.
- Daftar yang bersih yang terbuka dan diklik akan selalu unggul dibandingkan daftar yang lebih besar tetapi tidak terbuka — tahanlah keinginan untuk mengimpor daftar lama yang tidak diverifikasi "hanya sekadar dalam keadaan darurat".
- Pantau angka Anda secara relatif terhadap pengiriman sebelumnya, bukan benchmark industri umum — riwayat Anda sendiri adalah indikator terpercaya dari masalah nyata.
- Jika Anda berada pada rencana yang dihosting oleh Spwig, tanda tangan DKIM dan pengelolaan reputasi gateway email yang dihosting akan ditangani untuk Anda — tanggung jawab tersisa adalah kualitas daftar dan konten, bukan DNS.
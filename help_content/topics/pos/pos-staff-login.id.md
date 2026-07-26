---
title: Login Pegawai POS & Masuk dengan Biometrik
---

Setiap orang yang melayani pelanggan di meja POS membutuhkan akun pegawai dengan izin yang tepat. Topik ini menjelaskan cara membuat akun tersebut, menetapkan pegawai ke terminal, dan kemudian mengatur masuk dengan biometrik sehingga mereka dapat membuka kunci meja dengan sidik jari, pemindaian wajah, atau kunci perangkat keras alih-alih mengetikkan kata sandi setiap kali.

Untuk kode PIN, batasan diskon, dan pengaturan kunci terminal, lihat [Diskon Pegawai POS & Keamanan Terminal](pos-staff-discounts).

## Apa yang dibutuhkan pegawai untuk menggunakan terminal POS

Untuk masuk ke terminal POS, seseorang membutuhkan:

1. **Akun pegawai** — pengguna Spwig dengan **status pegawai** yang dicentang.
2. **Peran yang mencakup akses POS** — peran mengontrol apa yang dapat dilakukan pegawai di dalam admin. Peran dengan izin POS diperlukan untuk mengakses meja.
3. **Penugasan ke terminal** — terminal harus mencantumkan mereka sebagai pegawai yang ditugaskan, atau mereka harus ditugaskan di tingkat lokasi toko.

## Membuat akun pegawai yang layak untuk POS

Navigasikan ke **Pegawai & Akun > Anggota Pegawai** (atau pergi ke `/admin/accounts/staffmember/`).

1. Klik **+ Tambahkan Anggota Pegawai**.
2. Isi **nama depan**, **nama belakang**, dan **alamat email** pegawai.
3. Tetapkan kata sandi sementara dan minta pegawai untuk mengubahnya saat login pertama.
4. Pastikan **status pegawai** dicentang — ini yang memungkinkan mereka untuk masuk ke admin dan aplikasi POS.
5. Klik **Simpan**.

> **Catatan:** Jangan centang **status superuser** untuk kasir biasa atau supervisor. Status superuser melewati semua pemeriksaan izin dan sebaiknya disisihkan untuk pemilik toko.

### Menetapkan peran dengan akses POS

Akun pegawai sendiri tidak memiliki izin — peran memberikan kemampuan spesifik. Setelah membuat akun, buka catatan pegawai dan pergi ke bagian **Peran**. Tetapkan peran yang mencakup akses POS.

Untuk penjelasan lengkap tentang cara kerja peran dan izin yang harus dimasukkan, lihat [Peran Pegawai](staff-roles).

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: Daftar pegawai menampilkan pengguna yang layak untuk POS dengan badge peran mereka
-->

![Daftar pegawai](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Menetapkan pegawai ke terminal

Pengaturan mengikuti cascading: **default situs → kelompok toko → lokasi toko → terminal individu**. Untuk sebagian besar toko, tempat yang tepat untuk menetapkan pegawai adalah di tingkat terminal.

1. Navigasikan ke **POS > Terminal** (atau pergi ke `/admin/pos_app/posterminal/`).
2. Buka terminal yang ingin dikonfigurasikan.
3. Pergi ke tab **Penugasan Pegawai**.
4. Di bidang **Pegawai yang ditugaskan**, cari dan tambahkan pegawai.
5. Klik **Simpan**.

Pegawai yang muncul dalam daftar **Pegawai yang ditugaskan** untuk terminal dapat memilih nama mereka di layar login terminal tersebut. Pegawai yang tidak ditugaskan ke terminal mana pun masih dapat masuk dengan mengetikkan email mereka secara langsung.

> **Tips:** Jika toko Anda memiliki banyak pegawai yang berpindah-pindah antar terminal, tetapkan mereka di tingkat lokasi toko (gudang) alih-alih terminal demi terminal. Setiap pegawai yang ditugaskan ke lokasi secara otomatis memiliki akses ke semua terminal di lokasi tersebut.

## Masuk di meja POS

Ketika kasir membuka aplikasi POS (`/pos/`) di terminal, mereka melihat layar pemilihan pegawai. Alur login bekerja sebagai berikut:

1. Kasir mengetuk atau mengklik nama mereka di daftar (atau mengetikkan email mereka jika tidak terdaftar).
2. Mereka memasukkan kata sandi mereka.
3. Mereka masuk dan meja terbuka untuk shift mereka.

Untuk membuka kunci berbasis PIN (setelah terminal terkunci selama shift), lihat [Diskon Pegawai POS & Keamanan Terminal](pos-staff-discounts).

## Masuk dengan biometrik

Masuk dengan biometrik memungkinkan kasir menyentuh sensor sidik jari, melihat kamera wajah, atau mengetuk kunci perangkat keras alih-alih mengetikkan kata sandi. Di meja yang sibuk ini menghemat beberapa detik per shift dan menghindari kesalahan selama jam sibuk.

Spwig menggunakan standar browser **WebAuthn** untuk masuk dengan biometrik.

"Kredensial WebAuthn" adalah pasangan kunci yang terikat perangkat: kunci privat disimpan di perangkat keras aman perangkat dan tidak pernah meninggalkannya.

Aplikasi POS berkomunikasi dengan perangkat keras tersebut melalui browser.

### Perangkat dan browser yang mendukung masuk dengan biometrik

WebAuthn didukung oleh semua browser modern — Chrome, Edge, Firefox, dan Safari — pada perangkat yang memiliki perangkat keras yang kompatibel. Konfigurasi umum yang bekerja dengan baik:

| Perangkat | Authenticator |
|--------|---------------|
| iPad (Touch ID) | Sidik jari melalui Safari atau Chrome |
| Tablet Android | Sidik jari atau wajah melalui Chrome |
| Tablet atau PC Windows | Windows Hello (sidik jari, wajah, atau PIN) |
| Setiap perangkat + kunci keamanan | Kunci FIDO2 USB, NFC, atau Bluetooth (misalnya YubiKey) |
| iPhone (Face ID) | Wajah melalui Safari |

Aplikasi POS hanya akan menampilkan opsi masuk dengan biometrik ketika browser telah memverifikasi bahwa kredensial telah didaftarkan untuk pengguna saat ini di perangkat tersebut.

### Cara pendaftaran berlangsung

Pendaftaran terjadi di terminal POS, bukan di admin. Anggota staf harus menyelesaikan masuk dengan kata sandi normal terlebih dahulu, lalu memilih untuk mengatur masuk dengan biometrik dari dalam aplikasi POS. Browser kemudian meminta mereka untuk memverifikasi identitas mereka menggunakan sensor biometrik perangkat (atau passkey yang disimpan di akun mereka di iOS/macOS/Windows). Setelah dikonfirmasi, kredensial disimpan dan masuk dengan biometrik tersedia untuk shift mendatang di perangkat tersebut.

Seorang anggota staf dapat mendaftarkan di beberapa perangkat — misalnya, tablet pribadi dan register bersama — dan setiap perangkat menyimpan kredensialnya sendiri.

> **Catatan:** Kata-kata persis dari prompt pendaftaran ("Daftarkan biometrik", "Atur masuk dengan sidik jari", dll.) berasal dari aplikasi POS dan mungkin bervariasi berdasarkan browser dan perangkat.

### Masuk dengan biometrik

Setelah didaftarkan, nama kasir di layar masuk akan menampilkan tombol masuk dengan biometrik (ikon sidik jari atau yang serupa). Kasir:

1. Menyentuh nama mereka di layar masuk terminal.
2. Menyentuh **Masuk dengan sidik jari** (atau yang setara).
3. Menyentuh sensor atau melihat kamera.
4. Terminal langsung terbuka.

Jika verifikasi biometrik gagal (sidik jari tidak dikenali, wajah tertutup), kasir kembali ke masuk dengan memasukkan kata sandi mereka.

### Membatalkan kredensial

Jika perangkat hilang, dicuri, atau anggota staf meninggalkan, Anda harus segera menghapus kredensial biometrik mereka.

1. Navigasikan ke **Staff & Accounts > Staff Members**.
2. Buka catatan anggota staf.
3. Gulir ke bagian **POS Settings**.
4. Di baris **Biometric Unlock**, klik **Remove All**.
5. Konfirmasi tindakan tersebut.

Ini menghapus semua kredensial WebAuthn yang didaftarkan untuk anggota staf tersebut di setiap perangkat. Kali berikutnya mereka mencoba menggunakan masuk dengan biometrik di terminal mana pun, mereka akan diminta untuk masuk dengan kata sandi mereka.

> **Penting:** Menghapus kredensial di sini tidak menghalangi anggota staf dari masuk dengan kata sandi mereka. Untuk membatalkan akses secara penuh, juga nonaktifkan akun staf mereka atau hapus mereka dari daftar staf yang ditugaskan ke terminal.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Form perubahan anggota staf yang menampilkan bagian POS Settings dengan jumlah kredensial biometrik dan tombol Remove All
-->

## Catatan keamanan

- **Kredensial terikat perangkat.** Kunci privat tidak pernah meninggalkan elemen aman perangkat.

Jika tablet dicuri, pelaku tidak dapat mengekstrak kunci biometrik — mereka masih memerlukan mengatasi layar kunci perangkat sebelum browser melepaskan kunci tersebut.
- **Kehilangan perangkat tidak menyebabkan kebocoran kata sandi.** WebAuthn menggantikan kata sandi untuk perangkat tersebut; kata sandi staf tetap terpisah dan tidak terpengaruh.
- **Batalkan dengan segera saat staf meninggalkan perusahaan.** Hapus kredensial biometrik dan nonaktifkan akun staf dalam sesi yang sama saat mengakhiri masa kerja staf.
- **Data biometrik itu sendiri tidak pernah dikirimkan.** Sidik jari atau pemindaian wajah diproses sepenuhnya oleh perangkat keras perangkat.

Spwig hanya menerima respons tantangan yang ditandatangani, bukan data biometrik apa pun.

## Penyelesaian Masalah

### Tombol "Masuk dengan sidik jari" tidak muncul

Opsi biometrik hanya muncul ketika:
- Staf memiliki kredensial yang terdaftar di perangkat ini.
- Browser mendukung WebAuthn (semua browser modern mendukung — perbarui jika menggunakan versi lama).

Jika tombol tidak muncul, staf belum mendaftar di perangkat ini. Mereka harus masuk dengan kata sandi mereka dan mengatur masuk dengan biometrik melalui aplikasi POS.

### Pendaftaran gagal

Alasan umum:
- **Izin browser ditolak.** Browser meminta izin untuk mengakses autentikator dan staf menolak. Mereka perlu mencoba lagi dan mengetuk **Izinkan** saat diminta.
- **Tidak ditemukan autentikator yang kompatibel.** Perangkat tidak memiliki sensor sidik jari, kamera wajah, atau kunci keamanan yang terhubung. Periksa perangkat keras perangkat.
- **Kredensial duplikat.** Staf mungkin sudah mendaftar di perangkat ini. Kredensial yang sudah ada dikecualikan selama pendaftaran ulang untuk menghindari duplikat.

### Biometrik bekerja di satu perangkat tetapi tidak di perangkat lain

Setiap perangkat menyimpan kredensialnya sendiri. Mendaftar di iPad tidak secara otomatis bekerja di iPad kedua. Staf harus menyelesaikan pendaftaran secara terpisah di setiap perangkat yang akan mereka gunakan.

### Passkey lintas perangkat

Beberapa sistem operasi (iOS 16+, macOS Ventura+, Windows 11 dengan akun Microsoft) dapat menyinkronkan passkey lintas perangkat melalui iCloud Keychain atau Windows Hello. Jika staf mendaftar menggunakan passkey yang disinkronkan, mungkin bekerja secara otomatis di beberapa perangkat. Perilaku bergantung pada sistem operasi dan browser, bukan Spwig.

## Tips

- Atur masuk dengan biometrik di mesin kasir yang dibagikan sebelum staf tiba untuk shift mereka — proses pendaftaran dua menit jauh lebih mulus dilakukan tanpa pelanggan menunggu.
- Berikan peran dengan izin POS terbatas kepada kasir dan peran manajer terpisah kepada supervisor. Pertahankan akun mereka terpisah dari akun pemilik toko.
- Ketika staf mengganti perangkat (tablet baru, ponsel baru), mintalah mereka mendaftar di perangkat baru terlebih dahulu, lalu batalkan kredensial lama dari admin jika perangkat tidak lagi digunakan.
- Untuk toko dengan tingkat pergantian staf yang tinggi, tinjau daftar **Staf yang ditugaskan** di setiap terminal secara berkala dan hapus staf yang tidak lagi bekerja di lokasi tersebut.
- Jika Anda menggunakan kunci keamanan perangkat keras (YubiKey atau yang serupa), satu kunci dapat didaftarkan di beberapa terminal tanpa perubahan apa pun di admin — cukup colokkan kunci tersebut dan lengkapi pendaftaran di setiap terminal.
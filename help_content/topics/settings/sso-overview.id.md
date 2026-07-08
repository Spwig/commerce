---
title: Single Sign-On (SSO) Admin
---

Single Sign-On (SSO) memungkinkan staf Anda untuk masuk ke panel admin menggunakan penyedia identitas organisasi Anda, bukan nama pengguna dan kata sandi terpisah. Spwig mendukung penyedia identitas apa pun yang menggunakan protokol OpenID Connect (OIDC), termasuk Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, dan lainnya.

## Apa Itu Enterprise SSO?

Enterprise SSO berbeda dari login sosial (masuk dengan akun Google atau Facebook pribadi). Dengan Enterprise SSO:

- Staf mengautentikasi melalui **penyedia identitas organisasi** — sistem yang sama yang mereka gunakan untuk email, alat internal, dan aplikasi bisnis lainnya
- Tim IT Anda mengontrol akses secara terpusat — ketika seseorang meninggalkan organisasi, menonaktifkan akun mereka di penyedia identitas akan segera membatalkan akses mereka ke Spwig
- Autentikasi multi-faktor (MFA) diterapkan oleh penyedia identitas, memberi Anda kebijakan keamanan yang konsisten di semua aplikasi
- Staf tidak perlu mengingat kata sandi terpisah untuk Spwig

## Cara Kerjanya

Ketika SSO diaktifkan, halaman login admin menampilkan tombol **Masuk dengan [Penyedia]**. Alur autentikasi bekerja seperti ini:

1. Anggota staf mengklik tombol SSO di halaman login Spwig
2. Mereka dialihkan ke halaman login penyedia identitas Anda (misalnya, login Microsoft)
3. Mereka mengautentikasi dengan penyedia identitas (termasuk MFA yang diperlukan oleh penyedia)
4. Penyedia identitas mengarahkan mereka kembali ke Spwig dengan kode otorisasi yang aman
5. Spwig menukar kode tersebut untuk informasi pengguna dan membuat sesi
6. Anggota staf tiba di dashboard admin, sepenuhnya terautentikasi

Ini menggunakan protokol **OpenID Connect (OIDC)** standar industri, yang didukung oleh hampir semua penyedia identitas perusahaan.

## Mengaktifkan SSO

SSO dikonfigurasi di dua tempat:

1. **Pengaturan Situs > Tab Keamanan** — Aktifkan atau nonaktifkan SSO dan kendalikan visibilitas login kata sandi
2. **Konfigurasi Penyedia SSO** — Masukkan detail OIDC penyedia identitas Anda

### Langkah 1: Konfigurasikan penyedia identitas Anda

Sebelum mengaktifkan SSO di Spwig, Anda perlu mendaftarkan Spwig sebagai aplikasi di penyedia identitas Anda. Lihat panduan spesifik penyedia:

- **Microsoft Entra ID** — lihat panduan pengaturan Microsoft Entra ID
- **Google Workspace** — lihat panduan pengaturan Google Workspace
- **Okta** — lihat panduan pengaturan Okta
- **Penyedia lain** — penyedia OIDC apa pun yang sesuai. Daftarkan aplikasi web dengan URI pengalihan `https://your-store.com/oidc/callback/` dan konsultasikan dokumentasi penyedia Anda untuk URL OIDC Discovery, Client ID, dan Client Secret.

### Langkah 2: Konfigurasikan Penyedia SSO di Spwig

Navigasikan ke halaman **Konfigurasi Penyedia SSO** (terkait dari tab Keamanan atau dapat diakses di **Enterprise SSO > Konfigurasi Penyedia SSO** di bilah sisi admin). Masukkan:

1. **Nama Penyedia** — ditampilkan pada tombol login (misalnya, "Microsoft Entra ID")
2. **URL OIDC Discovery** — URL `.well-known/openid-configuration` penyedia Anda. Klik **Auto-Discover** untuk mengisi otomatis bidang endpoint.
3. **Client ID** dan **Client Secret** — dari pendaftaran aplikasi penyedia identitas Anda

Client secret disimpan dalam bentuk terenkripsi dan tidak pernah ditampilkan setelah disimpan.

### Langkah 3: Aktifkan SSO di Pengaturan Situs

Navigasikan ke **Pengaturan Situs > Tab Keamanan** dan centang **Aktifkan SSO untuk login admin**. Tombol SSO akan segera muncul di halaman login admin.

## Pengaturan SSO

| Pengaturan | Deskripsi |
|---------|-------------|
| **Aktifkan SSO untuk login admin** | Menampilkan tombol SSO di halaman login admin. Tidak memengaruhi login kata sandi biasa kecuali Anda juga menonaktifkannya. |
| **Izinkan login kata sandi di halaman admin** | Ketika tidak dicentang, formulir kata sandi disembunyikan di balik toggle yang dapat dikembangkan. Staf hanya melihat tombol SSO secara default. Formulir kata sandi masih dapat diakses dengan mengklik "Masuk dengan akun lokal" atau dengan menambahkan `?password=1` ke URL login. |

### Perilaku Halaman Login

| SSO Diaktifkan | Login dengan Kata Sandi | Hasil |
|-------------|---------------|--------|
| Off | On | Halaman login standar dengan formulir username/kata sandi saja |
| On | On | Tombol SSO di bagian atas, pemisah "atau", lalu formulir kata sandi di bawah |
| On | Off | Hanya tombol SSO. Formulir kata sandi berada di balik toggle "Masuk dengan akun lokal" |
| Off | Off | Tidak mungkin — login dengan kata sandi secara otomatis diaktifkan kembali jika SSO dinonaktifkan atau tidak dikonfigurasi |

## Pemetaan Pengguna

Ketika seorang staf masuk melalui SSO, Spwig memetakan mereka ke akun pengguna yang sudah ada dengan **alamat email** (tidak memperhatikan huruf besar-kecil). Email dari klaim penyedia identitas harus cocok dengan email pada akun staf Spwig.

Jika tidak ditemukan pengguna yang cocok:

- **Auto-Buat Pengguna dinonaktifkan** (default) — login ditolak. Anda harus membuat akun staf di Spwig terlebih dahulu dengan alamat email yang cocok.
- **Auto-Buat Pengguna diaktifkan** — akun pengguna baru dibuat secara otomatis dengan nama dan email dari klaim penyedia identitas.

Pengaturan **Batas ke Staf** (diaktifkan secara default) menambahkan pengecekan tambahan: bahkan jika akun pengguna ada, login akan ditolak kecuali pengguna memiliki status staf. Ini mencegah akun non-staf mengakses panel admin melalui SSO.

## Pemetaan Peran

Jika penyedia identitas Anda mengirimkan informasi keanggotaan grup dalam klaim OIDC, Spwig dapat secara otomatis menetapkan status staf dan superuser berdasarkan keanggotaan grup.

Untuk mengonfigurasi pemetaan peran:

1. Di Konfigurasi Penyedia SSO, atur bidang **Klaim Grup** ke nama klaim yang digunakan oleh penyedia Anda (default: `groups`)
2. Di **Grup Staf**, masukkan nama atau ID grup yang dipisahkan oleh koma. Pengguna dalam salah satu grup ini diberi status staf.
3. Di **Grup Superuser**, masukkan nama atau ID grup yang dipisahkan oleh koma. Pengguna dalam salah satu grup ini diberi status superuser.

Pemetaan peran dievaluasi setiap kali pengguna masuk melalui SSO. Jika pengguna dihapus dari grup di penyedia identitas, status staf atau superuser mereka diperbarui saat login SSO berikutnya.

**Penting:** Microsoft Entra ID mengirimkan **Object ID** (UUID) grup secara default, bukan nama grup. Salin Object ID dari portal Azure saat mengonfigurasi pemetaan peran. Penyedia lain seperti Okta biasanya mengirimkan nama grup.

## Pemetaan Klaim

Spwig membaca informasi pengguna dari klaim OIDC standar. Default bekerja dengan sebagian besar penyedia, tetapi Anda dapat menyesuaikan nama bidang klaim di Konfigurasi Penyedia SSO:

| Pengaturan | Default | Deskripsi |
|---------|---------|-------------|
| **Klaim Email** | `email` | Klaim yang berisi alamat email pengguna |
| **Klaim Nama Depan** | `given_name` | Klaim yang berisi nama depan pengguna |
| **Klaim Nama Belakang** | `family_name` | Klaim yang berisi nama belakang pengguna |
| **Klaim Grup** | `groups` | Klaim yang berisi keanggotaan grup (biarkan kosong untuk menonaktifkan pemetaan peran) |

## Perilaku MFA

Ketika seorang staf masuk melalui SSO, persyaratan otentikasi dua faktor (2FA) bawaan Spwig secara otomatis diabaikan. Ini karena penyedia identitas bertanggung jawab untuk menerapkan MFA sebagai bagian dari alur login SSO.

Jika organisasi Anda memerlukan MFA, konfigurasikan di kebijakan akses kondisional penyedia identitas, bukan di pengaturan 2FA Spwig. Ini memberi Anda manajemen MFA terpusat di semua aplikasi Anda.

## Akses Pemulihan

Jika penyedia identitas Anda mengalami gangguan atau konfigurasi yang salah, Anda masih dapat mengakses formulir login admin:

- **Klik toggle** — Jika login dengan kata sandi dinonaktifkan, klik "Masuk dengan akun lokal" di halaman login untuk menampilkan formulir kata sandi
- **Parameter URL** — Tambahkan `?password=1` ke URL login admin (misalnya, `https://your-store.com/en/admin/login/?password=1`) untuk menampilkan formulir kata sandi secara langsung
- **Login dengan kata sandi selalu tersedia** — Bahkan ketika disembunyikan dari UI, backend otentikasi kata sandi tetap aktif. Hanya visibilitas formulir yang terpengaruh.

Spwig juga mencegah Anda dari menonaktifkan login dengan kata sandi kecuali SSO sudah diaktifkan dan dikonfigurasikan dengan benar — Anda tidak akan secara tidak sengaja memblokir diri sendiri.

## Penyedia yang Didukung

Spwig bekerja dengan penyedia identitas apa pun yang mendukung protokol OpenID Connect (OIDC). Panduan konfigurasi terperinci tersedia untuk:

- **Microsoft Entra ID** (sebelumnya Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

Untuk penyedia OIDC lainnya (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud, dll.), langkah konfigurasi Spwig sama — Anda memerlukan URL OIDC Discovery penyedia, Client ID, dan Client Secret. Konsultasikan dokumentasi penyedia Anda untuk cara mendaftarkan aplikasi web dan mendapatkan kredensial tersebut. URI redirect yang digunakan selalu `https://your-store.com/oidc/callback/`.

## Tips

- **Mulailah dengan login kata sandi yang diaktifkan** — Aktifkan SSO bersamaan dengan login kata sandi. Setelah Anda memverifikasi bahwa SSO berfungsi untuk tim Anda, Anda dapat memilih untuk menonaktifkan login kata sandi.
- **Uji di jendela incognito** — Gunakan jendela browser pribadi/incognito untuk menguji SSO tanpa terpengaruh oleh sesi admin saat ini Anda.
- **Buat akun staf terlebih dahulu** — Kecuali Anda mengaktifkan Auto-Create Users, staf memerlukan akun Spwig yang sudah ada dengan alamat email yang cocok sebelum mereka dapat masuk melalui SSO.
- **Gunakan tombol Auto-Discover** — Masukkan URL OIDC Discovery penyedia Anda dan klik Auto-Discover untuk mengisi otomatis semua bidang endpoint. Ini lebih cepat dan kurang rentan terhadap kesalahan daripada memasukkan endpoint secara manual.
- **Buat akun admin lokal** — Selalu pertahankan setidaknya satu akun admin lokal dengan kata sandi sebagai opsi pemulihan jika terjadi masalah dengan penyedia identitas.
- **Pantau tanggal kedaluwarsa client secret** — Beberapa penyedia (terutama Microsoft Entra ID) mengeluarkan client secret dengan tanggal kedaluwarsa. Tetapkan pengingat kalender untuk memutar ulang secret sebelum kedaluwarsa.
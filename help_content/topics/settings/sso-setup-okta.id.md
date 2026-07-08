---
title: 'Pengaturan SSO: Okta'
---

Panduan ini akan membimbing Anda melalui proses menghubungkan Spwig dengan Okta untuk single sign-on (SSO) admin. Setelah dikonfigurasi, staf Anda dapat masuk ke panel admin Spwig menggunakan akun Okta mereka.

**Catatan:** Okta mungkin akan memperbarui antarmuka konsol admin mereka dari waktu ke waktu. Petunjuk ini ditulis berdasarkan konsol admin Okta hingga awal tahun 2026. Jika langkah-langkah ini berbeda dari apa yang Anda lihat, lihat dokumentasi resmi Okta tentang [membuat integrasi aplikasi OIDC](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Prasyarat

- Organisasi Okta (semua tingkatan — akun pengembang gratis dapat digunakan untuk pengujian)
- Peran **Super Administrator** atau **Application Administrator** di Okta
- URL toko Spwig Anda (misalnya, `https://your-store.com`)
- Alamat email staf harus sesuai dengan akun Okta mereka di Spwig

## Langkah 1: Membuat Aplikasi

1. Masuk ke [Okta Admin Console](https://your-org-admin.okta.com)
2. Navigasi ke **Applications > Applications**
3. Klik **Create App Integration**
4. Pilih:

| Field | Value |
|-------|-------|
| **Sign-in method** | OIDC - OpenID Connect |
| **Application type** | Web Application |

5. Klik **Next**

## Langkah 2: Mengonfigurasi Aplikasi

Isi pengaturan aplikasi:

| Field | Value |
|-------|-------|
| **App integration name** | `Spwig Admin SSO` (atau nama apa pun yang Anda sukai) |
| **Grant type** | Authorization Code (seharusnya sudah dipilih secara default) |
| **Sign-in redirect URIs** | `https://your-store.com/oidc/callback/` |
| **Sign-out redirect URIs** | `https://your-store.com/en/admin/login/` |
| **Controlled access** | Pilih berdasarkan kebutuhan Anda (lihat di bawah) |

Untuk **Controlled access**, pilih salah satu:

- **Allow everyone in your organization to access** — semua pengguna Okta dapat masuk (Anda masih dapat mengontrol akses Spwig dengan pengaturan Restrict to Staff)
- **Limit access to selected groups** — hanya pengguna dalam kelompok Okta tertentu yang dapat masuk
- **Skip group assignment for now** — Anda akan menetapkan pengguna atau kelompok secara manual nanti

Klik **Save**.

**Penting:** URI redirect masuk harus tepat sesuai dengan `https://your-store.com/oidc/callback/` — termasuk slash akhir.

## Langkah 3: Mendapatkan Kredensial Klien

Setelah disimpan, tab **General** aplikasi menampilkan kredensial Anda:

| Value | Where to Find It |
|-------|-----------------|
| **Client ID** | Tab General, bagian Client Credentials |
| **Client Secret** | Tab General, bagian Client Credentials (klik ikon mata untuk menampilkan) |

Salin kedua nilai tersebut — Anda membutuhkannya untuk Spwig.

## Langkah 4: Membangun URL Discovery

URL Discovery bergantung pada organisasi Okta dan server otorisasi Anda:

**Server otorisasi default (paling umum):**
```
https://your-org.okta.com/.well-known/openid-configuration
```

**Server otorisasi khusus (jika dikonfigurasi):**
```
https://your-org.okta.com/oauth2/{authorization-server-id}/.well-known/openid-configuration
```

Ganti `your-org.okta.com` dengan domain Okta Anda yang sebenarnya. Anda dapat menemukan domain Okta Anda di bilah URL konsol admin atau di bawah **Settings > Account**.

**Tips:** Sebagian besar organisasi menggunakan Org Authorization Server (default). Hanya gunakan URL server otorisasi khusus jika administrator Okta Anda telah menyiapkan satu secara khusus.

## Langkah 5: Menetapkan Pengguna atau Kelompok

Jika Anda memilih "Skip group assignment" di Langkah 2, Anda perlu menetapkan pengguna sebelum mereka dapat masuk:

1. Di tab **Assignments** aplikasi, klik **Assign**
2. Pilih **Assign to People** atau **Assign to Groups**
3. Pilih pengguna atau kelompok dan klik **Assign**
4. Klik **Done**

Pengguna yang tidak ditetapkan ke aplikasi akan melihat kesalahan saat mencoba SSO.

## Langkah 6: Mengonfigurasi Klaim Kelompok (Opsional)

Jika Anda ingin Spwig secara otomatis menetapkan status staf atau superuser berdasarkan keanggotaan kelompok Okta:

1.

Navigasi ke **Security > API** di konsol admin
2.

Pilih **Authorization Server** Anda (gunakan "default" jika Anda belum membuat satu khusus, atau Org Authorization Server)
3.

Pergi ke tab **Claims**
4.



Klik **Tambahkan Klaim**
5.

Konfigurasikan klaim:

| Field | Value |
|-------|-------|
| **Name** | `groups` |
| **Include in token type** | ID Token, Always |
| **Value type** | Groups |
| **Filter** | Matches regex: `.*` (untuk menyertakan semua grup) |
| **Include in** | Any scope (atau `openid` jika Anda ingin membatasinya) |

6. Klik **Buat**

**Tip:** Berbeda dengan Microsoft Entra ID yang mengirimkan Object IDs, Okta secara default mengirimkan **nama grup**. Hal ini membuat pemetaan peran lebih intuitif — Anda dapat menggunakan nama tampilan grup Okta Anda langsung di bidang Grup Staf dan Grup Superuser Spwig.

### Filtering Groups

Jika pengguna Anda termasuk dalam banyak grup Okta dan Anda hanya ingin menyertakan beberapa grup tertentu dalam token:

- Ubah filter dari `.*` menjadi regex yang lebih spesifik, misalnya `^Spwig.*` untuk hanya menyertakan grup yang dimulai dengan "Spwig"
- Atau gunakan filter **Starts with**, **Equals**, atau **Contains** alih-alih regex

## Langkah 7: Konfigurasikan di Spwig

1. Di admin Spwig, navigasikan ke **Enterprise SSO > Konfigurasi SSO Provider**
2. Atur **Nama Provider** menjadi `Okta`
3. Masukkan URL Penemuan dari Langkah 4
4. Klik **Auto-Discover** — ini akan mengisi semua bidang endpoint secara otomatis
5. Masukkan **Client ID** dari Langkah 3
6. Masukkan **Client Secret** dari Langkah 3
7. Jika Anda mengonfigurasikan klaim grup di Langkah 6:
   - Atur **Groups Claim** menjadi `groups`
   - Di **Staff Groups**, masukkan nama grup Okta yang anggotanya harus menjadi staf (dipisahkan oleh koma)
   - Di **Superuser Groups**, masukkan nama grup Okta yang anggotanya harus menjadi superuser (dipisahkan oleh koma)
8. Klik **Simpan**

## Langkah 8: Aktifkan dan Uji

1. Navigasikan ke **Pengaturan Situs > Tab Keamanan**
2. Centang **Aktifkan SSO untuk login admin**
3. Klik **Simpan**
4. Buka halaman login admin di **jendela pribadi/incognito**
5. Anda seharusnya melihat tombol **Masuk dengan Okta**
6. Klik tombol tersebut — Anda seharusnya dialihkan ke halaman login Okta
7. Masuk dengan akun Okta yang ditugaskan ke aplikasi dan emailnya cocok dengan pengguna staf di Spwig
8. Anda seharusnya dialihkan kembali ke dashboard admin Spwig

## Masalah Umum

| Masalah | Penyebab | Solusi |
|---------|-------|----------|
| **URI redirect tidak diperbolehkan** | URI redirect tidak cocok dengan konfigurasi aplikasi | Verifikasi URI redirect login tepatnya adalah `https://your-store.com/oidc/callback/` dengan slash akhir |
| **Pengguna tidak ditugaskan ke aplikasi client** | Pengguna tidak ditugaskan ke aplikasi Okta | Tugaskan pengguna atau grup mereka ke aplikasi di tab Assignments |
| **Login berhasil di Okta tetapi gagal di Spwig** | Tidak ada pengguna yang cocok di Spwig | Pastikan akun staf ada di Spwig dengan email yang sama. Periksa pengaturan Restrict to Staff. |
| **Klaim grup kosong** | Klaim grup tidak dikonfigurasikan di server otorisasi | Ikuti Langkah 6 untuk menambahkan klaim grup. Pastikan Anda menambahkannya ke server otorisasi yang benar. |
| **Server otorisasi yang salah** | URL penemuan menggunakan server otorisasi berbeda dari tempat klaim grup dikonfigurasikan | Verifikasi URL penemuan cocok dengan server otorisasi tempat Anda mengonfigurasikan klaim grup |
| **"Client_id yang diberikan tidak valid"** | Client ID tidak cocok atau aplikasi tidak aktif | Periksa bahwa Client ID benar dan status aplikasi adalah Active di Okta |

## Tips

- **Okta mengirimkan nama grup, bukan ID** — ini membuat pemetaan peran menjadi sederhana.

Masukkan nama tampilan grup yang tepat (misalnya, `Spwig Admins`) di bidang Grup Staf atau Grup Superuser Spwig.
- **Gunakan penugasan grup untuk kontrol akses** — tugaskan grup Okta tertentu ke aplikasi Spwig, bukan memungkinkan semua pengguna.

# Pengaturan Otorisasi

Dengan cara ini, hanya staf yang dimaksud yang dapat masuk.
- **Kunci rahasia klien Okta tidak kedaluwarsa secara default** — tetapi Anda dapat memutarnya kapan saja dari tab Umum aplikasi untuk praktik keamanan terbaik.
- **Uji dengan akun non-admin** — gunakan pengguna Okta biasa (bukan super admin) yang ditugaskan ke aplikasi untuk memverifikasi SSO berfungsi seperti yang diharapkan.
- **MFA di Okta** — konfigurasikan kebijakan sesi global Okta atau kebijakan otentikasi untuk memerlukan MFA.

Ini akan berlaku untuk semua login SSO ke Spwig tanpa perlu mengonfigurasi MFA secara terpisah di Spwig.
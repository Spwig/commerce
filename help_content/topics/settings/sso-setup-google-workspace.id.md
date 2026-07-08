---
title: 'SSO Setup: Google Workspace'
---

Pengaturan SSO: Google Workspace

Panduan ini akan membimbing Anda melalui proses menghubungkan Spwig dengan Google Workspace untuk single sign-on (SSO) admin. Setelah dikonfigurasi, staf Anda dapat masuk ke panel admin Spwig menggunakan akun Google Workspace mereka.

**Catatan:** Google mungkin akan memperbarui antarmuka Cloud Console dari waktu ke waktu. Petunjuk ini ditulis berdasarkan antarmuka seperti pada awal tahun 2026. Jika ada langkah yang berbeda dari apa yang Anda lihat, lihat dokumentasi resmi Google tentang [mengatur OAuth 2.0](https://support.google.com/cloud/answer/6158849).

## Prasyarat

- Langganan Google Workspace (Google Workspace Business, Enterprise, atau Education)
- Akses admin ke [Google Cloud Console](https://console.cloud.google.com)
- URL toko Spwig Anda (misalnya, `https://your-store.com`)
- Alamat email staf harus sesuai dengan akun Google Workspace mereka

## Langkah 1: Membuat atau Memilih Proyek Google Cloud

1. Buka [Google Cloud Console](https://console.cloud.google.com)
2. Klik pemilih proyek di bagian atas
3. Klik **New Project** (atau pilih proyek yang sudah ada jika Anda lebih suka)
4. Masukkan nama proyek (misalnya, `Spwig SSO`)
5. Pilih organisasi Anda
6. Klik **Create**

## Langkah 2: Mengatur Layar Persetujuan OAuth

1. Di Cloud Console, navigasikan ke **APIs & Services > OAuth consent screen**
2. Pilih **Internal** sebagai tipe pengguna — ini membatasi login hanya untuk pengguna dalam organisasi Google Workspace Anda
3. Klik **Create**
4. Isi bidang yang diperlukan:

| Field | Value |
|-------|-------|
| **App name** | `Spwig Admin` (atau nama toko Anda) |
| **User support email** | Alamat email admin Anda |
| **Authorized domains** | `your-store.com` (domain toko Anda, tanpa `https://`) |
| **Developer contact email** | Alamat email admin Anda |

5. Klik **Save and Continue**
6. Di halaman **Scopes**, klik **Add or Remove Scopes** dan tambahkan:
   - `openid`
   - `email`
   - `profile`
7. Klik **Save and Continue**
8. Tinjau ringkasan dan klik **Back to Dashboard**

## Langkah 3: Membuat Kredensial OAuth

1. Navigasikan ke **APIs & Services > Credentials**
2. Klik **Create Credentials > OAuth client ID**
3. Konfigurasikan klien:

| Field | Value |
|-------|-------|
| **Application type** | Web application |
| **Name** | `Spwig SSO` |
| **Authorized redirect URIs** | `https://your-store.com/oidc/callback/` |

4. Klik **Create**
5. Dialog menampilkan **Client ID** dan **Client Secret** Anda — salin kedua nilai tersebut. Anda juga dapat mengunduhnya sebagai JSON untuk penyimpanan yang aman.

**Penting:** URI redirect harus tepat sesuai dengan `https://your-store.com/oidc/callback/` — termasuk slash akhir dan skema `https://`. Ganti `your-store.com` dengan domain toko Anda yang sebenarnya.

## Langkah 4: Mendapatkan URL Discovery

Google menggunakan satu URL Discovery standar untuk semua tenant Workspace:

```
https://accounts.google.com/.well-known/openid-configuration
```

URL ini sama untuk setiap organisasi Google Workspace — Anda tidak perlu menyesuaikannya dengan tenant atau domain.

## Langkah 5: Mengonfigurasi di Spwig

1. Di admin Spwig, navigasikan ke **Enterprise SSO > SSO Provider Configuration**
2. Atur **Provider Name** menjadi `Google Workspace`
3. Masukkan URL Discovery: `https://accounts.google.com/.well-known/openid-configuration`
4. Klik **Auto-Discover** — ini mengisi semua bidang endpoint secara otomatis
5. Masukkan **Client ID** dari Langkah 3
6. Masukkan **Client Secret** dari Langkah 3
7. Klik **Save**

### Pemetaan Klaim

Google menggunakan nama klaim OIDC standar, sehingga konfigurasi Spwig default berfungsi dengan baik:

| Pengaturan Spwig | Klaim Google | Nilai Default |
|---------------|-------------|---------------|
| Email Claim | `email` | `email` |
| First Name Claim | `given_name` | `given_name` |
| Last Name Claim | `family_name` | `family_name` |

Tidak diperlukan perubahan pada pemetaan klaim.

## Langkah 6: Mematikan dan Menguji

1.

Navigasikan ke **Site Settings > Security** tab
2.

Centang **Enable SSO for admin login**
3.

Klik **Save**
4.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Buka halaman login admin di **jendela pribadi/incognito**
5.

Anda seharusnya melihat tombol **Masuk dengan Google Workspace**
6.

Klik tombol tersebut — Anda seharusnya akan dialihkan ke halaman login Google
7.

Masuk dengan akun Google Workspace yang email-nya cocok dengan pengguna staf di Spwig
8.

Anda seharusnya akan dialihkan kembali ke dashboard admin Spwig

## Pemetaan Peran Berbasis Grup

Berbeda dengan Microsoft Entra ID atau Okta, Google secara default tidak menyertakan keanggotaan grup dalam token OIDC standar. Menerapkan klaim grup dengan Google memerlukan Google Workspace Directory API dan konfigurasi tambahan di luar OIDC dasar.

Untuk sebagian besar penggunaan Google Workspace, kami merekomendasikan mengelola status staf dan superuser secara langsung di Spwig, bukan melalui pemetaan peran otomatis:

1. Buat akun staf di Spwig dengan izin yang sesuai
2. Gunakan sistem Peran Staf Spwig untuk mengontrol tingkat akses
3. Staf masuk melalui SSO, dan Spwig menggunakan izin yang sudah ada

Jika Anda memerlukan pemetaan peran otomatis berbasis grup, konsultasikan dengan [dokumentasi Google Workspace Admin SDK Directory API](https://developers.google.com/admin-sdk/directory) untuk mengonfigurasi klaim kustom.

## Masalah Umum

| Masalah | Penyebab | Solusi |
|---------|-------|----------|
| **Error 400: redirect_uri_mismatch** | URI alih arah di Google Cloud tidak cocok secara tepat | Periksa URI alih arah adalah `https://your-store.com/oidc/callback/` dengan slash akhir. Periksa HTTP vs HTTPS. |
| **Error 403: access_denied** | Pengguna tidak berada dalam organisasi Google Workspace | Dengan tipe pengguna "Internal", hanya pengguna dalam organisasi Anda yang dapat masuk. Pastikan akun pengguna adalah bagian dari domain Workspace Anda. |
| **Layar persetujuan OAuth menampilkan "Aplikasi ini tidak diverifikasi"** | Normal untuk aplikasi Internal | Peringatan ini diharapkan untuk aplikasi Internal dan tidak memengaruhi fungsi. Pengguna dalam organisasi Anda masih dapat masuk. |
| **Masuk berhasil di Google tetapi gagal di Spwig** | Tidak ada pengguna yang cocok di Spwig | Pastikan akun staf ada di Spwig dengan email yang sama dengan akun Google Workspace. Periksa bahwa "Batas ke Staf" dikonfigurasikan dengan benar. |
| **"Akses diblokir: Permintaan aplikasi ini tidak valid"** | Cakupan tidak dikonfigurasikan dengan benar | Pastikan cakupan `openid`, `email`, dan `profile` ditambahkan ke layar persetujuan OAuth. |

## Tips

- **Gunakan tipe pengguna "Internal"** — ini membatasi masuk ke organisasi Google Workspace Anda dan tidak memerlukan proses verifikasi aplikasi Google.
- **Rahasia klien Google tidak kedaluwarsa** — berbeda dengan Microsoft Entra ID, rahasian klien OAuth Google tidak memiliki tanggal kedaluwarsa. Namun, Anda dapat memutasi mereka kapan saja dari halaman Kredensial.
- **Satu proyek untuk beberapa aplikasi** — Anda dapat membuat beberapa ID klien OAuth dalam proyek Google Cloud yang sama jika Anda memiliki beberapa instalasi Spwig.
- **Uji dengan akun non-admin** — buat akun staf uji di Spwig dan gunakan pengguna Google Workspace biasa (bukan super admin) untuk memverifikasi SSO berfungsi seperti yang diharapkan.
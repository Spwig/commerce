<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.tr.md">Türkçe</a> |
  <strong>Tiếng Việt</strong> |
  <a href="README.th.md">ไทย</a>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>Thương mại điện tử tự lưu trữ dành cho các thương nhân muốn sở hữu cửa hàng của chính mình.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Trang web</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Tài liệu</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Cộng đồng</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/vi/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/vi/demos">Bản demo trực tiếp</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Spwig là gì?

Spwig là một nền tảng thương mại điện tử đầy đủ tính năng: danh mục sản phẩm, giỏ hàng, thanh toán, đơn hàng, khách hàng, phương thức thanh toán, vận chuyển, giao diện, trình dựng trang, API quản trị, POS, gói đăng ký, chương trình khách hàng thân thiết, blog, SEO — toàn bộ ngăn xếp. Được xây dựng trên **Django 5**, **PostgreSQL** và **Redis**, phân phối dưới dạng một tập hợp container Docker, chạy được trên VPS $5 hoặc trên phần cứng của riêng bạn.

Không như các nền tảng lưu trữ dịch vụ, **bạn sở hữu mã nguồn, cơ sở dữ liệu và dữ liệu khách hàng.** Không có phí trên từng giao dịch. Không bị khóa nhà cung cấp. Nếu bạn muốn fork và đi con đường riêng, giấy phép cho phép điều đó một cách rõ ràng.

<br />

## Các phiên bản

Cùng một tệp nhị phân. Một tệp giấy phép có chữ ký sẽ bật/tắt các cờ tính năng khi chạy. Community là phiên bản bạn nhận được mặc định khi chạy `docker compose up`; nâng cấp chỉ là một khóa mà bạn dán vào trang quản trị.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| Thương mại điện tử đầy đủ, giao diện, trình dựng trang, giao diện POS | ✓ | ✓ | ✓ |
| Tự mang nhà cung cấp thanh toán của bạn | ✓ | ✓ | ✓ |
| Tự mang nhà cung cấp vận chuyển của bạn | ✓ | ✓ | ✓ |
| Truy cập Marketplace (giao diện cao cấp + tích hợp) | ✓ | ✓ | ✓ |
| Tự động điền địa chỉ do Spwig lưu trữ | Miễn phí · giới hạn tần suất | Hạn mức cao hơn | Hạn mức cao nhất |
| GeoIP do Spwig lưu trữ (vị trí khách truy cập) | Miễn phí · giới hạn tần suất | Hạn mức cao hơn | Hạn mức cao nhất |
| Thông báo đẩy (ứng dụng quản trị iOS) | Miễn phí · giới hạn tần suất | Hạn mức cao hơn | Hạn mức cao nhất |
| Điểm bán hàng (hỗ trợ terminal POS) | ✓ | ✓ | ✓ |
| Cổng email lưu trữ với IP làm ấm + DKIM | – | ✓ | ✓ |
| Hỗ trợ ưu tiên | – | ✓ | ✓ |
| SSO cấp doanh nghiệp (Azure AD, Okta) | – | – | ✓ |

<br />

## Bắt đầu nhanh

### Cách 1 — Cài đặt bằng một dòng lệnh (khuyến nghị)

[Trình cài đặt Spwig](https://github.com/Spwig/spwig) thiết lập tất cả chỉ trong một câu lệnh: Docker, PostgreSQL, Redis, MinIO, TLS qua Cloudflare hoặc chứng chỉ tự ký, trình hướng dẫn khởi động lần đầu, người dùng quản trị. Các image có chữ ký được kéo từ `registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Việc nâng cấp diễn ra qua trang quản trị — xem [UPGRADING.md](UPGRADING.md).

### Cách 2 — Từ mã nguồn

Bạn muốn build từ repo này, tùy biến nó, hoặc phát hành một bản fork:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Cửa hàng trước tại `http://localhost`, trang quản trị tại `http://localhost/vi/admin/`. Phiên bản Community tự động kích hoạt khi khởi động lần đầu — không cần gọi về máy chủ giấy phép, không cần khóa. Nâng cấp về sau bằng `git pull` và `docker compose build`.

<br />

## Tính năng

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Cửa hàng trước & thanh toán</h3>
      <p>Kết xuất phía máy chủ theo mặc định — thời gian đến byte đầu tiên nhanh, hoạt động không cần JavaScript, ưu tiên di động (80% lưu lượng đến từ màn hình nhỏ). Tùy chọn chế độ headless qua
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> và <a href="https://github.com/Spwig/react">các component React</a>.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/storefront-product.webp" alt="Storefront product page">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/page-builder.webp" alt="Page builder">
    </td>
    <td width="50%" valign="top">
      <h3>Trình dựng trang</h3>
      <p>Thương nhân xây dựng các trang cửa hàng từ những widget có thể tái sử dụng — phần hero, lưới sản phẩm, lời chứng thực, nhúng — và xem trước trực tiếp trong trang quản trị. Widget được cài đặt từ Marketplace hoặc từ kho component của riêng bạn.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Quản lý đơn hàng & khách hàng</h3>
      <p>Mọi đơn hàng, hoàn tiền, gia hạn gói đăng ký, tải xuống kỹ thuật số và điểm chạm khách hàng ở cùng một nơi. Thao tác hàng loạt, vai trò nhân viên có phạm vi quyền, xuất ra CSV/XLSX, ứng dụng quản trị di động (iOS) kèm thông báo đẩy.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/order-management.webp" alt="Order management">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/branding-builder.webp" alt="Branding builder">
    </td>
    <td width="50%" valign="top">
      <h3>Giao diện & thương hiệu</h3>
      <p>Các token thiết kế (màu sắc, kiểu chữ, khoảng cách) chi phối mọi bề mặt — cả cửa hàng trước lẫn quản trị. Đổi một token, mọi thứ được cập nhật. Giao diện nằm ở
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      và được cài qua Marketplace; hãy viết giao diện của riêng bạn bằng
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Điểm bán hàng</h3>
      <p>Terminal POS đầy đủ dành cho các thương nhân có cửa hàng vật lý: quét mã vạch, thanh toán chia nhỏ, in hóa đơn, tích hợp ngăn kéo tiền, màn hình hướng về khách hàng, chế độ ngoại tuyến. Phiên bản Community vẫn chứa mã nguồn nhưng bề mặt quản trị hiển thị lời mời nâng cấp — hãy vá bỏ nếu bạn fork, không sao cả.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/pos-terminal.webp" alt="POS terminal">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/developer-portal.webp" alt="Developer portal">
    </td>
    <td width="50%" valign="top">
      <h3>Hệ sinh thái nhà cung cấp</h3>
      <p>Bất cứ thứ gì giao tiếp với hệ thống bên ngoài — thanh toán, vận chuyển, tỷ giá hối đoái, dịch thuật, GeoIP, SMS, email — đều là một provider có thể cắm vào. Xây dựng provider của riêng bạn bằng
      <a href="https://github.com/Spwig/provider-sdks">provider SDK</a>,
      công bố lên Marketplace, hoặc tự lưu trữ một registry riêng.</p>
    </td>
  </tr>
</table>

<br />

## Kiến trúc

- **Đơn khách thuê (single-tenant).** Mỗi bản cài là một cửa hàng, một thương nhân, một Django Site. Thương nhân đa cửa hàng chạy một bản cài Spwig cho mỗi cửa hàng.
- **Khối đơn mô-đun (modular monolith).** Không phải mạng lưới microservice. Một tiến trình Django duy nhất xử lý cửa hàng trước + quản trị + REST API + Celery workers. Dễ triển khai, dễ suy luận và dễ fork.
- **Cổng tính năng khi chạy.** Community/Pro/Enterprise đều chạy cùng một tệp nhị phân. Giấy phép có chữ ký bật/tắt cờ — không bóc tách mã.

Tham quan đầy đủ: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Cộng đồng & hỗ trợ

- **Discussions.** Câu hỏi mở, ý tưởng, chia sẻ:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Diễn đàn cộng đồng.** [community.spwig.com](https://community.spwig.com)
  — các luồng thảo luận dài, công thức thực hành tốt nhất, giới thiệu tiện ích mở rộng.
- **Báo cáo lỗi.** [Issues](https://github.com/Spwig/commerce/issues)
  kèm bước tái hiện. Xem [SECURITY.md](SECURITY.md) về việc công bố lỗ hổng.
- **Hỗ trợ thương mại.** Có sẵn cho giấy phép Pro và Enterprise.

<br />

## Đóng góp

Chúng tôi dùng **DCO** (Developer Certificate of Origin) — mỗi commit được ký xác nhận bằng `git commit -s`. Không giấy tờ, không CLA. Hướng dẫn đầy đủ tại
[CONTRIBUTING.md](CONTRIBUTING.md).

Ghi chú dành cho các trợ lý lập trình AI làm việc trên repo này nằm ở
[CLAUDE.md](CLAUDE.md).

<br />

## Hệ sinh thái

Các dự án mã nguồn mở liên quan thuộc [tổ chức Spwig](https://github.com/Spwig):

| Repo | Là gì |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Repo này — nền tảng lõi (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Trình cài đặt một dòng lệnh |
| [Spwig/components](https://github.com/Spwig/components) | Giao diện, tích hợp và tiện ích (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK để xây dựng giao diện (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | Các SDK để xây dựng provider thanh toán / vận chuyển / v.v. (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | SDK headless / client API (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | Thư viện component React (Apache-2.0) |

<br />

## Giấy phép

Spwig được cấp phép theo [AGPL-3.0-or-later](LICENSE). Bạn có thể chạy, sửa đổi, phân phối, cung cấp dưới dạng dịch vụ lưu trữ — đều được cho phép. Các phiên bản đã sửa đổi được cung cấp qua mạng phải công khai mã nguồn cho người dùng của chúng. Đó chính là điểm mấu chốt của AGPL so với GPL.

Các tích hợp provider xây dựng bằng SDK được cấp phép Apache-2.0, vì vậy việc dựng một tích hợp thanh toán / vận chuyển / SMS độc quyền trên nền các SDK không kích hoạt AGPL. Đây là chủ ý — chúng tôi muốn có một hệ sinh thái provider phát triển mạnh.

<br />

## Quyền riêng tư & telemetry

Spwig gửi một ping ẩn danh mỗi ngày đến `updates.spwig.com/api/v1/telemetry/`:

- UUID cài đặt (tạo lần khởi động đầu tiên, lưu tại chỗ)
- Phiên bản Spwig
- Phiên bản phát hành (community / pro / enterprise / trial / dev)
- Quốc gia (giải mã từ IP tại điểm vào; bản thân IP không được lưu)
- Số đếm theo nhóm của các cờ tính năng (các nhà cung cấp thanh toán đã cấu hình, các giao diện đã cài) — không bao giờ là dữ liệu khách hàng hay đơn hàng thô

**Chọn không tham gia** bằng cách đặt `SPWIG_TELEMETRY=0` trong môi trường của bạn. Điều đó sẽ đảo `settings.SPWIG_TELEMETRY_ENABLED` và tác vụ định kỳ hằng ngày sẽ không làm gì.

<br />

<p align="center">
  <sub>
    Được xây dựng bằng tâm huyết tại Singapore.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">tài liệu</a> — <a href="https://community.spwig.com">cộng đồng</a>
  </sub>
</p>

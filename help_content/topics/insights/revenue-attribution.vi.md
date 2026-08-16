---
title: Phân bổ doanh thu
---

Phân bổ doanh thu cho bạn biết nguồn doanh thu thực sự đến từ đâu — không chỉ là liên kết cuối cùng mà khách hàng đã nhấp chuột trước khi mua hàng, mà còn bao gồm mọi kênh đã góp phần đưa họ đến đó. Nếu một khách hàng đọc bài viết blog mà bạn chia sẻ trên mạng xã hội, sau đó quay lại một tuần sau thông qua tìm kiếm Google, rồi cuối cùng mua hàng sau khi nhấp vào liên kết trong email, cả ba lần tiếp xúc này đều đã đóng góp vào doanh thu đó. Bảng điều khiển này ghi nhận tất cả các lần tiếp xúc này, sử dụng mô hình bạn chọn, để bạn có thể xem chiến dịch tiếp thị của mình theo cách mà nó thực sự hoạt động thay vì cách "lần nhấp cuối cùng chiến thắng" giả vờ hoạt động.

![Bảng điều khiển Phân bổ doanh thu: bộ chuyển đổi mô hình phân bổ, dải KPI với nhãn "Phân bổ vào doanh thu ròng", doanh thu theo kênh, doanh thu theo thời gian, luồng hành trình khách hàng, và bảng chiến dịch](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## Tìm kiếm ở đâu

Đi đến **Nhận diện > Phân bổ doanh thu** trong thanh bên. Nhận diện là một nhóm menu riêng biệt ở trên Products, do đó Phân bổ doanh thu có một trang chủ riêng biệt, tách biệt với báo cáo đơn hàng và khách hàng của bạn.

Nhận diện bị chặn bởi danh mục **Quyền Nhận diện & Phân tích**. Nếu bạn không thấy nó trong thanh bên, hãy yêu cầu người quản trị cửa hàng cấp quyền này cho bạn — xem [Vai trò và Quyền của Nhân viên](/help/staff-roles) để biết cách quản lý quyền truy cập của nhân viên.

## Hiểu về phân bổ nhiều lần tiếp xúc

Hầu hết các cửa hàng đều quen với việc suy nghĩ theo cách "đơn hàng này đến từ đâu?" như thể có một câu trả lời duy nhất. Trên thực tế, khách hàng hiếm khi mua hàng trong lần truy cập đầu tiên. Họ phát hiện ra bạn theo một cách, quay lại theo cách khác, và chuyển đổi theo cách thứ ba — đôi khi là nhiều lần truy cập cách nhau vài ngày hoặc vài tuần. Mỗi lần truy cập đó là một **lần tiếp xúc**: một lần đến được cửa hàng của bạn, mang theo tín hiệu về nguồn gốc của nó (một liên kết email, kết quả tìm kiếm, bài đăng mạng xã hội, liên kết đại lý, v.v.).

**Phân bổ nhiều lần tiếp xúc** có nghĩa là nhận ra mọi lần tiếp xúc trong hành trình đó và quyết định mức độ tín nhiệm mà mỗi lần tiếp xúc xứng đáng với doanh thu cuối cùng, thay vì giao 100% tín nhiệm cho kênh nào đó đã nhấp chuột cuối cùng. Điều này quan trọng vì báo cáo nhấp chuột cuối cùng luôn đánh giá thấp các kênh thực hiện công việc khám phá ban đầu — blog của bạn, vị trí tìm kiếm tự nhiên của bạn, bài đăng mạng xã hội của bạn — vì chúng hiếm khi có thể là lần nhấp cuối cùng trước khi thanh toán.

## Chọn mô hình phân bổ

Bộ chuyển đổi mô hình ở đầu bảng điều khiển là yếu tố kiểm soát quan trọng nhất trên trang. Nhấp vào bất kỳ mô hình nào và mọi con số trên bảng điều khiển — dải KPI, thanh kênh, biểu đồ, bảng chiến dịch — sẽ tự động phân bổ lại để phù hợp. Đây là một bản xem trước thời gian thực: việc chuyển đổi mô hình ở đây thay đổi cách bạn xem doanh thu hiện có của mình, chứ không phải ghi đè lên các bản ghi hoặc thay đổi mô hình mặc định đã lưu của cửa hàng bạn.

![Bộ chuyển đổi mô hình phân bổ - Lần chạm cuối cùng, Lần chạm đầu tiên, Tuyến tính, Giảm dần theo thời gian và Vị trí 40/20/40 - với chỉ báo "Phân bổ theo thời gian thực · không cần xử lý lại"](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Model | What it does | Best for |
|-------|---------------|----------|
| **Last touch** | Gives full credit to the last channel before the order, ignoring earlier touches (except pure "direct" visits, which are skipped in favor of the last real source) | A quick, familiar view — how most basic analytics tools report revenue |
| **First touch** | Gives full credit to whichever channel first brought the customer to your store | Understanding what's driving new customer discovery and top-of-funnel growth |
| **Linear** | Splits credit evenly across every touch in the journey | A balanced, no-opinion view when you don't want any single channel favored |
| **Time decay** | Gives more credit to touches closer to the order, less to touches further back | Campaigns with a short consideration window, where recent nudges matter most |
| **Position 40/20/40** | Gives 40% credit to the first touch, 40% to the last touch, and splits the remaining 20% across everything in between | Recognizing both "who found us" and "who closed the sale" while still crediting the middle of the journey |

There's no single "correct" model — each one answers a different question. A common approach is to check **First touch** to see what's driving discovery, then **Last touch** or **Position 40/20/40** to see what's driving conversions, and use both views together rather than picking one and ignoring the rest.

## Reading the KPI strip

Just below the model switcher, four figures summarize the selected period and model:

- **Attributed revenue** — the total revenue credited across all channels for the current model. It carries a **Reconciles to net revenue** badge when the figures add up correctly to your store's actual net revenue for the period — in other words, the model is splitting real revenue between channels, not inventing or losing any of it.
- **Orders** — how many orders fall in the selected date range.
- **Avg. touches / order** — the average number of recorded touches per order. A number above 1 confirms that most of your customers' journeys involve more than a single visit, which is exactly why multi-touch attribution matters for your store.
- **Leading channel** — whichever channel currently holds the largest share of attributed revenue under the selected model, with its share percentage and revenue.

## Revenue by channel

The **Revenue by channel** card shows a horizontal bar for each channel, sized by attributed revenue. Switch the attribution model and watch the bars smoothly reorder themselves by rank — this is the same underlying revenue, just re-split by a different set of rules, so a channel that looks strong under **Last touch** may drop several places under **First touch** if it mostly plays a supporting role.

## Revenue over time

The **Revenue over time** chart stacks attributed revenue by channel across each day in the selected range, so you can see not just how much each channel is worth but when it's contributing. Use it to spot seasonal patterns, confirm a campaign's impact landed on the days you expected, or check whether a channel's contribution is growing or fading over the period.

## How customers actually arrive

The **How customers actually arrive** panel is a journey flow chart connecting the channel that first brought a customer in (on the left) to the channel present when they converted (on the right). Thicker ribbons mean more revenue flowed through that path. This is the clearest way to see multi-step journeys at a glance — for example, a thick ribbon from Organic Search to Email tells you that search is bringing people in, but your email marketing is what's bringing them back to buy.

![The customer-journey flow chart, with the Influenced lens selected, showing first-touch channels on the left flowing to the channel each order converted on](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

Use the **Attributed** / **Influenced** toggle above the chart to switch lenses:

- **Được ghi nhận** tách biệt doanh thu của mỗi đơn hàng theo mô hình bạn đã chọn, do đó tổng cộng sẽ bằng 100% doanh thu được ghi nhận — những con số giống với những gì được hiển thị ở các nơi khác trên bảng điều khiển.
- **Có ảnh hưởng** ghi nhận *mọi* kênh đã tiếp xúc với đơn hàng với *toàn bộ* giá trị của đơn hàng đó, được tính một lần cho mỗi đơn hàng.

Điều này cố ý không cộng lại thành 100% — một kênh có thể bị "có ảnh hưởng" bởi doanh thu mà cũng được tính đầy đủ cho một kênh khác.

Nó tồn tại để làm nổi bật phạm vi tiếp cận mà kênh đó đã có, điều mà báo cáo cuối cùng (last-click) đã che giấu hoàn toàn, ví dụ như một bài viết blog hoặc một lượt chia sẻ mạng xã hội đã khiến ai đó quan tâm ngay cả khi họ không nhấp vào nó trong lần truy cập cuối cùng.

## Chiến dịch

Bảng **Chiến dịch** phân tích doanh thu, đơn hàng và giá trị đơn hàng trung bình (AOV) cho mỗi chiến dịch được gắn thẻ của bạn — các liên kết hoặc mã bạn đã đánh dấu với tên chiến dịch, bao gồm cả mã giảm giá được gắn thẻ chiến dịch (xem [Ý tưởng chiến dịch voucher](/help/voucher-campaign-ideas)). Sử dụng nó để so sánh hiệu suất của các chương trình khuyến mãi, mã của người ảnh hưởng hoặc chiến dịch tiếp thị với nhau, độc lập với kênh nào đã mang chúng đi.

## Khoảng thời gian ngày và xuất dữ liệu của bạn

Sử dụng bộ chọn khoảng thời gian ở góc trên cùng bên phải để chuyển đổi giữa **7 ngày gần đây**, **14 ngày gần đây**, **30 ngày gần đây**, **90 ngày gần đây**, và **Tính đến ngày hiện tại**. Bảng điều khiển sẽ được làm mới cho khoảng thời gian mới.

Nhấn **Xuất CSV** để tải xuống bảng phân tích kênh cho mô hình và khoảng thời gian được chọn hiện tại — hữu ích để kéo số liệu vào bảng tính hoặc chia sẻ với một công ty đại lý.

## Cách các lần tiếp xúc được ghi nhận

Spwig tự động ghi nhận một lần tiếp xúc mỗi khi một khách truy cập đến cửa hàng của bạn mang theo tín hiệu nguồn nhận biết được, và chỉ khi khách truy cập đã cấp **Phân tích** trong banner cookie của cửa hàng bạn (nếu bạn không chạy banner đồng ý, việc theo dõi được bật mặc định, theo chính sách riêng của cửa hàng bạn). Điều này giữ cho việc ghi nhận doanh thu ở cùng một mức độ bảo mật như phần còn lại của phân tích cửa hàng của bạn.

Nhiều nguồn được ghi nhãn tự động, không cần cài đặt:

| Kênh | Cách nhận diện |
|---------|----------------------|
| **Email** | Các liên kết trong email tiếp thị của bạn (không bao gồm email đơn hàng hoặc vận chuyển) |
| **Tìm kiếm hữu cơ / Quảng cáo** | Người dùng truy cập từ công cụ tìm kiếm, hoặc các giá trị `utm_medium` đánh dấu chiến dịch quảng cáo tìm kiếm |
| **Mạng xã hội hữu cơ / Quảng cáo** | Người dùng truy cập từ mạng xã hội, hoặc các giá trị `utm_medium` của mạng xã hội |
| **Đại lý** | Các liên kết được tạo thông qua chương trình Đại lý của bạn |
| **Giới thiệu bạn bè** | Các liên kết được tạo thông qua chương trình giới thiệu khách hàng của bạn |
| **Chiến dịch** | Mọi liên kết hoặc mã mang theo thẻ chiến dịch, bao gồm cả mã giảm giá được gắn thẻ chiến dịch |
| **Liên kết bên ngoài** | Một liên kết đến từ một trang web khác không được phân loại khác |
| **Trực tiếp** | Không có tín hiệu nguồn nào được hiện diện — khách truy cập nhập địa chỉ cửa hàng của bạn, sử dụng bookmark, hoặc đến từ ứng dụng mà không có referrer |

Các bài viết blog được chia sẻ tự động đến các tài khoản mạng xã hội được kết nối của bạn sẽ được ghi nhãn tự động, do đó lưu lượng truy cập do chúng tạo ra sẽ xuất hiện dưới kênh mạng xã hội phù hợp thay vì bị mất vào mục **Trực tiếp** hoặc **Liên kết bên ngoài**.

Bạn cũng có thể ghi nhãn các liên kết của riêng mình bằng tay bằng cách sử dụng các tham số chuẩn `utm_source`, `utm_medium` và `utm_campaign` trên bất kỳ URL nào chỉ đến cửa hàng của bạn — hữu ích cho tài liệu in ấn, bản tin đối tác hoặc bất kỳ kênh nào mà Spwig không tự động ghi nhãn.

## Những giới hạn cần lưu ý

- **Ghi nhận theo trình duyệt, không phải theo người dùng.** Nếu một khách hàng nghiên cứu trên điện thoại và mua hàng trên máy tính xách tay, chúng sẽ là hai hành trình riêng biệt theo cách theo dõi — không có cách nào để liên kết hoạt động giữa các thiết bị khác nhau.

Điều này có nghĩa là một số khoản tín dụng mà 'nên' thuộc về lần tiếp xúc trước trên thiết bị khác sẽ bị ghi nhận là Direct thay vì được ghi nhận theo kênh khác.
- **Direct là nơi doanh thu không được theo dõi được ghi nhận.** Tỷ lệ Direct cao không nhất thiết có nghĩa là mọi người đang nhập URL của bạn từ trí nhớ — nó cũng có thể có nghĩa là các lần tiếp xúc trước của khách hàng xảy ra trên thiết bị khác, hoặc là một liên kết mà họ sử dụng không được ghi nhãn.
- **Việc từ chối sự đồng ý có nghĩa là không có lần tiếp xúc nào được ghi nhận.** Những người truy cập từ chối sự đồng ý phân tích trong banner cookie của bạn sẽ không được theo dõi, vì vậy đơn hàng của họ sẽ xuất hiện dưới dạng Direct ngay cả khi họ đến từ một kênh mà bạn thường nhận diện được.

## Mẹo

- Kiểm tra nhiều mô hình hơn trước khi đưa ra kết luận — một kênh có vẻ yếu dưới **Lần tiếp xúc cuối** có thể là phương tiện phát hiện mạnh nhất của bạn dưới **Lần tiếp xúc đầu**.
- Nếu **Direct** chiếm một tỷ lệ lớn trong doanh thu của bạn, hãy xem xét xem liệu có thể có nhiều liên kết tiếp thị hơn của bạn có thể được ghi nhãn bằng `utm_source`/`utm_medium`/`utm_campaign` không — lưu lượng truy cập không được ghi nhãn sẽ không có nơi nào khác để ghi nhận.
- Sử dụng **Influenced** (được ảnh hưởng) trên biểu đồ luồng hành trình khi bạn quyết định xem có nên tiếp tục đầu tư vào một kênh như tìm kiếm tự nhiên hoặc nội dung blog mà hiếm khi nhận được lần click cuối nhưng luôn bắt đầu các hành trình hay không.
- So sánh **Số lần tiếp xúc trung bình / đơn hàng** theo thời gian — số lượng tăng dần thường cho thấy khách hàng mất nhiều thời gian hơn để đưa ra quyết định, đây là tín hiệu hữu ích khi lập kế hoạch thời gian email theo dõi hoặc nhắm mục tiêu lại.
- Xuất tệp CSV cho mô hình và khoảng thời gian bạn đang báo cáo trước khi chuyển sang mô hình khác, vì bản xuất tệp CSV phản ánh mô hình nào đang được chọn tại thời điểm bạn nhấn **Xuất CSV**.
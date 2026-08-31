---
title: Trình tạo Hành trình
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: The template picker with all eight starters visible (Welcome series,
    First-order onboarding, Post-purchase & review, VIP vs. standard offer, Abandoned
    cart recovery, Win-back lapsed customers, Post-delivery review request,
    Back-in-stock alert) — replaces the existing four-template screenshot at the same
    path, which is now stale.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

**Trình tạo Hành trình** là bảng vẽ trực quan, kéo-thả nơi bạn thiết kế những gì một [Hành trình](/help/triggered-journeys) thực sự thực hiện — email nào được gửi đi, thời gian chờ giữa các email là bao lâu, và liệu các người đăng ký khác nhau có nên đi theo các đường dẫn khác nhau hay không. Thay vì điền vào một biểu mẫu, bạn xây dựng luồng dưới dạng sơ đồ khối: các hộp được kết nối trên bảng vẽ mà bạn có thể sắp xếp lại, phân nhánh và xem trước chỉ trong một cái nhìn.

## Mở trình tạo

Mỗi hành trình có bảng vẽ trình tạo riêng. Bạn có thể truy cập theo hai cách:

- Tạo một hành trình mới — điền **Tên**, **Trình kích hoạt** và đối tượng trên trang cài đặt và nhấp vào **Lưu** — sẽ đưa bạn thẳng vào trình tạo để bạn có thể bắt đầu thiết kế ngay lập tức.
- Mở trang cài đặt của một hành trình hiện có và nhấp vào **Thiết kế hành trình** ở phía trên.

Trình tạo là một không gian làm việc toàn màn hình với ba khu vực: một **bảng công cụ** các loại bước ở bên trái, **bảng vẽ** ở giữa, và một **bảng cài đặt bước** ở bên phải xuất hiện khi bạn chọn một mục nào đó.

![Bảng vẽ Trình tạo Hành trình hiển thị chuỗi chào mừng với một nhánh Có/Không](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

Ở phía trên bảng vẽ, một tiêu đề lặp lại **Trình kích hoạt** và **đối tượng** (hoặc "Tất cả người đăng ký" nếu không có phân khúc nào được đặt) để bạn luôn biết mình đang thiết kế cho ai mà không cần rời khỏi trình tạo. Sử dụng nút **Quay lại** để trở về trang cài đặt của hành trình.

## Các loại bước

Kéo một bước từ bảng công cụ bên trái vào bảng vẽ, hoặc nhấp vào một mục trong bảng công cụ để tự động thả nó vào. Có bốn loại bước khả dụng:

| Bước | Nó làm gì |
|------|--------------|
| **Gửi email** | Gửi một trong các chiến dịch của bạn đến người đăng ký. |
| **Chờ** | Tạm dừng trong một số giờ hoặc ngày nhất định trước khi tiếp tục. |
| **Phân nhánh** | Chia đường dẫn thành hai — **Có** hoặc **Không** — dựa trên việc người đăng ký có thuộc một phân khúc bạn chọn hay không. |
| **Thoát** | Kết thúc hành trình cho người đăng ký. |

Mỗi hành trình bắt đầu với một bước **Điểm vào** duy nhất, được tạo tự động lần đầu tiên bạn mở trình tạo. Nó hiển thị trình kích hoạt của hành trình và không thể bị xóa — nó đơn giản là nơi người đăng ký đi vào luồng.

## Kết nối các bước

Mỗi bước có một **cổng** tròn nhỏ: một ở phía trên (đầu vào) và một hoặc nhiều hơn ở phía dưới (đầu ra). Để kết nối hai bước, kéo từ cổng dưới của một bước đến cổng trên của một bước khác — một đường cong xuất hiện liên kết chúng.

Một bước **Phân nhánh** có hai cổng đầu ra thay vì một: một **Có** màu xanh lá và một **Không** màu đỏ. Kết nối mỗi cổng đến nơi mà đường dẫn đó nên dẫn đến — chúng có thể hợp nhất lại sau đó tại cùng một bước (như trong ví dụ ở trên, nơi cả hai đường dẫn đều quay lại cùng một **Thoát**) hoặc đi theo các hướng hoàn toàn riêng biệt.

Để sắp xếp lại bố cục, kéo thân của một bước để định vị lại nó — các đường kết nối sẽ tự động theo dõi. Kéo một phần trống của nền bảng vẽ để di chuyển xung quanh, và sử dụng bánh xe cuộn để phóng to hoặc thu nhỏ. Nếu bạn mất theo dõi luồng, nhấp vào **Vừa** trong thanh công cụ để căn giữa lại và phóng to để vừa tất cả trên màn hình.

## Cấu hình một bước

Nhấp vào bất kỳ bước nào để mở cài đặt của nó trong bảng bên phải:


{"Step":"Cài đặt","|------|---------|","**Gửi email**":"Chọn **Email để gửi** từ danh sách thả xuống các chiến dịch của bạn. |","**Chờ**":"Thiết lập **Chờ đợi** — một số nguyên cộng với **giờ** hoặc **ngày**. |","**Chi nhánh**":"Chọn **Nếu người đăng ký thuộc nhóm** — nhóm quyết định giữa Có và Không. |","**Kết thúc**":"Không có cài đặt nào — đó chỉ là một điểm kết thúc. |","![The right-hand panel configuring a Branch step, with the canvas dimmed behind it](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)":"","Changes save automatically as soon as you pick a value — there's no separate **Save** button on the canvas. Every step except **Entry** has a **Delete step** button at the bottom of its settings panel.":"","The emails you pick for **Send email** steps are ordinary campaigns you design in Campaign Studio's regular visual builder — subject line, content blocks, everything. Leave them as **Draft** and just choose them from the dropdown here; the journey sends them for you, you never click Send on them yourself.":"","## Starting from a template":"","Building a flow from a blank canvas isn't always necessary — click **Templates** in the toolbar (or **Browse templates** on an empty canvas) to open a picker with eight ready-made starters:":"","| Template | What it builds |","|----------|-----------------|","| **Welcome series** | Greet new subscribers, share what you're about, then a first-order nudge. |","| **First-order onboarding** | Turn a first-time buyer into a repeat customer with a gentle onboarding sequence. |","| **Post-purchase & review** | Say thanks after any order, then ask for a review once it's arrived. |","| **VIP vs. standard offer** | After an order, branches on your VIP segment to send the right follow-up offer to each group. |","| **Abandoned cart recovery** | Remind a shopper who left items behind, then a follow-up nudge a day later. |","| **Win-back lapsed customers** | Re-engage a customer who hasn't bought in a while with a reason to return. |","| **Post-delivery review request** | Ask for a review a few days after an order is marked Delivered. |","| **Back-in-stock alert** | Tell a waiting shopper the moment a product they wanted is available again. |","Each template is pre-wired to the matching trigger — for example, applying **Win-back lapsed customers** to a new journey also expects that journey's **Trigger** to be **Customer lapsed (win-back)**. See [Triggered journeys](/help/triggered-journeys) for what fires each of these trigger events and how the recovery-focused ones behave (idle windows, guest checkout, once-per-order review requests, and how a back-in-stock journey takes over from the plain one-off alert).":"","![The template picker showing the ready-made starter journeys](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)":"","Applying a template **replaces the current flow** on the canvas, so use it at the start of designing a journey rather than partway through. Spwig re-links each step to a real email or segment wherever the names match something you already have; anywhere it can't find a match, the header reports how many steps still need an email or segment chosen so you know exactly what to finish before going live.":"","## Sharing journeys":"","Two toolbar buttons let you move a journey's design between steps or between stores:":"","- **Export** downloads the journey as a `.journey.json` file — a portable description of the flow's shape (its steps, waits, branches, and Yes/No paths) plus the *names* of the emails and segments each step uses. It doesn't include the email designs themselves or any subscriber data.":"","- **Import** loads a `.journey.json` file into the current journey, replacing what's on the canvas.":"","This is useful for backing up a flow you're proud of, handing a proven welcome series to another Spwig store, or rebuilding a journey after cloning your store to a new install.":""}

Giống như các mẫu, Spwig liên kết lại email và các đoạn bằng tên nơi có sự khớp giữa cửa hàng đích, và đánh dấu những gì nó không thể khớp để bạn hoàn tất cài đặt.

## Kích hoạt hành trình của bạn

Khi luồng đã sẵn sàng, sử dụng nút trạng thái ở góc trên cùng bên phải của trình xây dựng. Một nút nhỏ hiển thị trạng thái hiện tại của hành trình — **Bản nháp**, **Đang hoạt động**, hoặc **Tạm dừng** — bên cạnh nút **Kích hoạt**.

Bấm vào **Kích hoạt** **sẽ kiểm tra luồng trước**. Nếu bất kỳ điều gì có thể làm gián đoạn hoạt động của nó, việc kích hoạt sẽ bị chặn và một thanh thông báo liệt kê các vấn đề — ví dụ như một bước **Gửi email** mà không có email nào được chọn, một bước **Chi nhánh** mà không có đoạn nào hoặc không có đường dẫn Yes/No, một email hoặc đoạn đã bị xóa sau này, hoặc một vòng lặp sẽ chạy mãi mãi. Mỗi vấn đề có thể bấm được: chọn nó sẽ chuyển đến bước gây lỗi, bước đó sẽ được đánh dấu bằng màu đỏ cho đến khi bạn sửa xong. Các cảnh báo (ví dụ như một bước không thể tiếp cận hoặc một bước **Chờ** mà không có thời gian chờ được đặt) cũng được liệt kê nhưng không làm gián đoạn việc kích hoạt.

![Kích hoạt bị chặn, với vấn đề được liệt kê trong thanh thông báo và bước gây lỗi được đánh dấu bằng màu đỏ](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Một khi luồng vượt qua, nút sẽ chuyển sang **Đang hoạt động** và hành trình bắt đầu ghi nhận người đăng ký mỗi khi trigger của nó được kích hoạt. Nút sẽ trở thành **Tạm dừng**, điều này làm dừng việc ghi nhận mới — người đăng ký đã ở giữa chừng sẽ tiếp tục nhận các bước còn lại. Xem [Hành trình được kích hoạt](/help/triggered-journeys) để biết cách các bước ghi nhận, thời gian chờ và trạng thái tương tác với nhau.

## Xem ai đang ở trong hành trình

Một khi hành trình đã hoạt động, mỗi bước sẽ hiển thị một **thẻ đếm** nhỏ ở góc: số lượng người đăng ký đang ở bước đó ngay bây giờ. Đây là cách nhanh để xem mọi người đang chảy đến đâu và nơi nào họ đang tích tụ — một con số lớn trên bước **Chờ** là điều bình thường, trong khi việc tích tụ chỉ xảy ra trước một email cụ thể có thể đáng để xem xét. Các con số được làm mới mỗi khi bạn quay lại tab trình xây dựng.

![Bản vẽ với các thẻ đếm đang hoạt động trên các bước và nút Kích hoạt trong thanh công cụ](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## Mẹo

- Thiết kế luồng trong khi nó vẫn ở trạng thái **Bản nháp** — không ai được ghi nhận cho đến khi bạn **Kích hoạt** nó. Việc kích hoạt từ trình xây dựng sẽ thực hiện kiểm tra nhanh trước và sẽ không cho phép một luồng bị hỏng hoạt động, do đó không có rủi ro về một hành trình chưa hoàn tất ghi nhận người đăng ký.
- Bắt đầu từ một **Mẫu** ngay cả khi bạn có kế hoạch tùy chỉnh nhiều — nó nhanh hơn để chỉnh sửa một luồng hiện có so với việc xây dựng từng nút một, và nó thể hiện mẫu chi nhánh nếu bạn chưa từng sử dụng nó trước đây.
- Sau khi áp dụng mẫu hoặc nhập tệp, kiểm tra tiêu đề để xem có ghi chú về các bước không khớp không và điền vào bất kỳ bước nào **Gửi email** hoặc **Chi nhánh** nào mà nó không thể khớp trước khi kích hoạt.
- Bấm vào **Thích hợp** mỗi khi luồng trở nên rộng (đặc biệt là các nhánh) — đó là cách nhanh nhất để xem lại hình dạng toàn bộ sau khi phóng to hoặc di chuyển.
- Giữ tên bước dễ quét bằng cách giữ mỗi bước **Chờ** ngay trước email mà nó làm chậm, thay vì tập hợp nhiều bước **Chờ** cùng nhau.
- **Xuất** một hành trình đang hoạt động trước khi thực hiện các thay đổi lớn cho nó — đó là cách nhanh để giữ một bản sao dự phòng bạn có thể nhập lại nếu bạn không thích kết quả.
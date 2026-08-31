---
title: Chiến dịch định kỳ
---

Tính năng **Chiến dịch định kỳ** trong Campaign Studio cho phép bạn thiết lập một bản tin một lần — chẳng hạn như bản tổng hợp sản phẩm hàng tuần hoặc bản tin blog hàng tháng — và để Spwig tự động gửi theo lịch lặp lại, thay vì bạn phải tạo và gửi một chiến dịch mới thủ công mỗi lần.

## Phát sóng (Broadcast) so với định kỳ (Recurring)

Mỗi chiến dịch trong Campaign Studio đều có một **Loại chiến dịch**:

| Loại | Hành vi |
|------|-----------|
| **Phát sóng (Broadcast)** | Gửi một lần — ngay lập tức hoặc vào một ngày và giờ đã lên lịch cụ thể. Sử dụng loại này cho các email thông báo, khuyến mãi hoặc ra mắt sản phẩm chỉ diễn ra một lần. |
| **Định kỳ (Recurring)** | Hoạt động như một mẫu (template) được gửi theo lịch lặp lại. Mỗi lần gửi là một bản sao mới, có ngày tháng, được gọi là một **lần thực thi (occurrence)** — bản thân mẫu không bao giờ được "gửi" trực tiếp. |

Để chuyển một chiến dịch thành chiến dịch định kỳ, hãy mở nó trong **Campaign Studio > Campaigns** và đặt **Loại chiến dịch** thành **Định kỳ (Recurring)**, sau đó lưu. Một phần **Lịch (Schedule)** sẽ xuất hiện trên chiến dịch khi bạn mở lại nó — phần này chỉ hiển thị cho các chiến dịch định kỳ.

![Loại chiến dịch được đặt thành Định kỳ](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## Thiết lập lịch

Khi một chiến dịch là định kỳ, phần **Lịch (Schedule)** của nó kiểm soát thời điểm nó được kích hoạt:

| Trường | Mô tả |
|-------|-------------|
| **Hoạt động (Active)** | Bật hoặc tắt tính lặp lại mà không xóa lịch. |
| **Tần suất (Cadence)** | **Hàng ngày**, **Hàng tuần**, hoặc **Hàng tháng**. |
| **Khoảng cách (Interval)** | Gửi mỗi N đơn vị tần suất — ví dụ: khoảng cách `2` với tần suất **Hàng tuần** có nghĩa là mỗi 2 tuần. |
| **Ngày trong tuần (Weekday)** | Ngày nào để gửi cho tần suất hàng tuần (`0` = Thứ Hai … `6` = Chủ Nhật). |
| **Ngày trong tháng (Day of month)** | Ngày nào để gửi cho tần suất hàng tháng (`1`–`28`, để đảm bảo mọi tháng đều có ngày đó). |
| **Thời gian gửi (Send time)** | Thời điểm trong ngày mà chiến dịch được gửi đi. |
| **Múi giờ (Timezone)** | Tên múi giờ IANA, ví dụ: `Europe/London` hoặc `America/New_York` — thời gian gửi được diễn giải theo múi giờ này, không phải múi giờ của máy chủ. |

![Phần lịch hàng tuần trên một chiến dịch định kỳ](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

Ngay khi bạn lưu một lịch đang hoạt động, nó sẽ **tự động kích hoạt** — Spwig tính toán thời điểm kích hoạt tiếp theo và hiển thị nó trong **Thời điểm chạy tiếp theo (Next run at)**. Bạn không cần phải kích hoạt bất cứ điều gì thủ công; một tác vụ nền sẽ kiểm tra các lịch đến hạn và gửi lần thực thi khi đến thời điểm. **Thời điểm chạy cuối cùng (Last run at)** và **Số lần thực thi đã gửi (Occurrences sent)** sẽ tự động cập nhật sau mỗi lần gửi để bạn có thể thấy lịch đang hoạt động.

## Chính sách không có nội dung mới

Các bản tin định kỳ thường có nội dung động — phổ biến nhất là khối **Bài viết Blog** (hoặc **Lưới sản phẩm**) được đặt thành **Mới kể từ lần gửi trước** trong trình tạo trực quan, chỉ lấy các bài viết đã được xuất bản — hoặc các sản phẩm được thêm — kể từ lần gửi trước của chiến dịch. Điều này đặt ra một câu hỏi rõ ràng: điều gì sẽ xảy ra nếu một lần chạy theo lịch đến mà không có nội dung mới nào để giới thiệu?

Spwig giải quyết điều này bằng **Chính sách không có nội dung mới (No-new-content policy)** của lịch:

{"| Policy | What happens | Best for |
|--------|---------------|----------|
| **Skip this send** *(default)* | The occurrence is skipped entirely — nothing sends. The schedule moves straight on to its next scheduled run. | A blog or product digest, so subscribers are never sent an email that just repeats what they already saw. |
| **Send anyway (omit empty blocks)** | The email sends on schedule regardless. Any block that has nothing new — like an empty "New since last send" Blog Posts block — simply renders nothing in that spot. | Newsletters that always have other content worth sending (a welcome message, evergreen sections, or several dynamic blocks) even if one block comes up empty. |
| **Hold and send late** | The send is postponed. Spwig checks again once a day for fresh content, up to the **Hold window (days)**. If new content appears within that window, the occurrence sends late; if the window elapses with nothing new, that occurrence is given up and the schedule moves on to its next slot. | A cadence you want to protect (e.g. always send *something* eventually) without firing an empty issue the moment nothing new happened to publish that week. |

Only campaigns using delta-aware content — a Blog Posts block or a Product Grid set to **New since last send** — trigger this check. A recurring campaign with no such blocks is always considered to have fresh content and sends normally on schedule.

**Hold window (days)** only applies to the **Hold and send late** policy — it sets how many days Spwig will keep retrying before giving up on that occurrence.

## A/B testing each occurrence

A recurring newsletter is a natural place to A/B test your **subject lines** — you send on a regular cadence to the same audience, so you can keep learning what wording earns more opens. Spwig can run a fresh subject-line A/B on **every occurrence** automatically.

Set it up in the **Schedule** section:

1. In **A/B subject lines**, enter **two to four** subject lines, one per line. Leave it blank to send occurrences normally with the template's own subject.
2. Set the **A/B test sample %** — the share of each occurrence's audience used to test, split evenly across the subjects. The rest is the holdout that receives the winner.
3. Choose the **A/B winner metric** (open or click rate), the **A/B test window (hours)** to gather results before deciding, and whether to **auto-send the winner** to the holdout.

From then on, each time the schedule fires, that occurrence splits its audience, sends each subject line to a slice, waits out the test window, then picks the winning subject and sends it to everyone else — with no further action from you. Each occurrence is its own self-contained test, so you get a fresh read every send and can watch which subjects win over the weeks. Each occurrence's result shows up under **Occurrence history** below, linking straight to its results page with the per-variant rates, the winner, and how confident Spwig is (see [A/B Testing](ab-testing) for how to read those results).

Two things worth knowing:

- **A/B testing here is subject-line only.** To compare entirely different designs, use a one-off broadcast A/B test — the full wizard, which supports content variants, is for broadcast campaigns.
- If an occurrence's audience is ever **too small to split** across the variants, Spwig quietly sends that occurrence as a normal newsletter instead — a lean week never means a missed send.

## Occurrence history

Every time a recurring campaign actually sends, Spwig creates a dated **occurrence** — a real, independent campaign record with its own subject, recipients, and send statistics (sent, failed, skipped, opens, clicks). The occurrence is named after the template with the send date appended, e.g. "Weekly Blog Digest — 2026-08-19".}

Trang chỉnh sửa chiến dịch định kỳ liệt kê **Lịch sử xuất hiện** — các lần xuất hiện gần nhất, mỗi lần liên kết đến bản ghi chiến dịch riêng của nó để bạn có thể xem xét chính xác những gì đã được gửi và hiệu suất ra sao.

![Danh sách lịch sử xuất hiện trên chiến dịch định kỳ](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## Mẹo

- Kết hợp chiến dịch định kỳ với khối **Bài viết Blog** được đặt ở chế độ **Mới kể từ lần gửi trước** để tạo bản tin tự động "bài viết mới trong tuần" — bạn viết bài, Spwig lo việc gửi email.
- Bắt đầu với **Bỏ qua lần gửi này** cho các bản tin nội dung. Đây là mặc định an toàn nhất: người đăng ký sẽ không bao giờ nhận lại nội dung của lần trước.
- Chỉ chuyển sang **Gửi bất kể** nếu mẫu của bạn có nội dung khác đáng để gửi riêng, ngay cả khi khối động trống.
- Sử dụng **Giữ lại và gửi muộn** khi việc bỏ lỡ nhịp độ đôi khi là chấp nhận được, nhưng bỏ lỡ liên tục trong nhiều tuần thì không — đặt thời gian giữ lại phù hợp với khoảng thời gian bạn chấp nhận được.
- Kiểm tra **Thời gian chạy tiếp theo** sau khi lưu lịch trình để xác nhận nó rơi vào ngày và giờ như mong đợi, đặc biệt khi làm việc qua nhiều múi giờ.
- Xem xét **Lịch sử xuất hiện** thường xuyên — một mẫu liên tục bị bỏ qua là dấu hiệu cho thấy nguồn nội dung động (ví dụ: blog) đã ngừng hoạt động.
---
title: 반복 캠페인
---

Campaign Studio의 **반복 캠페인**은 단일 이메일로 뉴스레터를 설정할 수 있으며, 주간 제품 리뷰나 월간 블로그 요약과 같이 Spwig가 반복적으로 자동으로 전송하도록 설정할 수 있습니다. 이는 매번 새로운 캠페인을 수동으로 생성하고 보낼 필요 없이, 한 번씩 생성하고 보냅니다.

## 방송 vs. 반복

Campaign Studio의 모든 캠페인에는 **캠페인 유형**이 있습니다.

| 유형 | 동작 | 
|------|-----------| 
| **방송** | 한 번만 전송합니다 — 즉시 또는 단일 예약 날짜 및 시간에 전송합니다. 단일 발표, 할인 이벤트, 제품 출시 이메일에 사용하십시오. | 
| **반복** | 반복 일정에 따라 전송되는 템플릿 역할을 합니다. 각 전송은 날짜가 새롭게 적용된 복사본으로, **발생**이라고 불립니다. 템플릿 자체는 직접 전송되지 않습니다. | 

**Campaign Studio > 캠페인**에서 캠페인을 열고 **캠페인 유형**을 **반복**로 설정하면, 캠페인을 다시 열었을 때 **스케줄** 섹션이 표시됩니다. 이는 반복 캠페인에서만 표시됩니다.

![캠페인 유형이 반복으로 설정됨](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## 스케줄 설정

캠페인이 반복형이 되면, **스케줄** 섹션이 캠페인의 실행 시점을 제어합니다:

| 필드 | 설명 | 
|-------|-------------| 
| **활성** | 스케줄을 삭제하지 않고 반복을 켜거나 끄는 것입니다. | 
| **주기** | **일일**, **주간**, 또는 **월간**입니다. | 
| **인터벌** | N개의 주기 단위마다 전송합니다. 예를 들어, 주간 주기와 인터벌 `2`는 2주마다 전송됩니다. | 
| **요일** | 주간 주기에서 전송할 요일을 지정합니다(`0` = 월요일 … `6` = 일요일). | 
| **일** | 월간 주기에서 전송할 날을 지정합니다(`1`–`28`로, 모든 달에 해당 날이 포함됩니다). | 
| **전송 시간** | 캠페인이 전송되는 시간입니다. | 
| **시간대** | IANA 시간대 이름, 예: `Europe/London` 또는 `America/New_York` — 전송 시간은 서버의 시간대가 아닌 이 시간대에서 해석됩니다. |

![반복 캠페인의 주간 일정 섹션](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

활성 일정을 저장하는 즉시 **자동으로 활성화**됩니다 — Spwig은 다음 실행 시간을 계산하여 **다음 실행 시간**에 표시합니다. 수동으로 무언가를 트리거할 필요가 없으며, 백그라운드 작업이 기한이 도래한 일정을 확인하여 시간이 되면 해당 발생 이벤트를 전송합니다. **마지막 실행 시간**과 **전송된 발생 횟수**는 모든 전송 후 자동으로 업데이트되므로 일정이 정상적으로 작동하고 있는지 확인할 수 있습니다.

## 새 콘텐츠 없음 정책

반복 뉴스레터에는 동적 콘텐츠가 자주 포함됩니다 — 가장 흔한 예는 시각적 빌더에서 **새로 추가된 항목만**으로 설정된 **블로그 게시물** 블록(또는 **제품 그리드**)입니다. 이는 캠페인의 이전 전송 이후에 게시된 게시물 — 또는 추가된 제품 — 만 가져옵니다. 이는 명백한 질문을 제기합니다: 예정된 실행이 도착했을 때 특징을 지을 새 콘텐츠가 없다면 어떻게 되나요?

Spwig은 일정의 **새 콘텐츠 없음 정책**으로 이 질문에 답합니다:


| 정책 | 발생하는 내용 | 적합한 경우 | 
|--------|---------------|----------| 
| **이 발송을 건너뜀** *(기본값)* | 이 발생은 완전히 건너뛰어집니다. 이메일이 전송되지 않습니다. 일정은 바로 다음 예정된 실행으로 이동합니다. | 구독자가 이미 본 내용을 반복하는 이메일을 받지 않도록 하기 위해 블로그나 제품 요약을 보내는 경우입니다. | 
| **어쨌든 발송 (비어 있는 블록 생략)** | 이메일은 일정에 따라 발송됩니다. "이전 발송 이후 새 콘텐츠" 블록과 같이 아무것도 없는 블록은 해당 영역에서 아무것도 표시되지 않습니다. | 한 블록이 비어 있어도 다른 콘텐츠가 항상 존재하는 뉴스레터(환영 메시지, 영구히 유효한 섹션, 여러 개의 동적 블록 등)에 적합합니다. | 
| **지연 및 발송** | 발송이 연기됩니다. Spwig는 **보류 기간(일)**까지 하루에 한 번씩 새 콘텐츠가 있는지 확인합니다. 해당 기간 내에 새 콘텐츠가 나타나면 발송이 지연되며, 기간이 지나도 새 콘텐츠가 없으면 해당 발생은 포기하고 일정이 다음 슬롯으로 이동합니다. | 한 번은 발송되어야 하는 일정을 보호하고 싶은 경우(예: 결국 무언가라도 발송하고 싶음)이며, 새 콘텐츠가 없었을 때 빈 이슈를 발송하지 않도록 하기 위해 적합합니다. | 

이 체크는 델타 인식 콘텐츠를 사용하는 캠페인만 트리거합니다. 블로그 게시물 블록 또는 "이전 발송 이후 새 콘텐츠"로 설정된 제품 그리드가 있는 블로그 게시물 블록만 해당됩니다. 반복되는 캠페인에 이러한 블록이 없으면 항상 새 콘텐츠가 있다고 간주되며, 정해진 일정에 따라 정상적으로 발송됩니다. 

**보류 기간(일)**은 **지연 및 발송** 정책에만 적용되며, 이는 Spwig가 해당 발생에 대해 포기하기 전까지 다시 시도할 일 수를 설정합니다. 

## 각 발생에 대한 A/B 테스트 

반복되는 뉴스레터는 **제목 줄**에 대한 A/B 테스트를 수행하기에 적합한 장소입니다. 정기적으로 동일한 대상에게 발송하므로, 어떤 표현이 더 많은 열림을 얻는지 배울 수 있습니다. Spwig는 **모든 발생**에 대해 자동으로 새 제목 줄 A/B 테스트를 실행할 수 있습니다. 

**일정** 섹션에서 설정할 수 있습니다: 

1. 

In **A/B subject lines**, enter **two to four** subject lines, one per line.

Leave it blank to send occurrences normally with the template's own subject.
2.

Set the **A/B test sample %** — the share of each occurrence's audience used to test, split evenly across the subjects.

The rest is the holdout that receives the winner.
3.

Choose the **A/B winner metric** (open or click rate), the **A/B test window (hours)** to gather results before deciding, and whether to **auto-send the winner** to the holdout.

From then on, each time the schedule fires, that occurrence splits its audience, sends each subject line to a slice, waits out the test window, then picks the winning subject and sends it to everyone else — with no further action from you. Each occurrence is its own self-contained test, so you get a fresh read every send and can watch which subjects win over the weeks. Each occurrence's result shows up under **Occurrence history** below, linking straight to its results page with the per-variant rates, the winner, and how confident Spwig is (see [A/B Testing](ab-testing) for how to read those results).

Two things worth knowing:

- **A/B testing here is subject-line only.** To compare entirely different designs, use a one-off broadcast A/B test — the full wizard, which supports content variants, is for broadcast campaigns.
- If an occurrence's audience is ever **too small to split** across the variants, Spwig quietly sends that occurrence as a normal newsletter instead — a lean week never means a missed send.

## Occurrence history

Every time a recurring campaign actually sends, Spwig creates a dated **occurrence** — a real, independent campaign record with its own subject, recipients, and send statistics (sent, failed, skipped, opens, clicks). The occurrence is named after the template with the send date appended, e.g. "Weekly Blog Digest — 2026-08-19".


반복 캠페인의 편집 페이지에는 **발생 이력**이 표시됩니다. 이는 최근 발생한 이벤트들을 보여주며, 각 이벤트는 해당 이벤트의 고유한 캠페인 기록으로 연결되어 있어 정확히 무엇이 전송되었는지 및 그 성과가 어떻게인지 확인할 수 있습니다.

![반복 캠페인의 발생 이력 목록](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## 팁

- 콘텐츠 디지 estates를 위해 **블로그 게시물** 블록을 **마지막 전송 이후 새롭게**로 설정하여, 당신이 게시물을 작성하면 Spwig가 이메일을 보내주는 자동 유지되는 '이번 주 신규 게시물' 디지스트를 생성할 수 있습니다.
- 콘텐츠 디지ests를 시작할 때는 **이번 전송은 건너뛰기**를 선택하세요. 이는 가장 안전한 기본 설정입니다. 구독자는 이전에 전송된 콘텐츠를 다시 받지 않습니다.
- 동적 블록이 비어 있을지라도 전송할 만한 가치가 있는 다른 템플릿 콘텐츠가 있다면 **이傪 전송해도 됩니다**로 전환하세요.
- 가끔은 주기적인 이벤트를 놓치는 것이 문제가 아니라 몇 주 연속으로 이벤트를 놓치는 것이 문제가 될 때는 **지연 시켜서 전송하기**를 사용하세요. 이때는 편안하게 느끼는 간격에 맞게 보류 기간을 설정하세요.
- 일정을 저장한 후 **다음 실행 시간**을 확인하여 원하는 날짜와 시간에 정확히 설정되었는지 확인하세요. 특히 시간대를 넘나들며 작업할 때는 특히 중요합니다.
- **발생 이력**을 정기적으로 검토하세요. 반복되는 이벤트가 계속해서 건너뛰는 경우, 동적 콘텐츠 소스(예: 블로그)가 잠들어 있는 것을 나타냅니다.

모든 마크다운 포맷, 이미지 경로, 코드 블록, 기술 용어를 보존합니다.
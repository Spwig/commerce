---
title: CSV에서 구독자 가져오기
---

다른 곳에 이미 메일링 리스트가 있다면 — 오래된 이메일 도구, 뉴스레터 가입자 스프레드시트, 트레이드 쇼 배지 스캔 자료 등 — Spwig에 해당 연락처를 하나씩 추가할 필요가 없습니다. Campaign Studio의 구독자 가져오기 기능은 CSV 또는 Excel 파일을 읽어 모든 유효한 연락처를 한 번에 대상 고객에 추가하며, 태그 지정, 세그먼트 설정 및 이메일 전송을 즉시 수행할 수 있는 상태로 준비합니다.

## 가져오기 전: 동의

모든 가져오기 작업에서는 다음 내용을 확인하는 상자를 체크해야 합니다: **"이 연락처들은 저로부터 마케팅 이메일을 수신하는 데 동의했습니다."** 이는 형식적인 절차가 아닙니다 — 실제로 귀하로부터의 마케팅 이메일 수신에 동의한 연락처만 가져오세요. 이는 두 가지 이유로 중요합니다:

- **대부분의 지역에서 법적 요구사항입니다.** 수신에 동의하지 않은 사람에게 마케팅 이메일을 보내면 많은 관할권에서 동의 법을 위반하게 됩니다.
- **전달률을 보호합니다.** 수신에 동의하지 않은 사람에게 이메일을 보내면 스팸 신고와 반송이 발생하며, 메일함 제공업체는 이를 근거로 귀하가 보낸 *모든* 이메일 — 동의한 사람에게 보낸 이메일을 포함하여 — 수신함에 도달하는지 여부를 결정합니다.

리스트가 명확하게 동의한 가입자로부터 온 것이 아니라면, 가져오지 마세요.

## 파일 준비

가져오기 도구는 헤더 행이 있는 `.csv` 또는 `.xlsx` 파일을 지원합니다. 필수 항목은 한 가지 열뿐입니다:

| 열 | 필수 여부 | 참고 |
|--------|-----------|-------|
| **이메일** | 예 | 유효한 이메일 주소여야 합니다. |
| **이름** | 아니오 | 이메일 개인화에 사용됩니다. |
| **성** | 아니오 | 이메일 개인화에 사용됩니다. |
| **언어** | 아니오 | 구독자의 선호 언어 코드 (예: `en`, `es`). |

열은 헤더 이름에 따라 해당 필드에 자동으로 매핑되므로, 먼저 이름을 변경할 필요가 없습니다 — `E-mail`, `Email Address`, `First Name`, `Given Name`, `Surname`, `Locale`과 같은 일반적인 변형은 모두 인식됩니다.

각 가져오기 작업은 **5 MB** 및 **5,000행**으로 제한됩니다. 리스트가 이보다 크다면 더 작은 파일로 나누어 순서대로 가져오세요.

## 연락처 가져오기

1.

Open **Campaign Studio > Subscribers** and click **Import CSV**.
2.

Choose your `.csv` or `.xlsx` file.
3.

Choose what happens **for contacts already on your list** — see [Handling duplicates](#handling-duplicates) below.
4.

Optionally choose a tag under **Tag imported contacts as** to label everyone in this import (e.g. `Event 2026`) — see [Subscriber Tags](/help/subscriber-tags) for more on tags.
5.

Tick **These contacts have agreed to receive marketing email from me**.
6.

Click **Continue**.

![The import upload form with a file chosen, a tag selected, and consent confirmed](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

Spwig then shows you a preview before anything is actually imported:

![The import preview showing new, existing, and skipped-invalid counts with reasons](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **New contacts** — rows that will create a brand-new subscriber.
- **Already on your list** — rows whose email address matches an existing subscriber.
- **Skipped (invalid)** — rows that couldn't be read, each listed with its row number and the reason (an invalid email format, an empty email cell, or a duplicate of an earlier row in the same file).

Check these numbers, then click **Import now** to commit the import, or **Cancel** to back out without changing anything.

## Handling duplicates

A row counts as a duplicate when its email address matches a subscriber you already have. You choose how Spwig treats those rows on the upload form:

| Option | What happens |
|--------|--------------|
| **Leave them unchanged** *(default)* | The existing subscriber's name and language are kept as-is. |
| **Update their name / language** | The existing subscriber's first name, last name, and language are updated from the file (only for the fields the file actually provides). |

가져오기용으로 선택한 태그는 파일에 있는 **모든 사람** - 새 연락처이든 기존 연락처이든 - 어떤 중복 옵션을 선택하든 적용됩니다.

"VIP 목록"을 **VIP** 태그와 함께 가져오면 기존에 보유한 사람들에게도 태그가 적용됩니다.

중복 옵션는 이미 존재하는 연락처의 *이름과 언어*가 덮어씌워지는지를 결정합니다.

## 가져오기 후

가져오기로 생성된 모든 연락처는 소스 **Import**로 기록되며, 가져오기를 실행한 시점에 동의한 것으로 표시됩니다 (그들이 다른 곳에서 이미 동의한 날짜보다 이른 시점이 아님).

파일에 제공된 경우, 그들의 구독자 기록에 이름과 성이 저장되며, 이는 캠페인에서 사용하는 `[[first_name]]` 및 `[[last_name]]` 병합 필드가 이들에게 대해 올바르게 개인화되도록 합니다. 이들은 Spwig 계정을 생성한 적이 없지만, 이에 관계없이 적용됩니다.

## 팁

- 업로드하기 전에 소스 목록을 단일 시트의 CSV 또는 `.xlsx` 파일로 내보내십시오. 헤더 행이 깨끗해야 합니다. 추가 시트, 병합된 셀, 요약 행은 열 매칭을 방해할 수 있습니다.
- **가져온 연락처에 태그 지정**을 사용하여 나중에 타겟팅할 정확한 대상을 즉시 생성하십시오. 이에 대한 세그먼트를 만드는 방법은 [구독자 태그](/help/subscriber-tags)를 참조하십시오.
- 가져오기가 실패했다고 가정하기 전에 **Skipped (invalid)** 이유를 항상 읽으십시오. 대부분의 실제 목록에서는 명확한 이유가 있는 수십 개의 건너뛴 행이 정상입니다.
- 동일한 파일을 다시 실행하는 것은 안전합니다. 이미 가져온 연락처는 두 번째에 중복으로 간주되며, 다시 생성되지 않습니다.
- 여러 개의 작은 목록을 통합하고 있다면, 각 가져오기에 다른 태그를 지정하십시오 (예: `Import: Jan Event`, `Import: Trade Show`). 이렇게 하면 나중에 모두 주요 대상 집단에 혼합되어 있어도 구분할 수 있습니다.
- 5,000줄 이상의 목록의 경우, 임의의 경계로 나누는 대신 명백한 경계(알파벳, 소스, 수집 날짜 등)로 나누십시오. 이렇게 하면 각 배치가 나중에 식별하기 쉬워집니다.
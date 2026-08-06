---
title: 플랫폼 업데이트
---

Your Spwig installation is built from a collection of components — themes, widgets, integrations, page builder elements, and provider connections — each with its own version that can be updated independently. The Component Registry gives you a central view of everything installed, shows which components have updates waiting, and lets you install or roll back updates at any time.

![Component Registry Overview](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Understanding the component registry

Navigate to **System Dashboard > Component Updates** to see every component installed on your store. Each row shows:

- **Name** — the component's display name
- **Type** — what kind of component it is (theme, widget, integration, etc.)
- **Current version** — the version currently running on your store
- **Update status** — whether an update is available
- **Channel** — which update channel the component follows
- **Auto Update** — whether updates install automatically
- **Locked** — whether the component is frozen at its current version

The dashboard at the top of the page shows summary counts: total components installed, how many have updates available, and how many are up to date.

### Component types

| Type | What it is |
|------|------------|
| Theme | Your store's visual design |
| Widget | Reusable page builder blocks |
| Page Builder Element | Custom elements for the page builder |
| Page Builder Utility | Editor tools and utilities |
| Header / Footer Template | Header and footer layouts |
| Shipping Provider | Carrier integrations (FedEx, UPS, etc.) |
| Email Provider | Email delivery services |
| Payment Provider | Payment gateway integrations |
| Exchange Rate Provider | Currency rate data sources |
| Translation Provider | AI translation services |
| Language Pack | Interface translation files |

## Update channels

Every component follows an update channel that controls which releases it receives.

각 구성 요소를 얼마나 많은 위험을 감수할 수 있는지에 따라 다른 채널에 할당할 수 있습니다.

| 채널 | 설명 | 최적의 사용 대상 |
|---------|-------------|----------|
| **Stable** | 프로덕션용, 철저히 테스트된 릴리스 | 라이브 스토어의 모든 구성 요소 |
| **Beta** | 안정화 전에 새로운 기능을 테스트하기 위한 사전 릴리스 빌드 | 미리보기를 원하는 비중요 구성 요소 |
| **Development** | 최신 기능, 불안정할 수 있음 | 테스트 환경만 |
| **Security** | 중요한 보안 패치만, 최고 우선순위로 제공 | 안정성이 필수적인 구성 요소 |

구성 요소의 채널을 변경하려면 이름을 클릭하여 세부 정보 뷰를 열고, **Update Channel**(채널 업데이트) 필드에서 새 값을 선택한 후 저장합니다.

## 업데이트 확인

Spwig은 업데이트 서버 설정에서 구성된 간격(기본값: 24시간마다)에 따라 자동으로 업데이트를 확인합니다. 즉시 확인하려면:

1. **System Dashboard > Component Updates**(시스템 대시보드 > 구성 요소 업데이트)로 이동합니다.
2. 페이지 상단의 **Check for Updates**(업데이트 확인) 버튼을 클릭합니다.
3. 시스템이 Spwig 업데이트 서버에 연결하여 모든 구성 요소의 업데이트 상태를 새로고침합니다.
4. 업데이트가 가능한 구성 요소는 강조 표시되고, **Updates Available**(가능한 업데이트) 카운트가 업데이트됩니다.

리스트의 액션 메뉴에서 **Check for Updates**(업데이트 확인) 액션을 사용하여 개별 구성 요소에 대한 업데이트 확인을 트리거할 수도 있습니다.

## 업데이트 설치

### 단일 구성 요소 업데이트

1. **System Dashboard > Component Updates**(시스템 대시보드 > 구성 요소 업데이트)로 이동합니다.
2. 업데이트하려는 구성 요소를 찾습니다. 업데이트가 가능한 구성 요소는 버전 번호 옆에 업데이트 지시 표시가 나타납니다.
3. 해당 구성 요소의 행에서 **Install Update**(업데이트 설치) 버튼을 클릭합니다.
4. 확인 요청이 표시되면 업데이트를 확인합니다.
5. 업데이트가 다운로드, 검증 및 설치됩니다. 각 단계에 대한 진행 표시가 나타납니다.
6. 완료되면 구성 요소의 **Current Version**(현재 버전)이 새 버전 번호로 업데이트됩니다.

### 여러 구성 요소 업데이트

1.

업데이트하려는 구성 요소 옆의 체크박스를 선택합니다.
2.


업데이트를 설치하려면 **Action** 드롭다운에서 **Install updates**을 선택하세요
3.

**Go**를 클릭하여 계속합니다
4.

업데이트는 종속성 순서에 따라 설치됩니다 — 다른 구성 요소에 의존하는 구성 요소가 먼저 업데이트됩니다

### 업데이트 중에 발생하는 일

업데이트 프로세스는 다음 단계를 거칩니다:

1. **Checking** — 업데이트가 사용 가능한지 확인하고 라이선스가 유효한지 확인합니다
2. **Downloading** — Spwig 업데이트 서버에서 패키지를 다운로드합니다
3. **Verifying** — SHA-256 체크섬을 사용하여 패키지의 무결성을 확인합니다
4. **Extracting** — 새 파일을 압축 해제합니다
5. **Deploying** — 새 버전을 활성화합니다
6. **Health check** — 업데이트 후 구성 요소가 정상 작동하는지 확인합니다

어떤 단계든 실패하면 시스템은 자동으로 이전 버전으로 복원을 시도합니다

## 플랫폼 수준 업데이트

개별 구성 요소 외에도 Spwig는 플랫폼 수준 업데이트를 받을 수 있으며, 이는 코어 스토어 엔진 자체를 업데이트합니다. 이러한 업데이트는 데이터베이스 마이그레이션과 짧은 유지보수 시간을 포함한 더 철저한 프로세스를 거칩니다.

**System Dashboard > Platform Updates**로 이동하여 개별 구성 요소와 별도로 플랫폼 수준 업데이트를 볼 수 있고 관리할 수 있습니다.

### 설치하기 전에 변경 사항 확인

**Check for Updates**을 클릭하여 새 플랫폼 버전이 있는지 확인합니다. 새 버전이 발견되면 **Update Available** 카드에 버전 변경 사항(예: `v1.7.0 → v1.7.1`), **Package Size**, **Est. Time**, 업데이트 **Channel** — 그리고 설치하기 전에 변경 사항을 확인할 수 있는 **What's New** 미리보기가 표시됩니다:

- 새 릴리스를 설명하는 짧은 요약 줄
- 해당 버전의 주요 변경 사항 목록(최대 5개, 더 많은 경우에 대한 참고사항 포함)

업데이트가 데이터베이스 스키마를 변경하는 경우, **Requires database migration** 알림이 표시되며 예상 시간이 표시됩니다.

보안 릴리스는 즉시 설치해야 한다고 권장하는 **Security update** 배지가 표시됩니다.

업데이트 설치 전에 What's New 미리보기를 확인하세요 — 이는 업데이트 후 추가 작업이 필요한지 여부를 가장 빠르게 확인할 수 있는 방법입니다. 예를 들어, 업그레이드가 완료된 후 수행해야 하는 단계가 표시될 수 있습니다.

플랫폼 업데이트 기록은 페이지 하단에 표시됩니다. 각 항목은 버전 전환(예: `v1.3.2 → v1.3.3`), 상태 및 업데이트 프로세스의 지속 시간을 보여줍니다.

보안 업데이트는 별도로 표시되며, 업데이트 서버 구성에서 **Auto Install Security Updates**가 활성화된 경우, 수동 작업 없이 자동으로 설치됩니다.

## 버전 기록 보기

성분의 이전에 설치된 모든 버전을 보려면:

1. 성분 이름을 클릭하여 세부 정보 뷰를 엽니다
2. 페이지 하단의 **Component Versions** 섹션으로 스크롤합니다
3. 각 버전 항목은 버전 번호, 설치 시간, 설치 방법 및 건강 상태를 보여줍니다

시스템은 마지막으로 설치된 세 버전을 롤백용으로 유지합니다. 그 이상의 버전은 자동으로 삭제됩니다.

## 성분 롤백

업데이트가 문제가 발생하면 이전 버전으로 롤백할 수 있습니다:

1. 성분의 세부 정보 뷰를 엽니다
2. 페이지 하단의 **Rollback** 섹션으로 스크롤합니다
3. 복원하려는 버전을 선택합니다
4. **Roll Back to this Version**을 클릭합니다

**Rollback Available**로 표시된 버전만 복원할 수 있습니다. 롤백 로그 항목은 롤백을 시작한 사람과 시간을 기록합니다.

## 성분 잠금

성분을 잠그면 자동 업데이트 포함 모든 업데이트 설치가 방지됩니다. 특정 버전에 의존하는 커스터마이징 또는 통합이 있는 경우에 이 기능이 유용합니다.

1. 성분의 세부 정보 뷰를 엽니다
2. **Lock & Freeze** 섹션의 **Locked** 체크박스를 선택합니다
3. **Lock Reason**에 잠금 이유를 입력하여 팀이 왜 동결되었는지 이해하도록 합니다
4. 기록을 저장합니다

잠긴 성분은 등록 목록에서 잠금 지시자로 표시됩니다. 해제하려면 **Locked**를 선택 해제하고 저장합니다.

## 업데이트 로그 읽기

업데이트 로그는 모든 설치, 업데이트, 롤백 및 건강 상태 확인 작업을 기록합니다:

1. 구성 요소의 상세 보기로 이동
2. **업데이트 로그**는 페이지 하단에 인라인으로 표시됩니다
3. 각 항목은 다음과 같은 정보를 보여줍니다: 수행된 작업, 시작 및 종료 시간, 이전 및 새 버전, 자동 또는 수동 여부, 작업이 실패한 경우 발생한 오류 메시지

**실패** 상태의 로그 항목은 문제 해결에 도움이 되는 전체 오류 메시지를 포함합니다.

## 자동 업데이트 활성화

Spwig이 업데이트가 제공될 때마다 자동으로 설치하도록 허용할 수 있습니다:

1. 구성 요소의 상세 보기로 이동
2. **버전 및 업데이트 상태** 섹션에서 **자동 업데이트**를 선택합니다
3. 기록을 저장합니다

자동 업데이트가 활성화된 경우, 시스템은 다음 예약된 확인 주기 동안 업데이트를 설치합니다. 보안 업데이트는 개별 구성 요소 설정과 관계없이 전역 **보안 업데이트 자동 설치** 설정을 따릅니다.

## 팁

- 테마 및 결제 제공업체는 항상 **Stable** 채널에서 업데이트하세요 — 이들은 가장 고객과 직접 관련된 구성 요소이며 안정성이 가장 중요합니다
- 구성 요소를 수정하기 전에 해당 구성 요소를 잠급니다. 그리고 수정 이유를 명확히 기록하여 향후 팀원들이 업데이트하지 않도록 알 수 있도록 합니다
- 주요 버전 업데이트를 설치하기 전에 구성 요소의 버전 항목에서 **릴리스 노트**를 확인하세요 — 중단 변경 사항은 여기에 표시됩니다
- 플랫폼 업데이트를 설치하기 전에 **Platform Updates** 페이지의 **What's New** 미리보기를 확인하세요 — 릴리스 노트의 전체 내용을 보려면, 추가로 수행해야 할 단계가 있을 수 있으므로 **System Upgrade** 페이지로 이동하세요
- 업데이트 후, 상점의 영향을 받은 영역을 확인하여 모든 것이 예상대로 작동하고 있는지 확인한 후 업데이트가 완료되었음을 선언하세요
- 구성 요소에 자동 업데이트가 활성화된 경우, 자동 업데이트가 성공적으로 완료되고 있는지 확인하기 위해 주기적으로 **업데이트 로그**를 확인하세요
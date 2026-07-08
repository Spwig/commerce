---
title: 'SSO 설정: Google Workspace'
---

이 가이드는 Spwig을 Google Workspace에 연결하여 관리자용 단일 로그인(Single Sign-On)을 설정하는 방법을 안내합니다. 설정이 완료되면 직원들은 Google Workspace 계정을 사용하여 Spwig 관리자 패널에 로그인할 수 있습니다.

**참고:** Google은 시간이 지남에 따라 클라우드 콘솔 인터페이스를 업데이트할 수 있습니다. 이 지침은 2026년 초의 인터페이스를 기준으로 작성되었습니다. 보여지는 화면과 단계가 다를 경우 Google의 공식 문서인 [OAuth 2.0 설정](https://support.google.com/cloud/answer/6158849)을 참조하십시오.

## 사전 조건

- Google Workspace 구독 (Google Workspace Business, Enterprise 또는 Education)
- [Google Cloud Console](https://console.cloud.google.com)에 대한 관리자 액세스
- Spwig 스토어 URL (예: `https://your-store.com`)
- 직원의 이메일 주소는 Spwig에서 Google Workspace 계정과 일치해야 합니다

## 단계 1: Google Cloud 프로젝트 생성 또는 선택

1. [Google Cloud Console](https://console.cloud.google.com)로 이동합니다
2. 상단 바의 프로젝트 선택기를 클릭합니다
3. **새 프로젝트**를 클릭합니다 (기존 프로젝트를 선택하려면 선택할 수 있습니다)
4. 프로젝트 이름을 입력합니다 (예: `Spwig SSO`)
5. 조직을 선택합니다
6. **생성**을 클릭합니다

## 단계 2: OAuth 동의 화면 구성

1. 클라우드 콘솔에서 **API 및 서비스 > OAuth 동의 화면**으로 이동합니다
2. 사용자 유형으로 **내부**를 선택합니다 — 이는 로그인을 Google Workspace 조직 내 사용자로 제한합니다
3. **생성**을 클릭합니다
4. 필요한 필드를 입력합니다:

| 필드 | 값 |
|-------|-------|
| **앱 이름** | `Spwig Admin` (또는 스토어 이름) |
| **사용자 지원 이메일** | 관리자 이메일 주소 |
| **허용된 도메인** | `your-store.com` (스토어 도메인, `https://` 없이) |
| **개발자 연락 이메일** | 관리자 이메일 주소 |

5. **저장 및 계속**을 클릭합니다
6. **범위** 페이지에서 **추가 또는 제거 범위**를 클릭하고 다음을 추가합니다:
   - `openid`
   - `email`
   - `profile`
7. **저장 및 계속**을 클릭합니다
8. 요약을 확인하고 **대시보드로 돌아가기**를 클릭합니다

## 단계 3: OAuth 자격 증명 생성

1. **API 및 서비스 > 자격 증명**으로 이동
2. **자격 증명 생성 > OAuth 클라이언트 ID**를 클릭
3. 클라이언트를 구성:

| 필드 | 값 |
|-------|-------|
| **응용 프로그램 유형** | 웹 애플리케이션 |
| **이름** | `Spwig SSO` |
| **허용된 리디렉션 URI** | `https://your-store.com/oidc/callback/` |

4. **생성**을 클릭
5. 대화상자에 **클라이언트 ID** 및 **클라이언트 비밀**이 표시됩니다 — 두 값을 모두 복사하세요. JSON 파일로 다운로드하여 안전하게 보관할 수도 있습니다.

**중요:** 리디렉션 URI는 `https://your-store.com/oidc/callback/`과 정확히 일치해야 합니다 — 끝에 슬래시와 `https://` 스키마를 포함합니다. `your-store.com`을 실제 상점 도메인으로 대체하세요.

## 단계 4: 발견 URL 가져오기

Google은 모든 Workspace 임차인에 대해 단일 표준 발견 URL을 사용합니다:

```
https://accounts.google.com/.well-known/openid-configuration
```

이 URL은 모든 Google Workspace 조직에 동일합니다 — 임차인 또는 도메인으로 맞춤화할 필요가 없습니다.

## 단계 5: Spwig에서 구성

1. Spwig 관리자에서 **기업용 SSO > SSO 제공자 구성**으로 이동
2. **제공자 이름**을 `Google Workspace`로 설정
3. 발견 URL을 입력: `https://accounts.google.com/.well-known/openid-configuration`
4. **자동 발견**을 클릭 — 이 작업은 모든 엔드포인트 필드를 자동으로 채웁니다
5. 단계 3에서의 **클라이언트 ID**를 입력
6. 단계 3에서의 **클라이언트 비밀**을 입력
7. **저장**을 클릭

### 클레임 매핑

Google은 표준 OIDC 클레임 이름을 사용하므로 기본 Spwig 구성은 즉시 작동합니다:

| Spwig 설정 | Google 클레임 | 기본 값 |
|---------------|-------------|---------------|
| 이메일 클레임 | `email` | `email` |
| 이름 클레임 | `given_name` | `given_name` |
| 성 클레임 | `family_name` | `family_name` |

클레임 매핑에 대한 변경은 필요 없습니다.

## 단계 6: 활성화 및 테스트

1.

**사이트 설정 > 보안** 탭으로 이동
2.

**관리자 로그인용 SSO 활성화**를 선택
3.

**저장**을 클릭
4.


관리자 로그인 페이지를 **프라이버트/인코그니토 창**에서 열어주세요
5.

**Google Workspace로 로그인** 버튼을 보실 수 있어야 합니다
6.

클릭해 주세요 — Google의 로그인 페이지로 이동해야 합니다
7.

Spwig에 등록된 직원 사용자의 이메일과 일치하는 Google Workspace 계정으로 로그인하세요
8.

Spwig 관리 대시보드로 다시 이동해야 합니다

## 그룹 기반 역할 매핑

Microsoft Entra ID 또는 Okta와 달리 Google은 기본적으로 표준 OIDC 토큰에 그룹 멤버십을 포함하지 않습니다. Google에서 그룹 클레임을 구현하려면 Google Workspace 디렉터리 API와 기본 OIDC를 넘어 추가 설정이 필요합니다.

대부분의 Google Workspace 배포 사례에서 자동 역할 매핑을 통해 대신 Spwig에서 직원 및 슈퍼유저 상태를 직접 관리하는 것이 좋습니다:

1. Spwig에서 적절한 권한을 가진 직원 계정을 생성하세요
2. Spwig의 직원 역할 시스템을 사용하여 접근 수준을 제어하세요
3. 직원은 SSO를 통해 로그인하고, Spwig은 기존 권한을 사용합니다

자동 그룹 기반 역할 매핑이 필요한 경우, [Google Workspace Admin SDK Directory API 문서](https://developers.google.com/admin-sdk/directory)에서 사용자 정의 클레임을 구성하는 방법을 참조하세요.

## 일반적인 문제

| 문제 | 원인 | 해결 방법 |
|---------|-------|----------|
| **Error 400: redirect_uri_mismatch** | Google Cloud의 리디렉션 URI가 정확히 일치하지 않음 | 리디렉션 URI가 `https://your-store.com/oidc/callback/`로 끝나는지 확인하세요. HTTP와 HTTPS를 확인하세요. |
| **Error 403: access_denied** | 사용자가 Google Workspace 조직에 속하지 않음 | "Internal" 사용자 유형의 경우, 사용자가 귀하의 조직에 속해야 로그인할 수 있습니다. 사용자의 계정이 Workspace 도메인에 속하는지 확인하세요. |
| **OAuth 동의 화면에 "이 앱은 인증되지 않았습니다" 표시** | Internal 앱에 대한 일반적인 현상 | Internal 앱에 대해 이 경고는 기능에 영향을 주지 않습니다. 귀하의 조직에 속한 사용자는 여전히 로그인할 수 있습니다. |
| **Google에서 로그인 성공하지만 Spwig에서 실패** | Spwig에 일치하는 사용자가 없음 | Spwig에 Google Workspace 계정과 동일한 이메일을 가진 직원 계정이 있는지 확인하세요. "직원 제한"이 올바르게 구성되었는지 확인하세요. |
| **"Access blocked: This app's request is invalid"** | 범위가 올바르게 구성되지 않음 | OAuth 동의 화면에 `openid`, `email`, `profile` 범위가 추가되어 있는지 확인하세요. |

## 팁

- **"Internal" 사용자 유형 사용** — 이 설정은 Google Workspace 조직 내에서만 로그인을 제한하며, Google의 앱 인증 절차가 필요하지 않습니다.
- **Google 클라이언트 비밀은 만료되지 않음** — Microsoft Entra ID와 달리 Google OAuth 클라이언트 비밀은 만료 날짜가 없습니다. 그러나 언제든지 자격 증명 페이지에서 회전할 수 있습니다.
- **여러 앱을 위한 하나의 프로젝트** — 여러 Spwig 설치가 있는 경우, 동일한 Google Cloud 프로젝트 내에서 여러 OAuth 클라이언트 ID를 생성할 수 있습니다.
- **비관리자 계정으로 테스트** — Spwig에 테스트 직원 계정을 생성하고, 일반 Google Workspace 사용자(슈퍼 관리자가 아닌 사용자)를 사용하여 SSO가 예상대로 작동하는지 확인하세요.
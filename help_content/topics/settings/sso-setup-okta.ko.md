---
title: 'SSO 설정: Okta'
---

이 가이드는 Spwig을 Okta와 연결하여 관리자용 단일 로그인(Single Sign-On)을 설정하는 방법을 안내합니다. 설정이 완료되면 직원들은 Okta 계정을 사용하여 Spwig 관리자 패널에 로그인할 수 있습니다.

**참고:** Okta는 시간이 지남에 따라 관리자 콘솔 인터페이스를 업데이트할 수 있습니다. 이 지침은 2026년 초의 Okta 관리자 콘솔 기준으로 작성되었습니다. 보여지는 내용과 다른 경우 Okta 공식 문서의 [OIDC 앱 통합 생성](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/) 섹션을 참조하십시오.

## 사전 조건

- Okta 조직 (어떤 계층이든 - 테스트용으로 무료 개발자 계정도 사용 가능)
- Okta에서 **Super Administrator** 또는 **Application Administrator** 역할
- Spwig 스토어 URL (예: `https://your-store.com`)
- 직원의 이메일 주소는 Spwig에서 Okta 계정과 일치해야 합니다

## 단계 1: 애플리케이션 생성

1. [Okta 관리자 콘솔](https://your-org-admin.okta.com)에 로그인합니다.
2. **Applications > Applications**로 이동합니다.
3. **Create App Integration**을 클릭합니다.
4. 다음을 선택합니다:

| 필드 | 값 |
|-------|-------|
| **로그인 방법** | OIDC - OpenID Connect |
| **애플리케이션 유형** | Web Application |

5. **Next**을 클릭합니다.

## 단계 2: 애플리케이션 구성

애플리케이션 설정을 입력합니다:

| 필드 | 값 |
|-------|-------|
| **앱 통합 이름** | `Spwig Admin SSO` (또는 원하는 이름을 입력하세요) |
| **허가 유형** | Authorization Code (기본적으로 선택되어 있어야 합니다) |
| **로그인 리디렉션 URI** | `https://your-store.com/oidc/callback/` |
| **로그아웃 리디렉션 URI** | `https://your-store.com/en/admin/login/` |
| **제어된 액세스** | 필요에 따라 선택 (아래 참조) |

**제어된 액세스**에 대해 다음 중 하나를 선택합니다:

- **조직 내 모든 사용자가 액세스할 수 있도록 허용** - 모든 Okta 사용자가 로그인할 수 있습니다 (Spwig 액세스는 Restrict to Staff 설정으로 여전히 제어할 수 있습니다)
- **선택된 그룹에만 액세스 제한** - 특정 Okta 그룹에 속한 사용자만 로그인할 수 있습니다
- **현재는 그룹 할당을 건너뜁니다** - 나중에 사용자 또는 그룹을 수동으로 할당할 수 있습니다

저장을 클릭하세요.

**중요:** 로그인 리디렉션 URI는 `https://your-store.com/oidc/callback/`과 정확히 일치해야 합니다 — 끝에 슬래시도 포함합니다.

## 단계 3: 클라이언트 자격 증명 가져오기

저장한 후, 애플리케이션의 **General** 탭에서 자격 증명을 확인할 수 있습니다:

| 값 | 찾을 위치 |
|-------|-----------------|
| **Client ID** | General 탭, Client Credentials 섹션 |
| **Client Secret** | General 탭, Client Credentials 섹션 (눈 아이콘을 클릭하여 표시) |

두 값을 모두 복사하세요 — Spwig에서 사용해야 합니다.

## 단계 4: Discovery URL 구성

Discovery URL은 Okta 조직 및 인증 서버에 따라 달라집니다:

**기본 인증 서버 (가장 일반적인 경우):**
```
https://your-org.okta.com/.well-known/openid-configuration
```

**사용자 정의 인증 서버 (사용자 정의된 경우):**
```
https://your-org.okta.com/oauth2/{authorization-server-id}/.well-known/openid-configuration
```

`your-org.okta.com`을 실제 Okta 도메인으로 대체하세요. Okta 도메인은 관리자 콘솔 URL 바에 있거나 **Settings > Account** 아래에서 확인할 수 있습니다.

**팁:** 대부분의 조직은 Org Authorization Server(기본값)를 사용합니다. Okta 관리자가 특별히 설정한 경우에만 사용자 정의 인증 서버 URL을 사용하세요.

## 단계 5: 사용자 또는 그룹 할당

단계 2에서 "Skip group assignment"을 선택했다면, 사용자가 로그인할 수 있도록 사용자를 할당해야 합니다:

1. 애플리케이션의 **Assignments** 탭에서 **Assign**을 클릭합니다
2. **Assign to People** 또는 **Assign to Groups**을 선택합니다
3. 사용자 또는 그룹을 선택하고 **Assign**을 클릭합니다
4. **Done**을 클릭합니다

애플리케이션에 할당되지 않은 사용자는 SSO를 시도할 때 오류를 보게 됩니다.

## 단계 6: 그룹 클레임 구성 (선택 사항)

Spwig이 Okta 그룹 멤버십에 따라 직원 또는 슈퍼유저 상태를 자동으로 설정하고자 한다면:

1.

관리자 콘솔에서 **Security > API**로 이동합니다
2.

**Authorization Server**를 선택합니다 (사용자 정의한 것이 없다면 "default" 또는 Org Authorization Server를 사용합니다)
3.

**Claims** 탭으로 이동합니다
4.

모든 마크다운 형식, 이미지 경로, 코드 블록 및 기술 용어를 유지합니다.

클릭 **Add Claim**
5.

클레임을 구성하세요:

| Field | Value |
|-------|-------|
| **Name** | `groups` |
| **Include in token type** | ID Token, Always |
| **Value type** | Groups |
| **Filter** | Matches regex: `.*` (모든 그룹을 포함하려면) |
| **Include in** | Any scope (또는 `openid`로 제한하고 싶다면) |

6. 클릭 **Create**

**Tip:** Microsoft Entra ID는 Object ID를 전송하지만, Okta는 기본적으로 **그룹 이름**을 전송합니다. 이는 역할 매핑을 더 직관적으로 만들며, Okta 그룹의 표시 이름을 Spwig의 Staff Groups 및 Superuser Groups 필드에 직접 사용할 수 있습니다.

### 그룹 필터링

사용자가 많은 Okta 그룹에 속해 있고 토큰에 포함하고 싶은 특정 그룹만 포함하고자 하는 경우:

- `.*` 필터를 더 구체적인 정규식으로 변경하세요. 예: `^Spwig.*`으로 "Spwig"으로 시작하는 그룹만 포함합니다
- 또는 정규식 대신 **Starts with**, **Equals**, 또는 **Contains** 필터를 사용할 수 있습니다

## 단계 7: Spwig에서 구성

1. Spwig 관리자에서 **Enterprise SSO > SSO Provider Configuration**으로 이동하세요
2. **Provider Name**을 `Okta`로 설정하세요
3. 단계 4에서 받은 Discovery URL을 입력하세요
4. **Auto-Discover**를 클릭하세요 — 이는 모든 엔드포인트 필드를 자동으로 채웁니다
5. 단계 3에서 받은 **Client ID**를 입력하세요
6. 단계 3에서 받은 **Client Secret**을 입력하세요
7. 단계 6에서 그룹 클레임을 구성한 경우:
   - **Groups Claim**을 `groups`로 설정하세요
   - **Staff Groups**에 Okta 그룹의 이름을 입력하세요. 해당 그룹의 멤버가 스태프가 되어야 하는 경우 (콤마로 구분)
   - **Superuser Groups**에 Okta 그룹의 이름을 입력하세요. 해당 그룹의 멤버가 슈퍼유저가 되어야 하는 경우 (콤마로 구분)
8. **Save**를 클릭하세요

## 단계 8: 활성화 및 테스트

1.

**Site Settings > Security** 탭으로 이동하세요
2.

**Enable SSO for admin login**을 선택하세요
3.

**Save**를 클릭하세요
4.

**private/incognito window**에서 관리자 로그인 페이지를 열고
5.

**Sign in with Okta** 버튼을 보게 될 것입니다
6.

클릭하세요 — Okta의 로그인 페이지로 리디렉션됩니다
7.



Okta 계정으로 인증하되, 해당 계정이 애플리케이션에 할당되어 있고 이메일이 Spwig의 직원 사용자와 일치해야 합니다

# SSO 설정 검증

이 방법을 사용하면 의도된 직원만 로그인할 수 있습니다.
- **Okta 클라이언트 시크릿은 기본적으로 만료되지 않음** — 보안 최선 실천을 위해 애플리케이션의 일반 탭에서 언제든지 회전할 수 있습니다.
- **비관리자 계정으로 테스트** — 애플리케이션에 할당된 일반 Okta 사용자(초기 관리자가 아님)를 사용하여 SSO가 예상대로 작동하는지 확인하세요.
- **Okta에서 MFA 구성** — Okta의 전역 세션 정책 또는 인증 정책을 구성하여 MFA를 요구할 수 있습니다.

이 설정은 Spwig에 대한 모든 SSO 로그인에 적용되며, Spwig에서 별도로 MFA를 구성할 필요가 없습니다.
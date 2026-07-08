---
title: 'SSO 설정: Microsoft Entra ID'
---

이 가이드는 Spwig을 Microsoft Entra ID(이전 Azure Active Directory)에 연결하여 관리자용 단일 로그인(Single Sign-On)을 설정하는 방법을 안내합니다. 설정이 완료되면 직원들은 Microsoft 작업 계정을 사용하여 Spwig 관리자 패널에 로그인할 수 있습니다.

**참고:** Microsoft는 시간이 지남에 따라 Entra 관리 센터 인터페이스를 업데이트할 수 있습니다. 이 지침은 2026년 초의 인터페이스를 기준으로 작성되었습니다. 보여지는 화면과 다른 경우 Microsoft의 공식 문서인 [Microsoft ID 플랫폼과의 애플리케이션 등록](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)을 참조하십시오.

## 사전 조건

- Microsoft Entra ID에 액세스할 수 있는 Azure 구독
- Entra ID 테넌트에서 **애플리케이션 관리자** 또는 **전역 관리자** 역할
- Spwig 스토어 URL (예: `https://your-store.com`)
- 직원의 이메일 주소는 Spwig에서 Microsoft 계정과 일치해야 합니다

## 단계 1: 애플리케이션 등록

1. [Microsoft Entra 관리 센터](https://entra.microsoft.com)에 로그인합니다
2. **아이덴티티 > 애플리케이션 > 애플리케이션 등록**으로 이동합니다
3. **새 등록**을 클릭합니다
4. 등록을 구성합니다:

| 필드 | 값 |
|-------|-------|
| **이름** | `Spwig Admin SSO` (또는 원하는 이름을 사용하세요) |
| **지원하는 계정 유형** | **이 조직 디렉터리의 계정만** (단일 테넌트) |
| **리디렉션 URI** | 플랫폼: **웹**, URI: `https://your-store.com/oidc/callback/` |

5. **등록**을 클릭합니다

**중요:** 리디렉션 URI는 `https://your-store.com/oidc/callback/`과 정확히 일치해야 합니다 — 끝에 슬래시도 포함합니다. `your-store.com`을 실제 스토어 도메인으로 대체합니다.

## 단계 2: 애플리케이션 ID 확인

등록 후, 애플리케이션의 **개요** 페이지를 볼 수 있습니다. 다음 두 값을 확인하세요 — 나중에 필요합니다:

| 값 | 찾을 위치 | 사용 목적 |
|-------|-----------------|---------------|
| **Application (client) ID** | 개요 페이지, 상단 섹션 | Spwig에서 **Client ID**로 입력 |
| **Directory (tenant) ID** | 개요 페이지, 상단 섹션 | Discovery URL을 구성하는 데 사용 |

## 단계 3: 클라이언트 비밀 생성

1. 앱 등록에서 **인증서 및 비밀**로 이동
2. **새로운 클라이언트 비밀**을 클릭
3. 설명을 입력(예: `Spwig SSO`)하고 유효 기간을 선택
4. **추가**를 클릭
5. **값을 즉시 복사**하세요 — 이 값은 한 번만 표시됩니다. 이는 Spwig에 입력할 클라이언트 비밀입니다.

**Secret ID를 복사하지 마세요** — ID 열이 아닌 **값** 열이 필요합니다.

**기억하세요** 비밀이 만료되기 전에 비밀을 다시 생성하는 것을 잊지 마세요. 비밀이 만료되면 SSO가 작동을 중단하고, 새로운 비밀을 생성하고 Spwig에서 업데이트해야 합니다.

## 단계 4: API 권한 구성

1. **API 권한**으로 이동
2. **Microsoft Graph > User.Read**(위임)이 목록에 있는지 확인합니다. 이는 기본적으로 추가됩니다.
3. `openid`, `email`, `profile` 권한이 목록에 없는 경우 **권한 추가 > Microsoft Graph > 위임 권한**을 클릭하고 추가합니다.
4. 요청이 표시되면 **[귀하의 조직]을 위한 관리자 동의 부여**를 클릭합니다.

## 단계 5: Discovery URL 구성

OIDC Discovery URL은 다음과 같은 형식을 따릅니다:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

{tenant-id}를 단계 2에서 얻은 **Directory (tenant) ID**로 대체합니다.

예: 테넌트 ID가 `a1b2c3d4-e5f6-7890-abcd-ef1234567890`인 경우 Discovery URL은 다음과 같습니다:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## 단계 6: 그룹 클레임 구성 (선택 사항)

Spwig이 Entra ID 그룹 소속에 따라 직원 또는 슈퍼유저 상태를 자동으로 할당하고자 하는 경우:

1.

앱 등록에서 **토큰 구성**으로 이동
2.

**그룹 클레임 추가**를 클릭
3.

모든 마크다운 형식, 이미지 경로, 코드 블록 및 기술 용어를 유지합니다.

# 3. 그룹 유형 선택

선택할 그룹 유형을 선택하세요(보통 **보안 그룹**)
4.

**Customize token properties by type**(토큰 속성을 유형별로 사용자 지정) 아래에서 **ID** 토큰에 대해 **Group ID**(그룹 ID)를 선택합니다.
5.

**추가**를 클릭합니다.

**중요:** Entra ID는 그룹 **Object ID**(예: `a1b2c3d4-...`와 같은 UUID)를 보냅니다. 그룹 표시 이름이 아닙니다. Spwig에서 역할 매핑을 구성할 때 이러한 Object ID를 사용해야 합니다.

그룹의 Object ID를 찾는 방법:
1. Entra 관리 센터에서 **Identity > Groups > All groups**(모든 그룹)으로 이동합니다.
2. 그룹을 클릭합니다.
3. 그룹의 개요 페이지에서 **Object ID**를 복사합니다.

### 그룹 제한

Microsoft Entra ID는 토큰에 최대 **200개의 그룹**을 포함합니다. 사용자가 200개 이상의 그룹에 속해 있는 경우 그룹 클레임은 Microsoft Graph API로 이동하는 링크로 대체됩니다. 많은 그룹이 있는 조직의 경우 Spwig 액세스를 위한 전용 보안 그룹을 생성하고 [그룹 필터링](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference)을 사용하여 포함할 그룹을 제한하는 것이 좋습니다.

## 단계 7: Spwig에서 구성

1. Spwig 관리자에서 **Enterprise SSO > SSO Provider Configuration**(SSO 제공자 구성)으로 이동합니다.
2. **Provider Name**(제공자 이름)을 `Microsoft Entra ID`로 설정합니다.
3. 단계 5에서 복사한 **OIDC Discovery URL**을 **OIDC Discovery URL**에 붙여넣습니다.
4. **Auto-Discover**(자동 탐색)을 클릭합니다 — 이 작업은 모든 엔드포인트 필드를 자동으로 채웁니다.
5. 단계 2에서의 **Client ID**(클라이언트 ID)를 입력합니다.
6. 단계 3에서의 **Client Secret**(클라이언트 비밀)(값)을 입력합니다.
7. 단계 6에서 그룹 클레임을 구성한 경우:
   - **Groups Claim**(그룹 클레임)을 `groups`로 설정합니다.
   - **Staff Groups**(직원 그룹)에 그룹의 멤버가 직원이 되어야 하는 그룹의 Object ID를 입력합니다(콤마로 구분).
   - **Superuser Groups**(슈퍼유저 그룹)에 그룹의 멤버가 슈퍼유저가 되어야 하는 그룹의 Object ID를 입력합니다(콤마로 구분).
8. **Save**(저장)을 클릭합니다.

## 단계 8: 활성화 및 테스트

1.

**Site Settings > Security**(사이트 설정 > 보안) 탭으로 이동합니다.
2.

**Enable SSO for admin login**(관리자 로그인용 SSO 활성화)을 선택합니다.
3.

**Save**(저장)을 클릭합니다.
4.

**private/incognito window**(개인/익명 창)에서 관리자 로그인 페이지를 엽니다.
5.

**Sign in with Microsoft Entra ID**(Microsoft Entra ID로 로그인) 버튼을 보아야 합니다.
6.



# 4. Microsoft 계정으로 로그인

클릭하세요 — Microsoft의 로그인 페이지로 이동해야 합니다
7.

Spwig의 직원 사용자 이메일과 일치하는 Microsoft 계정으로 로그인
8.

Spwig 관리 대시보드로 다시 이동해야 합니다

## 일반적인 문제

| 문제 | 원인 | 해결 방법 |
|---------|-------|----------|
| **AADSTS50011: 리디렉션 URI가 일치하지 않습니다** | Entra의 리디렉션 URI가 정확히 일치하지 않음 | 리디렉션 URI가 `https://your-store.com/oidc/callback/`인지 확인하세요. 끝에 슬래시가 포함되어 있는지 확인하고 HTTP와 HTTPS 불일치를 확인하세요. |
| **AADSTS700016: 애플리케이션을 찾을 수 없습니다** | 잘못된 클라이언트 ID 또는 테넌트 | 클라이언트 ID를 다시 확인하고 Discovery URL이 올바른 테넌트 ID를 사용하는지 확인하세요 |
| **Microsoft에서 로그인은 성공하지만 Spwig에서 실패** | Spwig에 일치하는 사용자가 없음 | Microsoft 계정과 동일한 이메일 주소를 가진 Spwig의 직원 계정이 있는지 확인하세요. Restrict to Staff가 활성화된 경우 사용자가 직원 상태인지 확인하세요. |
| **Groups 클레임이 비어 있음** | 그룹 클레임이 구성되지 않음 | 단계 6을 따르고 토큰 구성에 groups 클레임을 추가하세요 |
| **Groups 클레임이 ID 대신 URL을 반환** | 사용자가 200개 이상의 그룹에 속함 | 토큰에 포함될 그룹을 제한하기 위해 그룹 필터링을 사용하거나 특정 그룹을 할당하세요 |
| **몇 달 후 SSO가 작동하지 않음** | 클라이언트 비밀이 만료됨 | Entra에서 새로운 클라이언트 비밀을 생성하고 Spwig의 SSO 제공자 구성에 업데이트하세요 |

## 팁

- **보안 그룹**을 사용하여 역할 매핑을 수행하세요. Microsoft 365 그룹 또는 분배 목록은 사용하지 마세요.

보안 그룹은 액세스 제어를 위해 설계되었으며 OIDC 클레임과 가장 잘 작동합니다.
- **단일 테넌트가 권장됩니다** — "이 조직 디렉터리의 계정만"을 선택하면 SSO가 조직의 사용자에게만 제한됩니다.


# 다중 테넌트 구성
다중 테넌트 구성은 추가 검증이 필요합니다.
- **긴 비밀번호 만료 설정** — 클라이언트 비밀번호를 생성할 때 24개월을 선택하고, 22개월에 달력을 통해 회전을 알리는 알림을 설정하세요.
- **조건부 액세스** — Entra ID에서 Spwig 앱 등록에 특별히 적용할 조건부 액세스 정책을 생성할 수 있습니다.

예를 들어, MFA를 요구하거나 신뢰할 수 없는 위치에서의 로그인을 차단하거나, 보안된 장치를 요구할 수 있습니다.
- **비관리자 계정으로 테스트** — Spwig에서 테스트용 직원 계정을 생성하여 전체 팀에 배포하기 전에 SSO가 작동하는지 확인하세요.
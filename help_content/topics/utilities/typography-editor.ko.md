---
title: 타이포그래피 편집기
---

타이포그래피 편집기는 텍스트의 외형을 완전히 제어할 수 있는 공유 스타일 유틸리티입니다. 페이지 빌더, 헤더/푸터 빌더 또는 메뉴 빌더의 요소에서 타이포그래피 속성을 편집할 때마다 패널로 열립니다.

![타이포그래피 편집기](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## 실시간 미리보기

편집기는 패널 상단에 옆으로 옆 비교를 표시합니다:

| 박스 | 목적 |
|-----|---------|
| **현재** | 기존 타이포그래피 스타일에서 "The quick brown fox..."를 표시 |
| **새로운** | 설정을 조정하면서 실시간으로 업데이트되며, 적용하기 전 결과를 보여줍니다 |

이렇게 하면 변경 사항을 적용하지 않고도 변경 전과 후를 비교할 수 있습니다.

## 글꼴 탭

편집기가 열릴 때 기본적으로 표시되는 것은 글꼴 탭입니다.

**글꼴 가족** — 범주별로 정렬된 70개 이상의 글꼴을 포함하는 검색 가능한 드롭다운. 각 글꼴은 자체 글꼴로 미리보기되어 선택하기 전에 어떻게 보이는지 확인할 수 있습니다. 필요한 경우 Google Fonts에서 글꼴이 필요할 때에 따라 로드됩니다.

**글꼴 크기** — px, em, rem, %를 지원하는 단위 선택기를 포함한 숫자 입력. 기본값은 16px입니다.

**글꼴 굵기** — 100(가늘음)에서 900(검은색)까지의 슬라이더:

| 값 | 이름 |
|-------|------|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

모든 9개의 굵기를 지원하는 글꼴은 아닙니다. 편집기는 선택한 글꼴 가족에 사용 가능한 굵기를 표시합니다.

**글꼴 스타일** — 일반, 이탈릭, 기울임 스타일의 토글 버튼입니다.

## 간격 탭

문자 주위 및 사이의 간격을 세부적으로 조정합니다:

| 제어 | 기능 | 기본값 |
|---------|-------------|---------|
| **줄 간격** | 텍스트 줄 사이의 수직 간격 | normal |
| **문자 간격** | 개별 문자 사이의 수평 간격 | normal |
| **단어 간격** | 단어 사이의 수평 간격 | normal |
| **텍스트 들여쓰기** | 단락의 첫 줄 들여쓰기 | 0 |

각 간격 제어에는 단위 선택기(px, em, rem, %)가 포함되어 있습니다.

## 스타일 탭

텍스트 장식 및 시각 효과를 제어합니다:

- **텍스트 장식** — 없음, 밑줄, 윗줄, 취소선
- **장식 스타일** — 실선, 점선, 점, 이중선, 파동선(장식이 활성화된 경우에 적용됨)
- **장식 색상** — 장식선의 색상 선택기, 기본값은 텍스트 색상입니다.
- **텍스트 그림자** — 오프셋, 블러, 색상 제어를 포함한 선택적 그림자 효과

## 변환 탭

내용을 편집하지 않고 텍스트의 대문자화를 변경합니다:

| 옵션 | 결과 |
|--------|--------|
| **없음** | 텍스트는 작성된 대로 표시됩니다 |
| **대문자** | ALL LETTERS ARE CAPITALIZED |
| **소문자** | all letters are lowercase |
| **자음 대문자** | 각 단어의 첫 글자가 대문자입니다 |

이 탭의 추가 제어에는 **텍스트 정렬**(왼쪽, 가운데, 오른쪽, 정렬), **수직 정렬**, **텍스트 방향**(LTR 또는 RTL)이 포함됩니다.

## 사용 가능한 글꼴 가족

편집기는 범주별로 그룹화된 시스템 및 Google Fonts의 큐레이션된 라이브러리를 포함합니다:

| 카테고리 | 폰트
|----------|-------
| **시스템** | 시스템 기본, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS
| **산세리프 (현대)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans
| **산세리프 (전통)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend
| **세리프** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya
| **세리프 (시스템)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria
| **모노스페이스** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono
| **디스플레이** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black

Google Fonts는 선택 시 자동으로 로드됩니다. 시스템 폰트는 플랫폼별로 신뢰할 수 있는 CSS 대체 체인을 사용합니다.

## 어디에 나타나나요

Typography Editor는 텍스트 스타일링이 필요한 모든 곳에서 사용할 수 있습니다:

- **Page Builder** — 요소를 선택하고 스타일 탭을 열어 Typography 섹션을 클릭하세요
- **Header/Footer Builder** — 네비게이션 링크, 로고 텍스트, 메뉴 항목 및 푸터 콘텐츠의 텍스트 스타일을 지정합니다
- **Menu Builder** — 메뉴 라벨 및 하위 메뉴 항목의 타이포그래피를 제어합니다
- **Catalog Admin** — 제품 설명 및 콘텐츠 편집기에서 타이포그래피 제어가 노출된 경우에 사용됩니다

어떤 맥락에서도 항상 동일한 일관된 인터페이스를 통해 편집기를 사용합니다.

## 팁

- **폰트를 의도적으로 짝지어 사용하세요** — 헤딩에는 디스플레이 또는 세리프 폰트를 사용하고 본문 텍스트에는 깔끔한 산세리프 폰트를 사용하세요. Playfair Display + Inter 또는 Montserrat + Merriweather 같은 전통적인 조합이 잘 작동합니다.
- **페이지당 폰트 가족 수를 제한하세요** — 일반적으로 페이지당 두 개 또는 세 개의 폰트 가족이 충분합니다. 너무 많으면 로드 시간이 느려지고 시각적 혼란을 일으킬 수 있습니다.
- **반응형 텍스트를 위해 상대 단위를 사용하세요** — em 및 rem은 기본 폰트 크기와 함께 확장되어, 다양한 화면 크기에 따라 자동으로 타이포그래피가 조정됩니다.
- **가중치 가용성을 확인하세요** — 텍스트가 400과 500에서 동일하게 보인다면 선택한 폰트가 해당 가중치를 지원하지 않을 수 있습니다. 편집기는 각 폰트가 제공하는 가중치를 표시합니다.
- **모든 기기에서 미리보기** — 데스크탑 크기에서 잘 보이는 텍스트가 모바일에서는 너무 작거나 너무 클 수 있습니다. Page Builder의 기기 미리보기를 사용하여 확인하세요.
- **라이브 미리보기를 사용하세요** — 적용하기 전에 미리보기 상자에서 Current vs New를 항상 비교하여 예상치 못한 변경을 피하세요.

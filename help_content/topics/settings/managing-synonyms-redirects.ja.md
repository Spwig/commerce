---
title: 同義語とリダイレクトの管理
---

同義語とリダイレクトは、同等の語句を処理し、特定のクエリをターゲットページにルーティングすることで、検索をスマートにします。同義語は検索を関連語句（"laptop" は "notebook" も検索結果に含む）に拡張し、リダイレクトは "sale" のようなクエリを直接販売ページに送ります。このガイドでは、検索の関連性と顧客体験を向上させるために、これらの機能の作成と管理方法を説明します。

同義語は語句の同等性を、リダイレクトはナビゲーションのショートカットを用います。

![同義語リスト](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## 同義語の理解

同義語は、検索システムに特定の語句を同等とみなすように指示します。顧客が1つの語句で検索した場合、システムは自動的に同義語の語句に一致する結果を含めます。

**例**: "laptop" → "notebook", "portable computer" という同義語マッピングを作成します。これにより、誰かが "laptop" で検索すると、"notebook" または "portable computer" が製品名や説明に含まれる製品の結果も表示されます。

同義語は特に次のケースで価値があります：
- 英語（イギリス）と英語（アメリカ）の違い（jumper/sweater, trainers/sneakers）
- ブランド名と汎用語（tissues/Kleenex）
- 一般的な誤字（accommodate/accomodate）
- 業界用語と日常用語（CPU/processor）

## 同義語の作成

**Search > Synonyms** に移動し、**+ Add Synonym** をクリックします。

![同義語の追加フォーム](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - トリガーとなる元の検索語句

**Synonyms** - 例: `[
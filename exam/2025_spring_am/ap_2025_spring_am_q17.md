---
year: 2025
season: 秋
question_no: 17
category: テクノロジ系
subcategory: 開発ツール・API
tags: [OpenAPI, Swagger, API設計, OSS]
answer: エ
---

## 問題文

OpenAPI Specification に従った API の定義・開発を支援する機能を提供する OSS はどれか。

ア　curl　　イ　OpenAM　　ウ　Serverspec　　エ　Swagger

## 参照画像

（なし）
<!-- 画像がある場合: ![図1](images/2025a_q17_fig1.jpg) -->

## 正解

**エ**：Swagger

## 選択肢補足

| 選択肢 | 内容 | 補足 |
|:--|:--|:--|
| ア | curl | HTTPなどのプロトコルを用いてサーバーとデータをやり取りするためのコマンドラインツールであり、API定義・開発支援とは異なる用途のツール |
| イ | OpenAM | シングルサインオン（SSO）やアイデンティティ・アクセス管理（IAM）を提供するOSSであり、API定義の支援とは無関係 |
| ウ | Serverspec | サーバーの構成（インフラの状態）が意図通りであるかをテストするためのOSSであり、API定義・開発支援とは異なる用途 |
| **エ** | **Swagger** | **正解。OpenAPI Specification（旧称Swagger Specification）に準拠したAPIの設計・定義・文書化・コード生成などを支援するツール群（Swagger UI、Swagger Editor、Swagger Codegenなど）を提供するOSS** |

## 解き方

1. 「OpenAPI Specification」とは何かを確認する。
   - OpenAPI Specification（OAS）は、RESTful APIのインタフェース（エンドポイント、パラメータ、レスポンス形式など）を、人間にも機械にも読みやすい形式（YAMLやJSON）で記述するための標準仕様である。
2. 各選択肢のツールの本来の用途を確認する。
   - curl：HTTPリクエストを送信し、Webサーバーとの通信結果を確認するためのコマンドラインツール。API呼び出しのテストには使えるが、API自体の「定義・開発支援」を目的としたツールではない。
   - OpenAM：シングルサインオンやアクセス管理を実現するためのOSS製品であり、認証・認可の領域に特化しており、API定義とは異なる分野のツール。
   - Serverspec：サーバーのインフラ構成（インストールされているパッケージやサービスの状態など）が期待通りであるかをテストするためのOSSであり、API定義とは無関係。
3. OpenAPI Specificationとの関連性が最も強いツールを特定する。
   - Swaggerは、もともとOpenAPI Specificationの基盤となった仕様・ツール群であり、現在もSwagger UI（APIドキュメントの可視化）、Swagger Editor（API定義ファイルの編集）、Swagger Codegen（API定義からのコード自動生成）など、OpenAPI Specificationに準拠したAPIの定義・開発を直接支援する機能を提供している。
4. 以上より、OpenAPI Specificationに従ったAPIの定義・開発支援機能を提供するOSSとして**エ（Swagger）**が最も適切であると判断する。
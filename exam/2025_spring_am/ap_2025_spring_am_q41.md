---
exam: 応用情報技術者試験
year: 2025
season: 春
question_no: 41
category: テクノロジ系
subcategory: セキュリティ（Cookie属性）
tags: [Cookie, Secure属性, HTTPS, Webセキュリティ, 通信の暗号化]
answer: イ
---

## 問題文

cookieにSecure属性を設定しなかったときと比較した，設定したときのWebブラウザの動作として，適切なものはどれか。

ア　cookieに設定された有効期間を過ぎると，Webブラウザがcookieを無効であると判断する。
イ　URL内のスキームがhttpsのときだけ，Webブラウザからcookieが送出される。
ウ　WebブラウザがアクセスするURL内のパスとcookieに設定されたパスのプレフィックスが一致するときだけ，Webブラウザからcookieが送出される。
エ　WebブラウザではJavaScriptによるcookieの読出しが禁止される。

## 参照画像

（なし）
<!-- 画像がある場合: ![図1](images/2025a_q41_fig1.jpg) -->

## 正解

**イ**：URL内のスキームがhttpsのときだけ，Webブラウザからcookieが送出される。

## 選択肢補足

| 選択肢 | 内容 | 補足 |
|:--|:--|:--|
| ア | 有効期間を過ぎると無効と判断する | これは`Expires`属性または`Max-Age`属性の動作の説明であり、Secure属性とは無関係 |
| **イ** | **URL内のスキームがhttpsのときだけcookieが送出される** | **正解。Secure属性を設定すると、Webブラウザはアクセス先のURLスキームがhttpsである場合に限ってcookieを送出するようになり、平文のHTTP通信では送出されなくなる** |
| ウ | URLのパスとcookieのパスのプレフィックスが一致するときだけ送出される | これは`Path`属性の動作の説明であり、Secure属性とは無関係 |
| エ | JavaScriptによるcookieの読出しが禁止される | これは`HttpOnly`属性の動作の説明であり、Secure属性とは無関係（Secure属性自体はJavaScriptからの読出し可否には影響しない） |

## 解き方

1. 問題文のキーワードを整理する。
   - 「Secure属性を設定したとき」と「設定しなかったとき」の**Webブラウザの動作の違い**を問われている。
2. Secure属性の定義を確認する。
   - Secure属性が設定されたcookieは、HTTPSプロトコルによる暗号化された通信のときにのみ、Webブラウザからサーバーへ送出される。HTTP（平文）通信では送出されないため、盗聴や中間者攻撃によるcookieの窃取リスクを低減できる。
3. 各選択肢が、cookieのどの属性の説明に該当するかを切り分ける。
   - ア：有効期限に関する記述 → `Expires`/`Max-Age`属性の話。
   - イ：通信のスキーム（http/https）に関する記述 → `Secure`属性の話。
   - ウ：URLのパスに関する記述 → `Path`属性の話。
   - エ：JavaScriptからの読出し制限に関する記述 → `HttpOnly`属性の話。
4. 問題が「Secure属性」を設定したときの動作を聞いていることを踏まえ、該当する選択肢を絞り込む。
   - ア・ウ・エはいずれも別の属性（Expires/Max-Age、Path、HttpOnly）の説明であり、Secure属性の動作とは一致しない。
5. 「URLのスキームがhttpsのときだけcookieが送出される」という、Secure属性の本来の機能と完全に一致する**イ**を正解と判断する。

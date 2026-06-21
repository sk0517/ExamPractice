---
year: 2025
season: 秋
question_no: 12
category: テクノロジ系
subcategory: システムの信頼性
tags: [稼働率, MTBF, MTTR, アベイラビリティ]
answer: イ
---

## 問題文

二つのシステム A，B の稼働率をそれぞれ αA（0＜αA＜1），αB（0＜αB＜1），MTBF をそれぞれ MTBFA，MTBFB，MTTR をそれぞれ MTTRA，MTTRB としたとき，これらの関係として，常に成り立つものはどれか。

ア　αA＝αB ならば，MTBFA＝MTBFB であり，かつ MTTRA＝MTTRB である。
イ　αA＝αB ならば，MTTRA／MTBFA＝MTTRB／MTBFB である。
ウ　αA＞αB ならば，MTBFA＞MTBFB であり，かつ MTTRA＞MTTRB である。
エ　αA＞αB ならば，MTTRA／MTBFA＞MTTRB／MTBFB である。

## 参照画像

（なし）
<!-- 画像がある場合: ![図1](images/2025a_q12_fig1.jpg) -->

## 正解

**イ**：αA＝αB ならば，MTTRA／MTBFA＝MTTRB／MTBFB である。

## 選択肢補足

| 選択肢 | 内容 | 補足 |
|:--|:--|:--|
| ア | 稼働率が等しければMTBF・MTTRも等しい | 反例あり。例えばA(MTBF=9,MTTR=1)とB(MTBF=90,MTTR=10)はいずれも稼働率0.9だが、MTBF・MTTRの値自体は異なるため誤り |
| **イ** | **稼働率が等しければMTTR／MTBFの比も等しい** | **正解。稼働率α＝MTBF／(MTBF＋MTTR)を変形すると1／α＝1＋MTTR／MTBFとなり、αが等しければMTTR／MTBFの比も必然的に等しくなる** |
| ウ | 稼働率が大きい方がMTBF・MTTRも大きい | 反例あり。例えばA(MTBF=9,MTTR=1,α=0.9)とB(MTBF=100,MTTR=50,α≒0.667)では、αA＞αBだがMTBFA＜MTBFBとなり誤り |
| エ | 稼働率が大きい方がMTTR／MTBFの比も大きい | 実際には逆の関係になる。αが大きいほど1／α－1＝MTTR／MTBFは小さくなるため、αA＞αBのときMTTRA／MTBFA＜MTTRB／MTBFBとなり誤り |

## 解き方

1. 稼働率の定義式を確認する。
   - 稼働率 α＝MTBF／(MTBF＋MTTR) という式で定義される。MTBFは平均故障間隔（正常稼働時間の平均）、MTTRは平均修復時間を表す。
2. 稼働率の式を変形し、MTTR／MTBFとの関係を導く。
   - α＝MTBF／(MTBF＋MTTR) の逆数を取ると、1／α＝(MTBF＋MTTR)／MTBF＝1＋MTTR／MTBF となる。
   - この式から、MTTR／MTBF＝1／α－1 という関係が導ける。つまり、MTTR／MTBFの値は稼働率αのみによって一意に決まる。
3. 選択肢アを検証する。
   - 稼働率αが等しくても、MTBFとMTTRの**比**が等しいだけで、それぞれの**絶対値**まで等しいとは限らない（例：MTBF=9,MTTR=1とMTBF=90,MTTR=10は同じα=0.9だが値は異なる）。よってアは誤り。
4. 選択肢イを検証する。
   - 上記2.の関係式「MTTR／MTBF＝1／α－1」より、αA＝αBであれば、MTTRA／MTBFA＝1／αA－1＝1／αB－1＝MTTRB／MTBFB が常に成り立つ。よってイは常に成立する。
5. 選択肢ウを検証する。
   - αA＞αBであっても、MTBFやMTTRの絶対値の大小関係は一意に定まらない（反例として、αが大きくてもMTBF自体は小さい組み合わせが存在する）。よってウは誤り。
6. 選択肢エを検証する。
   - 「MTTR／MTBF＝1／α－1」の関係から、αが大きいほど1／αは小さくなり、結果としてMTTR／MTBFは**小さく**なる。つまりαA＞αBならばMTTRA／MTBFA＜MTTRB／MTBFBとなり、エの記述（＞）とは逆の関係になる。よってエは誤り。
7. 以上の検証から、稼働率の定義式から数学的に常に導ける**イ**を正解と判断する。
# DTI local 8503 app Manual

## 0. このManualの位置づけ

このManualは、DTI local 8503 app の正式な取扱説明書です。

このアプリは、DTI / AxiCLASS / vanilla CLASS 周辺の parameter profile、local probe、continuity / discontinuity examiner、boundary confirmation を扱うためのローカル補助UIです。

このManualは、READMEよりも詳しく、1つずつ丁寧に操作と境界を確認するために作成します。

### 0.1 このアプリが行うこと

このアプリが行うことは、次の通りです。

```text
registered profile の確認
Candidate / Reference profile の比較
local AxiCLASS fixed-example check
local vanilla CLASS live probe
continuity / discontinuity examiner
boundary / payload の確認
README / Manual のダウンロード
```

### 0.2 このアプリが行わないこと

このアプリは、以下を行いません。

```text
likelihood evaluation
posterior comparison
Planck validation
physics-value update
manuscript-value update
physical discontinuity proof
operator-phase transition proof
```

画面上に数値や比較が表示されても、それは統計的な採否判定ではありません。

---

## 1. 現在のアプリ状態

現在のアプリは、local 8503 用の Streamlit app です。

基本の起動URLは次です。

```text
http://localhost:8503
```

現在の重要な状態は次です。

```text
local-only app
README download button added
8011 unavailable guidance softened
7a / 7b / 7c Enable controls highlighted
RUN / probe buttons red
graph rendering closed / disabled
GitHub freeze already pushed before README/Manual follow-up work
```

### 1.1 app.py の扱い

`app.py` は、このアプリの本体です。

編集するときは、必ず backup を作り、py_compile、static scan、local 8503 restart、manual QA を行います。

### 1.2 docs の扱い

`docs/` には README や Manual を置きます。

Manual は Markdown を source-of-record とします。

PDF が必要な場合も、まず Markdown を確定し、その後に PDF を作ります。

---

## 2. 起動方法

アプリは以下で起動します。

```bash
cd "/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_DTI_SECTION7C_CONTINUITY_EXAMINER_CLONE_20260525_124307/dti-real-app-v606-section7c-continuity-examiner"
python3 -m streamlit run app.py --server.port 8503 --server.address 127.0.0.1
```

### 2.1 起動確認

起動後、ブラウザで次を開きます。

```text
http://localhost:8503
```

確認することは次です。

```text
画面が表示される
左サイドバーが表示される
README download button が表示される
7c が表示される
Section 8 が表示される
赤い RUN / probe ボタンが表示される
```

### 2.2 local 8503 だけを再起動する理由

この作業では、local 8503 だけを再起動します。

Render deploy、public Streamlit update、local 8501 update は行いません。

---

## 3. 重要な境界

このアプリの最重要ルールは、境界を混同しないことです。

### 3.1 local UI と科学的結論を分ける

このアプリは local UI です。

表示された値や比較は、科学的な最終結論ではありません。

次のような読み方は禁止です。

```text
このアプリで表示されたから Planck validation 済みである
このアプリで近いから posterior 的に支持される
このアプリで動いたから manuscript value を更新する
このアプリで jump-like に見えたから physical discontinuity を証明した
```

### 3.2 安全な読み方

安全な読み方は次です。

```text
local UI 上で値を確認した
profile 間の差を表示した
local endpoint に payload を送った
derived quantity の応答を見た
次に監査すべき候補を整理した
```

---

## 4. 画面全体の構造

画面は大きく分けて、左サイドバーとメイン領域に分かれます。

```text
左サイドバー: profile selection / profile status / README or Manual download
メイン領域: Candidate / Reference, 7a, 7b, 7c, Section 8
```

### 4.1 左サイドバー

左サイドバーでは、主に profile の選択と現在状態の確認を行います。

### 4.2 メイン領域

メイン領域では、選択された profile をもとに比較・probe・examiner を行います。

---

## 5. 操作前チェックリスト

操作前には、次を確認します。

```text
1. 正しい app.py を開いているか
2. local 8503 を見ているか
3. Active profile は意図したものか
4. Enable が必要な操作では Enable が入っているか
5. RUN / probe ボタンを押す前に入力値を確認したか
6. 8011 が必要な操作では local 8011 API が起動しているか
7. 表示結果を likelihood / posterior / Planck validation と誤読していないか
```

### 5.1 Enable の見落とし

7a、7b、7c には Enable gate があります。

Enable を入れずに RUN / probe を押すと、期待した動作になりません。

そのため、現在のUIでは Enable control を目立たせています。

### 5.2 RUN / probe ボタン

RUN / probe 系ボタンは赤色にしています。

これは、通常の入力操作ではなく、実行操作であることを明示するためです。

---

## 次に追加する章

Part 02 では、以下を追記します。

```text
6. 左サイドバーの使い方
7. 1. Parameter profile cartridge
8. README / Manual download button
9. 2. Current profile status
10. Candidate / Reference 入力
```

---

## 6. 左サイドバーの使い方

左サイドバーは、このアプリの操作の入口です。

ここでは、登録済みプロファイルの選択、profile text の確認、現在選ばれている profile の状態確認、README / Manual のダウンロードなどを行います。

左サイドバーで行う操作は、基本的に「どのプロファイルを見ているか」を決める操作です。

### 6.1 左サイドバーで最初に見る場所

最初に見る場所は、次の順番です。

```text
1. Parameter profile cartridge
README / Manual download area
2. Current profile status
```

現在の設計では、README download button は Section 1 と Section 2 の間に置く方針です。

理由は、画面上部のメイン領域に置くと見落としやすく、操作説明に気づかないまま 7a / 7b / 7c に進む可能性があるためです。

### 6.2 左サイドバーの役割

左サイドバーの役割は、次の3つです。

```text
1. 使う profile を選ぶ
2. 選んだ profile の中身を確認する
3. 操作説明や現在状態を確認する
```

ここでは、科学的な判定は行いません。

左サイドバーで profile を選んだだけでは、likelihood evaluation、posterior comparison、Planck validation は行われません。

### 6.3 profile を選んだ後に確認すること

profile を選んだ後は、次を確認します。

```text
Active profile
Profile role
Profile text / generated block
Candidate / Reference に反映されている値
7b live probe の入力値
```

特に 7b を使う場合は、現在選んでいる profile と 7b に送る入力が一致しているかを確認します。

以前の問題として、画面で選んだ profile と 7b の入力がズレると、意図しない profile を probe する危険がありました。

現在のアプリでは、その混乱を避けるため、7b の default input source は current sidebar profile に寄せる方針です。

---

## 7. 1. Parameter profile cartridge

`1. Parameter profile cartridge` は、登録済み profile を読み込むための領域です。

ここは、アプリの起点です。

### 7.1 profile cartridge とは何か

profile cartridge とは、1つの parameter profile をまとめた入力ブロックです。

たとえば、次のような値を含みます。

```text
H0
omega_cdm
omega_b
n_s
ln1010A_s
sigma8
S8
profile_role
source_type
note
```

これは、論文値や確定値という意味ではありません。

アプリ内で比較・検査するための入力単位です。

### 7.2 登録済み profile を選ぶ

左サイドバーの selector から profile を選びます。

選ぶと、profile text や current profile status に内容が表示されます。

選んだだけでは、計算は走りません。

計算や probe を走らせるには、別途 Enable と Run が必要です。

### 7.3 Load registered profile の意味

`Load registered profile` は、選んだ profile を入力欄に読み込むための操作です。

この操作は、profile の値を画面内の入力状態へ反映するために使います。

注意点は次です。

```text
Load は読み込み操作であり、物理結論の採用ではない。
Load は manuscript value の更新ではない。
Load は likelihood / posterior / Planck validation ではない。
```

---

## 8. README / Manual download button

README / Manual download button は、操作説明をアプリ内から取得するためのボタンです。

### 8.1 なぜアプリ内に説明書ボタンが必要か

このアプリは、通常の簡単なフォームではありません。

7a、7b、7c、Section 8、Enable、Run、8011 endpoint、local-only boundary など、誤解しやすい要素が多くあります。

説明書がアプリ外にしかないと、操作中に見落とします。

そのため、アプリ内から直接 README / Manual を取得できることが重要です。

### 8.2 ボタンの配置

README download button は、左サイドバーの Section 1 と Section 2 の間に置く方針です。

現在の目標配置は次です。

```text
1. Parameter profile cartridge
[Download local app README]
2. Current profile status
```

この位置にする理由は、profile を選んだ直後、現在状態を見る前に説明書へアクセスできるからです。

### 8.3 README と Manual の違い

README は、短い操作メモです。

Manual は、1つずつ丁寧に確認する正式な取扱説明書です。

```text
README: すぐ見る短い説明
Manual: 1つずつ丁寧に確認する正式説明書
```

将来的には、README だけでなく Manual もダウンロードできる形にするのが自然です。

### 8.4 テキスト版と PDF 版

このアプリの性質を考えると、説明書はテキスト版または PDF 版が向いています。

理由は次です。

```text
操作中に検索しやすい
保存しやすい
GitHub に置きやすい
diff 管理しやすい
PDF にすれば配布しやすい
```

現時点では Markdown text を source-of-record とし、必要に応じて PDF に変換する方針が安全です。

---

## 9. 2. Current profile status

`2. Current profile status` は、現在選択中の profile の状態を確認する領域です。

### 9.1 Current profile status の目的

この領域の目的は、今アプリがどの profile を見ているかを明確にすることです。

主に次を表示します。

```text
Active profile
Profile role
現在の profile に関する説明
```

ここを見ることで、誤って別 profile を使っている可能性を減らせます。

### 9.2 Active profile

`Active profile` は、現在選ばれている profile 名です。

Run や probe の前には、必ず Active profile を確認します。

特に 7b live probe を使う前は重要です。

### 9.3 Profile role

`Profile role` は、その profile が candidate なのか、reference なのか、benchmark なのか、その他の登録済み profile なのかを示します。

これにより、比較時の読み違いを防げます。

### 9.4 Current profile status でやってはいけない読み方

Current profile status は、状態表示です。

ここに表示されたからといって、その profile が物理的に正しいとは言えません。

避けるべき読み方は次です。

```text
Active profile だから採用値である。
Profile role が candidate だから正しい。
Reference と近いから Planck validated である。
値が表示されたから likelihood 的に優れている。
```

正しい読み方は次です。

```text
いま画面がどの profile を参照しているかを確認する。
後続の入力・比較・probe の前提を確認する。
```

---

## 10. Candidate / Reference 入力

Candidate / Reference 入力は、2つの profile を比較するための領域です。

### 10.1 Candidate とは何か

Candidate は、比較対象となる候補 profile です。

候補という言葉は、正しいという意味ではありません。

あくまで比較・検査の対象です。

### 10.2 Reference とは何か

Reference は、比較の基準となる profile です。

Reference も、絶対的な正解という意味ではありません。

比較用の基準です。

### 10.3 Candidate / Reference の比較で分かること

比較で分かるのは、主に値の差です。

たとえば次です。

```text
H0 の差
omega_cdm の差
omega_b の差
n_s の差
ln1010A_s の差
sigma8 の差
S8 の差
```

これにより、どの parameter がどちら側に動いているかを確認できます。

### 10.4 Candidate / Reference の比較で分からないこと

比較だけでは、以下は分かりません。

```text
どちらが likelihood 的に優れているか
どちらが posterior 的に支持されるか
どちらが Planck validation を通るか
どちらが manuscript value になるか
```

この比較は、判断材料の整理であり、統計的判定ではありません。

### 10.5 入力値を扱うときの原則

このアプリで値を扱うときの原則は次です。

```text
表示値は確認用。
採用値ではない。
値の出所を残す。
manual edit と source-derived value を混同しない。
```

---

## 次に追加する章

次回 Part 03 では、以下を追記します。

```text
11. +/- ボタンと直接数値入力
12. 7a Enable と Run の使い方
13. 7b Enable と live probe の使い方
14. 8011 unavailable 表示の意味
15. 7c Enable と continuity examiner の使い方
```

---

## 11. +/- ボタンと直接数値入力

このアプリでは、数値入力に対して次の2種類の操作があります。

```text
+/- ボタン
直接数値入力
```

+/- ボタンは、細かい値の変化を試すための補助操作です。

直接数値入力は、明確に指定した値を入れるための操作です。

### 11.1 +/- ボタンの意味

+/- ボタンは、選択中のパラメータを少しずつ動かします。

これは探索用の操作です。

採用値を決める操作ではありません。

### 11.2 直接数値入力の意味

直接数値入力は、ユーザーが値を明示して入力する操作です。

ただし、入力できることと、その値が物理的・統計的に妥当であることは別です。

### 11.3 注意すること

数値を変更した場合は、次を確認します。

```text
どの値を変えたか
変更前の値
変更後の値
その値が source-derived なのか manual edit なのか
RUN / probe を押す前に Enable が必要か
```

---

## 12. 7a Enable と Run の使い方

7a は、local-only AxiCLASS fixed-example check を行う場所です。

7a の目的は、固定例に対して local check を行うことです。

### 12.1 Enable の役割

7a では、Run を押す前に Enable を確認します。

Enable は、実行系操作を明示的に許可するための gate です。

Enable を入れずに Run を押した場合、期待した check は実行されません。

### 12.2 Run ボタン

Run ボタンは赤色で表示されます。

これは、通常の入力ではなく実行操作であることを示すためです。

### 12.3 7a の読み方

7a の出力は、local fixed-example check の結果です。

次のようには読みません。

```text
posterior comparison
likelihood evaluation
Planck validation
manuscript value update
```

安全な読み方は次です。

```text
local fixed-example check が走った
payload と実行結果を確認した
次に監査すべき箇所を整理した
```

---

## 13. 7b Enable と live probe の使い方

7b は、local vanilla CLASS live probe を行う場所です。

7b の目的は、現在の入力値または互換可能な sidebar profile をもとに、local vanilla CLASS endpoint へ payload を送ることです。

### 13.1 7b の前提

7b を正常に使うには、local 8011 API が起動している必要があります。

通常の endpoint は次です。

```text
http://127.0.0.1:8011/axiclass/live-vanilla-probe
```

### 13.2 Enable の役割

7b でも、Run local vanilla CLASS live probe を押す前に Enable を確認します。

Enable を入れないまま Run を押しても、意図した live probe は実行されません。

### 13.3 live probe が返すもの

live probe が成功すると、local vanilla CLASS から derived parameters などが返ります。

ただし、これは likelihood ではありません。

次のようには読みません。

```text
この値が posterior 的に支持された
この値で Planck validation が完了した
この値で manuscript value を更新する
```

安全な読み方は次です。

```text
local vanilla CLASS endpoint が応答した
payload が通った
derived parameters を確認した
次の監査候補を得た
```

---

## 14. 8011 unavailable 表示の意味

7b で local 8011 API が起動していない場合、アプリは 8011 unavailable に関する案内を表示します。

これは、アプリ本体が壊れたという意味ではありません。

### 14.1 よくある状態

よくある状態は次です。

```text
local 8503 app は起動している
しかし local 8011 API は起動していない
そのため 7b live probe は connection refused になる
```

この場合、local 8503 の UI は正常でも、7b live probe は成功しません。

### 14.2 対応

8011 unavailable が出た場合は、次を確認します。

```text
local 8011 API を起動しているか
endpoint が http://127.0.0.1:8011/axiclass/live-vanilla-probe になっているか
Run 前に Enable を入れているか
local 8503 だけでなく 8011 側も生きているか
```

### 14.3 誤読しないこと

8011 unavailable は、科学的失敗ではありません。

これは通信・起動状態の問題です。

次のようには読みません。

```text
model が棄却された
Planck validation に失敗した
posterior が悪い
physical discontinuity が否定された
```

---

## 15. 7c Enable と continuity examiner の使い方

7c は、continuity / discontinuity examiner です。

目的は、選んだ parameter path や sweep design に対して、derived quantities の応答が smooth か、jump-like な候補を持つかを local に確認することです。

### 15.1 7c の位置づけ

7c は examiner panel です。

物理的な discontinuity を証明する場所ではありません。

operator-phase transition を証明する場所でもありません。

### 15.2 Enable の役割

7c でも、Run continuity / discontinuity examiner を押す前に Enable を確認します。

Enable を入れないまま Run を押すと、意図した examiner は動きません。

### 15.3 7c が判断できること

7c が判断できることは、限定的です。

```text
選んだ grid と tolerance の範囲で smooth に見えるか
jump-like candidate があるか
grid / endpoint / solver の都合で inconclusive か
```

### 15.4 7c が判断できないこと

7c が判断できないことは、次です。

```text
physical discontinuity の証明
operator-phase transition の証明
likelihood evaluation
posterior comparison
Planck validation
manuscript value update
```

### 15.5 7c の安全な読み方

安全な読み方は次です。

```text
local examiner で smooth / non-smooth candidate を見た
次に本格監査すべき sweep design を整理した
値の変化方向や応答の粗い特徴を確認した
```

7c の結果をそのまま論文結論には使いません。

---

## 次に追加する章

Part 04 では、以下を追記します。

```text
16. Section 8 の使い方
17. Boundary table の読み方
18. Boundary confirmation の読み方
19. graph rendering disabled の意味
20. README / Manual / source-of-record の管理
```

---

## 16. Section 8 の使い方

Section 8 は、Candidate payload と boundary confirmation を確認するための領域です。

ここでは、入力値、payload、境界的な読み方、確認表を整理します。

Section 8 は、結論を直接出す場所ではありません。

### 16.1 Section 8 で行うこと

Section 8 で行うことは次です。

```text
Candidate payload の確認
Boundary table の確認
Boundary confirmation の確認
入力値と出力表示の整合確認
境界文言が過剰主張になっていないかの確認
```

### 16.2 Section 8 で行わないこと

Section 8 で行わないことは次です。

```text
likelihood evaluation
posterior comparison
Planck validation
physics-value update
manuscript value update
physical-discontinuity proof
operator-phase transition proof
```

Section 8 は、payload と boundary を整理する場所です。

### 16.3 Section 8 の安全な読み方

安全な読み方は次です。

```text
この Candidate payload はこういう値を持つ
この boundary table は解釈範囲を限定している
この boundary confirmation は主張の上限を確認している
この表示は本格統計評価ではない
```

---

## 17. Boundary table の読み方

Boundary table は、アプリ内で表示される値や解釈が、どこまで言えるかを制限するための表です。

これは、結果を強く見せるための表ではありません。

過剰解釈を防ぐための表です。

### 17.1 Boundary table の目的

Boundary table の目的は次です。

```text
何を言ってよいかを明確にする
何を言ってはいけないかを明確にする
UI表示と論文主張を混同しない
local probe と統計評価を混同しない
```

### 17.2 Boundary table の基本姿勢

Boundary table を読むときは、次を守ります。

```text
OK と書いてあっても、それはその表示範囲内の OK である
NG と書いてある項目は、アプリ内の表示から主張してはいけない
source-of-record がない値は、採用値として扱わない
```

### 17.3 特に注意する境界

特に注意する境界は次です。

```text
not likelihood result
not posterior comparison
not Planck validation
not physics-value update
not manuscript update
not physical-discontinuity proof
not operator-phase transition proof
```

Boundary table は、レビュー安全性を保つための guardrail です。

---

## 18. Boundary confirmation の読み方

Boundary confirmation は、Boundary table の内容が UI 上で崩れていないかを確認する領域です。

これは、境界を突破して新しい主張を出す場所ではありません。

### 18.1 Boundary confirmation の目的

Boundary confirmation の目的は次です。

```text
表示されている値が boundary を超えて読まれていないか
説明文が過剰主張になっていないか
UI上のラベルが誤解を招かないか
read-only 表示として扱うべき箇所が実行操作に見えていないか
```

### 18.2 確認するポイント

確認するポイントは次です。

```text
likelihood / posterior / Planck という語が誤った文脈で使われていないか
physical discontinuity を証明したように見えていないか
operator-phase transition を証明したように見えていないか
local-only probe の結果を manuscript value に見せていないか
```

### 18.3 安全な読み方

Boundary confirmation は、次のように読みます。

```text
境界文言が守られているかを確認した
UI表示の誤読リスクを下げた
主張を広げるのではなく、主張の範囲を狭く管理した
```

---

## 19. graph rendering disabled の意味

現在のアプリでは、graph rendering は閉じています。

これは、グラフが不要という意味ではありません。

不確かな graph route を開くと、fake / synthetic / fallback graph が科学的出力に見えてしまう危険があるためです。

### 19.1 なぜ graph を閉じているか

graph rendering を閉じている理由は次です。

```text
fake graph を科学出力に見せないため
fallback graph を実測値に見せないため
UI reference graph を likelihood result に見せないため
source-of-record のない曲線を出さないため
```

### 19.2 graph を再開してよい条件

graph を再開してよい条件は限定されます。

```text
real output source がある
source-of-record が明示されている
graph が likelihood / posterior / Planck validation ではないことを明示できる
fake / fallback / synthetic / illustrative graph ではない
```

### 19.3 Strategy A / Strategy B との関係

今後 graph を再検討する場合、候補は次です。

```text
Strategy A: 多次元変化を1つの理論的 path に落とし、path coordinate をX軸にする
Strategy B: 多次元出力を散布図として表示し、色やサイズで stress を表す
```

ただし、どちらも source-of-record のある real output に限定します。

現時点の freeze では graph rendering は closed のままです。

---

## 20. README / Manual / source-of-record の管理

README と Manual は、アプリの使い方と境界を説明するための文書です。

README は短い導入用です。

Manual は詳しい操作説明用です。

### 20.1 README の役割

README の役割は次です。

```text
アプリの目的を短く説明する
起動方法を示す
local-only boundary を示す
8503 / 8011 の関係を説明する
```

README は、最初に読む簡易説明です。

### 20.2 Manual の役割

Manual の役割は次です。

```text
1つずつ丁寧に操作手順を説明する
各Sectionの意味を説明する
Enable / Run / probe の関係を説明する
境界文言を明確にする
誤読を防ぐ
```

Manual は、詳細な取扱説明書です。

### 20.3 source-of-record の役割

source-of-record は、値や図や判断の出所を固定するための記録です。

このアプリでは、値を見たときに次を区別します。

```text
manual input
sidebar profile
registered preset
local 8011 live output
external API response
audited run-derived TSV
source-of-record table
```

source-of-record がない値は、採用値として扱いません。

### 20.4 更新時のルール

README / Manual / app.py を更新する場合は、次を守ります。

```text
バックアップを作る
app.py を触るか docs だけかを分ける
py_compile を通す
static check を通す
local 8503 で確認する
Git add / commit / push は明示的に行う
Render deploy / public update は別判断にする
```

---

## 次に追加する章

Part 05 では、以下を追記します。

```text
21. よくある失敗と対処
22. 8011 API が動いているか確認する方法
23. GitHub 反映前チェック
24. freeze / pointer / handoff の考え方
25. 今後 graph Strategy A / B を試すときの安全ルール
```

---

## 21. よくある失敗と対処

このアプリでは、操作そのものよりも、境界の読み違い、Enable の押し忘れ、local 8011 API の未起動、source-of-record の混同が失敗の主原因になります。

ここでは、よくある失敗と対処を整理します。

### 21.1 RUN / probe を押しても期待した動作にならない

最初に確認することは Enable です。

7a / 7b / 7c には、それぞれ Enable checkbox があります。

Enable を入れずに RUN / probe を押すと、実行されない、または意図した確認にならない場合があります。

対処は次です。

```text
1. 対象Sectionの Enable checkbox を確認する
2. Enable が入っていることを確認する
3. 赤い RUN / probe ボタンを押す
4. 結果表示を確認する
```

### 21.2 7b live probe が失敗する

7b は local 8011 API を使います。

そのため、local 8011 API が起動していない場合、7b は接続できません。

この場合は、アプリの失敗ではなく、local endpoint が使えない状態です。

対処は次です。

```text
1. 8011 API が起動しているか確認する
2. 8011 API が不要なら、7b live probe を使わない
3. 8011 API を使う場合は、先に API を起動する
4. 再度 7b Enable を入れて live probe を押す
```

### 21.3 README / Manual が見つからない

README / Manual は docs directory に置かれます。

現在の Manual path は次です。

```text
docs/DTI_LOCAL_8503_MANUAL.md
```

README path は次です。

```text
docs/README_DTI_LOCAL_8503.md
```

見つからない場合は、docs directory が GitHub に反映されているか、local clone に存在しているかを確認します。

### 21.4 graph が出ない

現在の freeze では graph rendering は意図的に閉じています。

これは異常ではありません。

fake / fallback / synthetic / illustrative graph を科学的出力に見せないための安全措置です。

graph を出す作業は、別の experimental clone または branch で行います。

### 21.5 値を見て結論を出したくなる

このアプリの表示値は、すぐに論文結論へ移してはいけません。

値を見るときは、必ず次を確認します。

```text
source-of-record は何か
local probe か
manual input か
registered preset か
external API response か
audited run-derived TSV か
```

source-of-record が固定されていない値は、採用値ではありません。

---

## 22. 8011 API が動いているか確認する方法

7b live probe は、local 8011 API に接続します。

接続先は次です。

```text
http://127.0.0.1:8011/axiclass/live-vanilla-probe
```

### 22.1 8011 port を確認する

Terminal で次を実行します。

```bash
lsof -tiTCP:8011 -sTCP:LISTEN
```

PID が表示されれば、何かが 8011 port で listen しています。

何も表示されない場合、8011 API は起動していない可能性が高いです。

### 22.2 health endpoint がある場合

API に health endpoint がある場合は、次のように確認します。

```bash
curl -fsS http://127.0.0.1:8011/health
```

ただし、health endpoint が実装されていない場合もあります。

その場合、health が失敗しても、API 全体が壊れているとは限りません。

### 22.3 live-vanilla-probe endpoint の注意

live-vanilla-probe endpoint は POST 用です。

単純な browser access や curl GET では正しく確認できない場合があります。

7b live probe は、アプリ側から必要な payload を POST します。

### 22.4 8011 が不要な場合

8011 API を使わない場合は、7b live probe を使う必要はありません。

その場合でも、他の UI 確認、profile cartridge、boundary confirmation、Manual 参照は利用できます。

---

## 23. GitHub 反映前チェック

GitHub に反映する前には、必ず local check を行います。

特に app.py を変更した場合は、py_compile と static check を必須にします。

### 23.1 最小チェック

最小チェックは次です。

```bash
python3 -m py_compile app.py
git status --short
git diff --stat
```

### 23.2 反映対象を限定する

GitHub に反映するファイルは、必ず限定します。

例えば Manual だけを反映する場合は、docs file だけを stage します。

app.py と docs を同時に反映する場合も、意図しているか確認します。

```bash
git diff --cached --name-only
```

この出力で、stage されたファイルが意図どおりか確認します。

### 23.3 やってはいけない反映

やってはいけない反映は次です。

```text
意図せず app.py を含める
一時ファイルを含める
backup directory を含める
large output directory を含める
source-of-record でない graph を含める
```

### 23.4 commit message

commit message は、何を反映したかが分かる短い文にします。

例です。

```text
Add local 8503 manual sections
Update README and local 8011 guidance
Freeze local DTI 8503 UI state with guarded run controls
```

---

## 24. freeze / pointer / handoff の考え方

このプロジェクトでは、動いた状態をそのまま更新し続けるのではなく、freeze / pointer / handoff を分けます。

これは、後から状態を失わないためです。

### 24.1 freeze

freeze は、ある時点で受け入れた状態を固定することです。

freeze では、次を記録します。

```text
app.py SHA256
Git commit
branch
remote
主要な変更内容
境界条件
未実施の操作
```

### 24.2 pointer

pointer は、現在どの freeze を採用しているかを示す記録です。

pointer は record-only であるべきです。

pointer 作成だけで app.py を変更しません。

### 24.3 handoff

handoff は、次の作業者または次スレッドへ状態を渡すための記録です。

handoff には、次を含めます。

```text
現在の採用状態
変更済みファイル
未反映のファイル
GitHub commit
未実施の deploy
禁止事項
次の安全な作業
```

### 24.4 なぜ必要か

freeze / pointer / handoff を分ける理由は次です。

```text
どの状態が採用済みか分かる
実験と採用を混同しない
GitHub 反映と deploy を混同しない
local 8503 と public update を混同しない
失敗した patch から安全に戻れる
```

---

## 25. 今後 graph Strategy A / B を試すときの安全ルール

graph Strategy A / B は、今後の experimental work です。

現在の freeze では graph rendering は closed です。

graph を試す場合は、必ず別 branch または別 clone で行います。

### 25.1 Strategy A

Strategy A は、多次元パラメータ変化を1つの理論的 path に落とす方法です。

例えば、H0 と omega_cdm を別々に動かすのではなく、連動する path を定義し、その path coordinate を X 軸にします。

安全な表現は次です。

```text
path-coordinate sweep
one-dimensional trajectory
theory-motivated parameter path
diagnostic path, not likelihood scan
```

Strategy A は、美しい線を作りやすい一方で、path の定義に責任が生じます。

### 25.2 Strategy B

Strategy B は、多次元出力を scatter plot として表示する方法です。

線で結ばず、計算された点をそのまま表示します。

色やサイズで stress, S8, rs_drag, residual などを表すことができます。

安全な表現は次です。

```text
scatter diagnostic
point-cloud view
multi-parameter output map
not posterior distribution
not likelihood contour
```

Strategy B は、多次元性を隠さない点で安全です。

### 25.3 共通ルール

Strategy A / B 共通のルールは次です。

```text
fake graph を使わない
synthetic graph を使わない
fallback graph を使わない
UI reference graph を科学出力に見せない
source-of-record のある real output だけを使う
graph label に boundary を書く
likelihood / posterior / Planck validation と誤読されないようにする
```

### 25.4 現在の freeze に戻る方法

graph 実験が失敗した場合は、現在の freeze に戻します。

現在の基準は次です。

```text
app.py accepted local state around post README/sidebar/manual work
GitHub freeze commit lineage: ef0c602 and later docs/app updates if committed
graph rendering remains closed unless explicitly reopened in experimental line
```

graph は重要ですが、source-of-record と boundary が揃うまで、採用線には入れません。

---

## 次に追加する章

Part 06 では、以下を追記します。

```text
26. Manual / README をアプリ内から配布する設計
27. Markdown Manual と PDF Manual の使い分け
28. PDF化する場合の注意
29. docs を GitHub に反映する手順
30. Manual 完成後の freeze 手順
```

---

## 26. Manual / README をアプリ内から配布する設計

このアプリでは、README と Manual をアプリ内から直接ダウンロードできる形にするのが望ましいです。

理由は、アプリの操作が単純な数値入力だけではなく、境界条件、source-of-record、local 8011 API、Enable gate、GitHub freeze などを含むためです。

操作説明を別ファイルに置いたままだと、ユーザーが手順を見失いやすくなります。

### 26.1 README と Manual の役割分担

README は短い導入用です。

Manual は詳細な取扱説明書です。

役割は次のように分けます。

```text
README:
  起動方法
  現在の freeze identity
  最低限の境界条件
  8011 API がない場合の注意

Manual:
  各Sectionの使い方
  Enable / RUN / probe の意味
  source-of-record の扱い
  graph disabled の理由
  GitHub反映前チェック
  freeze / pointer / handoff の運用
```

README は入口、Manual は本体です。

### 26.2 アプリ内 download button の配置

download button は、左サイドバーの Section 1 と Section 2 の間が適切です。

理由は次です。

```text
最初に profile を選ぶ
その直後に説明書を確認できる
Current profile status を見る前に注意点を読める
上部に埋もれない
操作導線から外れない
```

現在の方針では、Manual / README download area は左サイドバーに置きます。

### 26.3 README / Manual button で避けること

避けるべきことは次です。

```text
Main page の最上部だけに置く
結果表示の下に置く
Section 7b や 7c の中だけに置く
RUN button と同じ見た目にする
Manual を graph output のように見せる
```

Manual は実行結果ではありません。

したがって、Manual download button は RUN / probe とは視覚的に区別します。

---

## 27. Markdown Manual と PDF Manual の使い分け

Manual は Markdown と PDF の両方で持つのが望ましいです。

ただし、役割は違います。

### 27.1 Markdown Manual

Markdown Manual は編集用・GitHub管理用です。

利点は次です。

```text
差分が見やすい
GitHub で管理しやすい
追記しやすい
source-of-record として扱いやすい
アプリ内 download に向いている
```

現在の Manual source-of-record は次です。

```text
docs/DTI_LOCAL_8503_MANUAL.md
```

### 27.2 PDF Manual

PDF Manual は配布用・閲覧用です。

利点は次です。

```text
見た目が固定される
ユーザーに渡しやすい
印刷しやすい
ページ番号を参照しやすい
外部共有に向いている
```

一方で、PDF は編集 source-of-record にはしません。

PDF は Markdown から生成した派生物として扱います。

### 27.3 どちらを優先するか

開発中は Markdown を優先します。

配布時は PDF を追加します。

運用は次の形が安全です。

```text
Markdown Manual = source-of-record
PDF Manual = generated distribution copy
```

### 27.4 アプリ内ではどちらを配るか

アプリ内では、まず Markdown を配ります。

PDF 生成が安定したら、PDF も追加します。

ただし、PDF を追加する場合でも、Markdown source-of-record を残します。

---

## 28. PDF化する場合の注意

PDF化は便利ですが、注意が必要です。

PDF生成で layout や font、改行、code block が崩れることがあります。

そのため、PDF化は Manual 完成後に行います。

### 28.1 PDF化前の確認

PDF化前に確認することは次です。

```text
Markdown Manual が完成している
章番号が重複していない
code block が閉じている
境界条件が正しく書かれている
app.py の SHA / Git commit が最新か確認する
source-of-record と generated PDF の関係を書く
```

### 28.2 PDF化後の確認

PDF化後に確認することは次です。

```text
ページ数
PDFが開けること
章見出しが欠けていないこと
code block が崩れていないこと
日本語が文字化けしていないこと
Manual source Markdown の SHA を記録すること
PDF SHA を記録すること
```

### 28.3 PDFを直接編集しない

PDF は直接編集しません。

修正が必要な場合は、Markdown を修正して、PDF を再生成します。

安全な流れは次です。

```text
1. Markdown Manual を修正
2. Markdown SHA を記録
3. PDF を生成
4. PDF SHA を記録
5. Markdown と PDF の対応表を作る
```

### 28.4 PDF化で避けること

避けるべきことは次です。

```text
Markdown と PDF の内容がズレる
PDFだけを更新する
古い freeze SHA をPDFに残す
未採用 graph をPDFに入れる
source-of-record でない値をManualに入れる
```

---

## 29. docs を GitHub に反映する手順

docs を GitHub に反映するときは、app.py の変更と混ぜないように注意します。

Manual だけを反映する場合は、docs file だけを stage します。

### 29.1 反映前チェック

まず状態を確認します。

```bash
git status --short
git diff --stat
```

Manual の差分を確認します。

```bash
git diff -- docs/DTI_LOCAL_8503_MANUAL.md
```

README も含める場合は、次も確認します。

```bash
git diff -- docs/README_DTI_LOCAL_8503.md
```

### 29.2 stage する

Manual だけを stage する場合は次です。

```bash
git add docs/DTI_LOCAL_8503_MANUAL.md
```

README も含める場合は次です。

```bash
git add docs/DTI_LOCAL_8503_MANUAL.md docs/README_DTI_LOCAL_8503.md
```

stage 後に必ず確認します。

```bash
git diff --cached --name-only
git diff --cached --stat
```

### 29.3 commit する

commit message は、Manual 追加であることが分かるようにします。

例です。

```bash
git commit -m "Add local 8503 app manual"
```

### 29.4 push する

push は次です。

```bash
git push origin main
```

push 後に確認します。

```bash
git log --oneline -1
git status --short
```

### 29.5 app.py が混ざっている場合

Manual だけを反映したいのに app.py が staged に入っている場合は、一度 reset します。

```bash
git reset
```

その後、docs file だけを stage し直します。

---

## 30. Manual 完成後の freeze 手順

Manual が完成したら、Manual freeze を作ります。

Manual freeze は、app freeze とは分けて管理します。

### 30.1 Manual freeze で記録するもの

記録するものは次です。

```text
Manual path
Manual SHA256
Manual bytes
README path
README SHA256
app.py SHA256
Git commit
branch
remote
作成日時
Manual の章範囲
PDF を生成した場合は PDF path / PDF SHA256
```

### 30.2 freeze の意味

Manual freeze は、その時点の説明書を採用状態として固定する記録です。

Manual freeze を作っても、app.py を変更する必要はありません。

### 30.3 pointer を作る

Manual freeze 後は、現在採用中の Manual を示す pointer を作ります。

pointer には次を書きます。

```text
current manual source-of-record
current manual SHA256
current app.py SHA256
current Git commit
docs committed or not
PDF generated or not
next action
```

### 30.4 handoff を作る

最後に handoff を作ります。

handoff には、次スレッドで迷わない情報を含めます。

```text
Manual はどこまで完成したか
未完成章があるか
GitHub に反映済みか
PDF化済みか
app.py は変更されたか
graph は reopened されたか
deploy は行ったか
次に何をするか
```

### 30.5 Manual 完成後の次工程

Manual 完成後の候補は次です。

```text
1. Manual Markdown の final audit
2. README と Manual の整合確認
3. GitHub docs commit
4. PDF Manual 生成
5. PDF Manual download button 追加
6. Manual freeze pointer 作成
7. graph Strategy A / B experimental branch 作成
```

この順番なら、説明書、GitHub、PDF、実験線を混同しにくくなります。

---

## 次に追加する章

Part 07 では、必要なら以下を追記します。

```text
31. README と Manual の整合チェック
32. Manual final audit checklist
33. PDF Manual 生成コマンド
34. PDF Manual download button 実装方針
35. Manual freeze pointer template
```


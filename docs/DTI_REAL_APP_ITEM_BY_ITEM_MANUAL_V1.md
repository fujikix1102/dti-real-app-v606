# DTI Real App — Item-by-Item Manual V1

This manual explains the visible and discoverable app items one by one, in human-readable language.

Created as a documentation file only. This file does not modify the app, does not run CLASS/AxiCLASS, does not compute a likelihood, does not run MCMC, does not compare posteriors, does not update the public app, and does not update the manuscript.

- Public app: https://dti-real-app-v606.streamlit.app/
- Git HEAD / origin target: `fb7970261e2fadc42e2ab673dba108e6262b4b20`
- `app.py` SHA256: `dd0bf188bdb74750a2dc8b6b952a050d51a502add1220bfd77ba9cb5e8a9254f`
- `app.py` line count: `11819`
- Extracted UI item count: `458`
- Extracted session-state key count: `46`

---

## 0. How to read this manual

Read this document as an operation guide. Each item explains what the UI element is, how to use it, and what it does not prove.

Negative phrases such as `not`, `do not`, `not a likelihood`, and `not validation` are normal in this manual. They are included to prevent overclaiming.

The app should be read through these labels:

- **diagnostic**: useful for checking behavior or consistency.
- **audit-only**: useful for reproducibility and provenance checks.
- **source-locked**: tied to a frozen source or displayed input.
- **bounded**: valid only within the stated scope.
- **display-only**: visible for reading, not a full inference computation.

---

## 1. Screen sections detected from the app

| index | line | kind | label |
| --- | ---: | --- | --- |
| 55 | 2217 | `expander` | top |
| 66 | 2345 | `expander` | Boundary note for reviewers and researchers |
| 78 | 2935 | `expander` | top |
| 101 | 3855 | `expander` | Candidate profile inputs |
| 103 | 3863 | `expander` | Reference profile inputs |
| 119 | 5346 | `expander` | Boundary and claim limits |
| 124 | 5425 | `expander` | Direction summary — static TSV only |
| 126 | 5439 | `expander` | Compact static delta table — audit display only |
| 128 | 5447 | `expander` | Compact static delta table — reader view |
| 130 | 5452 | `expander` | Boundary and safe interpretation |
| 132 | 5589 | `expander` | Raw data — audit view |
| 137 | 5620 | `expander` | Raw data — audit view |
| 138 | 5829 | `expander` | Background geometry anchor — local FLRW calculator |
| 140 | 5880 | `expander` | Raw data — audit view |
| 144 | 6106 | `expander` | Jump toy comparator — piecewise background geometry |
| 151 | 6201 | `expander` | Raw data — audit view |
| 161 | 6514 | `expander` | Raw data — audit view |
| 163 | 6549 | `expander` | Global claim limits / audit boundary |
| 165 | 6576 | `expander` | top |
| 167 | 6628 | `expander` | Raw data — audit view |
| 171 | 6682 | `expander` | Raw data — audit view |
| 174 | 6721 | `expander` | Raw data — audit view |
| 182 | 6765 | `expander` | Raw data — audit view |
| 190 | 7981 | `expander` | CMB spectra graph — real API arrays only |
| 197 | 8233 | `expander` | CMB array availability audit |
| 204 | 8372 | `title` | DTI-Core Grand Auditor v6.0.6 |
| 207 | 8415 | `header` | 1. Parameter profile cartridge |
| 218 | 8491 | `subheader` | 2. Current profile status |
| 225 | 8506 | `subheader` | 3. Export / share |
| 228 | 8520 | `header` | 1. Candidate / Reference parameter input form |
| 229 | 8525 | `expander` | TARGET_MODEL form |
| 240 | 8543 | `expander` | LCDM comparison form |
| 252 | 8571 | `header` | 2. Source metadata |
| 253 | 8573 | `expander` | Candidate and reference source metadata |
| 261 | 8594 | `header` | 3. Literature text audit |
| 262 | 8598 | `subheader` | TARGET_MODEL vs LCDM comparison |
| 265 | 8605 | `header` | 4. High-precision parameter search engine |
| 270 | 8634 | `subheader` | Current input model safety/readout cards |
| 274 | 8692 | `header` | 5. AxiCLASS FIX1 locked benchmark |
| 286 | 8769 | `header` | 6. RK45 background-universe proxy |
| 293 | 8795 | `header` | 7. Local experimental probes |
| 294 | 8811 | `subheader` | 7 preflight. Public API warm-up |
| 295 | 8820 | `expander` | Warm up configured API endpoints before 7a/7b |
| 297 | 8858 | `header` | 7a. AxiCLASS fixed-example check |
| 299 | 8911 | `expander` | How to use the AxiCLASS API endpoint |
| 308 | 9011 | `expander` | Raw fixed-example API response |
| 309 | 9020 | `header` | 7b. Vanilla-profile API check |
| 333 | 9925 | `header` | 7c. Continuity / discontinuity examiner |
| 345 | 10461 | `header` | 8. Candidate payload / boundary confirmation |
| 350 | 10670 | `header` | 9. External CLASS API sandbox |
| 359 | 10750 | `expander` | Raw external API response |
| 361 | 10755 | `expander` | CMB spectra graph — real API arrays only |
| 362 | 10760 | `header` | 10. Interpretation boundary |
| 367 | 10871 | `expander` | Jump parameter translator — backend boundary check |
| 378 | 10920 | `expander` | Request payload preview |
| 388 | 10960 | `expander` | Full translator response |
| 392 | 11053 | `expander` | DTI capability provenance and no-claim boundary |
| 395 | 11085 | `expander` | Paper / APJ conversion status |
| 396 | 11124 | `subheader` | Observed-data posterior |
| 397 | 11153 | `expander` | Boundary / audit status |
| 398 | 11209 | `expander` | Embedded posterior viewer — offline BAO chain, audit-only |
| 403 | 11243 | `expander` | Raw embedded tables — provenance / audit readback |
| 404 | 11244 | `subheader` | Chain summary |
| 405 | 11247 | `subheader` | G02 diagnostics — TSV |
| 406 | 11250 | `subheader` | MAP / best-fit table |
| 407 | 11253 | `subheader` | Source identity |
| 409 | 11270 | `expander` | Claim boundary |
| 415 | 11390 | `expander` | Source TSV table — G01 |
| 418 | 11406 | `expander` | Source TSV table — G02 |
| 421 | 11422 | `expander` | Source TSV table — G03 |
| 430 | 11489 | `expander` | Route A manual-sanity diagnostic — frozen independent lane |
| 434 | 11573 | `expander` | Route A/B Boundary Matrix — diagnostic available, full inference unavailable |
| 437 | 11624 | `expander` | Route A/B boundary provenance |
| 454 | 11770 | `expander` | Frozen CLAIM_BOUNDARY.md readback |
| 458 | 11793 | `expander` | About / Citation / Provenance |

---

## 2. Item-by-item explanation

The following list follows the order extracted from `app.py`. Some labels are literal screen labels; others are source expressions where the label is generated dynamically.


### Section: top

#### Item 1: line 22 — `markdown` — **{label}**

- **種類**: `markdown`
- **画面上の表示名**: **{label}**
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**{label}**"`

#### Item 2: line 73 — `warning` — Skipped dataframe display: Streamlit container object was passed without a data object.

- **種類**: `warning`
- **画面上の表示名**: Skipped dataframe display: Streamlit container object was passed without a data object.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Skipped dataframe display: Streamlit container object was passed without a data object."`

#### Item 3: line 116 — `dataframe` — (dynamic or variable-derived label)

- **種類**: `dataframe`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 表形式のデータ表示です。結果や監査表を確認するための表示であり、それ自体は新しい推論ではありません。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `df, *args, **kwargs`

#### Item 4: line 386 — `markdown` — ### Positive answer navigator

- **種類**: `markdown`
- **画面上の表示名**: ### Positive answer navigator
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Positive answer navigator"`

#### Item 5: line 450 — `markdown` — #### Answer format

- **種類**: `markdown`
- **画面上の表示名**: #### Answer format
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Answer format"`

#### Item 6: line 497 — `markdown` — ### Research motivation layer

- **種類**: `markdown`
- **画面上の表示名**: ### Research motivation layer
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Research motivation layer"`

#### Item 7: line 551 — `markdown` — #### Constructive answer template

- **種類**: `markdown`
- **画面上の表示名**: #### Constructive answer template
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Constructive answer template"`

#### Item 8: line 588 — `markdown` — ### Research Opportunity Engine

- **種類**: `markdown`
- **画面上の表示名**: ### Research Opportunity Engine
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Research Opportunity Engine"`

#### Item 9: line 595 — `markdown` — #### Research Opportunity Map

- **種類**: `markdown`
- **画面上の表示名**: #### Research Opportunity Map
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Research Opportunity Map"`

#### Item 10: line 646 — `markdown` — #### Next Test Composer

- **種類**: `markdown`
- **画面上の表示名**: #### Next Test Composer
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Next Test Composer"`

#### Item 11: line 662 — `markdown` — #### Claim Boundary Translator

- **種類**: `markdown`
- **画面上の表示名**: #### Claim Boundary Translator
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Claim Boundary Translator"`

#### Item 12: line 727 — `markdown` — ### Discovery Score and Claim Readiness

- **種類**: `markdown`
- **画面上の表示名**: ### Discovery Score and Claim Readiness
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Discovery Score and Claim Readiness"`

#### Item 13: line 736 — `markdown` — #### Lightweight scoring inputs

- **種類**: `markdown`
- **画面上の表示名**: #### Lightweight scoring inputs
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Lightweight scoring inputs"`

#### Item 14: line 823 — `markdown` — #### Constructive interpretation

- **種類**: `markdown`
- **画面上の表示名**: #### Constructive interpretation
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Constructive interpretation"`

#### Item 15: line 852 — `markdown` — #### Positive finding box

- **種類**: `markdown`
- **画面上の表示名**: #### Positive finding box
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Positive finding box"`

#### Item 16: line 875 — `markdown` — #### Safe claim translator

- **種類**: `markdown`
- **画面上の表示名**: #### Safe claim translator
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Safe claim translator"`

#### Item 17: line 960 — `markdown` — ### Legacy/detail Parameter Quality Matrix 1 — audit view

- **種類**: `markdown`
- **画面上の表示名**: ### Legacy/detail Parameter Quality Matrix 1 — audit view
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Legacy/detail Parameter Quality Matrix 1 — audit view"`

#### Item 18: line 969 — `markdown` — #### Parameter direction presets

- **種類**: `markdown`
- **画面上の表示名**: #### Parameter direction presets
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Parameter direction presets"`

#### Item 19: line 1078 — `markdown` — #### Total evaluation table

- **種類**: `markdown`
- **画面上の表示名**: #### Total evaluation table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Total evaluation table"`

#### Item 20: line 1102 — `markdown` — #### Best current leads

- **種類**: `markdown`
- **画面上の表示名**: #### Best current leads
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Best current leads"`

#### Item 21: line 1114 — `markdown` — #### How to use this table

- **種類**: `markdown`
- **画面上の表示名**: #### How to use this table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### How to use this table"`

#### Item 22: line 1264 — `markdown` — ### Legacy/detail Parameter Quality Matrix 2 — audit view

- **種類**: `markdown`
- **画面上の表示名**: ### Legacy/detail Parameter Quality Matrix 2 — audit view
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Legacy/detail Parameter Quality Matrix 2 — audit view"`

#### Item 23: line 1272 — `markdown` — #### Color meaning

- **種類**: `markdown`
- **画面上の表示名**: #### Color meaning
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Color meaning"`

#### Item 24: line 1276 — `markdown` — GREEN

- **種類**: `markdown`
- **画面上の表示名**: GREEN
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `_dti_pqm_v1g_badge_html("GREEN"), unsafe_allow_html=True`

#### Item 25: line 1277 — `caption` — Strong lead. Prioritize source-lock and strict follow-up.

- **種類**: `caption`
- **画面上の表示名**: Strong lead. Prioritize source-lock and strict follow-up.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Strong lead. Prioritize source-lock and strict follow-up."`

#### Item 26: line 1279 — `markdown` — YELLOW

- **種類**: `markdown`
- **画面上の表示名**: YELLOW
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `_dti_pqm_v1g_badge_html("YELLOW"), unsafe_allow_html=True`

#### Item 27: line 1280 — `caption` — Useful partial result. Needs one or more controls.

- **種類**: `caption`
- **画面上の表示名**: Useful partial result. Needs one or more controls.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Useful partial result. Needs one or more controls."`

#### Item 28: line 1282 — `markdown` — ORANGE

- **種類**: `markdown`
- **画面上の表示名**: ORANGE
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `_dti_pqm_v1g_badge_html("ORANGE"), unsafe_allow_html=True`

#### Item 29: line 1283 — `caption` — Control-needed direction. Do not claim yet.

- **種類**: `caption`
- **画面上の表示名**: Control-needed direction. Do not claim yet.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Control-needed direction. Do not claim yet."`

#### Item 30: line 1285 — `markdown` — RED

- **種類**: `markdown`
- **画面上の表示名**: RED
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `_dti_pqm_v1g_badge_html("RED"), unsafe_allow_html=True`

#### Item 31: line 1286 — `caption` — Blocked for claim-making, but useful as a boundary.

- **種類**: `caption`
- **画面上の表示名**: Blocked for claim-making, but useful as a boundary.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Blocked for claim-making, but useful as a boundary."`

#### Item 32: line 1288 — `markdown` — GRAY

- **種類**: `markdown`
- **画面上の表示名**: GRAY
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `_dti_pqm_v1g_badge_html("GRAY"), unsafe_allow_html=True`

#### Item 33: line 1289 — `caption` — No evaluation available yet.

- **種類**: `caption`
- **画面上の表示名**: No evaluation available yet.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No evaluation available yet."`

#### Item 34: line 1410 — `markdown` — #### Total evaluation table

- **種類**: `markdown`
- **画面上の表示名**: #### Total evaluation table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Total evaluation table"`

#### Item 35: line 1443 — `markdown` — #### Next-test priority order

- **種類**: `markdown`
- **画面上の表示名**: #### Next-test priority order
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Next-test priority order"`

#### Item 36: line 1444 — `caption` — This section shows the next practical test order, not a scientific ranking of truth.

- **種類**: `caption`
- **画面上の表示名**: This section shows the next practical test order, not a scientific ranking of truth.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"This section shows the next practical test order, not a scientific ranking of truth."`

#### Item 37: line 1465 — `markdown` — #### Research-role grouping

- **種類**: `markdown`
- **画面上の表示名**: #### Research-role grouping
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Research-role grouping"`

#### Item 38: line 1479 — `markdown` — #### How to use this table

- **種類**: `markdown`
- **画面上の表示名**: #### How to use this table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### How to use this table"`

#### Item 39: line 1578 — `markdown` — #### Color meaning

- **種類**: `markdown`
- **画面上の表示名**: #### Color meaning
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Color meaning"`

#### Item 40: line 1641 — `markdown` — ### Legacy/detail Parameter Quality Matrix 3 — audit view

- **種類**: `markdown`
- **画面上の表示名**: ### Legacy/detail Parameter Quality Matrix 3 — audit view
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Legacy/detail Parameter Quality Matrix 3 — audit view"`

#### Item 41: line 1800 — `markdown` — #### Legacy total evaluation table

- **種類**: `markdown`
- **画面上の表示名**: #### Legacy total evaluation table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Legacy total evaluation table"`

#### Item 42: line 1812 — `markdown` — #### Legacy next-test priority order

- **種類**: `markdown`
- **画面上の表示名**: #### Legacy next-test priority order
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Legacy next-test priority order"`

#### Item 43: line 1813 — `caption` — This is the practical test order, not a scientific ranking of truth.

- **種類**: `caption`
- **画面上の表示名**: This is the practical test order, not a scientific ranking of truth.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"This is the practical test order, not a scientific ranking of truth."`

#### Item 44: line 1843 — `markdown` — #### How to read this matrix

- **種類**: `markdown`
- **画面上の表示名**: #### How to read this matrix
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### How to read this matrix"`

#### Item 45: line 1898 — `markdown` — ### Probe Result Value Matrix

- **種類**: `markdown`
- **画面上の表示名**: ### Probe Result Value Matrix
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Probe Result Value Matrix"`

#### Item 46: line 1906 — `markdown` — #### Legacy color meaning

- **種類**: `markdown`
- **画面上の表示名**: #### Legacy color meaning
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Legacy color meaning"`

#### Item 47: line 1950 — `markdown` — #### Probe value summary

- **種類**: `markdown`
- **画面上の表示名**: #### Probe value summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Probe value summary"`

#### Item 48: line 2044 — `markdown` — #### Positive probe interpretation

- **種類**: `markdown`
- **画面上の表示名**: #### Positive probe interpretation
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Positive probe interpretation"`

#### Item 49: line 2079 — `markdown` — #### Research-fun summary

- **種類**: `markdown`
- **画面上の表示名**: #### Research-fun summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Research-fun summary"`

#### Item 50: line 2211 — `markdown` — **Research role:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Research role:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Research role:** {row['role']}"`

#### Item 51: line 2212 — `markdown` — **Why it matters:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Why it matters:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Why it matters:** {row['why']}"`

#### Item 52: line 2213 — `markdown` — **Safe interpretation:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Safe interpretation:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Safe interpretation:** {row['safe']}"`

#### Item 53: line 2214 — `markdown` — **Do not claim:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Do not claim:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Do not claim:** {row['not_claim']}"`

#### Item 54: line 2215 — `markdown` — **Next check:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Next check:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Next check:** {row['next']}"`

#### Item 55: line 2217 — `expander` — (dynamic or variable-derived label)

- **種類**: `expander`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `label, expanded=False`

#### Item 56: line 2218 — `markdown` — **Research role:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Research role:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Research role:** {row['role']}"`

#### Item 57: line 2219 — `markdown` — **Why it matters:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Why it matters:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Why it matters:** {row['why']}"`

#### Item 58: line 2220 — `markdown` — **Safe interpretation:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Safe interpretation:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Safe interpretation:** {row['safe']}"`

#### Item 59: line 2221 — `markdown` — **Do not claim:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Do not claim:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Do not claim:** {row['not_claim']}"`

#### Item 60: line 2222 — `markdown` — **Next check:** {row[

- **種類**: `markdown`
- **画面上の表示名**: **Next check:** {row[
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Next check:** {row['next']}"`

#### Item 61: line 2227 — `markdown` — #### Readout card detail guide

- **種類**: `markdown`
- **画面上の表示名**: #### Readout card detail guide
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Readout card detail guide"`

#### Item 62: line 2237 — `tabs` — Core branch

- **種類**: `tabs`
- **画面上の表示名**: Core branch
- **何をする項目か**: 表示内容を切り替えるタブです。タブ切替そのものは新しい推論や計算を意味しません。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `["Core branch", "Companion parameters", "Safety / next checks"]`

#### Item 63: line 2271 — `markdown` — ### Visitor Quick Guide

- **種類**: `markdown`
- **画面上の表示名**: ### Visitor Quick Guide
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Visitor Quick Guide"`

#### Item 64: line 2321 — `markdown` — #### Section flow

- **種類**: `markdown`
- **画面上の表示名**: #### Section flow
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Section flow"`

#### Item 65: line 2336 — `markdown` — #### Current best next action

- **種類**: `markdown`
- **画面上の表示名**: #### Current best next action
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Current best next action"`

#### Item 66: line 2345 — `expander` — Boundary note for reviewers and researchers

- **種類**: `expander`
- **画面上の表示名**: Boundary note for reviewers and researchers
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Boundary note for reviewers and researchers", expanded=False`

#### Item 67: line 2518 — `markdown` — ### Probe Result Value Matrix V2

- **種類**: `markdown`
- **画面上の表示名**: ### Probe Result Value Matrix V2
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Probe Result Value Matrix V2"`

#### Item 68: line 2549 — `markdown` — #### Probe value summary

- **種類**: `markdown`
- **画面上の表示名**: #### Probe value summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Probe value summary"`

#### Item 69: line 2562 — `markdown` — #### What each probe teaches

- **種類**: `markdown`
- **画面上の表示名**: #### What each probe teaches
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### What each probe teaches"`

#### Item 70: line 2586 — `markdown` — #### Research-use answer

- **種類**: `markdown`
- **画面上の表示名**: #### Research-use answer
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Research-use answer"`

#### Item 71: line 2677 — `markdown` — ### Parameter Quality Matrix

- **種類**: `markdown`
- **画面上の表示名**: ### Parameter Quality Matrix
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Parameter Quality Matrix"`

#### Item 72: line 2685 — `markdown` — #### Color meaning

- **種類**: `markdown`
- **画面上の表示名**: #### Color meaning
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Color meaning"`

#### Item 73: line 2847 — `markdown` — #### Compact total evaluation table

- **種類**: `markdown`
- **画面上の表示名**: #### Compact total evaluation table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Compact total evaluation table"`

#### Item 74: line 2878 — `markdown` — #### Next-test priority order

- **種類**: `markdown`
- **画面上の表示名**: #### Next-test priority order
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Next-test priority order"`

#### Item 75: line 2879 — `caption` — This is the practical test order, not a scientific ranking of truth.

- **種類**: `caption`
- **画面上の表示名**: This is the practical test order, not a scientific ranking of truth.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"This is the practical test order, not a scientific ranking of truth."`

#### Item 76: line 2930 — `markdown` — #### Full detail rows

- **種類**: `markdown`
- **画面上の表示名**: #### Full detail rows
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Full detail rows"`

#### Item 77: line 2931 — `caption` — Use these expanders for the long fields removed from the compact table.

- **種類**: `caption`
- **画面上の表示名**: Use these expanders for the long fields removed from the compact table.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Use these expanders for the long fields removed from the compact table."`

#### Item 78: line 2935 — `expander` — (dynamic or variable-derived label)

- **種類**: `expander`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `title, expanded=False`

#### Item 79: line 2936 — `markdown` — **Research role:** {row.get(

- **種類**: `markdown`
- **画面上の表示名**: **Research role:** {row.get(
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Research role:** {row.get('research_role')}"`

#### Item 80: line 2937 — `markdown` — **Role group:** {row.get(

- **種類**: `markdown`
- **画面上の表示名**: **Role group:** {row.get(
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Role group:** {row.get('role_group')}"`

#### Item 81: line 2938 — `markdown` — **Current value:** {row.get(

- **種類**: `markdown`
- **画面上の表示名**: **Current value:** {row.get(
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Current value:** {row.get('current_value')}"`

#### Item 82: line 2939 — `markdown` — **Positive signal:** {row.get(

- **種類**: `markdown`
- **画面上の表示名**: **Positive signal:** {row.get(
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Positive signal:** {row.get('positive_signal')}"`

#### Item 83: line 2940 — `markdown` — **Risk / blocker:** {row.get(

- **種類**: `markdown`
- **画面上の表示名**: **Risk / blocker:** {row.get(
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Risk / blocker:** {row.get('risk_blocker')}"`

#### Item 84: line 2941 — `markdown` — **Next test:** {row.get(

- **種類**: `markdown`
- **画面上の表示名**: **Next test:** {row.get(
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Next test:** {row.get('next_test')}"`

#### Item 85: line 2942 — `markdown` — **Safe interpretation:** {row.get(

- **種類**: `markdown`
- **画面上の表示名**: **Safe interpretation:** {row.get(
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Safe interpretation:** {row.get('safe_interpretation')}"`

#### Item 86: line 2944 — `markdown` — #### Use rule

- **種類**: `markdown`
- **画面上の表示名**: #### Use rule
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Use rule"`

#### Item 87: line 3565 — `markdown` — ### Candidate / Reference input

- **種類**: `markdown`
- **画面上の表示名**: ### Candidate / Reference input
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Candidate / Reference input"`

#### Item 88: line 3574 — `error` — No usable preset profiles were found. Check PRESETS/profile text registration.

- **種類**: `error`
- **画面上の表示名**: No usable preset profiles were found. Check PRESETS/profile text registration.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No usable preset profiles were found. Check PRESETS/profile text registration."`

#### Item 89: line 3601 — `button` — Load selected presets

- **種類**: `button`
- **画面上の表示名**: Load selected presets
- **内部キー**: `dti_ui_load_presets_v2`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Load selected presets", key="dti_ui_load_presets_v2", type="primary"`

#### Item 90: line 3606 — `success` — Candidate / Reference の入力欄へプリセット値を反映しました。

- **種類**: `success`
- **画面上の表示名**: Candidate / Reference の入力欄へプリセット値を反映しました。
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Candidate / Reference の入力欄へプリセット値を反映しました。"`

#### Item 91: line 3608 — `tabs` — Candidate

- **種類**: `tabs`
- **画面上の表示名**: Candidate
- **何をする項目か**: 表示内容を切り替えるタブです。タブ切替そのものは新しい推論や計算を意味しません。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `["Candidate", "Reference"]`

#### Item 92: line 3611 — `caption` — Candidate values.

- **種類**: `caption`
- **画面上の表示名**: Candidate values.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Candidate values."`

#### Item 93: line 3613 — `caption` — Edit the value column directly. Parameter names stay fixed.

- **種類**: `caption`
- **画面上の表示名**: Edit the value column directly. Parameter names stay fixed.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Edit the value column directly. Parameter names stay fixed."`

#### Item 94: line 3617 — `caption` — Reference values.

- **種類**: `caption`
- **画面上の表示名**: Reference values.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Reference values."`

#### Item 95: line 3626 — `markdown` — ### Current difference

- **種類**: `markdown`
- **画面上の表示名**: ### Current difference
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Current difference"`

#### Item 96: line 3632 — `caption` — /

- **種類**: `caption`
- **画面上の表示名**: /
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `" / ".join(diff_lines)`

#### Item 97: line 3827 — `markdown` — ### Candidate / Reference input

- **種類**: `markdown`
- **画面上の表示名**: ### Candidate / Reference input
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Candidate / Reference input"`

#### Item 98: line 3828 — `caption` — Use all registered presets as Candidate / Reference starting points. Edit values below as needed.

- **種類**: `caption`
- **画面上の表示名**: Use all registered presets as Candidate / Reference starting points. Edit values below as needed.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Use all registered presets as Candidate / Reference starting points. Edit values below as needed."`

#### Item 99: line 3847 — `caption` — Preset choices available: {len(preset_names)}

- **種類**: `caption`
- **画面上の表示名**: Preset choices available: {len(preset_names)}
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Preset choices available: {len(preset_names)}"`

#### Item 100: line 3849 — `button` — Load selected presets into inputs

- **種類**: `button`
- **画面上の表示名**: Load selected presets into inputs
- **内部キー**: `dti_ui_load_presets_v1`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Load selected presets into inputs", key="dti_ui_load_presets_v1"`

#### Item 101: line 3855 — `expander` — Candidate profile inputs

- **種類**: `expander`
- **画面上の表示名**: Candidate profile inputs
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Candidate profile inputs", expanded=True`

#### Item 102: line 3856 — `caption` — Candidate values: type directly or use +/- buttons.

- **種類**: `caption`
- **画面上の表示名**: Candidate values: type directly or use +/- buttons.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Candidate values: type directly or use +/- buttons."`

#### Item 103: line 3863 — `expander` — Reference profile inputs

- **種類**: `expander`
- **画面上の表示名**: Reference profile inputs
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Reference profile inputs", expanded=True`

#### Item 104: line 3864 — `caption` — Reference values: type directly or use +/- buttons.

- **種類**: `caption`
- **画面上の表示名**: Reference values: type directly or use +/- buttons.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Reference values: type directly or use +/- buttons."`

#### Item 105: line 3876 — `markdown` — ### Current difference

- **種類**: `markdown`
- **画面上の表示名**: ### Current difference
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Current difference"`

#### Item 106: line 3880 — `caption` — {key}: {row[

- **種類**: `caption`
- **画面上の表示名**: {key}: {row[
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"{key}: {row['delta']:+.5g}"`

#### Item 107: line 3889 — `markdown` — ## Candidate / Reference comparison guide

- **種類**: `markdown`
- **画面上の表示名**: ## Candidate / Reference comparison guide
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"## Candidate / Reference comparison guide"`

#### Item 108: line 3901 — `info` — Use the left sidebar Candidate / Reference input form to populate this comparison.

- **種類**: `info`
- **画面上の表示名**: Use the left sidebar Candidate / Reference input form to populate this comparison.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Use the left sidebar Candidate / Reference input form to populate this comparison."`

#### Item 109: line 3909 — `markdown` — ### Candidate vs Reference

- **種類**: `markdown`
- **画面上の表示名**: ### Candidate vs Reference
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Candidate vs Reference"`

#### Item 110: line 3912 — `markdown` — ### What changed from the reference?

- **種類**: `markdown`
- **画面上の表示名**: ### What changed from the reference?
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### What changed from the reference?"`

#### Item 111: line 3933 — `markdown` — \n

- **種類**: `markdown`
- **画面上の表示名**: \n
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"\n".join(notes)`

#### Item 112: line 3935 — `markdown` — ### Parameter guide

- **種類**: `markdown`
- **画面上の表示名**: ### Parameter guide
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Parameter guide"`

#### Item 113: line 5054 — `caption` — Source: {_dti_source_label_v1f}. This table is not an active selection control.

- **種類**: `caption`
- **画面上の表示名**: Source: {_dti_source_label_v1f}. This table is not an active selection control.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Source: {_dti_source_label_v1f}. This table is not an active selection control."`

#### Item 114: line 5303 — `markdown` — ### Correlated-boundary triage proxy

- **種類**: `markdown`
- **画面上の表示名**: ### Correlated-boundary triage proxy
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Correlated-boundary triage proxy"`

#### Item 115: line 5324 — `success` — Correlated-boundary proxy: GREEN / score={score}

- **種類**: `success`
- **画面上の表示名**: Correlated-boundary proxy: GREEN / score={score}
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Correlated-boundary proxy: GREEN / score={score}"`

#### Item 116: line 5326 — `warning` — Correlated-boundary proxy: ORANGE / score={score}

- **種類**: `warning`
- **画面上の表示名**: Correlated-boundary proxy: ORANGE / score={score}
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Correlated-boundary proxy: ORANGE / score={score}"`

#### Item 117: line 5328 — `error` — Correlated-boundary proxy: RED / score={score}

- **種類**: `error`
- **画面上の表示名**: Correlated-boundary proxy: RED / score={score}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Correlated-boundary proxy: RED / score={score}"`

#### Item 118: line 5330 — `info` — Correlated-boundary proxy: GRAY / insufficient inputs

- **種類**: `info`
- **画面上の表示名**: Correlated-boundary proxy: GRAY / insufficient inputs
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Correlated-boundary proxy: GRAY / insufficient inputs"`

#### Item 119: line 5346 — `expander` — Boundary and claim limits

- **種類**: `expander`
- **画面上の表示名**: Boundary and claim limits
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Boundary and claim limits", expanded=False`

#### Item 120: line 5364 — `caption` — safe_interpretation

- **種類**: `caption`
- **画面上の表示名**: safe_interpretation
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `result.get("safe_interpretation", "")`

#### Item 121: line 5365 — `caption` — not_claim

- **種類**: `caption`
- **画面上の表示名**: not_claim
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `result.get("not_claim", "")`

#### Item 122: line 5397 — `markdown` — ### AxiCLASS FIX1 static delta audit table

- **種類**: `markdown`
- **画面上の表示名**: ### AxiCLASS FIX1 static delta audit table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### AxiCLASS FIX1 static delta audit table"`

#### Item 123: line 5406 — `info` — Static delta audit table unavailable. {err}

- **種類**: `info`
- **画面上の表示名**: Static delta audit table unavailable. {err}
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Static delta audit table unavailable. {err}"`

#### Item 124: line 5425 — `expander` — Direction summary — static TSV only

- **種類**: `expander`
- **画面上の表示名**: Direction summary — static TSV only
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Direction summary — static TSV only", expanded=False`

#### Item 125: line 5437 — `caption` — Direction summary unavailable.

- **種類**: `caption`
- **画面上の表示名**: Direction summary unavailable.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Direction summary unavailable."`

#### Item 126: line 5439 — `expander` — Compact static delta table — audit display only

- **種類**: `expander`
- **画面上の表示名**: Compact static delta table — audit display only
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Compact static delta table — audit display only", expanded=False`

#### Item 127: line 5443 — `caption` — Compact reader-facing view: wide model names are shortened into columns; source TSV remains unchanged.

- **種類**: `caption`
- **画面上の表示名**: Compact reader-facing view: wide model names are shortened into columns; source TSV remains unchanged.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Compact reader-facing view: wide model names are shortened into columns; source TSV remains unchanged."`

#### Item 128: line 5447 — `expander` — Compact static delta table — reader view

- **種類**: `expander`
- **画面上の表示名**: Compact static delta table — reader view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Compact static delta table — reader view", expanded=True`

#### Item 129: line 5450 — `caption` — Compact static delta reader view unavailable; source TSV display remains bounded.

- **種類**: `caption`
- **画面上の表示名**: Compact static delta reader view unavailable; source TSV display remains bounded.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Compact static delta reader view unavailable; source TSV display remains bounded."`

#### Item 130: line 5452 — `expander` — Boundary and safe interpretation

- **種類**: `expander`
- **画面上の表示名**: Boundary and safe interpretation
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Boundary and safe interpretation", expanded=False`

#### Item 131: line 5588 — `info` — No vanilla-profile payload values are available yet.

- **種類**: `info`
- **画面上の表示名**: No vanilla-profile payload values are available yet.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No vanilla-profile payload values are available yet."`

#### Item 132: line 5589 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 133: line 5593 — `markdown` — ### Vanilla-profile API check result

- **種類**: `markdown`
- **画面上の表示名**: ### Vanilla-profile API check result
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Vanilla-profile API check result"`

#### Item 134: line 5600 — `success` — Vanilla-profile API check: PASS / HTTP {http_status if http_status is not None else

- **種類**: `success`
- **画面上の表示名**: Vanilla-profile API check: PASS / HTTP {http_status if http_status is not None else
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Vanilla-profile API check: PASS / HTTP {http_status if http_status is not None else 'unknown'}"`

#### Item 135: line 5602 — `warning` — Vanilla-profile API check: REVIEW / HTTP {http_status if http_status is not None else

- **種類**: `warning`
- **画面上の表示名**: Vanilla-profile API check: REVIEW / HTTP {http_status if http_status is not None else
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Vanilla-profile API check: REVIEW / HTTP {http_status if http_status is not None else 'unknown'}"`

#### Item 136: line 5617 — `markdown` — #### Input and derived summary

- **種類**: `markdown`
- **画面上の表示名**: #### Input and derived summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Input and derived summary"`

#### Item 137: line 5620 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 138: line 5829 — `expander` — Background geometry anchor — local FLRW calculator

- **種類**: `expander`
- **画面上の表示名**: Background geometry anchor — local FLRW calculator
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Background geometry anchor — local FLRW calculator", expanded=False`

#### Item 139: line 5879 — `warning` — Background geometry calculation returned invalid support for the selected parameters.

- **種類**: `warning`
- **画面上の表示名**: Background geometry calculation returned invalid support for the selected parameters.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Background geometry calculation returned invalid support for the selected parameters."`

#### Item 140: line 5880 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 141: line 5890 — `markdown` — #### Summary

- **種類**: `markdown`
- **画面上の表示名**: #### Summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Summary"`

#### Item 142: line 5893 — `markdown` — #### Time baseline

- **種類**: `markdown`
- **画面上の表示名**: #### Time baseline
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Time baseline"`

#### Item 143: line 5896 — `markdown` — #### Distance baseline

- **種類**: `markdown`
- **画面上の表示名**: #### Distance baseline
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Distance baseline"`

#### Item 144: line 6106 — `expander` — Jump toy comparator — piecewise background geometry

- **種類**: `expander`
- **画面上の表示名**: Jump toy comparator — piecewise background geometry
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Jump toy comparator — piecewise background geometry", expanded=True`

#### Item 145: line 6111 — `button` — Load jump-toy demonstration values

- **種類**: `button`
- **画面上の表示名**: Load jump-toy demonstration values
- **内部キー**: `dti_bggeom_load_jump_toy_demo_values_v1`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Load jump-toy demonstration values", key="dti_bggeom_load_jump_toy_demo_values_v1"`

#### Item 146: line 6148 — `markdown` — #### Summary

- **種類**: `markdown`
- **画面上の表示名**: #### Summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Summary"`

#### Item 147: line 6151 — `markdown` — #### Compact table

- **種類**: `markdown`
- **画面上の表示名**: #### Compact table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Compact table"`

#### Item 148: line 6156 — `info` — Jump comparator table is unavailable for the selected parameters.

- **種類**: `info`
- **画面上の表示名**: Jump comparator table is unavailable for the selected parameters.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Jump comparator table is unavailable for the selected parameters."`

#### Item 149: line 6160 — `markdown` — #### Jump toy curves

- **種類**: `markdown`
- **画面上の表示名**: #### Jump toy curves
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Jump toy curves"`

#### Item 150: line 6161 — `tabs` — Time baseline

- **種類**: `tabs`
- **画面上の表示名**: Time baseline
- **何をする項目か**: 表示内容を切り替えるタブです。タブ切替そのものは新しい推論や計算を意味しません。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `["Time baseline", "Distance baseline", "Delta"]`

#### Item 151: line 6201 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 152: line 6282 — `info` — Graph data is unavailable.

- **種類**: `info`
- **画面上の表示名**: Graph data is unavailable.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Graph data is unavailable."`

#### Item 153: line 6317 — `info` — Not enough numeric graph rows for this panel.

- **種類**: `info`
- **画面上の表示名**: Not enough numeric graph rows for this panel.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Not enough numeric graph rows for this panel."`

#### Item 154: line 6326 — `info` — No numeric graph values for this panel.

- **種類**: `info`
- **画面上の表示名**: No numeric graph values for this panel.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No numeric graph values for this panel."`

#### Item 155: line 6388 — `info` — No drawable numeric graph series for this panel.

- **種類**: `info`
- **画面上の表示名**: No drawable numeric graph series for this panel.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No drawable numeric graph series for this panel."`

#### Item 156: line 6411 — `markdown` — \n

- **種類**: `markdown`
- **画面上の表示名**: \n
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"\n".join(svg_parts), unsafe_allow_html=True`

#### Item 157: line 6470 — `info` — Background geometry graph data could not be prepared: {exc}

- **種類**: `info`
- **画面上の表示名**: Background geometry graph data could not be prepared: {exc}
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Background geometry graph data could not be prepared: {exc}"`

#### Item 158: line 6474 — `info` — Background geometry graph rows are unavailable.

- **種類**: `info`
- **画面上の表示名**: Background geometry graph rows are unavailable.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Background geometry graph rows are unavailable."`

#### Item 159: line 6477 — `markdown` — #### Background geometry curves

- **種類**: `markdown`
- **画面上の表示名**: #### Background geometry curves
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Background geometry curves"`

#### Item 160: line 6479 — `tabs` — Time baseline

- **種類**: `tabs`
- **画面上の表示名**: Time baseline
- **何をする項目か**: 表示内容を切り替えるタブです。タブ切替そのものは新しい推論や計算を意味しません。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `["Time baseline", "Distance baseline", "Angular scale"]`

#### Item 161: line 6514 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 162: line 6544 — `markdown` — ### Global claim limits / audit boundary

- **種類**: `markdown`
- **画面上の表示名**: ### Global claim limits / audit boundary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Global claim limits / audit boundary"`

#### Item 163: line 6549 — `expander` — Global claim limits / audit boundary

- **種類**: `expander`
- **画面上の表示名**: Global claim limits / audit boundary
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Global claim limits / audit boundary", expanded=False`

#### Item 164: line 6564 — `caption` — (dynamic or variable-derived label)

- **種類**: `caption`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `text`

#### Item 165: line 6576 — `expander` — (dynamic or variable-derived label)

- **種類**: `expander`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `title, expanded=False`

#### Item 166: line 6627 — `info` — 7c examiner payload is not available yet.

- **種類**: `info`
- **画面上の表示名**: 7c examiner payload is not available yet.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"7c examiner payload is not available yet."`

#### Item 167: line 6628 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 168: line 6671 — `markdown` — #### Sweep summary

- **種類**: `markdown`
- **画面上の表示名**: #### Sweep summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Sweep summary"`

#### Item 169: line 6675 — `markdown` — #### Base payload summary

- **種類**: `markdown`
- **画面上の表示名**: #### Base payload summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Base payload summary"`

#### Item 170: line 6679 — `markdown` — #### Boundary flags

- **種類**: `markdown`
- **画面上の表示名**: #### Boundary flags
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Boundary flags"`

#### Item 171: line 6682 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 172: line 6716 — `markdown` — ##### Examiner verdict record

- **種類**: `markdown`
- **画面上の表示名**: ##### Examiner verdict record
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Examiner verdict record"`

#### Item 173: line 6720 — `warning` — 7c examiner verdict record is not available in table form.

- **種類**: `warning`
- **画面上の表示名**: 7c examiner verdict record is not available in table form.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"7c examiner verdict record is not available in table form."`

#### Item 174: line 6721 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 175: line 6729 — `success` — 7c examiner verdict: {verdict}

- **種類**: `success`
- **画面上の表示名**: 7c examiner verdict: {verdict}
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"7c examiner verdict: {verdict}"`

#### Item 176: line 6731 — `warning` — 7c examiner verdict requires review: {verdict}

- **種類**: `warning`
- **画面上の表示名**: 7c examiner verdict requires review: {verdict}
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"7c examiner verdict requires review: {verdict}"`

#### Item 177: line 6743 — `markdown` — ###### Base payload summary

- **種類**: `markdown`
- **画面上の表示名**: ###### Base payload summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"###### Base payload summary"`

#### Item 178: line 6748 — `markdown` — ###### Sweep summary

- **種類**: `markdown`
- **画面上の表示名**: ###### Sweep summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"###### Sweep summary"`

#### Item 179: line 6753 — `markdown` — ###### Result summary

- **種類**: `markdown`
- **画面上の表示名**: ###### Result summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"###### Result summary"`

#### Item 180: line 6758 — `markdown` — ###### Boundary flags

- **種類**: `markdown`
- **画面上の表示名**: ###### Boundary flags
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"###### Boundary flags"`

#### Item 181: line 6763 — `caption` — (dynamic or variable-derived label)

- **種類**: `caption`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `str(warning)`

#### Item 182: line 6765 — `expander` — Raw data — audit view

- **種類**: `expander`
- **画面上の表示名**: Raw data — audit view
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw data — audit view", expanded=False`

#### Item 183: line 7929 — `markdown` — ### CMB / Likelihood capability matrix — API readiness audit

- **種類**: `markdown`
- **画面上の表示名**: ### CMB / Likelihood capability matrix — API readiness audit
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### CMB / Likelihood capability matrix — API readiness audit"`

#### Item 184: line 7935 — `info` — No API payload available in this session. Showing required fields and readiness boundaries.

- **種類**: `info`
- **画面上の表示名**: No API payload available in this session. Showing required fields and readiness boundaries.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No API payload available in this session. Showing required fields and readiness boundaries."`

#### Item 185: line 7940 — `markdown` — #### Summary

- **種類**: `markdown`
- **画面上の表示名**: #### Summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Summary"`

#### Item 186: line 7952 — `markdown` — #### Capability matrix

- **種類**: `markdown`
- **画面上の表示名**: #### Capability matrix
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Capability matrix"`

#### Item 187: line 7954 — `table` — (dynamic or variable-derived label)

- **種類**: `table`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 固定的な表表示です。整理済みの値や比較表を読むために使います。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `rows`

#### Item 188: line 7976 — `markdown` — #### Raw data — audit view

- **種類**: `markdown`
- **画面上の表示名**: #### Raw data — audit view
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Raw data — audit view"`

#### Item 189: line 7977 — `caption` — Large arrays are summarized here to keep the UI readable. The graph renderer still uses the full real API arrays.

- **種類**: `caption`
- **画面上の表示名**: Large arrays are summarized here to keep the UI readable. The graph renderer still uses the full real API arrays.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Large arrays are summarized here to keep the UI readable. The graph renderer still uses the full real API arrays."`

#### Item 190: line 7981 — `expander` — CMB spectra graph — real API arrays only

- **種類**: `expander`
- **画面上の表示名**: CMB spectra graph — real API arrays only
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"CMB spectra graph — real API arrays only", expanded=False`

#### Item 191: line 8148 — `info` — {label}: no valid real array available for plotting.

- **種類**: `info`
- **画面上の表示名**: {label}: no valid real array available for plotting.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"{label}: no valid real array available for plotting."`

#### Item 192: line 8170 — `markdown` — (dynamic or variable-derived label)

- **種類**: `markdown`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `svg, unsafe_allow_html=True`

#### Item 193: line 8179 — `markdown` — ### CMB spectra graph — real API arrays only

- **種類**: `markdown`
- **画面上の表示名**: ### CMB spectra graph — real API arrays only
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### CMB spectra graph — real API arrays only"`

#### Item 194: line 8182 — `info` — No API payload available. CMB graph is not rendered.

- **種類**: `info`
- **画面上の表示名**: No API payload available. CMB graph is not rendered.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No API payload available. CMB graph is not rendered."`

#### Item 195: line 8189 — `info` — No derived payload available. CMB graph is not rendered.

- **種類**: `info`
- **画面上の表示名**: No derived payload available. CMB graph is not rendered.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No derived payload available. CMB graph is not rendered."`

#### Item 196: line 8208 — `success` — CMB graph readiness = YES. Rendering only real arrays returned by the external API.

- **種類**: `success`
- **画面上の表示名**: CMB graph readiness = YES. Rendering only real arrays returned by the external API.
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"CMB graph readiness = YES. Rendering only real arrays returned by the external API."`

#### Item 197: line 8233 — `expander` — CMB array availability audit

- **種類**: `expander`
- **画面上の表示名**: CMB array availability audit
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"CMB array availability audit", expanded=False`

#### Item 198: line 8245 — `table` — (dynamic or variable-derived label)

- **種類**: `table`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 固定的な表表示です。整理済みの値や比較表を読むために使います。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `rows`

#### Item 199: line 8249 — `tabs` — TT

- **種類**: `tabs`
- **画面上の表示名**: TT
- **何をする項目か**: 表示内容を切り替えるタブです。タブ切替そのものは新しい推論や計算を意味しません。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `["TT", "TE", "EE", "Lensing"]`

#### Item 200: line 8257 — `info` — TT array not available.

- **種類**: `info`
- **画面上の表示名**: TT array not available.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"TT array not available."`

#### Item 201: line 8265 — `info` — TE array not available.

- **種類**: `info`
- **画面上の表示名**: TE array not available.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"TE array not available."`

#### Item 202: line 8273 — `info` — EE array not available.

- **種類**: `info`
- **画面上の表示名**: EE array not available.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"EE array not available."`

#### Item 203: line 8279 — `info` — Lensing array cl_pp not available.

- **種類**: `info`
- **画面上の表示名**: Lensing array cl_pp not available.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Lensing array cl_pp not available."`


### Section: DTI-Core Grand Auditor v6.0.6

#### Item 204: line 8372 — `title` — DTI-Core Grand Auditor v6.0.6

- **種類**: `title`
- **画面上の表示名**: DTI-Core Grand Auditor v6.0.6
- **何をする項目か**: 画面または大きな領域のタイトルです。アプリ内で現在どの領域を見ているかを示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"DTI-Core Grand Auditor v6.0.6"`

#### Item 205: line 8373 — `caption` — Public parameter-profile audit interface for cosmological model comparison, benchmark proximity review, and reproducibility-first inspection.

- **種類**: `caption`
- **画面上の表示名**: Public parameter-profile audit interface for cosmological model comparison, benchmark proximity review, and reproducibility-first inspection.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Public parameter-profile audit interface for cosmological model comparison, benchmark proximity review, and reproducibility-first inspection."`

#### Item 206: line 8403 — `info` — DOM-safe rendering mode: live/exploratory outputs are rendered as stable code blocks instead of dynamic JSON widgets.

- **種類**: `info`
- **画面上の表示名**: DOM-safe rendering mode: live/exploratory outputs are rendered as stable code blocks instead of dynamic JSON widgets.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"DOM-safe rendering mode: live/exploratory outputs are rendered as stable code blocks instead of dynamic JSON widgets."`


### Section: 1. Parameter profile cartridge

#### Item 207: line 8415 — `header` — 1. Parameter profile cartridge

- **種類**: `header`
- **画面上の表示名**: 1. Parameter profile cartridge
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"1. Parameter profile cartridge"`

#### Item 208: line 8432 — `caption` — Fallback only. Normal use should use Profile category → ACTIVE loader above.

- **種類**: `caption`
- **画面上の表示名**: Fallback only. Normal use should use Profile category → ACTIVE loader above.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Fallback only. Normal use should use Profile category → ACTIVE loader above."`

#### Item 209: line 8440 — `caption` — Fallback selection is visible for compatibility; categorized ACTIVE loader remains primary.

- **種類**: `caption`
- **画面上の表示名**: Fallback selection is visible for compatibility; categorized ACTIVE loader remains primary.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Fallback selection is visible for compatibility; categorized ACTIVE loader remains primary."`

#### Item 210: line 8452 — `info` — (dynamic or variable-derived label)

- **種類**: `info`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `preset_note`

#### Item 211: line 8464 — `text_area` — Profile text / generated block

- **種類**: `text_area`
- **画面上の表示名**: Profile text / generated block
- **内部キー**: `paper_text_widget`
- **何をする項目か**: 長い文字列を入力または表示する欄です。JSON、メモ、説明、raw response などに使われます。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Profile text / generated block", key="paper_text_widget", height=270`

#### Item 212: line 8473 — `markdown` — #### Step 1: apply text to form

- **種類**: `markdown`
- **画面上の表示名**: #### Step 1: apply text to form
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Step 1: apply text to form"`

#### Item 213: line 8474 — `caption` — After editing the TARGET_MODEL block, use this button to load the values into the form.

- **種類**: `caption`
- **画面上の表示名**: After editing the TARGET_MODEL block, use this button to load the values into the form.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"After editing the TARGET_MODEL block, use this button to load the values into the form."`

#### Item 214: line 8476 — `caption` — Step 1: edit the TARGET_MODEL block, then apply it to the form.

- **種類**: `caption`
- **画面上の表示名**: Step 1: edit the TARGET_MODEL block, then apply it to the form.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Step 1: edit the TARGET_MODEL block, then apply it to the form."`

#### Item 215: line 8477 — `button` — Apply text to form

- **種類**: `button`
- **画面上の表示名**: Apply text to form
- **内部キー**: `sidebar_text_to_form_v606`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Apply text to form", width="stretch", key="sidebar_text_to_form_v606", type="primary"`

#### Item 216: line 8481 — `button` — Form to text

- **種類**: `button`
- **画面上の表示名**: Form to text
- **内部キー**: `sidebar_form_to_text_v606`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Form to text", width="stretch", key="sidebar_form_to_text_v606"`

#### Item 217: line 8485 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`


### Section: 2. Current profile status

#### Item 218: line 8491 — `subheader` — 2. Current profile status

- **種類**: `subheader`
- **画面上の表示名**: 2. Current profile status
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"2. Current profile status"`

#### Item 219: line 8499 — `markdown` — **Active profile:** {active_profile_name}

- **種類**: `markdown`
- **画面上の表示名**: **Active profile:** {active_profile_name}
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Active profile:** {active_profile_name}"`

#### Item 220: line 8500 — `markdown` — **Profile role:** {active_profile_role}

- **種類**: `markdown`
- **画面上の表示名**: **Profile role:** {active_profile_role}
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"**Profile role:** {active_profile_role}"`

#### Item 221: line 8501 — `markdown` — **Mode:** Candidate / Reference comparison

- **種類**: `markdown`
- **画面上の表示名**: **Mode:** Candidate / Reference comparison
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"**Mode:** Candidate / Reference comparison"`

#### Item 222: line 8502 — `success` — AxiCLASS FIX1 benchmark: read-only

- **種類**: `success`
- **画面上の表示名**: AxiCLASS FIX1 benchmark: read-only
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"AxiCLASS FIX1 benchmark: read-only"`

#### Item 223: line 8503 — `caption` — Changing presets or form values does not recompute this locked benchmark.

- **種類**: `caption`
- **画面上の表示名**: Changing presets or form values does not recompute this locked benchmark.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Changing presets or form values does not recompute this locked benchmark."`

#### Item 224: line 8505 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`


### Section: 3. Export / share

#### Item 225: line 8506 — `subheader` — 3. Export / share

- **種類**: `subheader`
- **画面上の表示名**: 3. Export / share
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"3. Export / share"`

#### Item 226: line 8518 — `markdown` — [Open GitHub](https://github.com/fujikix1102/dti-real-app-v606)

- **種類**: `markdown`
- **画面上の表示名**: [Open GitHub](https://github.com/fujikix1102/dti-real-app-v606)
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"[Open GitHub](https://github.com/fujikix1102/dti-real-app-v606)"`

#### Item 227: line 8519 — `markdown` — [Open public app](https://dti-real-app-v606.streamlit.app)

- **種類**: `markdown`
- **画面上の表示名**: [Open public app](https://dti-real-app-v606.streamlit.app)
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"[Open public app](https://dti-real-app-v606.streamlit.app)"`


### Section: 1. Candidate / Reference parameter input form

#### Item 228: line 8520 — `header` — 1. Candidate / Reference parameter input form

- **種類**: `header`
- **画面上の表示名**: 1. Candidate / Reference parameter input form
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"1. Candidate / Reference parameter input form"`

#### Item 229: line 8525 — `expander` — TARGET_MODEL form

- **種類**: `expander`
- **画面上の表示名**: TARGET_MODEL form
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"TARGET_MODEL form", expanded=True`

#### Item 230: line 8528 — `number_input` — H0

- **種類**: `number_input`
- **画面上の表示名**: H0
- **内部キー**: `target_H0`
- **初期値または指定値**: `40.0`
- **最小値**: `40.0`
- **最大値**: `90.0`
- **刻み幅**: `0.01`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"H0", min_value=40.0, max_value=90.0, step=0.01, key="target_H0"`

#### Item 231: line 8529 — `number_input` — f_EDE

- **種類**: `number_input`
- **画面上の表示名**: f_EDE
- **内部キー**: `target_f_EDE`
- **初期値または指定値**: `0.0`
- **最小値**: `0.0`
- **最大値**: `0.30`
- **刻み幅**: `0.001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"f_EDE", min_value=0.0, max_value=0.30, step=0.001, key="target_f_EDE"`

#### Item 232: line 8531 — `number_input` — omega_cdm

- **種類**: `number_input`
- **画面上の表示名**: omega_cdm
- **内部キー**: `target_omega_cdm`
- **初期値または指定値**: `0.05`
- **最小値**: `0.05`
- **最大値**: `0.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="target_omega_cdm"`

#### Item 233: line 8532 — `number_input` — omega_b

- **種類**: `number_input`
- **画面上の表示名**: omega_b
- **内部キー**: `target_omega_b`
- **初期値または指定値**: `0.015`
- **最小値**: `0.015`
- **最大値**: `0.035`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="target_omega_b"`

#### Item 234: line 8534 — `number_input` — sigma8

- **種類**: `number_input`
- **画面上の表示名**: sigma8
- **内部キー**: `target_sigma8`
- **初期値または指定値**: `0.50`
- **最小値**: `0.50`
- **最大値**: `1.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"sigma8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="target_sigma8"`

#### Item 235: line 8535 — `number_input` — S8

- **種類**: `number_input`
- **画面上の表示名**: S8
- **内部キー**: `target_S8`
- **初期値または指定値**: `0.50`
- **最小値**: `0.50`
- **最大値**: `1.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"S8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="target_S8"`

#### Item 236: line 8537 — `number_input` — z_c

- **種類**: `number_input`
- **画面上の表示名**: z_c
- **内部キー**: `target_z_c`
- **初期値または指定値**: `0.0`
- **最小値**: `0.0`
- **最大値**: `10000.0`
- **刻み幅**: `50.0`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"z_c", min_value=0.0, max_value=10000.0, step=50.0, key="target_z_c"`

#### Item 237: line 8538 — `number_input` — ln10_10_As

- **種類**: `number_input`
- **画面上の表示名**: ln10_10_As
- **内部キー**: `target_ln10_10_As`
- **初期値または指定値**: `1.0`
- **最小値**: `1.0`
- **最大値**: `4.5`
- **刻み幅**: `0.001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"ln10_10_As", min_value=1.0, max_value=4.5, step=0.001, format="%.5f", key="target_ln10_10_As"`

#### Item 238: line 8540 — `number_input` — n_s

- **種類**: `number_input`
- **画面上の表示名**: n_s
- **内部キー**: `target_n_s`
- **初期値または指定値**: `0.80`
- **最小値**: `0.80`
- **最大値**: `1.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"n_s", min_value=0.80, max_value=1.20, step=0.0001, format="%.5f", key="target_n_s"`

#### Item 239: line 8541 — `number_input` — tau_reio

- **種類**: `number_input`
- **画面上の表示名**: tau_reio
- **内部キー**: `target_tau_reio`
- **初期値または指定値**: `0.0`
- **最小値**: `0.0`
- **最大値**: `0.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"tau_reio", min_value=0.0, max_value=0.20, step=0.0001, format="%.5f", key="target_tau_reio"`

#### Item 240: line 8543 — `expander` — LCDM comparison form

- **種類**: `expander`
- **画面上の表示名**: LCDM comparison form
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"LCDM comparison form", expanded=False`

#### Item 241: line 8546 — `number_input` — LCDM H0

- **種類**: `number_input`
- **画面上の表示名**: LCDM H0
- **内部キー**: `lcdm_H0`
- **初期値または指定値**: `40.0`
- **最小値**: `40.0`
- **最大値**: `90.0`
- **刻み幅**: `0.01`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM H0", min_value=40.0, max_value=90.0, step=0.01, key="lcdm_H0"`

#### Item 242: line 8547 — `number_input` — LCDM Omega_m

- **種類**: `number_input`
- **画面上の表示名**: LCDM Omega_m
- **内部キー**: `lcdm_Omega_m`
- **初期値または指定値**: `0.10`
- **最小値**: `0.10`
- **最大値**: `0.60`
- **刻み幅**: `0.001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM Omega_m", min_value=0.10, max_value=0.60, step=0.001, format="%.5f", key="lcdm_Omega_m"`

#### Item 243: line 8549 — `number_input` — LCDM omega_cdm

- **種類**: `number_input`
- **画面上の表示名**: LCDM omega_cdm
- **内部キー**: `lcdm_omega_cdm`
- **初期値または指定値**: `0.05`
- **最小値**: `0.05`
- **最大値**: `0.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_omega_cdm"`

#### Item 244: line 8550 — `number_input` — LCDM omega_b

- **種類**: `number_input`
- **画面上の表示名**: LCDM omega_b
- **内部キー**: `lcdm_omega_b`
- **初期値または指定値**: `0.015`
- **最小値**: `0.015`
- **最大値**: `0.035`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="lcdm_omega_b"`

#### Item 245: line 8552 — `number_input` — LCDM sigma8

- **種類**: `number_input`
- **画面上の表示名**: LCDM sigma8
- **内部キー**: `lcdm_sigma8`
- **初期値または指定値**: `0.50`
- **最小値**: `0.50`
- **最大値**: `1.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM sigma8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_sigma8"`

#### Item 246: line 8553 — `number_input` — LCDM S8

- **種類**: `number_input`
- **画面上の表示名**: LCDM S8
- **内部キー**: `lcdm_S8`
- **初期値または指定値**: `0.50`
- **最小値**: `0.50`
- **最大値**: `1.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM S8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_S8"`

#### Item 247: line 8555 — `number_input` — LCDM ln10_10_As

- **種類**: `number_input`
- **画面上の表示名**: LCDM ln10_10_As
- **内部キー**: `lcdm_ln10_10_As`
- **初期値または指定値**: `1.0`
- **最小値**: `1.0`
- **最大値**: `4.5`
- **刻み幅**: `0.001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM ln10_10_As", min_value=1.0, max_value=4.5, step=0.001, format="%.5f", key="lcdm_ln10_10_As"`

#### Item 248: line 8556 — `number_input` — LCDM n_s

- **種類**: `number_input`
- **画面上の表示名**: LCDM n_s
- **内部キー**: `lcdm_n_s`
- **初期値または指定値**: `0.80`
- **最小値**: `0.80`
- **最大値**: `1.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM n_s", min_value=0.80, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_n_s"`

#### Item 249: line 8558 — `number_input` — LCDM tau_reio

- **種類**: `number_input`
- **画面上の表示名**: LCDM tau_reio
- **内部キー**: `lcdm_tau_reio`
- **初期値または指定値**: `0.0`
- **最小値**: `0.0`
- **最大値**: `0.20`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"LCDM tau_reio", min_value=0.0, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_tau_reio"`

#### Item 250: line 8560 — `button` — Apply form values to text and update search engine

- **種類**: `button`
- **画面上の表示名**: Apply form values to text and update search engine
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Apply form values to text and update search engine", type="primary", width="stretch"`

#### Item 251: line 8569 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`


### Section: 2. Source metadata

#### Item 252: line 8571 — `header` — 2. Source metadata

- **種類**: `header`
- **画面上の表示名**: 2. Source metadata
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"2. Source metadata"`

#### Item 253: line 8573 — `expander` — Candidate and reference source metadata

- **種類**: `expander`
- **画面上の表示名**: Candidate and reference source metadata
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Candidate and reference source metadata", expanded=True`

#### Item 254: line 8574 — `markdown` — <div class=

- **種類**: `markdown`
- **画面上の表示名**: <div class=
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `'<div class="small-muted">These fields are optional, but recommended for public or collaborative use. They do not change the numerical calculation.</div>', unsafe_allow_html=True`

#### Item 255: line 8577 — `text_input` — Candidate source paper / arXiv / DOI

- **種類**: `text_input`
- **画面上の表示名**: Candidate source paper / arXiv / DOI
- **初期値または指定値**: `"User-entered / candidate parameter block"`
- **何をする項目か**: 短い文字列を入力する欄です。URL、ラベル、ソース名、メタデータなどに使われる場合があります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Candidate source paper / arXiv / DOI", value="User-entered / candidate parameter block"`

#### Item 256: line 8578 — `text_input` — Candidate source table / figure / line

- **種類**: `text_input`
- **画面上の表示名**: Candidate source table / figure / line
- **初期値または指定値**: `"manual entry"`
- **何をする項目か**: 短い文字列を入力する欄です。URL、ラベル、ソース名、メタデータなどに使われる場合があります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Candidate source table / figure / line", value="manual entry"`

#### Item 257: line 8580 — `text_input` — Reference source paper / arXiv / DOI

- **種類**: `text_input`
- **画面上の表示名**: Reference source paper / arXiv / DOI
- **初期値または指定値**: `"Reference / LCDM comparison block"`
- **何をする項目か**: 短い文字列を入力する欄です。URL、ラベル、ソース名、メタデータなどに使われる場合があります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Reference source paper / arXiv / DOI", value="Reference / LCDM comparison block"`

#### Item 258: line 8581 — `text_input` — Reference source table / figure / line

- **種類**: `text_input`
- **画面上の表示名**: Reference source table / figure / line
- **初期値または指定値**: `"manual entry"`
- **何をする項目か**: 短い文字列を入力する欄です。URL、ラベル、ソース名、メタデータなどに使われる場合があります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Reference source table / figure / line", value="manual entry"`

#### Item 259: line 8582 — `text_area` — Candidate source note

- **種類**: `text_area`
- **画面上の表示名**: Candidate source note
- **初期値または指定値**: `"Record extraction note`
- **何をする項目か**: 長い文字列を入力または表示する欄です。JSON、メモ、説明、raw response などに使われます。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Candidate source note", value="Record extraction note, table number, or assumptions.", height=80`

#### Item 260: line 8583 — `text_area` — Reference source note

- **種類**: `text_area`
- **画面上の表示名**: Reference source note
- **初期値または指定値**: `"Record reference extraction note`
- **何をする項目か**: 長い文字列を入力または表示する欄です。JSON、メモ、説明、raw response などに使われます。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Reference source note", value="Record reference extraction note, table number, or assumptions.", height=80`


### Section: 3. Literature text audit

#### Item 261: line 8594 — `header` — 3. Literature text audit

- **種類**: `header`
- **画面上の表示名**: 3. Literature text audit
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"3. Literature text audit"`


### Section: TARGET_MODEL vs LCDM comparison

#### Item 262: line 8598 — `subheader` — TARGET_MODEL vs LCDM comparison

- **種類**: `subheader`
- **画面上の表示名**: TARGET_MODEL vs LCDM comparison
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"TARGET_MODEL vs LCDM comparison"`

#### Item 263: line 8600 — `warning` — TARGET_MODEL and LCDM comparison values are incomplete.

- **種類**: `warning`
- **画面上の表示名**: TARGET_MODEL and LCDM comparison values are incomplete.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"TARGET_MODEL and LCDM comparison values are incomplete."`

#### Item 264: line 8604 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`


### Section: 4. High-precision parameter search engine

#### Item 265: line 8605 — `header` — 4. High-precision parameter search engine

- **種類**: `header`
- **画面上の表示名**: 4. High-precision parameter search engine
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"4. High-precision parameter search engine"`

#### Item 266: line 8622 — `warning` — Not enough parameters are available for search.

- **種類**: `warning`
- **画面上の表示名**: Not enough parameters are available for search.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Not enough parameters are available for search."`

#### Item 267: line 8627 — `metric` — Nearest reference model

- **種類**: `metric`
- **画面上の表示名**: Nearest reference model
- **何をする項目か**: 単一または少数の数値を強調表示する欄です。診断値や要約値を読むために使います。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `"Nearest reference model", top["reference_model"]`

#### Item 268: line 8629 — `metric` — Similarity score

- **種類**: `metric`
- **画面上の表示名**: Similarity score
- **何をする項目か**: 単一または少数の数値を強調表示する欄です。診断値や要約値を読むために使います。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `"Similarity score", f"{top['rank_score']:.2f}"`

#### Item 269: line 8631 — `caption` — difference_notes

- **種類**: `caption`
- **画面上の表示名**: difference_notes
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `top["difference_notes"]`


### Section: Current input model safety/readout cards

#### Item 270: line 8634 — `subheader` — Current input model safety/readout cards

- **種類**: `subheader`
- **画面上の表示名**: Current input model safety/readout cards
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Current input model safety/readout cards"`

#### Item 271: line 8643 — `markdown` — (dynamic or variable-derived label)

- **種類**: `markdown`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `card(p, value, note, color), unsafe_allow_html=True`

#### Item 272: line 8651 — `markdown` — (dynamic or variable-derived label)

- **種類**: `markdown`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `card(p, value, note, color), unsafe_allow_html=True`

#### Item 273: line 8653 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`


### Section: 5. AxiCLASS FIX1 locked benchmark

#### Item 274: line 8692 — `header` — 5. AxiCLASS FIX1 locked benchmark

- **種類**: `header`
- **画面上の表示名**: 5. AxiCLASS FIX1 locked benchmark
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"5. AxiCLASS FIX1 locked benchmark"`

#### Item 275: line 8722 — `warning` — AxiCLASS FIX1 results TSV was not found. Check app/data/axiclass_fix1_results.tsv.

- **種類**: `warning`
- **画面上の表示名**: AxiCLASS FIX1 results TSV was not found. Check app/data/axiclass_fix1_results.tsv.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"AxiCLASS FIX1 results TSV was not found. Check app/data/axiclass_fix1_results.tsv."`

#### Item 276: line 8726 — `success` — FIX1 checkpoint status: {ok_count}/{total_count} models OK

- **種類**: `success`
- **画面上の表示名**: FIX1 checkpoint status: {ok_count}/{total_count} models OK
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"FIX1 checkpoint status: {ok_count}/{total_count} models OK"`

#### Item 277: line 8728 — `tabs` — FUJIKI DTI

- **種類**: `tabs`
- **画面上の表示名**: FUJIKI DTI
- **何をする項目か**: 表示内容を切り替えるタブです。タブ切替そのものは新しい推論や計算を意味しません。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `["FUJIKI DTI", "Ivanov EDE", "Ivanov LCDM", "Full table", "Delta table"]`

#### Item 278: line 8740 — `warning` — {key} not found.

- **種類**: `warning`
- **画面上の表示名**: {key} not found.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"{key} not found."`

#### Item 279: line 8746 — `markdown` — H0

- **種類**: `markdown`
- **画面上の表示名**: H0
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `card("H0", f"{float(r.get('H0')):.2f}", "FIX1 locked value", status_color), unsafe_allow_html=True`

#### Item 280: line 8748 — `markdown` — rs_rec [Mpc]

- **種類**: `markdown`
- **画面上の表示名**: rs_rec [Mpc]
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `card("rs_rec [Mpc]", f"{float(r.get('rs_rec_Mpc_AxiCLASS')):.4f}", "AxiCLASS propagated value", "green"), unsafe_allow_html=True`

#### Item 281: line 8752 — `markdown` — sigma8

- **種類**: `markdown`
- **画面上の表示名**: sigma8
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `card("sigma8", f"{sig:.6f}", "AxiCLASS propagated value", sig_color), unsafe_allow_html=True`

#### Item 282: line 8756 — `markdown` — S8

- **種類**: `markdown`
- **画面上の表示名**: S8
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `card("S8", f"{s8:.6f}", "AxiCLASS propagated value", s8_color), unsafe_allow_html=True`

#### Item 283: line 8757 — `caption` — source_note

- **種類**: `caption`
- **画面上の表示名**: source_note
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `str(r.get("source_note", ""))`

#### Item 284: line 8764 — `warning` — AxiCLASS FIX1 delta TSV was not found.

- **種類**: `warning`
- **画面上の表示名**: AxiCLASS FIX1 delta TSV was not found.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"AxiCLASS FIX1 delta TSV was not found."`

#### Item 285: line 8768 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`


### Section: 6. RK45 background-universe proxy

#### Item 286: line 8769 — `header` — 6. RK45 background-universe proxy

- **種類**: `header`
- **画面上の表示名**: 6. RK45 background-universe proxy
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"6. RK45 background-universe proxy"`

#### Item 287: line 8774 — `button` — Run RK45 background proxy for current input model

- **種類**: `button`
- **画面上の表示名**: Run RK45 background proxy for current input model
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Run RK45 background proxy for current input model", width="stretch", type="primary"`

#### Item 288: line 8782 — `error` — h/H0, omega_b, and omega_cdm are required.

- **種類**: `error`
- **画面上の表示名**: h/H0, omega_b, and omega_cdm are required.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"h/H0, omega_b, and omega_cdm are required."`

#### Item 289: line 8787 — `metric` — z_rec proxy

- **種類**: `metric`
- **画面上の表示名**: z_rec proxy
- **何をする項目か**: 単一または少数の数値を強調表示する欄です。診断値や要約値を読むために使います。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `"z_rec proxy", f"{proxy['z_rec_proxy']:.4f}"`

#### Item 290: line 8789 — `metric` — rs_rec proxy

- **種類**: `metric`
- **画面上の表示名**: rs_rec proxy
- **何をする項目か**: 単一または少数の数値を強調表示する欄です。診断値や要約値を読むために使います。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `"rs_rec proxy", f"{proxy['rs_rec_proxy']:.4f} Mpc"`

#### Item 291: line 8791 — `error` — RK45 proxy failed: {e}

- **種類**: `error`
- **画面上の表示名**: RK45 proxy failed: {e}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"RK45 proxy failed: {e}"`

#### Item 292: line 8793 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`


### Section: 7. Local experimental probes

#### Item 293: line 8795 — `header` — 7. Local experimental probes

- **種類**: `header`
- **画面上の表示名**: 7. Local experimental probes
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"7. Local experimental probes"`


### Section: 7 preflight. Public API warm-up

#### Item 294: line 8811 — `subheader` — 7 preflight. Public API warm-up

- **種類**: `subheader`
- **画面上の表示名**: 7 preflight. Public API warm-up
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"7 preflight. Public API warm-up"`

#### Item 295: line 8820 — `expander` — Warm up configured API endpoints before 7a/7b

- **種類**: `expander`
- **画面上の表示名**: Warm up configured API endpoints before 7a/7b
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Warm up configured API endpoints before 7a/7b", expanded=False`

#### Item 296: line 8830 — `button` — Warm up public API

- **種類**: `button`
- **画面上の表示名**: Warm up public API
- **内部キー**: `dti_warmup_public_api_7a7b_v2`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Warm up public API", key="dti_warmup_public_api_7a7b_v2", width="stretch"`


### Section: 7a. AxiCLASS fixed-example check

#### Item 297: line 8858 — `header` — 7a. AxiCLASS fixed-example check

- **種類**: `header`
- **画面上の表示名**: 7a. AxiCLASS fixed-example check
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"7a. AxiCLASS fixed-example check"`

#### Item 298: line 8885 — `info` — Disabled by default. Enable only for bounded implementation testing.

- **種類**: `info`
- **画面上の表示名**: Disabled by default. Enable only for bounded implementation testing.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Disabled by default. Enable only for bounded implementation testing."`

#### Item 299: line 8911 — `expander` — How to use the AxiCLASS API endpoint

- **種類**: `expander`
- **画面上の表示名**: How to use the AxiCLASS API endpoint
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"How to use the AxiCLASS API endpoint", expanded=False`

#### Item 300: line 8927 — `button` — Run fixed-example check

- **種類**: `button`
- **画面上の表示名**: Run fixed-example check
- **内部キー**: `run_local_axiclass_fixed_example_v606`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Run fixed-example check", key="run_local_axiclass_fixed_example_v606", width="stretch", type="primary"`

#### Item 301: line 8968 — `markdown` — ##### Local fixed-example result

- **種類**: `markdown`
- **画面上の表示名**: ##### Local fixed-example result
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Local fixed-example result"`

#### Item 302: line 8969 — `caption` — HTTP status: {http_status}

- **種類**: `caption`
- **画面上の表示名**: HTTP status: {http_status}
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"HTTP status: {http_status}"`

#### Item 303: line 8972 — `success` — Local fixed-example endpoint returned status: ok

- **種類**: `success`
- **画面上の表示名**: Local fixed-example endpoint returned status: ok
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Local fixed-example endpoint returned status: ok"`

#### Item 304: line 8974 — `warning` — Local fixed-example endpoint did not return ok. Check that the local API is running.

- **種類**: `warning`
- **画面上の表示名**: Local fixed-example endpoint did not return ok. Check that the local API is running.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Local fixed-example endpoint did not return ok. Check that the local API is running."`

#### Item 305: line 8985 — `markdown` — ##### Derived values

- **種類**: `markdown`
- **画面上の表示名**: ##### Derived values
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Derived values"`

#### Item 306: line 9001 — `markdown` — ##### Selected scalar-field / axion background summary

- **種類**: `markdown`
- **画面上の表示名**: ##### Selected scalar-field / axion background summary
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Selected scalar-field / axion background summary"`

#### Item 307: line 9008 — `markdown` — ##### Boundary flags

- **種類**: `markdown`
- **画面上の表示名**: ##### Boundary flags
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Boundary flags"`

#### Item 308: line 9011 — `expander` — Raw fixed-example API response

- **種類**: `expander`
- **画面上の表示名**: Raw fixed-example API response
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw fixed-example API response", expanded=False`


### Section: 7b. Vanilla-profile API check

#### Item 309: line 9020 — `header` — 7b. Vanilla-profile API check

- **種類**: `header`
- **画面上の表示名**: 7b. Vanilla-profile API check
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"7b. Vanilla-profile API check"`

#### Item 310: line 9186 — `markdown` — ##### Current sidebar profile compatibility readout

- **種類**: `markdown`
- **画面上の表示名**: ##### Current sidebar profile compatibility readout
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Current sidebar profile compatibility readout"`

#### Item 311: line 9301 — `warning` — Enable the vanilla-profile API check before running.

- **種類**: `warning`
- **画面上の表示名**: Enable the vanilla-profile API check before running.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Enable the vanilla-profile API check before running."`

#### Item 312: line 9330 — `markdown` — ##### Vanilla-profile API check result

- **種類**: `markdown`
- **画面上の表示名**: ##### Vanilla-profile API check result
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Vanilla-profile API check result"`

#### Item 313: line 9340 — `success` — Local vanilla CLASS live probe returned status: ok

- **種類**: `success`
- **画面上の表示名**: Local vanilla CLASS live probe returned status: ok
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Local vanilla CLASS live probe returned status: ok"`

#### Item 314: line 9357 — `table` — (dynamic or variable-derived label)

- **種類**: `table`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 固定的な表表示です。整理済みの値や比較表を読むために使います。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `rows`

#### Item 315: line 9385 — `warning` — Local vanilla CLASS live probe did not return ok. Check that the 8011 API is running.

- **種類**: `warning`
- **画面上の表示名**: Local vanilla CLASS live probe did not return ok. Check that the 8011 API is running.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Local vanilla CLASS live probe did not return ok. Check that the 8011 API is running."`

#### Item 316: line 9641 — `markdown` — <a id=

- **種類**: `markdown`
- **画面上の表示名**: <a id=
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"<a id='{marker}'></a>", unsafe_allow_html=True`

#### Item 317: line 9644 — `markdown` — ##### Audit visualization: numerical smoothness profile

- **種類**: `markdown`
- **画面上の表示名**: ##### Audit visualization: numerical smoothness profile
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Audit visualization: numerical smoothness profile"`

#### Item 318: line 9651 — `info` — Graph libraries unavailable: {exc}

- **種類**: `info`
- **画面上の表示名**: Graph libraries unavailable: {exc}
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Graph libraries unavailable: {exc}"`

#### Item 319: line 9660 — `info` — No compatible sweep table is currently available in session memory. No graph is drawn until source-of-record data are present.

- **種類**: `info`
- **画面上の表示名**: No compatible sweep table is currently available in session memory. No graph is drawn until source-of-record data are present.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No compatible sweep table is currently available in session memory. No graph is drawn until source-of-record data are present."`

#### Item 320: line 9702 — `info` — Not enough numeric rows to draw adjacent-difference profile.

- **種類**: `info`
- **画面上の表示名**: Not enough numeric rows to draw adjacent-difference profile.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Not enough numeric rows to draw adjacent-difference profile."`

#### Item 321: line 9730 — `markdown` — <a id=

- **種類**: `markdown`
- **画面上の表示名**: <a id=
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"<a id='dti_graph_ui_v607_section8'></a>", unsafe_allow_html=True`

#### Item 322: line 9733 — `markdown` — ##### Audit visualization: heuristic reference-region profile

- **種類**: `markdown`
- **画面上の表示名**: ##### Audit visualization: heuristic reference-region profile
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Audit visualization: heuristic reference-region profile"`

#### Item 323: line 9740 — `info` — Graph libraries unavailable: {exc}

- **種類**: `info`
- **画面上の表示名**: Graph libraries unavailable: {exc}
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Graph libraries unavailable: {exc}"`

#### Item 324: line 9746 — `markdown` — ##### Reference-distance overview

- **種類**: `markdown`
- **画面上の表示名**: ##### Reference-distance overview
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Reference-distance overview"`

#### Item 325: line 9801 — `markdown` — ##### S8 response / stress view

- **種類**: `markdown`
- **画面上の表示名**: ##### S8 response / stress view
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### S8 response / stress view"`

#### Item 326: line 9837 — `info` — S8 table found, but fewer than two numeric rows are available for plotting.

- **種類**: `info`
- **画面上の表示名**: S8 table found, but fewer than two numeric rows are available for plotting.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"S8 table found, but fewer than two numeric rows are available for plotting."`

#### Item 327: line 9839 — `info` — S8 table found, but no recognized sweep axis was found.

- **種類**: `info`
- **画面上の表示名**: S8 table found, but no recognized sweep axis was found.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"S8 table found, but no recognized sweep axis was found."`

#### Item 328: line 9841 — `info` — No compatible S8 response table found in session memory. No graph is drawn until source-of-record data are present.

- **種類**: `info`
- **画面上の表示名**: No compatible S8 response table found in session memory. No graph is drawn until source-of-record data are present.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"No compatible S8 response table found in session memory. No graph is drawn until source-of-record data are present."`

#### Item 329: line 9848 — `markdown` — ##### Boundary confirmation view

- **種類**: `markdown`
- **画面上の表示名**: ##### Boundary confirmation view
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Boundary confirmation view"`

#### Item 330: line 9892 — `info` — rs_drag/S8 table found, but no numeric rows are available.

- **種類**: `info`
- **画面上の表示名**: rs_drag/S8 table found, but no numeric rows are available.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"rs_drag/S8 table found, but no numeric rows are available."`

#### Item 331: line 9901 — `markdown` — <a id=

- **種類**: `markdown`
- **画面上の表示名**: <a id=
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"<a id='dti_graph_ui_v607_section9'></a>", unsafe_allow_html=True`

#### Item 332: line 9904 — `markdown` — ##### Audit visualization: external API sandbox flow

- **種類**: `markdown`
- **画面上の表示名**: ##### Audit visualization: external API sandbox flow
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Audit visualization: external API sandbox flow"`


### Section: 7c. Continuity / discontinuity examiner

#### Item 333: line 9925 — `header` — 7c. Continuity / discontinuity examiner

- **種類**: `header`
- **画面上の表示名**: 7c. Continuity / discontinuity examiner
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"7c. Continuity / discontinuity examiner"`

#### Item 334: line 9968 — `markdown` — ##### Base profile

- **種類**: `markdown`
- **画面上の表示名**: ##### Base profile
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Base profile"`

#### Item 335: line 10042 — `markdown` — ##### Sweep design

- **種類**: `markdown`
- **画面上の表示名**: ##### Sweep design
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Sweep design"`

#### Item 336: line 10229 — `warning` — Enable the local-only continuity / discontinuity examiner before running.

- **種類**: `warning`
- **画面上の表示名**: Enable the local-only continuity / discontinuity examiner before running.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Enable the local-only continuity / discontinuity examiner before running."`

#### Item 337: line 10325 — `markdown` — ##### Examiner grid output

- **種類**: `markdown`
- **画面上の表示名**: ##### Examiner grid output
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Examiner grid output"`

#### Item 338: line 10340 — `markdown` — ##### Continuity / discontinuity score table

- **種類**: `markdown`
- **画面上の表示名**: ##### Continuity / discontinuity score table
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Continuity / discontinuity score table"`

#### Item 339: line 10353 — `warning` — Overall bounded verdict: solver_failure_or_partial_grid

- **種類**: `warning`
- **画面上の表示名**: Overall bounded verdict: solver_failure_or_partial_grid
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Overall bounded verdict: solver_failure_or_partial_grid"`

#### Item 340: line 10356 — `warning` — Overall bounded verdict: jump_candidate

- **種類**: `warning`
- **画面上の表示名**: Overall bounded verdict: jump_candidate
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Overall bounded verdict: jump_candidate"`

#### Item 341: line 10359 — `success` — Overall bounded verdict: continuous_response_within_tested_grid_after_micro_jitter_guard

- **種類**: `success`
- **画面上の表示名**: Overall bounded verdict: continuous_response_within_tested_grid_after_micro_jitter_guard
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Overall bounded verdict: continuous_response_within_tested_grid_after_micro_jitter_guard"`

#### Item 342: line 10362 — `success` — Overall bounded verdict: continuous_response_within_tested_grid

- **種類**: `success`
- **画面上の表示名**: Overall bounded verdict: continuous_response_within_tested_grid
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Overall bounded verdict: continuous_response_within_tested_grid"`

#### Item 343: line 10394 — `markdown` — ##### Examiner verdict record

- **種類**: `markdown`
- **画面上の表示名**: ##### Examiner verdict record
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Examiner verdict record"`

#### Item 344: line 10458 — `error` — Continuity / discontinuity examiner failed: {exc}

- **種類**: `error`
- **画面上の表示名**: Continuity / discontinuity examiner failed: {exc}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Continuity / discontinuity examiner failed: {exc}"`


### Section: 8. Candidate payload / boundary confirmation

#### Item 345: line 10461 — `header` — 8. Candidate payload / boundary confirmation

- **種類**: `header`
- **画面上の表示名**: 8. Candidate payload / boundary confirmation
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"8. Candidate payload / boundary confirmation"`

#### Item 346: line 10483 — `info` — Section 8 graph fallback unavailable: {_graph_v3_exc}

- **種類**: `info`
- **画面上の表示名**: Section 8 graph fallback unavailable: {_graph_v3_exc}
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Section 8 graph fallback unavailable: {_graph_v3_exc}"`

#### Item 347: line 10488 — `caption` — Section 8 audit visualization unavailable: {_dti_graph_exc_8_v607}

- **種類**: `caption`
- **画面上の表示名**: Section 8 audit visualization unavailable: {_dti_graph_exc_8_v607}
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Section 8 audit visualization unavailable: {_dti_graph_exc_8_v607}"`

#### Item 348: line 10590 — `markdown` — ##### Registered fit-region references

- **種類**: `markdown`
- **画面上の表示名**: ##### Registered fit-region references
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Registered fit-region references"`

#### Item 349: line 10594 — `markdown` — ##### Current input profile position

- **種類**: `markdown`
- **画面上の表示名**: ##### Current input profile position
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Current input profile position"`


### Section: 9. External CLASS API sandbox

#### Item 350: line 10670 — `header` — 9. External CLASS API sandbox

- **種類**: `header`
- **画面上の表示名**: 9. External CLASS API sandbox
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"9. External CLASS API sandbox"`

#### Item 351: line 10674 — `caption` — Section 9 audit visualization unavailable: {_dti_graph_exc_9_v607}

- **種類**: `caption`
- **画面上の表示名**: Section 9 audit visualization unavailable: {_dti_graph_exc_9_v607}
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Section 9 audit visualization unavailable: {_dti_graph_exc_9_v607}"`

#### Item 352: line 10695 — `markdown` — ##### Payload sent to external API

- **種類**: `markdown`
- **画面上の表示名**: ##### Payload sent to external API
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Payload sent to external API"`

#### Item 353: line 10698 — `button` — Run external CLASS API for current input model

- **種類**: `button`
- **画面上の表示名**: Run external CLASS API for current input model
- **内部キー**: `run_external_class_api_v606`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Run external CLASS API for current input model", key="run_external_class_api_v606", width="stretch", type="primary"`

#### Item 354: line 10722 — `markdown` — ##### External CLASS API result

- **種類**: `markdown`
- **画面上の表示名**: ##### External CLASS API result
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### External CLASS API result"`

#### Item 355: line 10723 — `caption` — HTTP status: {external_api_http_status}

- **種類**: `caption`
- **画面上の表示名**: HTTP status: {external_api_http_status}
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"HTTP status: {external_api_http_status}"`

#### Item 356: line 10727 — `success` — External CLASS API returned status: ok

- **種類**: `success`
- **画面上の表示名**: External CLASS API returned status: ok
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"External CLASS API returned status: ok"`

#### Item 357: line 10729 — `warning` — External CLASS API is available, but classy/PyCLASS is unavailable on the backend.

- **種類**: `warning`
- **画面上の表示名**: External CLASS API is available, but classy/PyCLASS is unavailable on the backend.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"External CLASS API is available, but classy/PyCLASS is unavailable on the backend."`

#### Item 358: line 10731 — `warning` — External CLASS API returned status: {status_value}

- **種類**: `warning`
- **画面上の表示名**: External CLASS API returned status: {status_value}
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"External CLASS API returned status: {status_value}"`

#### Item 359: line 10750 — `expander` — Raw external API response

- **種類**: `expander`
- **画面上の表示名**: Raw external API response
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw external API response", expanded=False`

#### Item 360: line 10751 — `caption` — Large arrays are summarized here to keep the UI readable. The CMB graph still uses the full real API arrays.

- **種類**: `caption`
- **画面上の表示名**: Large arrays are summarized here to keep the UI readable. The CMB graph still uses the full real API arrays.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Large arrays are summarized here to keep the UI readable. The CMB graph still uses the full real API arrays."`

#### Item 361: line 10755 — `expander` — CMB spectra graph — real API arrays only

- **種類**: `expander`
- **画面上の表示名**: CMB spectra graph — real API arrays only
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"CMB spectra graph — real API arrays only", expanded=True`


### Section: 10. Interpretation boundary

#### Item 362: line 10760 — `header` — 10. Interpretation boundary

- **種類**: `header`
- **画面上の表示名**: 10. Interpretation boundary
- **何をする項目か**: 大きな説明ブロックの見出しです。ここから下に関連する操作項目や結果表示がまとまります。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"10. Interpretation boundary"`

#### Item 363: line 10826 — `markdown` — ##### Boundary confirmation

- **種類**: `markdown`
- **画面上の表示名**: ##### Boundary confirmation
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Boundary confirmation"`

#### Item 364: line 10842 — `success` — (dynamic or variable-derived label)

- **種類**: `success`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `label`

#### Item 365: line 10844 — `warning` — {label} — not confirmed in response

- **種類**: `warning`
- **画面上の表示名**: {label} — not confirmed in response
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"{label} — not confirmed in response"`

#### Item 366: line 10870 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`

#### Item 367: line 10871 — `expander` — Jump parameter translator — backend boundary check

- **種類**: `expander`
- **画面上の表示名**: Jump parameter translator — backend boundary check
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Jump parameter translator — backend boundary check", expanded=False`

#### Item 368: line 10881 — `number_input` — H0

- **種類**: `number_input`
- **画面上の表示名**: H0
- **内部キー**: `dti_jump_tr_h0_v1`
- **初期値または指定値**: `1.0`
- **最小値**: `1.0`
- **最大値**: `150.0`
- **刻み幅**: `0.1`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"H0", min_value=1.0, max_value=150.0, value=72.6, step=0.1, key="dti_jump_tr_h0_v1"`

#### Item 369: line 10882 — `number_input` — omega_b

- **種類**: `number_input`
- **画面上の表示名**: omega_b
- **内部キー**: `dti_jump_tr_omega_b_v1`
- **初期値または指定値**: `0.0001`
- **最小値**: `0.0001`
- **最大値**: `0.2`
- **刻み幅**: `0.00001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"omega_b", min_value=0.0001, max_value=0.2, value=0.02237, step=0.00001, format="%.5f", key="dti_jump_tr_omega_b_v1"`

#### Item 370: line 10883 — `number_input` — omega_cdm

- **種類**: `number_input`
- **画面上の表示名**: omega_cdm
- **内部キー**: `dti_jump_tr_omega_cdm_v1`
- **初期値または指定値**: `0.0001`
- **最小値**: `0.0001`
- **最大値**: `1.0`
- **刻み幅**: `0.0001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"omega_cdm", min_value=0.0001, max_value=1.0, value=0.1200, step=0.0001, format="%.4f", key="dti_jump_tr_omega_cdm_v1"`

#### Item 371: line 10885 — `number_input` — ln10_10_As

- **種類**: `number_input`
- **画面上の表示名**: ln10_10_As
- **内部キー**: `dti_jump_tr_ln10as_v1`
- **初期値または指定値**: `0.1`
- **最小値**: `0.1`
- **最大値**: `10.0`
- **刻み幅**: `0.001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"ln10_10_As", min_value=0.1, max_value=10.0, value=3.044, step=0.001, format="%.3f", key="dti_jump_tr_ln10as_v1"`

#### Item 372: line 10886 — `number_input` — n_s

- **種類**: `number_input`
- **画面上の表示名**: n_s
- **内部キー**: `dti_jump_tr_ns_v1`
- **初期値または指定値**: `0.1`
- **最小値**: `0.1`
- **最大値**: `2.0`
- **刻み幅**: `0.001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"n_s", min_value=0.1, max_value=2.0, value=0.965, step=0.001, format="%.3f", key="dti_jump_tr_ns_v1"`

#### Item 373: line 10887 — `number_input` — tau_reio

- **種類**: `number_input`
- **画面上の表示名**: tau_reio
- **内部キー**: `dti_jump_tr_tau_v1`
- **初期値または指定値**: `0.0`
- **最小値**: `0.0`
- **最大値**: `1.0`
- **刻み幅**: `0.001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"tau_reio", min_value=0.0, max_value=1.0, value=0.054, step=0.001, format="%.3f", key="dti_jump_tr_tau_v1"`

#### Item 374: line 10889 — `number_input` — A_J

- **種類**: `number_input`
- **画面上の表示名**: A_J
- **内部キー**: `dti_jump_tr_aj_v1`
- **初期値または指定値**: `-1.0`
- **最小値**: `-1.0`
- **最大値**: `1.0`
- **刻み幅**: `0.00001`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"A_J", min_value=-1.0, max_value=1.0, value=-0.00022, step=0.00001, format="%.5f", key="dti_jump_tr_aj_v1"`

#### Item 375: line 10890 — `number_input` — z_J

- **種類**: `number_input`
- **画面上の表示名**: z_J
- **内部キー**: `dti_jump_tr_zj_v1`
- **初期値または指定値**: `0.0001`
- **最小値**: `0.0001`
- **最大値**: `5000.0`
- **刻み幅**: `1.0`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"z_J", min_value=0.0001, max_value=5000.0, value=1100.0, step=1.0, key="dti_jump_tr_zj_v1"`

#### Item 376: line 10891 — `number_input` — Delta_z

- **種類**: `number_input`
- **画面上の表示名**: Delta_z
- **内部キー**: `dti_jump_tr_dz_v1`
- **初期値または指定値**: `0.0001`
- **最小値**: `0.0001`
- **最大値**: `2000.0`
- **刻み幅**: `1.0`
- **何をする項目か**: 数値を入力する欄です。値を変えると対応する診断表示や簡易計算の結果が変わります。
- **使い方**: 数値を直接入力するか、UIの増減操作で値を変えます。値を変えた後は、関連する表示、表、グラフ、診断結果を確認します。
- **注意**: この入力欄は診断や表示のための値です。この欄を変えただけで、物理モデルの正しさや likelihood の優劣が確定するわけではありません。
- **ソース上の式**: `"Delta_z", min_value=0.0001, max_value=2000.0, value=30.0, step=1.0, key="dti_jump_tr_dz_v1"`

#### Item 377: line 10918 — `caption` — Fixed request fields: backend_mode=jump_parameter_translation_only, jump_target=E_z, transition_form=smoothed_tanh_step, request_claim_level=translation_only.

- **種類**: `caption`
- **画面上の表示名**: Fixed request fields: backend_mode=jump_parameter_translation_only, jump_target=E_z, transition_form=smoothed_tanh_step, request_claim_level=translation_only.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Fixed request fields: backend_mode=jump_parameter_translation_only, jump_target=E_z, transition_form=smoothed_tanh_step, request_claim_level=translation_only."`

#### Item 378: line 10920 — `expander` — Request payload preview

- **種類**: `expander`
- **画面上の表示名**: Request payload preview
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Request payload preview", expanded=False`

#### Item 379: line 10923 — `button` — Run translator boundary check

- **種類**: `button`
- **画面上の表示名**: Run translator boundary check
- **内部キー**: `dti_jump_translator_run_v1`
- **何をする項目か**: ユーザーが押して処理を起動するボタンです。プリセット読み込み、表示更新、診断実行などに使われます。
- **使い方**: 必要な条件を確認してから押します。押すとプリセット読み込み、表示更新、または診断処理が走る場合があります。
- **注意**: ボタンを押して表示が変わっても、それは通常アプリ上の操作結果です。論文上の新しい主張や posterior 計算を意味しません。
- **ソース上の式**: `"Run translator boundary check", key="dti_jump_translator_run_v1"`

#### Item 380: line 10928 — `error` — Translator request failed: {exc!r}

- **種類**: `error`
- **画面上の表示名**: Translator request failed: {exc!r}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Translator request failed: {exc!r}"`

#### Item 381: line 10935 — `success` — Translator response accepted. Boundary-only response received.

- **種類**: `success`
- **画面上の表示名**: Translator response accepted. Boundary-only response received.
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Translator response accepted. Boundary-only response received."`

#### Item 382: line 10937 — `warning` — Translator response was not accepted or returned a non-OK HTTP status.

- **種類**: `warning`
- **画面上の表示名**: Translator response was not accepted or returned a non-OK HTTP status.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Translator response was not accepted or returned a non-OK HTTP status."`

#### Item 383: line 10943 — `error` — Errors

- **種類**: `error`
- **画面上の表示名**: Errors
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Errors"`

#### Item 384: line 10946 — `warning` — Warnings

- **種類**: `warning`
- **画面上の表示名**: Warnings
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Warnings"`

#### Item 385: line 10949 — `markdown` — ##### Normalized values

- **種類**: `markdown`
- **画面上の表示名**: ##### Normalized values
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Normalized values"`

#### Item 386: line 10952 — `markdown` — ##### Formula

- **種類**: `markdown`
- **画面上の表示名**: ##### Formula
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Formula"`

#### Item 387: line 10955 — `markdown` — ##### Implementation status

- **種類**: `markdown`
- **画面上の表示名**: ##### Implementation status
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"##### Implementation status"`

#### Item 388: line 10960 — `expander` — Full translator response

- **種類**: `expander`
- **画面上の表示名**: Full translator response
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Full translator response", expanded=False`

#### Item 389: line 10992 — `markdown` — ### DTI backend capability status

- **種類**: `markdown`
- **画面上の表示名**: ### DTI backend capability status
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### DTI backend capability status"`

#### Item 390: line 11016 — `warning` — DTI capability endpoint is not available in this session.

- **種類**: `warning`
- **画面上の表示名**: DTI capability endpoint is not available in this session.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"DTI capability endpoint is not available in this session."`

#### Item 391: line 11018 — `caption` — (dynamic or variable-derived label)

- **種類**: `caption`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `error_text`

#### Item 392: line 11053 — `expander` — DTI capability provenance and no-claim boundary

- **種類**: `expander`
- **画面上の表示名**: DTI capability provenance and no-claim boundary
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"DTI capability provenance and no-claim boundary", expanded=False`

#### Item 393: line 11080 — `warning` — DTI capability status panel could not be rendered.

- **種類**: `warning`
- **画面上の表示名**: DTI capability status panel could not be rendered.
- **何をする項目か**: 注意メッセージです。この表示がある場合は、その項目を強い主張として読まないでください。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"DTI capability status panel could not be rendered."`

#### Item 394: line 11081 — `caption` — (dynamic or variable-derived label)

- **種類**: `caption`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `str(_dti_status_panel_exc)`

#### Item 395: line 11085 — `expander` — Paper / APJ conversion status

- **種類**: `expander`
- **画面上の表示名**: Paper / APJ conversion status
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Paper / APJ conversion status", expanded=False`


### Section: Observed-data posterior

#### Item 396: line 11124 — `subheader` — Observed-data posterior

- **種類**: `subheader`
- **画面上の表示名**: Observed-data posterior
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Observed-data posterior"`

#### Item 397: line 11153 — `expander` — Boundary / audit status

- **種類**: `expander`
- **画面上の表示名**: Boundary / audit status
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Boundary / audit status", expanded=True`

#### Item 398: line 11209 — `expander` — Embedded posterior viewer — offline BAO chain, audit-only

- **種類**: `expander`
- **画面上の表示名**: Embedded posterior viewer — offline BAO chain, audit-only
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Embedded posterior viewer — offline BAO chain, audit-only", expanded=True`

#### Item 399: line 11229 — `info` — Embedded posterior package is not loaded here; frozen BAO graph/table sections remain audit-only where available.

- **種類**: `info`
- **画面上の表示名**: Embedded posterior package is not loaded here; frozen BAO graph/table sections remain audit-only where available.
- **何をする項目か**: 補足情報です。操作前後の状態や使い方のヒントを示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Embedded posterior package is not loaded here; frozen BAO graph/table sections remain audit-only where available."`

#### Item 400: line 11231 — `caption` — Local package path details hidden for UI safety.

- **種類**: `caption`
- **画面上の表示名**: Local package path details hidden for UI safety.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Local package path details hidden for UI safety."`

#### Item 401: line 11237 — `error` — Could not read posterior payload JSON: {exc}

- **種類**: `error`
- **画面上の表示名**: Could not read posterior payload JSON: {exc}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Could not read posterior payload JSON: {exc}"`

#### Item 402: line 11240 — `caption` — Boundary: offline BAO chain only; public display does not imply physics validation.

- **種類**: `caption`
- **画面上の表示名**: Boundary: offline BAO chain only; public display does not imply physics validation.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Boundary: offline BAO chain only; public display does not imply physics validation."`

#### Item 403: line 11243 — `expander` — Raw embedded tables — provenance / audit readback

- **種類**: `expander`
- **画面上の表示名**: Raw embedded tables — provenance / audit readback
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Raw embedded tables — provenance / audit readback", expanded=False`


### Section: Chain summary

#### Item 404: line 11244 — `subheader` — Chain summary

- **種類**: `subheader`
- **画面上の表示名**: Chain summary
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Chain summary"`


### Section: G02 diagnostics — TSV

#### Item 405: line 11247 — `subheader` — G02 diagnostics — TSV

- **種類**: `subheader`
- **画面上の表示名**: G02 diagnostics — TSV
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"G02 diagnostics — TSV"`


### Section: MAP / best-fit table

#### Item 406: line 11250 — `subheader` — MAP / best-fit table

- **種類**: `subheader`
- **画面上の表示名**: MAP / best-fit table
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"MAP / best-fit table"`


### Section: Source identity

#### Item 407: line 11253 — `subheader` — Source identity

- **種類**: `subheader`
- **画面上の表示名**: Source identity
- **何をする項目か**: 小さめの見出しです。直前の大項目の中にある補助的な説明領域を示します。
- **使い方**: 周辺の見出しや説明文と合わせて読みます。
- **注意**: この項目だけで物理的結論を出さず、必ず境界説明と provenance を確認してください。
- **ソース上の式**: `"Source identity"`

#### Item 408: line 11254 — `caption` — Local absolute paths are redacted in the public UI. Full provenance remains in the frozen local artifact.

- **種類**: `caption`
- **画面上の表示名**: Local absolute paths are redacted in the public UI. Full provenance remains in the frozen local artifact.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Local absolute paths are redacted in the public UI. Full provenance remains in the frozen local artifact."`

#### Item 409: line 11270 — `expander` — Claim boundary

- **種類**: `expander`
- **画面上の表示名**: Claim boundary
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Claim boundary", expanded=False`

#### Item 410: line 11271 — `markdown` — utf-8

- **種類**: `markdown`
- **画面上の表示名**: utf-8
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `claim_boundary_path.read_text(encoding="utf-8")`

#### Item 411: line 11275 — `markdown` — #### Embedded graph viewer — frozen offline BAO chain, audit-only

- **種類**: `markdown`
- **画面上の表示名**: #### Embedded graph viewer — frozen offline BAO chain, audit-only
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"#### Embedded graph viewer — frozen offline BAO chain, audit-only"`

#### Item 412: line 11290 — `markdown` — ### Real-data TSV chart board — G01/G02/G03

- **種類**: `markdown`
- **画面上の表示名**: ### Real-data TSV chart board — G01/G02/G03
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Real-data TSV chart board — G01/G02/G03"`

#### Item 413: line 11378 — `markdown` — **TSV-derived chart — G01 chain summary**

- **種類**: `markdown`
- **画面上の表示名**: **TSV-derived chart — G01 chain summary**
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"**TSV-derived chart — G01 chain summary**"`

#### Item 414: line 11389 — `error` — G01 chart could not render because no numeric TSV columns were available after coercion.

- **種類**: `error`
- **画面上の表示名**: G01 chart could not render because no numeric TSV columns were available after coercion.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"G01 chart could not render because no numeric TSV columns were available after coercion."`

#### Item 415: line 11390 — `expander` — Source TSV table — G01

- **種類**: `expander`
- **画面上の表示名**: Source TSV table — G01
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Source TSV table — G01", expanded=False`

#### Item 416: line 11394 — `markdown` — **TSV-derived chart — G02 diagnostics**

- **種類**: `markdown`
- **画面上の表示名**: **TSV-derived chart — G02 diagnostics**
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"**TSV-derived chart — G02 diagnostics**"`

#### Item 417: line 11405 — `error` — G02 chart could not render because no numeric TSV columns were available after coercion.

- **種類**: `error`
- **画面上の表示名**: G02 chart could not render because no numeric TSV columns were available after coercion.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"G02 chart could not render because no numeric TSV columns were available after coercion."`

#### Item 418: line 11406 — `expander` — Source TSV table — G02

- **種類**: `expander`
- **画面上の表示名**: Source TSV table — G02
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Source TSV table — G02", expanded=False`

#### Item 419: line 11410 — `markdown` — **TSV-derived chart — G03 MAP / best-fit**

- **種類**: `markdown`
- **画面上の表示名**: **TSV-derived chart — G03 MAP / best-fit**
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"**TSV-derived chart — G03 MAP / best-fit**"`

#### Item 420: line 11421 — `error` — G03 chart could not render because no numeric TSV columns were available after coercion.

- **種類**: `error`
- **画面上の表示名**: G03 chart could not render because no numeric TSV columns were available after coercion.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"G03 chart could not render because no numeric TSV columns were available after coercion."`

#### Item 421: line 11422 — `expander` — Source TSV table — G03

- **種類**: `expander`
- **画面上の表示名**: Source TSV table — G03
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Source TSV table — G03", expanded=False`

#### Item 422: line 11426 — `error` — Real-data TSV chart board failed closed: {board_exc}

- **種類**: `error`
- **画面上の表示名**: Real-data TSV chart board failed closed: {board_exc}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Real-data TSV chart board failed closed: {board_exc}"`

#### Item 423: line 11437 — `error` — Missing frozen embedded file: chain_summary.tsv

- **種類**: `error`
- **画面上の表示名**: Missing frozen embedded file: chain_summary.tsv
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Missing frozen embedded file: chain_summary.tsv"`

#### Item 424: line 11440 — `caption` — G01 — source readback from frozen chain_summary.tsv.

- **種類**: `caption`
- **画面上の表示名**: G01 — source readback from frozen chain_summary.tsv.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"G01 — source readback from frozen chain_summary.tsv."`

#### Item 425: line 11445 — `error` — Missing frozen embedded file: diagnostics.tsv

- **種類**: `error`
- **画面上の表示名**: Missing frozen embedded file: diagnostics.tsv
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Missing frozen embedded file: diagnostics.tsv"`

#### Item 426: line 11448 — `caption` — G02 — source readback from frozen diagnostics.tsv.

- **種類**: `caption`
- **画面上の表示名**: G02 — source readback from frozen diagnostics.tsv.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"G02 — source readback from frozen diagnostics.tsv."`

#### Item 427: line 11453 — `error` — Missing frozen embedded file: map_or_bestfit.tsv

- **種類**: `error`
- **画面上の表示名**: Missing frozen embedded file: map_or_bestfit.tsv
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Missing frozen embedded file: map_or_bestfit.tsv"`

#### Item 428: line 11456 — `caption` — G03 — source readback from frozen map_or_bestfit.tsv.

- **種類**: `caption`
- **画面上の表示名**: G03 — source readback from frozen map_or_bestfit.tsv.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"G03 — source readback from frozen map_or_bestfit.tsv."`

#### Item 429: line 11481 — `error` — Frozen real-data graph viewer failed closed: {exc}

- **種類**: `error`
- **画面上の表示名**: Frozen real-data graph viewer failed closed: {exc}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Frozen real-data graph viewer failed closed: {exc}"`

#### Item 430: line 11489 — `expander` — Route A manual-sanity diagnostic — frozen independent lane

- **種類**: `expander`
- **画面上の表示名**: Route A manual-sanity diagnostic — frozen independent lane
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Route A manual-sanity diagnostic — frozen independent lane", expanded=False`

#### Item 431: line 11500 — `markdown` — ### Frozen diagnostic comparison

- **種類**: `markdown`
- **画面上の表示名**: ### Frozen diagnostic comparison
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Frozen diagnostic comparison"`

#### Item 432: line 11522 — `markdown` — ### Manual-sanity algebraic decomposition

- **種類**: `markdown`
- **画面上の表示名**: ### Manual-sanity algebraic decomposition
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Manual-sanity algebraic decomposition"`

#### Item 433: line 11565 — `error` — Embedded posterior viewer failed safely: {_dti_embed_exc}

- **種類**: `error`
- **画面上の表示名**: Embedded posterior viewer failed safely: {_dti_embed_exc}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Embedded posterior viewer failed safely: {_dti_embed_exc}"`

#### Item 434: line 11573 — `expander` — Route A/B Boundary Matrix — diagnostic available, full inference unavailable

- **種類**: `expander`
- **画面上の表示名**: Route A/B Boundary Matrix — diagnostic available, full inference unavailable
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Route A/B Boundary Matrix — diagnostic available, full inference unavailable", expanded=False`

#### Item 435: line 11579 — `markdown` — ### Diagnostic availability matrix

- **種類**: `markdown`
- **画面上の表示名**: ### Diagnostic availability matrix
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Diagnostic availability matrix"`

#### Item 436: line 11617 — `table` — (dynamic or variable-derived label)

- **種類**: `table`
- **画面上の表示名**: 自動生成または変数由来のため、ソース式を参照します。
- **何をする項目か**: 固定的な表表示です。整理済みの値や比較表を読むために使います。
- **使い方**: 値、比較、状態、監査結果を読むために使います。行名、列名、注記、境界表示を一緒に確認してください。
- **注意**: 表示値は source-locked、diagnostic、audit-only、display-only のいずれかとして読む必要があります。
- **ソース上の式**: `_dti_route_ab_boundary_rows_v1`

#### Item 437: line 11624 — `expander` — Route A/B boundary provenance

- **種類**: `expander`
- **画面上の表示名**: Route A/B boundary provenance
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Route A/B boundary provenance", expanded=False`

#### Item 438: line 11657 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`

#### Item 439: line 11675 — `error` — SAFE V5 embedded viewer file is missing.

- **種類**: `error`
- **画面上の表示名**: SAFE V5 embedded viewer file is missing.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"SAFE V5 embedded viewer file is missing."`

#### Item 440: line 11679 — `error` — SAFE V5 embedded viewer failed safely: {_dti_inline_safe_v5_exc}

- **種類**: `error`
- **画面上の表示名**: SAFE V5 embedded viewer failed safely: {_dti_inline_safe_v5_exc}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"SAFE V5 embedded viewer failed safely: {_dti_inline_safe_v5_exc}"`

#### Item 441: line 11699 — `markdown` — ## Panel 8: Likelihood Definition Binder — audit-only

- **種類**: `markdown`
- **画面上の表示名**: ## Panel 8: Likelihood Definition Binder — audit-only
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"## Panel 8: Likelihood Definition Binder — audit-only"`

#### Item 442: line 11707 — `markdown` — utf-8

- **種類**: `markdown`
- **画面上の表示名**: utf-8
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `definition_path.read_text(encoding="utf-8", errors="replace")`

#### Item 443: line 11709 — `error` — LIKELIHOOD_DEFINITION_TEXT_V1.md is missing.

- **種類**: `error`
- **画面上の表示名**: LIKELIHOOD_DEFINITION_TEXT_V1.md is missing.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"LIKELIHOOD_DEFINITION_TEXT_V1.md is missing."`

#### Item 444: line 11711 — `markdown` — ### Execution readiness matrix

- **種類**: `markdown`
- **画面上の表示名**: ### Execution readiness matrix
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Execution readiness matrix"`

#### Item 445: line 11717 — `error` — Could not render readiness matrix: {e}

- **種類**: `error`
- **画面上の表示名**: Could not render readiness matrix: {e}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Could not render readiness matrix: {e}"`

#### Item 446: line 11719 — `error` — READINESS_MATRIX_V1.tsv is missing.

- **種類**: `error`
- **画面上の表示名**: READINESS_MATRIX_V1.tsv is missing.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"READINESS_MATRIX_V1.tsv is missing."`

#### Item 447: line 11721 — `markdown` — ### Static audit requirements

- **種類**: `markdown`
- **画面上の表示名**: ### Static audit requirements
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"### Static audit requirements"`

#### Item 448: line 11727 — `error` — Could not render static audit requirements: {e}

- **種類**: `error`
- **画面上の表示名**: Could not render static audit requirements: {e}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Could not render static audit requirements: {e}"`

#### Item 449: line 11729 — `error` — STATIC_AUDIT_REQUIREMENTS.tsv is missing.

- **種類**: `error`
- **画面上の表示名**: STATIC_AUDIT_REQUIREMENTS.tsv is missing.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"STATIC_AUDIT_REQUIREMENTS.tsv is missing."`

#### Item 450: line 11746 — `markdown` — ---

- **種類**: `markdown`
- **画面上の表示名**: ---
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"---"`

#### Item 451: line 11747 — `error` — 🛑 Panel 7: Claim Boundary Red Shield — audit guardrail

- **種類**: `error`
- **画面上の表示名**: 🛑 Panel 7: Claim Boundary Red Shield — audit guardrail
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"🛑 Panel 7: Claim Boundary Red Shield — audit guardrail"`

#### Item 452: line 11748 — `caption` — This panel is a claim-boundary guardrail. It is not a new computation and it does not change the frozen payloads.

- **種類**: `caption`
- **画面上の表示名**: This panel is a claim-boundary guardrail. It is not a new computation and it does not change the frozen payloads.
- **何をする項目か**: 短い補足説明です。表示結果の読み方や注意点を示します。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"This panel is a claim-boundary guardrail. It is not a new computation and it does not change the frozen payloads."`

#### Item 453: line 11769 — `success` — Frozen claim-boundary file found.

- **種類**: `success`
- **画面上の表示名**: Frozen claim-boundary file found.
- **何をする項目か**: 処理や表示が成功したことを示します。ただし物理的検証の成功を意味するとは限りません。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Frozen claim-boundary file found."`

#### Item 454: line 11770 — `expander` — Frozen CLAIM_BOUNDARY.md readback

- **種類**: `expander`
- **画面上の表示名**: Frozen CLAIM_BOUNDARY.md readback
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"Frozen CLAIM_BOUNDARY.md readback", expanded=False`

#### Item 455: line 11771 — `markdown` — utf-8

- **種類**: `markdown`
- **画面上の表示名**: utf-8
- **何をする項目か**: 説明文または補助テキストです。操作そのものではなく、読み方や境界条件を示すために使われます。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `boundary_path.read_text(encoding="utf-8", errors="replace")`

#### Item 456: line 11773 — `error` — Frozen claim-boundary file is missing.

- **種類**: `error`
- **画面上の表示名**: Frozen claim-boundary file is missing.
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `"Frozen claim-boundary file is missing."`

#### Item 457: line 11785 — `error` — Claim Boundary Red Shield failed to render: {exc}

- **種類**: `error`
- **画面上の表示名**: Claim Boundary Red Shield failed to render: {exc}
- **何をする項目か**: 処理または入力に問題があることを示します。原因を確認してから次に進む必要があります。
- **使い方**: その周辺の項目をどう読むべきかを示す説明です。特に warning や caption は結果の一部として扱います。
- **注意**: 否定語や禁止語が含まれていても、説明書では正常です。境界を明確にするための文です。
- **ソース上の式**: `f"Claim Boundary Red Shield failed to render: {exc}"`

#### Item 458: line 11793 — `expander` — About / Citation / Provenance

- **種類**: `expander`
- **画面上の表示名**: About / Citation / Provenance
- **何をする項目か**: 開閉式の説明・操作ブロックです。閉じていても無効ではなく、必要なときに開いて確認します。
- **使い方**: 必要な情報を開いたり、表示対象を切り替えたりします。閉じている項目も無効ではありません。
- **注意**: 開閉やタブ切替は表示整理のためのUI操作です。新しい計算を意味するとは限りません。
- **ソース上の式**: `"About / Citation / Provenance", expanded=False`

---

## 3. Session-state keys detected

These keys are internal app memory names. They help the app remember UI choices, loaded presets, button states, or temporary values.

| index | line | key | meaning |
| --- | ---: | --- | --- |
| 1 | 3634 | `dti_ui_candidate_reference_rows_v1` | Internal state key used to store or recall a value in the Streamlit session. |
| 2 | 3635 | `dti_ui_candidate_profile_v1` | Internal state key used to store or recall a value in the Streamlit session. |
| 3 | 3636 | `dti_ui_reference_profile_v1` | Internal state key used to store or recall a value in the Streamlit session. |
| 4 | 3637 | `dti_ui_candidate_preset_name_v1` | Internal state key related to preset selection or loading. |
| 5 | 3638 | `dti_ui_reference_preset_name_v1` | Internal state key related to preset selection or loading. |
| 6 | 3882 | `dti_ui_candidate_reference_rows_v1` | Internal state key used to store or recall a value in the Streamlit session. |
| 7 | 3883 | `dti_ui_candidate_profile_v1` | Internal state key used to store or recall a value in the Streamlit session. |
| 8 | 3884 | `dti_ui_reference_profile_v1` | Internal state key used to store or recall a value in the Streamlit session. |
| 9 | 6112 | `dti_bggeom_jump_z_v1b` | Internal state key related to Jump toy or jump-parameter controls. |
| 10 | 6113 | `dti_bggeom_jump_factor_v1b` | Internal state key related to Jump toy or jump-parameter controls. |
| 11 | 7661 | `paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 12 | 7664 | `paper_text_widget` | Internal state key used to store or recall a value in the Streamlit session. |
| 13 | 7667 | `paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 14 | 7668 | `paper_text_widget` | Internal state key used to store or recall a value in the Streamlit session. |
| 15 | 7668 | `paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 16 | 8444 | `selected_preset` | Internal state key related to preset selection or loading. |
| 17 | 8445 | `paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 18 | 8446 | `paper_text_widget` | Internal state key used to store or recall a value in the Streamlit session. |
| 19 | 8447 | `pending_paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 20 | 8460 | `paper_text_widget` | Internal state key used to store or recall a value in the Streamlit session. |
| 21 | 8462 | `paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 22 | 8467 | `paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 23 | 8468 | `pending_paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 24 | 8482 | `pending_paper_text` | Internal state key used to store or recall a value in the Streamlit session. |
| 25 | 8835 | `dti_public_api_warmup_rows_7a7b_v2` | Internal state key used to store or recall a value in the Streamlit session. |
| 26 | 8838 | `dti_public_api_warmup_rows_7a7b_v2` | Internal state key used to store or recall a value in the Streamlit session. |
| 27 | 8939 | `local_axiclass_fixed_result_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 28 | 8940 | `local_axiclass_fixed_http_status_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 29 | 8941 | `local_axiclass_fixed_elapsed_sec_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 30 | 8942 | `local_axiclass_fixed_cache_meta_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 31 | 8944 | `local_axiclass_fixed_result_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 32 | 8960 | `local_axiclass_fixed_http_status_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 33 | 9179 | `live_vanilla_H0_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 34 | 9180 | `live_vanilla_omega_cdm_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 35 | 9181 | `live_vanilla_omega_b_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 36 | 9182 | `live_vanilla_ns_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 37 | 9183 | `live_vanilla_ln1010As_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 38 | 9184 | `live_vanilla_source_signature_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 39 | 9316 | `live_vanilla_probe_result_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 40 | 9317 | `live_vanilla_probe_http_status_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 41 | 9318 | `live_vanilla_probe_elapsed_sec_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 42 | 9319 | `live_vanilla_probe_cache_meta_v606_8d` | Internal state key used to store or recall a value in the Streamlit session. |
| 43 | 10704 | `external_class_api_result_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 44 | 10705 | `external_class_api_http_status_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 45 | 10707 | `external_class_api_result_v606` | Internal state key used to store or recall a value in the Streamlit session. |
| 46 | 10716 | `external_class_api_http_status_v606` | Internal state key used to store or recall a value in the Streamlit session. |

---

## 4. Boundary summary

This item-by-item manual is intentionally broad. It does not certify that every displayed panel is a full physical calculation. It explains what the app shows and how to read each item safely.

Do not use this manual or the app to claim:

- DTI is validated.
- The Hubble tension is solved.
- A physical discontinuity has been proven.
- A full eBOSS/BAO likelihood has been implemented where the app says it is unavailable.
- Planck or JWST validation has been completed by this public UI.
- A live MCMC posterior has been computed by a display-only or frozen panel.

Use the app as a diagnostic, audit, source-locked, bounded, display-only companion unless a specific frozen source package says otherwise.


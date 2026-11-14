# v32・135資産の容量、ファイル同一性、保存の最終ゲート統合（2026-11-15）

## 1.〈本論〉結果

`catalog/CURRENT.json` v32は182登録、SELECT53＋CONDITIONAL82＝135有効を維持。次の**異なる測度**を混同せず、一次報告に遡って再計算した。

| 測度 | byte（十進TB） | 根拠・境界 |
|---|---:|---|
| v27旧126資産の一次ファイル延べ容量 | 3,413,612,735,064（3.413613 TB） | [v27原報告](../../catalog/capacity/2026-11-07/v27/capacity-report.md)、126行のbyte再集計は[v27 summary](../../catalog/capacity/2026-11-07/v27/capacity-summary.json)と一致 |
| 新規9資産の固定・参考一次ファイル容量 | 44,296,102,441（0.044296 TB） | [R64](../../manifests/drafts/r64-eight-source-scopes.candidate.json)の8資産＋[R48](../../catalog/research/2026-11-12-r48-pinned-scopes.json)のZONOS3 Native keep2参考 |
| **135資産の一次ファイル延べ容量** | **3,457,908,837,505（3.457909 TB）** | [全135件・1資産1行](../../catalog/capacity/2026-11-15/v32/135-primary-file-source-reconciliation.json)。外部重みを別に計上 |
| ACE-Stepの依存repo追加参照 | 5,300,324,640（0.005300 TB） | `ACE-Step/Ace-Step1.5`は**有効136番目の資産ではない** |
| 135資産＋ACE外部repoの**ファイル参照単純合計** | 3,463,209,162,145（3.463209 TB） | [R73ファイル同一性全件監査](../../catalog/readiness/v32-2026-11-15-r73-135-publisher-file-identity-coverage.json)の60,043参照と完全一致 |
| 旧v27の依存を含む公開元SHA-aware union | 3,417,685,712,585（3.417686 TB） | v27の一次ファイルのみ合計とは異なる |
| ACE共通Qwenの発行元SHA一致による再利用 | **1,211,907,493（0.001212 TB）** | [R62一次ファイル照合](../../catalog/research/2026-11-14-r62-ace-exact-source-scope-and-kumo-tag.json)の6参照をR64で再確認 |
| **SHA調整済み既知sourceのみの参考計画値** | **3,466,070,232,173（3.466070 TB）** | [R63試算](../../catalog/estimates/2026-11-14-v32-exact-source-scope-r62.json)と**1 byte単位で一致** |
| 4TB計画上限・200GB最低空き床を引いた**算術上の差** | 333,929,767,827（0.333930 TB） | 実機の空き容量・残余予算・最終保存余裕と解釈してはならない |

**計算の独立性：** [R73容量台帳](../../catalog/capacity/2026-11-15/v32/135-primary-file-source-reconciliation.json)は、旧126件の1行あたりのbytesと新9資産の配布元ファイル参照を厳密IDで結合した。別の[R73ファイル同一性監査](../../catalog/readiness/v32-2026-11-15-r73-135-publisher-file-identity-coverage.json)は、v27の約21.4MB原本を解析し、126件の59,938ファイル、今回合計60,043参照を確認した。両者の延べbyte合計は一致しており、**別手法で重ねた算術検査である**。どちらも実HDDの現物SHA検証ではない。

### 17件のGatedと未確認hash

[R73公開元ファイル同一性監査](../../docs/strategy/73-v32-135-publisher-file-identity-audit.md)によると、旧126件のうち762のファイル、計785,001,541,355 byteでは配布元ペイロードSHA-256がmasked/未確認。該当資産17件は[R72](../../catalog/readiness/v32-2026-11-15-r72-consolidated-135-cross-evidence.json)で確認したGatedリスク17件と一致する。この17件は**大きいことを理由に選定を取り消すのでも、権利のない取得を試みるのでもない**。個々のアカウントの正規許諾が確認できるまで取得準備を止める。公開metadataの観測があっても個人のアクセス権は証明されない。

### 現行モデル特性と重複排除

- 量子化や別backend原本、特殊LoRA、RL/SFT、蒸留による**別の学習済み状態**をファイル名だけで同一と決めない。逆に単純な再量子化を別原本の保存対象として二重計上しない。
- [R70 RFD4](70-rfd4-identity-resolution-stale-release-manifest-2026-11-15.md)では異なるrevisionの主重みが同一公開SHA。ただしREADME・inference.yaml・provenance等が相違するので、固定revの対応を保持。
- 150B以上は現行ルールの同等RAM実測・速度・品質・権利・容量などの独立ゲートを満たした場合のみ例外研究。実測なしの研究候補を自動的にACTIVEへ昇格しない。
- 外部必須Codec・親モデル・VAE/Encoder、runtime wheelhouse、staging、障害時再取得、同意のあるデータはまだ容量・復元完全性のPASSではない。

## 2.〈応用・転用例〉監査の実行と保存手順

`main`をclone済みのPython 3.10以上の読み取り可能な環境で、**ネットワークなし・モデル実行なし**の算術監査を実行できる：

```bash
python3 scripts/verify_v32_primary_source_capacity.py
python3 -m unittest tests.test_verify_v32_primary_source_capacity
```

スクリプトはv27容量原報告、現行135資産、R48/R64固定subset、R62のQwen重複、R73台帳、`queues/approved.json`の空状態を検査し、不整合があれば停止する。**Python構文検査は実施済み。上記unittestのリポジトリ実データによる実行結果は未確認**であり、CI合格を推定しない。

初回の合法的な最小パイロットは、[IBM TinyTimeMixer R3の原本6ファイル](../../catalog/research/2026-11-15-r69-ibm-ttm-r3-publisher-runtime-pin.json)のソース・利用条件・実行環境を閉包してから、既存の[オフライン読み取り専用ハッシュ確認手順](65-v32-owner-offline-preflight.md)を所有者のHDDに適用。**外部モデルコードを実行した事実はない**。残るのは本人権利、固定wheel/ABI、実ファイルSHA、実空き200GBとcache/staging、所有者の取得承認、オフライン実行試験。

## 3. 変数表・単位チェック・H/T/D/C/U

| 変数 | 意味（日本語） | SI単位 | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| P27 | 旧126資産の一次ファイル延べ容量 | byte | 3,413,612,735,064、v27歴史値 | 整数スカラー |
| P9 | 新9資産の固定・参考一次ファイル容量 | byte | 44,296,102,441、ZONOS nonminimalを含む | 整数スカラー |
| E | ACE-Step外部依存repoの追加source参照 | byte | 5,300,324,640、既存Qwenの重複を含む | 整数スカラー |
| U27 | v27 SHA-aware source union | byte | 3,417,685,712,585、既知外部依存含む | 整数スカラー |
| Q | R62で確認したQwen同一ファイルの参照重複 | byte | 1,211,907,493、6参照 | 整数スカラー |
| S | v32 SHA-adjusted source参考容量 | byte | U27＋P9＋E－Q、計3,466,070,232,173 | 整数スカラー |
| C | 保存計画上限 | byte | 4,000,000,000,000、実物HDD容量と区別 | 整数スカラー |
| F | 最低物理空き領域 | byte | 200,000,000,000、実機で要測定 | 整数スカラー |
| M | 空HDD仮定の参考差額 | byte | C－F－S、計333,929,767,827 | 整数スカラー |

**次元チェック：** P27/P9/E/U27/Q/S/C/F/Mは全てbyteなので加減算は有効。ファイル件数、総パラメータ数、実行VRAM（容量byteだが対象と用途が異なる）を同一の保存容量に算入しない。

**H（反証可能仮説）:** v27の全126件と追加9件を1対1に結び、公開SHAが一致するQwen 6参照を差し引くと、R63のsource参考値を再現できる。  
**T（最小検証）:** n_min=135資産（旧126行と新9資産）＋R64の9repo、R48 ZONOS14ファイル、R62同一参照6件。旧報告とmanifestのbyteを全件再計算。ハッシュは発行元表示の一致に限る。  
**D（判定）:** 126+9=135、旧126件のbyte一致、R64ファイル計数、Qwen6参照のSHA＋byte一致、R63参考値とbyte一致なら**公開元メタデータのsource計画PASS**。合法取得・最終bundle・実HDD空き・offline restoreは**UNCERTAIN**。  
**C（破れ方）:** 旧v27版の履歴元と現行sourceが違う、ZONOS nonminimal範囲が縮む/増える、未評価Codec等が増える、発行元hashと実HDDが不一致。  
**U（不確かさ）:** 17 Gatedの本人権限、762 masked、実HDD使用率、追加学習済み依存、トランジットのstaging/cache。統計分布がないため合成標準不確かさu_cと包含係数kは数値化しない。

**ERROR CHECK：** 135資産全件source容量あり／v27 126行＝3,413,612,735,064 byte／追加9＝44,296,102,441 byte／外部ACE＝5,300,324,640 byte／SHA一致Qwen6＝1,211,907,493 byte／補正後参考3,466,070,232,173 byte。モデル選定変更0、ユーザーHDD測定0、本体DL0、承認0。

関連分野：デジタルアーカイブ（物理保全とbitwise同一性）、ソフトウェア供給網（revision/ハッシュ）、機械学習（訓練済み依存・runtime ABI）、契約/アクセス制御（Gatedの本人許可）。

## 4.〈次に考える問い〉

**仮に最終候補の重みSHAが全部わかっても、現在のHDD内にどのSHAのファイルがすでに存在するかを確認しなければ、実際の増分取得容量をどう確定できるか。**

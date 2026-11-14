# R70｜RFD4-Proteinaのrev不一致解決：root重み同一、旧releaseマニフェスト不整合（2026-11-15）

## 1.〈本論〉

v32正本とR64原本マニフェストのrevision相違について、**Hugging Face配布元の固定リビジョンの公開ファイルページ**を直接比較した（ウェブ内容の再取得）。[R69](69-r64-v32-revision-conflict-and-source-reuse-2026-11-15.md)の「別revisionのため同一性未確定」を**rootモデルだけ解消**する。詳細は[R70機械可読証拠](../../catalog/research/2026-11-15-r70-rfd4-root-identity-and-stale-manifest.json)。

| 対象 | v32の観測rev `cf31b935…` | R64の選定rev `a06e2509…` |
|---|---|---|
| `model.safetensors`公開SHA-256 | `5b549dd61adb2f6c6b5cb95bda13f40f5e31556b4e6c755edc0ca6f011c68fb0` | **同一** |
| `config.json`の`weights_sha256` | `5b549dd61…`（rootと一致） | 公開配布記録と一致 |
| `release-checkpoints.json`の`bundle_sha256` | `5f00cdcd4df57b121ad8edcbe7f2d16b9f2ffa1f878056e23b97a2eaf978f4cc` | `5b549dd61…`（rootと一致） |
| `release-checkpoints.json`の`stored_parameters` | 435,622,721（旧マニフェストの値） | 435,622,465 |
| 原本としての扱い | **同一revision内の説明矛盾**、最終保存単位にしない | **採用候補を維持**、最終取得ロックは別途不可 |

### 原因と範囲

- `cf31b935…`時点の**root重みファイル**はすでに2026-10-19版のSHA `5b549d…`。同じrevの`config.json`もそのSHAを指す。
- ただし、そのrevの`release-checkpoints.json`だけ旧2026-10-15版`5f00cd…`と記載。少なくともこの時点のメタデータは**整合していない**。
- `a06e2509…`では`model.safetensors`の公開SHAと`release-checkpoints.json`の`bundle_sha256`が一致。発行者の実行例も`hf_ckpt_revision=a06e2509…`を使用。R57/R64はすでにこれを固定している。
- 従って、**同じroot重みをrev違いだけで二重ダウンロードする理由はない**。一方、`cf31`と`a06e`のすべてのREADME/LICENSE/provenance等が一致するとまでは証明していない。
- 旧10/15版のSHA `5f00cd…`は、新10/19版とは**別の学習済みcheckpoint**。これは「旧リリースの研究価値」を別途判断する対象だが、今回の`cf31`のroot payloadではない。自動追加も削除もしない。

### 一次配布元証拠

1. [旧観測rev rootモデル公開SHA](https://huggingface.co/nvidia/RFD4-Proteina/blob/cf31b93509df5af854c7f6ad704f5c83c77c0698/model.safetensors)
2. [旧観測rev config.json](https://huggingface.co/nvidia/RFD4-Proteina/blob/cf31b93509df5af854c7f6ad704f5c83c77c0698/config.json)
3. [旧観測rev release-checkpoints.json（不一致）](https://huggingface.co/nvidia/RFD4-Proteina/blob/cf31b93509df5af854c7f6ad704f5c83c77c0698/release-checkpoints.json)
4. [選定rev rootモデル公開SHA](https://huggingface.co/nvidia/RFD4-Proteina/blob/a06e2509c7033b010fc43614e9fd840303588502/model.safetensors)
5. [選定rev release-checkpoints.json（整合）](https://huggingface.co/nvidia/RFD4-Proteina/blob/a06e2509c7033b010fc43614e9fd840303588502/release-checkpoints.json)
6. [公式RFD4開発手引き（選定revを明記）](https://rfd4-proteina.org/latest/contributing/developer-guide.html)
7. [R57の選定ファイル台帳](../../catalog/research/2026-11-14-r57-v32-frozen-source-scopes.json)と[R64の7ファイル原本マニフェスト](../../manifests/drafts/r64-eight-source-scopes.candidate.json)。

## 2.〈応用・転用例〉

**保存形式の判定をrevision文字列と重み本体のSHAに分離する。** 1つのモデルファミリー内でREADME更新・LICENSE変更・コード修正と重み更新が異なるコミットに発生する場合、単純なコミット相違は新モデルの存在を意味しない。逆に`release-checkpoints.json`の説明だけを信じると誤った原本を対応付ける。配布元ファイルポインタ・config・manifestの三者突合が必要。

RFD4のオフライン保存対象は現行R64に記録された**7ファイル・1,742,698,063 byte（選定subset）**を維持し、完全なFlow/AE、必要な実行コード、optional refolding oracleのライセンスを別に確認する。大容量の重複checkpoint、コンテナ、データセットを一律に加えない。

## 3. H/T/D/C/U・変数表・次元チェック

| 変数 | 意味 | SI単位 | 定義・定義域／前提 | 型 |
|---|---|---|---|---|
| B | R64選定RFD4ファイル7件の公表bytes合計 | byte | 1,742,698,063、元ファイル参照で現物未計測 | 整数スカラー |
| P_old | 旧release台帳に記録された要素数 | 1（個） | 435,622,721、**旧releaseに帰属** | 整数スカラー |
| P_new | 新release台帳に記録された要素数 | 1（個） | 435,622,465、R64 rootに帰属 | 整数スカラー |

次元チェック：P_oldとP_newの差は要素数であり、B（byte）とは加減しない。root SHA一致は1件のバイナリ同一性を示すにとどまり、7ファイル全部の同一性を示さない。

**H:** v32観測revとR64 revのroot学習済み重みは同一だが、旧revのrelease台帳が取り残された。  
**T:** 異なる2つの固定revにおける`model.safetensors`・`config.json`・`release-checkpoints.json`（計6参照）を直接照合。n_min=2rev/3file-path。  
**D:** 両root SHA一致・旧マニフェスト不一致・新マニフェスト一致なら`ROOT_IDENTITY_MATCH_METADATA_MISMATCH_RESOLVED`。7全ファイルの現物照合、依存・権利・実HDDはUNCERTAIN。  
**C:** 公開Xetポインタが誤り、後から同一revファイルメタデータが改変、異なる補助学習状態が存在する。  
**U:** SHA情報は配布元表示であり、取得物の現地再ハッシュは実施していない。実HDD/コードABI/権利の未知について統計分布がないため合成標準不確かさu_c・包含係数kは未算定。

**ERROR CHECK:** v32=cf31、R64=a06e。両revのroot公開SHAは64桁で完全一致、新revのrelease台帳も一致、旧rev台帳は別SHA。正本v32の対象資産数変更0、追加原本コピー0、承認0、本体DL0、実行0。

機械学習（学習状態）、ソフトウェア供給網（署名付きスナップショット）、デジタルアーカイブ（原本同一性）、契約法（ライセンスの独立性）に関わる。

## 4.〈次に考える問い〉

同じ重みSHAが固定できたあと、**異なるrevisionに含まれるLICENSEや実行コードの差分をどう記録すれば、将来の再現性と契約条件を同時に保全できるか？**

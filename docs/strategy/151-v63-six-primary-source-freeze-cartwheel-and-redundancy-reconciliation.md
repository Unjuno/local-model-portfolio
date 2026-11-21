# R151／v63：新規6原本の公開ソース統合監査—Cartwheel制御3ポリシー・WeMM・確率決定と無検閲重複

2026-11-22 JST。**現行正本はv63の235登録・188有効。R151は研究結果でありv64の正式追加やダウンロード承認ではない。**
直近の99取得報告は所有者Windows Dの再ハッシュ・本人の使用権・完全オフライン復元とは別証拠。正式 `queues/approved.json` は0件。本調査の新規weight取得0、第三者コード実行0、owner HDD変更0。

- [R151の6モデル・243ファイル固定publisher tree（LFS SHA256、Git blob OID、bytes）](../../manifests/drafts/r150-2026-11-22-six-specialists-source-freeze.candidate.json)
- [R151個別採否・停止条件（機械可読）](../../catalog/decisions/2026-11-22-r150-six-specialists-review-and-uncensored-dedup.json)
- [既存R149：99取得後11原本の研究キュー](../../queues/proposed-v63-r149-after99-11-research-only.json)
- [既存R150：WeMM publisher SHA256SUMSの25/25照合](150-v63-post99-wemm-video2b-uncensored-and-armenian-evidence.md)
- [既存R150：BisonとGroundhogの同条件比較待ち](150-v63-after99-uncensored-tiny-and-decision-model-triage.md)

## 1. 個別判定（上位3件＝将来のCONDITIONAL収録審査。**現時点では取得不可**）

| Publisher（すべてHub 40桁revisionで固定） | 全repo file | 固定bytes | 選定判断 |
|---|---:|---:|---|
| [GetCartwheelInc/cartwheel-control](https://huggingface.co/GetCartwheelInc/cartwheel-control/tree/24fc279af8f70097f503767b81db5384d779aae5) | 154 | **304,057,444** | **新規発見・高優先研究**。RP1・Asimov-1・G1の独立制御policy学習済み重みとモーション、MJCF、meshの復元閉包。所有者のライセンス・simulation安全性審査で正式CONDITIONAL検討 |
| [tencent/WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B/tree/821690998399cac0f55bb7f7f805ebafa650c3a4) | 27 | **6,590,699,556** | **高優先研究**。音声付き動画の同期理解。既存OpenMOSSや通常VLMの置換を断定せず、独立小型checkpointを比較 |
| [baselabs/groundhog-1](https://huggingface.co/baselabs/groundhog-1/tree/f4602c43599114a7af2c158472b59a4ff2d13663) | 16 | **53,120,939,617** | **ソース固定、取得HOLD**。26B MoEの複数選択確率／校正decision。新しい学習成果だがBrier独立評価、非生成APIのlocal ABI、53GBの費用未解決 |
| [169Pi/Alpie_seed](https://huggingface.co/169Pi/Alpie_seed/tree/c8f6ac9416ce5f6843f905b06d9dd695b40c85bc) | 15 | **18,857,555,320** | **HOLD**。Qwen3.5-9BにDoRA SFT→GRPOの別学習結果。ただし既保全Qwen9Bとの公平評価がなく作者カードは比較他モデルの異なるharnessを明記 |
| [OpenUncensored/Inkling-2-Mini-Uncensored](https://huggingface.co/OpenUncensored/Inkling-2-Mini-Uncensored/tree/4e5f06d72b5a70c9dcd5e8046aea576eb3ee8487) | 15 | **20,191,617,908** | **フル重複排除**。v58親Inkling＋v59同Publisher rank2 LoRAを正式収録済。LoRA公開者は丸め1step相違の345/141.6m個を除きフル版に再合成可と説明。bitwise一致の独立証明なし |
| [baselabs/bison-1](https://huggingface.co/baselabs/bison-1/tree/bf8350b2c59eb6c36e95d02a2af870aec18724a7) | 16 | **65,398,108,261** | **HOLD**。Groundhogとは別31B dense learned state。公表AA Decision Index 76/BrierはBison固有でGroundhogへ転用不可。追加65GBに対応する比較便益未確認 |

6repo合計**243 file／164,462,978,106byte**は原本研究の**論理source参照容量**。Cartwheel＋WeMM＋Groundhogの3系統は**197 file／60,015,696,617byte**。いずれもowner HDDへの必要な新規書込量・現在の空き容量を意味しない。既存99モデルを再ダウンロードしない。

## 2. 特に保存価値が高いCartwheel：法的変更の可能性と出力の境界

[Publisher card](https://huggingface.co/GetCartwheelInc/cartwheel-control)は**simulation only、実ロボット実験なし**と明記。3重み原本は次のPublisher SHA256で別々に固定した。

| 対象 | ファイル | 固定SHA256 |
|---|---|---|
| Menlo Asimov-1 | `asimov-1/policy.safetensors`（34,837,748byte） | `e3d44811fbd368e22b084898f00628eb74cd3e29b6be9fb3d8dff24de6ceeb5a` |
| Unitree G1 | `g1/policy.safetensors`（36,481,860byte） | `8ea0488d9bc655987696cd10ce19fbd93c41b2f2bc4afa994056923447f8cd6a` |
| RoboParty RP1 | `rp1/policy.safetensors`（36,070,832byte） | `5e46723697325917530a6c89f8231190e8ef812ebb81b870778bcc22e9e7a4a2` |

このモデルの[Cartwheel Open Model License](https://huggingface.co/GetCartwheelInc/cartwheel-control/blob/24fc279af8f70097f503767b81db5384d779aae5/LICENSE)には配布元が法令遵守のため条文を更新したときに従うかコピー・使用・配布を停止する旨がある。**将来制限が実施されるという観測事実ではない**が、固定したライセンス条文と原本SHAの同時保存を検討する根拠となる。模型・mesh等の別権利は `NOTICE`で確認。使用・再配布・シミュレーションと実機制御を同一視しない。

## 3. 他の独立性・実装ゲート

**WeMM**：学術一次資料[Tang et al., arXiv:2611.26409](https://arxiv.org/abs/2611.26409)。作者は映像フレーム＋音声を同期扱いし、中英の動画音声推論を目指す。HFの2重み `model-00001-of-00002.safetensors`／`model-00002-of-00002.safetensors`、オリジナルのPython processor、音声/画像encoder、tokenizerとLICENSEを同時保全する。推論環境はパッチ済みvLLM（0.18.0/0.31.0）またはSGLang（0.5.16/0.5.19）条件のため、owner OS/driver/CUDA/ABIが未検証なら自動実行不可。別文書にPublisher SHA256SUMSの25/25独立照合がある。

**Groundhog**：Gemma4元原本とは異なるdecision lossと複数選択項目の確率出力を学習。複合ライセンスはBaseten差分MIT＋Google元重みApache2、LICENSEとNOTICE両方を読む。著者カード自体に**GroundhogはAA Decision Index未採点**とありBisonの76を引用して性能を保証できない。APIの確率readout・block-bidirectional maskのローカル実装が無ければ重みだけ保存しても非生成decisionのoffline復元に失敗する可能性がある。

**Inkling**：[OpenUncensoredのLoRAカード](https://huggingface.co/OpenUncensored/Inkling-2-Mini-Uncensored-LoRA)は20 attention output重みのrank2変更を親weightから再合成可能と記載。新フル版の主重みSHAは親と異なるがMTP同一SHA。旧v58/v59で親とLoRAを保全対象にしているので20.19GBフル複写はしない。変換コードの静的監査と出力差チェックが先。作者の拒否テスト32例・MMLU1140問は独立再実験ではない。

## 4. 容量／承認の区別と証明水準

公開元APIの一時点のファイル集合を6固定revisionで全走査し、pathの一意性・整数byte・Git blob SHA1・LFS SHA256参照を記録した。これらの公開元SHAは**ユーザー媒体上のローカルSHAではない**。現時点では既存のR149先頭4件（2,234,744,280byte）の審査を妨げない。研究上の優先提案はCartwheel→WeMM→Groundhogの順。厳密な権利/親/同梱依存・媒体空き（4TB予算・処理中200GB安全床＋cache/staging）・ownerの原本ごとファイル別明示承認まで新規weight取得は禁止。

**H**：別学習済みロボット3構成・動画音声・確率校正は既存ポートフォリオにない保存価値を持ち、重複無検閲フルcheckpointの転送回避で容量を節約できる。
**T**：6原本のPublisher全243ファイルを40桁rev/byte/参照SHAで全数静的検証。実機ではまず読み取り専用の既存99件現物SHA、LICENSE、ABI、完全復元を確認。モデル性能の比較は同HW・clock・backend/ABI・batch・quant/zero-point・context/seedの条件で最低30反復を計画、条件違反なら即停止。
**D**：全source identity一意・不変と未承認維持なら**静的PASS**。本人承認なしの転送/ライセンス擬制/親重みの重複は**FAIL**。実機・法律上の適法行為・校正精度は**UNCERTAIN**。
**C**：新原本が実タスク上既存MOSS/VLMに劣る、Groundhogの特殊readoutが欠損、Cartwheelの機構資料利用権が不足、LoRA再合成の丸め差が推論に影響する。
**U**：現物HDD未観測、ライセンスの実際の適用、Publisherの品質ベンチ偏り、VRAM/driver/codec ABI、メディア時刻同期/画像量子化誤差。統計的反復がないため合成標準不確かさ `u_c` と係数 `k` は未算定。

**ERROR CHECK**：6repo243 fileと全Publisher bytesを整数加算・一意pathで監査。既存235/188を変更せず、取得実行台帳99報告に変更なし。正式`queues/approved.json`0、owner HDD rehash0、新規weight DL0、既存ファイル削除0。法的・性能・完全復元は静的source PASSと混同しない。

**連携分野**：ロボット制御、動画音声信号処理、確率校正・意思決定、供給網/デジタル保存、知的財産法。

###〈次に考える問い〉
**同じ4TB予算なら、再現に必要な小型原本＋依存を3系統新規保存する価値と、既存99報告済みの復元閉包を検証する価値のどちらが大きいか。** 固定ソースと実機Dの読取専用監査で比較する。

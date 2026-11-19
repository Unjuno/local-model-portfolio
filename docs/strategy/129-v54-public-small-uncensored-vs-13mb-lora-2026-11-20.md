# R129｜v54 小型無検閲原本と13MB LoRAの保存価値・アクセス／権利比較（2026-11-20）

> 調査時点の正式正本：**v54、207登録・160有効**。本R129の役割は**追加する学習済み成果の候補を確定し、その取得前停止要因を定義**すること。モデル取得、承認、モデル本体のカタログ追加、既存ファイル削除は実施しない。公開元の全40桁revisionが未取得のため、実行可能なmanifestを偽造しない。

## 1.〈本論〉選定の結論と根拠

| source原本 | 公開状態（2026-11-20調査） | 容量と保存独自性 | 優先・採否 |
| --- | --- | --- | --- |
| [FrostWolfAI/LFM3-1.7B-abliterated](https://huggingface.co/FrostWolfAI/LFM3-1.7B-abliterated) | HF公開・非Gated、`lfm1.0` | **約3.48GB** の独立BF16、LFM3のconv＋局所/大域Attention混在を保全。親とは拒否方向が編集されている | **P0：CONDITIONAL追加予定としてsourceと権利を優先閉包。今は未登録** |
| [PhalaCloud/Qwen3.8-27B-Uncensored-LoRA](https://huggingface.co/PhalaCloud/Qwen3.8-27B-Uncensored-LoRA) | HF公開・非Gated、AdapterはApache-2.0 | Publisher約13MBの**rank3 LoRA**。親Qwen/Qwen3.8-27Bと再利用でき、フル27Bの別マージ複製より大幅に小さい | **P1：親・学習データ由来の権利を閉包してからCONDITIONAL追加を再判定。今は未登録** |
| [orcarouter/LFM3-1.7B-abliterated](https://huggingface.co/orcarouter/LFM3-1.7B-abliterated) | HF Gated、license:other、親LFMライセンス | 別作者による別拒否方向編集学習済み結果 | **HOLD：本人Gated権限と源ライセンスが先** |

**交換判断**：FrostWolfはOrcaRouterと同じLiquid LFM3から派生していても**別作者・別方向編集**であり、データの出自と重みは異なる。FrostWolfの公開BF16を「Orca原本そのもの」の鏡像と偽って分類しない。FrostWolfの同作者GGUFやadolanのOrcaGGUFは同一各派生の**変換形式**で、独立学習成果ではないため資産登録を増やさない。

**Phalaの重要な条件**：約13MBは**追加Adapter**の量であり、単体モデルの完全保存容量ではない。出版社が評価に使った親は`Qwen/Qwen3.8-27B-FP8@017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`。既存カタログのQwen BF16参考revとは違う。既存61モデルVERIFIED台帳にはQwen親本体がないので、**今の実行報告から「13MBで単独動作可能」と結論できない**。重み親のSHA/版とruntimeの受理確認が必要。一方、Qwen親はREMORY/pi LoRA/DaisyRose系譜監査のため別に選定済みで、親の実保全が完了すればPhalaの追加取得量は非常に小さい。

## 2. 権利とコードの実際の相違

- **FrostWolf**：配布者カードはHeretic v2 ARA、24層の編集、BF16、作者選定trialの拒否1/100を報告。独立ベンチマークではなく最適化trial選択バイアスがある。Custom`lfm3` codeとtokenizerを含むため`trust_remote_code`は未監査で実行しない。[Liquid AI公式のLFM Open License 1.0](https://www.liquid.ai/lfm-license) §5では**年商1,000万USD以上の法人の商用利用に追加契約が必要**。個人研究と商用配布・サービスを同じ権利区分と扱わない。
- **Phala**：出版社の`adapter_model.safetensors`公開SHA256は`1abf13b2191c9973a4dc4d978448512d3ce2efabfd1e671edd5956b6aebfa5ac`、`adapter_config.json`は`d716fa478316e84ed9d08875db621c84ec377145297bbb834a338ac5ae0de285`。ただし**repo全体の固定40桁revision、全選択ファイルとbyteは今回閉包していない**。公開READMEのApache-2.0はAdapterのみを対象とし、構築に使った`mlabonne/harmless_alpaca`は[Stanford AlpacaのCC BY-NC 4.0／研究専用注意事項](https://github.com/tatsu-lab/stanford_alpaca)に由来する。AI Adapterへの法的派生範囲を自動断定せず、**本人の非商用／商用目的別の契約評価**を停止ゲートにする。
- **OrcaRouter**：現時点Gatedであるという事実と、将来の公的禁止リスクは別。公開されている第三者量子化ファイルをGated原本と同じ学習時ソースとして流用したり、本人のGated許諾を回避しない。

## 3. 性能値は出版社の条件を維持して記録

| 対象・測度 | 発行者報告 | 測定条件・留保 |
| --- | --- | --- |
| FrostWolf ARA選択試行 | 拒否1/100、KL=0.0555 | Heretic v2.1.0、120 Optuna trials、seed2026110901。GPU・clock・batch不明、実装の再現未実施 |
| Phala StrongREJECT一次judge | thinking off/onとも0/60拒否 | NVIDIA H200、Publisher専用SGLang／FP8 parent+KV+EAGLE。二次judgeは異なる判定（off4/60、on1/60） |
| Phala GSM8K／IFEval | 96.36→96.66%／82.44→81.70% | 同じ出版社benchmark群。+0.30pp／-0.74pp、ユーザーGPUの品質未確認 |

**出版社の拒否ベンチだけではモデルの汎用品質、安全性、将来のアクセス制限を証明できない。** 標本誤差は小標本である。例えば反復独立・試験集合が事前固定という**満たされない可能性のある理想化仮定**の下でも、95% Wilson区間の単なる参考値はFrostWolf拒否1/100で**0.18%～5.45%**、Phala一次judge0/60で**0～6.02%**。実際にはtrial選択・判定者・課題重複があるため信頼保証とみなさない。

## 4. 米BIS・公開制限の事実と将来仮説

[米BISの2026年11月IFR原文](https://www.bis.gov/media/documents/rin-0694-ak50.pdf)はAI Diffusion Rule由来のモデルweight向けECCN 4E091指定を撤回する。他方で、輸出先、半導体、遠隔計算への規制と、出版社の個別LICENSE/Gatedには別の条件がありうる。「全open-weightモデルが近日禁止される」という予測は法律の確認事実でない。モデル別の公開停止確率は推定不能。

## 5. 変数表・次元チェック／H・T・D・C・U

| 記号 | 意味（日本語） | SI単位 | 定義（必要なら式） | 定義域／前提 | 型 |
| --- | --- | --- | --- | --- | --- |
| `n` | 一条件で試験した質問数 | 1（無次元） | 出版社測度の母数 | 60または100、独立保証なし | 整数スカラー |
| `x` | 拒否と判定された件数 | 1（無次元） | Publisher judgeの判定カウント | 0以上n以下 | 整数スカラー |
| `p` | 拒否率 | 1（無次元） | `x/n` | 0〜1、上記試験条件に限定 | 実数スカラー |
| `z` | Wilson区間の正規分位点 | 1（無次元） | 95%名目値1.96 | 試験独立を理想仮定 | 実数スカラー |
| `B_a` | Adapter原本重み容量 | byte（非SIの情報量単位） | 約13 MB、厳密値未固定 | 正式SHA原本のbyteは未確認 | 非負整数／欠損 |
| `B_p` | 親Qwen原本保存容量 | byte（非SIの情報量単位） | 参考のQwen BF16 source約55.586GB | Owner実保存は未検証 | 非負整数／欠損 |
| `N_m` | 全学習済みパラメータ数 | 1（無次元） | MoE inactive expertと全学習部品を含む | 150B基準。未閉包はSTOP | 整数／欠損 |
| `u_c` | 合成標準不確かさ | 対象の測度に依存 | 未算出 | 独立再計測不足 | 実数／欠損 |
| `k` | 包含係数 | 1（無次元） | 未設定 | 不確かさモデル不足 | 実数／欠損 |

**次元チェック**：拒否率`p=x/n`は個数/個数で無次元。親とAdapterのsource bytesは条件付きに加算できるが、`N_m`というパラメータ個数とは加減算できず、量子化で`N_m`を減らしたとみなさない。Wilson区間は`n,x,z`の無次元量で、同じ評価設計にのみ適用できる。

**H**：既存親を将来実体SHAで確認できるなら、PhalaのLoRAは新たなフル27B全重みより大幅に少ない増分容量で別の拒否方向編集成果を保全できる。一方FrostWolfは3.48GB程度で異なるLFM学習結果を独立に保持できる。  
**T**：2モデルのPublisher 40hex revision、全file byte/sha、再現・ライセンス・親のSHAとABIを静的照合。ユーザー許可後、同一HW/clock/backend/quant/zero-point/context/batch、拒否だけでなく安全過剰拒否・GSM8K・IFEval・日本語をそれぞれ最低30 paired promptsで比較。どのゲート違反でも停止。  
**D**：PASS_METADATA＝現在Public/UnGated、モデルの互いに異なる学習成果、出版社記載の権利とsample条件が矛盾なく記録されている。FAIL＝未許諾Gated回避、親不一致、版/sha不一致、LICENSE違反、別量子化を別原本として計上。UNCERTAIN＝今回の全file SHA・現在の本人D・完全offline再現・本人使用権利。  
**C**：著者の試験が最適化に過剰適合し、別日本語・低リソース用途で性能が悪化する可能性。LoRAは親BF16版/ほかのSGLang ABIで正しく適用できない可能性。  
**U**：最適化選択バイアス、出版社sample、データLICENSE、親revision、推論ABI、Owner HDD未測定。実機反復分散がないため`u_c`と`k`の数値は未確定。

**ERROR CHECK**：調査基準v54 207登録・160有効。今回正式追加0、ダウンロード承認0、モデル本体取得0、他の資産削除0。両候補は現行61 VERIFIED ledgerに含まれない。出版社公開元本体の全source_sha・40桁revisionは**未確定**なので**取得実行不可**とした。

**関連分野**：モデル学習系譜・量子化（別学習結果を区別）、長期保存（SHAと復元依存）、ライセンス・出版政策（LFMとCC BY-NC）、統計実験計画（選択バイアスと再現試験）。

## 6.〈次に考える問い〉

**新たな13MB LoRAを保存候補へ追加する前に、共有する55.586GBの親Qwenが実際にハッシュ検証可能な状態で保存されていることを、どのファイル集合で立証するか。** 先に親保全とライセンスを閉じる方が「小型モデルの数」を増やすだけより再現価値が高い。

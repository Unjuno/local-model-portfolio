# NVIDIA・希少専門モデルの保存価値再評価（2026-11-13）

対象：`Unjuno/local-model-portfolio` / `strategy/2026-11-03-01-risk` / v31 / 基準HEAD `86d299d1028312b62db37cae278bfb8ca50c13b3`。**本成果は研究のみ。選定変更・Gated同意・重み取得・実行・承認は0。**

## 1.目的と政策の食い違い

保存価値を「現時点のベンチ順位」で削るのは、再現困難な学習済み重みを確保するアーカイブ目的と整合しない。`policies/archival-insurance.json` は独自学習成果・再構築困難性を最上位に置くが、`policies/selection-decision-v17.json` の PROMOTE_SELECT は独立性能と固定HWを要求する。
**提案：ARCHIVE_KEEP（独自原本の長期研究保存価値）／ACQUISITION_READY（法令・全依存・SHA・実HDD・本人承認）／RUNTIME_READY（性能・速度/品質・RAM測定）を分離**。これらは非補償型の別判定。既存の正式ポリシー自体は今ラウンドでは編集しない。

## 2.NVIDIAの配布政策について確認できた事実

- [2026-10-21 NVIDIA発表](https://blogs.nvidia.com/blog/open-models-europe-industry/) はKumo・BioNeMo・Cosmosなどオープン公開の拡張。現段階でNVIDIA全体が公開ウェイトの撤回を予告した証拠はない。
- [2026-11-09 CoRL](https://blogs.nvidia.com/blog/robotics-simulation-advancements-corl/) はGR00T 2の発表。しかしHF `nvidia/GR00T-2`の実体は確認できないため、本体公開済み・取得可と書かない。
- [2025-10-24 NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/) の原文には契約更新時の遵守/利用停止、適切な保護措置、元モデルと別ライセンス部品・表示条項がある。**既存契約上の事実≠次月の削除予測**。
- [2026-05-28 Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-releases-openmdw-1-1-nvidia-adopts-openmdw-for-cosmos-isaac-gr00t-ising-and-nemotron-ai-model-families) ではOpenMDW-1.1の将来家族への採用方針。GR00T N1.7の旧NVIDIA LicenseとIsingのOpenMDWなど、版別適用を再確認する。
- Ising ColorCode FastとSurfaceCode FastはいずれもGated表示。本人の正式同意が得られない限りファイルは取らない。

## 3.新規／未選定候補：21件の一次調査

この21件はv31既存179件にID重複しない。P0は特殊性・アクセス制限の一次研究、P1は独立機序、P2は法的/容量/依存の追加調査、P3は公開重み未確認で監視。**調査順位はダウンロード順位ではない**。

| # | repo ID・公式URL | 調査 | 公開状態 | 公表パラメータ（全学習済み依存は未確定） | 配布ライセンス表示 | 独自性 | 既存との境界 |
| ---: | --- | --- | --- | ---: | --- | --- | --- |
| 1 | [`nvidia/Ising-Decoder-ColorCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | P0 | Gated | 2936580 | openmdw-1.1 | 量子ColorCodeのCNNプリデコーダ。元の推論符号・学習過程はLLMやSurfaceCodeから復元できない | SurfaceCodeと別タスク・別モデル。別のグローバルデコーダが必要 |
| 2 | [`nvidia/Ising-Decoder-SurfaceCode-1-Fast`](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | P0 | Gated | 910000 | nvidia-open-model-license | 量子SurfaceCodeの約0.91Mプリデコーダ。異なるエラー訂正方式の原本 | ColorCodeと別学習状態。同一系列のAccurate版は無条件追加しない |
| 3 | [`nvidia/QCalEval`](https://huggingface.co/datasets/nvidia/QCalEval) | P0 | 公開表示 | 未知 | cc-by-4.0 | 量子校正の309枚実験図と243のQAベンチマーク。重みだけから再構築できない | Ising Calibrationと対になる評価データ。元図の権利を別審査 |
| 4 | [`nvidia/RFD4-Proteina`](https://huggingface.co/nvidia/RFD4-Proteina) | P0 | 公開表示 | 435622465 | bsd-3-clause | 生体分子のFlowモデル＋専用AEを対で保存する必要がある独自生成重み | Diffusers形式はネイティブと同一テンソル。repo約106GBの全取得不要、ネイティブ重み約1.74GB |
| 5 | [`nvidia/Kumo-Relational`](https://huggingface.co/nvidia/Kumo-Relational) | P0 | 公開表示 | 未知 | openmdw-1.1 | 多表データの関係・時間・履歴を扱う学習済み予測モデル | Chronos2やKumo Tabularと異なる。TabICL由来BSD条項とkumo-engineが依存 |
| 6 | [`nvidia/Kumo-Anomaly`](https://huggingface.co/nvidia/Kumo-Anomaly) | P0 | 公開表示 | 8000000 | apache-2.0 | 多変量時系列の拡散異常検知。単純予測モデルにはない学習成果 | Kumo Forecast/Chronos/TTMと異なる異常検知タスク |
| 7 | [`nvidia/Nemotron-3-Diarization`](https://huggingface.co/nvidia/Nemotron-3-Diarization) | P0 | 公開表示 | 99200000 | openmdw-1.1 | 誰がいつ話したかを検出する話者分離/ストリーミング系原本 | 既存WhisperやQwen ASRは転写用途、話者分離は別部品 |
| 8 | [`nvidia/Ising-Calibration-1.5-31B-BF16`](https://huggingface.co/nvidia/Ising-Calibration-1.5-31B-BF16) | P1 | 公開表示 | 31273100000 | HF other; publisher OpenMDW | 量子実験・校正プロット解釈に専門学習した31B VLM | Isingプリデコーダとは全く別タスク。NVFP4形式を重複採用しない |
| 9 | [`nvidia/Kumo-Tabular`](https://huggingface.co/nvidia/Kumo-Tabular) | P1 | 公開表示 | 未知 | openmdw-1.1 | 単一表の分類・回帰の事前学習状態。28M〜215M複数サイズ | Kumo Relationalとは別入力、同族の全サイズは不要 |
| 10 | [`nvidia/Kumo-Forecast`](https://huggingface.co/nvidia/Kumo-Forecast) | P1 | 公開表示 | 未知 | apache-2.0 | DARR履歴パターン検索付き時系列予測 | MOMENT約340M＋forecast headの別学習状態。Chronos/TTMと同一ではない |
| 11 | [`nvidia/Nemotron-3.5-Embed-1B-BF16`](https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16) | P1 | 公開表示 | 1554700000 | HF other; publisher OpenMDW | 図表・文書画像とテキストの共同埋込用に蒸留した別重み | BGE-M3・Qwen text Embeddingは文書画像検索と異なる。8B teacherとNVFP4は自動追加しない |
| 12 | [`nvidia/Nemotron-3.5-Parse`](https://huggingface.co/nvidia/Nemotron-3.5-Parse) | P1 | 公開表示 | 630800000 | openmdw-1.1 | 図表/読み順/領域情報を構造化する別の文書parser | LightOnOCRと機能重複するが別学習状態。任意DFlash2約89.3Mは別部品 |
| 13 | [`nvidia/Nemotron-3.5-Rerank-8B-BF16`](https://huggingface.co/nvidia/Nemotron-3.5-Rerank-8B-BF16) | P1 | 公開表示 | 8381200000 | HF other; publisher OpenMDW | 画像・文書を直接比較する多モーダル再順位付けモデル | 既存Qwen3-Reranker-0.6B text-onlyと入力形式が異なる |
| 14 | [`nvidia/Cosmos-H-Surgical`](https://huggingface.co/nvidia/Cosmos-H-Surgical) | P1 | 公開表示 | 15188500000 | HF other; publisher OpenMDW | 手術動画予測・手術転送へ専門学習したCosmos3派生 | Root BaseとDMD2 studentは別学習状態。元手術データ権利とv0.3.1 code/AEが必要 |
| 15 | [`nvidia/GR00T-N1.7-3B`](https://huggingface.co/nvidia/GR00T-N1.7-3B) | P1 | 公開表示 | 3144000000 | HF other; publisher NVIDIA Open Model License | N1.6とは別の視覚・言語・動作Flowモデル世代 | DROID/Bridge等の後学習版を全部取得しない。embodimentとIsaac-GR00T ABIが必要 |
| 16 | [`nvidia/Cosmos3-Edge-Policy-DROID`](https://huggingface.co/nvidia/Cosmos3-Edge-Policy-DROID) | P1 | 公開表示 | 3859000000 | other | DROIDロボット行動の専門的なCosmos3 Edge Policy | Sim-Autoの車載未来映像/ LiDARモデルとは別。GR00Tとaction schemaを比較 |
| 17 | [`nvidia/Kimodo-SOMA-RP-v1.2`](https://huggingface.co/nvidia/Kimodo-SOMA-RP-v1.2) | P1 | 公開表示 | 283300000 | HF other; publisher NVIDIA Open Model License | テキストと関節拘束から人体骨格動作を生成する独立モーション拡散 | v1.1は分割混入あり、v1.2が修正版。BONES-Rigplay学習データ非公開 |
| 18 | [`nvidia/NV-JEPA-DNA-NTv3`](https://huggingface.co/nvidia/NV-JEPA-DNA-NTv3) | P2 | 公開表示 | 未知 | nvidia-noncommercial-license | DNA token予測＋JEPA潜在表現を統合する100M級継続事前学習 | タンパク質生成RFD4、ESM、言語LLMと異なる。非商用条件要確認 |
| 19 | [`nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-Base-BF16`](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-Base-BF16) | P2 | 公開表示 | 124453400000 | other | 派生後学習から戻せない124B総数の事前学習Base | 約248GB BF16重み下限目安、実ファイル未確定。4TBの残量と競合 |
| 20 | [`nvidia/video-to-data-robot-dexterity-task-library-and-dataset`](https://huggingface.co/datasets/nvidia/video-to-data-robot-dexterity-task-library-and-dataset) | P2 | 公開表示 | 未知 | cc-by-4.0 | 人操作映像から両腕ロボットの学習デモへ変換した資料 | HF規模区分100GB〜1TB。全量ではなく合法subsetと同意・出典を検証 |
| 21 | [`nvidia/GR00T-2`](https://blogs.nvidia.com/blog/robotics-simulation-advancements-corl/) | P3 | 未公開重み | 未知 | 未確認 | 2026-11-09のGR00T 2発表。直接の公開重みのrepo IDは未確認 | nvidia/GR00T-2はHubで該当repoを確認できない。将来の別ID配布を否定はしない |

### 誤った重複判定を避けるための確定資料

- [RFD4 原本](https://huggingface.co/nvidia/RFD4-Proteina) はFlowとAutoencoderの対応セット。Root native約1.74GBとfull repo約106GBの表示は違う。Diffusers分割版は同じテンソルの変換で、追加学習済み状態ではない。
- [Ising](https://github.com/NVIDIA/Ising) のSurfaceCode 0.91M／ColorCode 2.94Mは別の量子誤り訂正符号。校正画像VLM 31Bとも別学習成果。
- [Kumo Tabular](https://huggingface.co/blog/nvidia/kumo-tabular) は単表、[Relational](https://huggingface.co/blog/nvidia/kumo-relational) は複数関係表、[Anomaly](https://huggingface.co/blog/nvidia/kumo-anomaly) は拡散異常検出、[Forecast](https://huggingface.co/blog/nvidia/kumo-forecast) はDARR履歴検索付き予測。4件が同じ量子化だとは扱わない。
- [Nemotron Retriever](https://huggingface.co/blog/nvidia/nemotron-retriever-world-class-agentic-retrieval) にはEmbed 1B（画像+テキスト）、Rerank 8B（クロスモーダル）、Parse 631M（図表/読み順）があり、同じモデルの形式違いではない。Parseの任意DFlash2は別学習済み補助、必須とは断定しない。
- [Cosmos-H Surgical](https://huggingface.co/nvidia/Cosmos-H-Surgical) は手術動画のBaseと蒸留DMD2が同一repoにある。後者は独立学習済みstudent。医療データの権利と臨床利用の禁止境界を守る。

## 4.既存EXCLUDED 6件を性能以外で再評価

| ID | 現行 | 再調査判定 | 理由・未解決事項 |
| --- | --- | --- | --- |
| [`nvidia/nemotron-labs-unified-asr-0.6b`](https://huggingface.co/nvidia/nemotron-labs-unified-asr-0.6b) | EXCLUDED | P1 research-reopen | 同一重みでofflineとstreaming ASR。非日本語というだけのEXCLUDEDは保存価値の反証にならない／NVIDIA LICENSE本文、NeMo ABI、版と全学習済み部品 |
| [`PerceptronAI/Isaac-0.2-2B-Preview`](https://huggingface.co/PerceptronAI/Isaac-0.2-2B-Preview) | EXCLUDED | P2 research-reopen | Focus操作を伴うGUI/視覚特化訓練成果。単なるベンチ弱さを理由に全削除しない／CC-BY-NCとcustom code/Focus依存 |
| [`qvac/TranscribePsy-250M-EU`](https://huggingface.co/qvac/TranscribePsy-250M-EU) | EXCLUDED | P2 research-reopen | Parakeetからの独立した多言語蒸留。日本語非対応は否定理由にならない／元重みライセンス/ファイル/NeMo依存 |
| [`state-spaces/mamba-2.8b`](https://huggingface.co/state-spaces/mamba-2.8b) | EXCLUDED | P1 research-reopen | Transformerと異なるSSMの事前学習原本。RWKV/iLLaDAと代替できない／専用runtimeと保存代表版、源SHA |
| [`Wigtn/KoGovDoc-Bench`](https://huggingface.co/datasets/Wigtn/KoGovDoc-Bench) | EXCLUDED | P1 research-reopen | 韓国行政文書の専門注釈と評価データはモデルから復元できない／原画像・政府文書の著作権/個人情報 |
| [`Wigtn/Qwen3-VL-2B-WigtnOCR`](https://huggingface.co/Wigtn/Qwen3-VL-2B-WigtnOCR) | EXCLUDED | P1 research-reopen | Qwen3-VLからの別蒸留・専門LoRA。親と違う学習状態／親/adapterの選択範囲・重複排除・ライセンス |

これらは**復帰案**であってv31のSELECTやCONDITIONALを自動変更しない。NVIDIA Unified ASRは同重みのストリーミング/オフライン、MambaはSSM事前学習、Wigtnは専門蒸留＋評価データ。日本語非対応や現行ベンチ不足だけでは保存価値の否定にならない。

## 5.既にv31で追跡している特殊な原本・未解決機構

| 既存repo | 状態 | 実行/保存上の意味 |
| --- | --- | --- |
| `nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B` | deferred | 独立34B音声認識重み、deferred。既存Whisperを性能で上回らないことだけで除外しない |
| `nvidia/Granary-v2` | conditional | ASR再ラベル資料。元音声は含まれず合法な別素材必要 |
| `nvidia/Alpamayo2-Edge` | conditional | 因果説明・操舵軌道の独立後学習、Sim-Autoとは別 |
| `nvidia/Cosmos3-Nano-Sim-Auto` | conditional | 車載カメラ+LiDARの学習成果、共通VAEを再計上しない |
| `nvidia/Cosmos3-Nano-Sim-Bimanual` | conditional | 双腕操作の行動条件付け。Sim-Autoと機能重複扱いしない |
| `PrunaAI/P-H3-Image` | conditional | 独立蒸留成果だが全学習済み部品数が未確認。取得準備停止 |
| `Louis0324/StyleStream` | hold | 公開欠落のEncoderがあり不完全。回避取得せず研究記録のみ |
| `Nanbeige/Nanbeige4.3-33B-Base` | deferred | Baseと後学習の別学習状態を考慮し、容量費用と追加学習価値を比較 |

## 6.次に実行すべき静的調査

1. Gated Isingの契約・本人承認の確認方法、RFD4 root Flow+AEの固定SHA、Kumo・Diarization・QCalEvalの独立原本/注釈の完全範囲を調べる。
2. 既存EXCLUDED6の学習機序を精査。正規の権利がある原本ならアーカイブ候補復帰、形式だけの重複なら引き続き除外。実モデルの性能比較は別レーン。
3. GR00T N1.7 / Cosmos3 Edge Policy DROIDと既選定N1.6 / Sim-Auto / Sim-Bimanualの行動スキーマと親子関係を比較。全DROID派生/量子化を重複収集しない。
4. 4TBの実物空き200GB床と、推定版ではない全trained component・原本Sha・selected bytes・依存runtimeの一致を確認。モデル全総数未知は取得準備STOP、150B以上量子化例外も現在HOLD。

## 7.H/T/D/C/U・変数表・ERROR CHECK

| 変数 | 意味（日本語） | SI単位 | 定義／定義域・型・前提 |
| --- | --- | --- | --- |
| N | 新しい調査repo数 | 1（件数） | N=21、非負整数スカラー、全ID一意 |
| P | MoE全expertと別学習部品を含む総パラメータ | 1（個数） | 整数≥0、未確認null、活性数ではない |
| B | 選択重みと必要全依存の重複排除後保存容量 | byte | 非負整数/null、repo表示全量は代入不可 |
| C | HDD選定上限 | byte | 4,000,000,000,000、整数、物理実測前 |
| F | 保存後最低残量 | byte | 200,000,000,000、整数 |
| M | 推論時OS/KV/backend/codec含むピークRAM | byte | 非負整数/null、HW・ABI・量子化zero-point固定 |

次元チェック：B、C、F、Mはbyteで比較し、Pは無次元の要素個数であってファイルbyteや活性expert数に置換できない。RFD4 root約1.74GBは完全復元Bの実測ではない。

- H: 稀少学習成果の保存価値は現在の一般ベンチ優劣から独立。仮説を覆す条件は同一trained-state/合法的に完全再生成可能、または利用権限・依存が確実に不適格な場合。
- T: 既存v31の179と追加21のrepo IDを静的に照合（n_min=200件）。P0候補の固定weights/AE/license/依存と既存の同一SHAを検証。実推論はユーザー別承認を得た別レーンだけ。
- D: PASS=別学習状態の識別と権利・依存/容量・最終lockが成立した時だけ保全SELECT/取得を個別判断。FAIL=同形式重複、法的禁止、欠落必須重み。UNCERTAIN=現状の不明点を残す研究HOLD。取得承認0。
- C: 複数repoが同一学習済みテンソル、独自学習の再現が容易、提供者の明示的許諾がない、または特定分野の学習状態に継続的な使用価値がない。
- U: 消失確率、ライセンス適用、学習履歴、実HDD・外部依存、モデル実体の配布変更。測定分布未定義につき合成標準不確かさu_c/包含係数kは算定不可。

ERROR CHECK：v31 179一意。追加21のrepo IDはv31と不一致で新規。旧EXCLUDED6は一意に再評価。公開済み学習重みの確認がないGR00T 2はWATCHのみ。新モデル取得0、ユーザー承認0、実機推論0。

〈次に考える問い〉：将来の一般用途の速度ではなく、量子誤り訂正・手術・表形式推論・ロボット動作などの独立学習済み状態を保存するために、最低限どの証拠を揃えれば「アーカイブ候補確定」とできるか。

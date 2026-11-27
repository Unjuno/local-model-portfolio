# R168／v73 — 133件取得報告の検証・合成承認遮断・小型無検閲4原本の採否（2026-11-27）

## 1.〈本論〉現行正本と完了内容

現行正本は v73-20261125：265登録、211有効（SELECT 56、CONDITIONAL 155、HOLD 35）を維持する。本研究で新しいモデル重み取得、Gated回避、利用者Windows DのSHA検査／削除、モデルコード実行、本人明示承認の追加は0。

最新版の取得台帳は133 VERIFIED、4 HOLD、2095ファイル、2,451,205,481,822 byteを報告。2026-11-24の旧GitHub固定コミット6fd190ce077dec748130a69c76fbd26c0fbae190の117レコード（116 VERIFIED、1 HOLD）と現行台帳をモデルIDで突き合わせ、revision、status、ファイル数、参照容量、weight SHAを全件比較した。117レコードに内容の不一致なし。順序変更、空のhold_reason補助フィールド付加は検証事実の消失ではない。

[履歴のSHA256固定監査](../../catalog/audits/2026-11-27-r168-133-receipts-original117-signedness-and-historical-integrity.json) ／ [履歴検証関数](../../scripts/ledger_history_r168.py)。

現在の133 VERIFIEDはレポート上の取得照合であり、今回所有者HDDを再ハッシュした結果ではない。公開の承認キューは空で、過去の本人の用途別個別許可が存在したかどうかも、本調査では独立確認できない。台帳上の取得報告、配布元メタデータ、本人権利、完全offline復元は別の証明とする。

## 2. 重大修正：v73の偽承認生成を停止

現行 scripts/build_v73_candidates.py の旧実装は、ライセンス表示にApache/MITがある、正確な出典SHAがあるというだけで、承認ファイルapproved-v73.jsonの approved_by_user、license_text_reviewed、parent_dependency_rights_reviewed、download_enabled などを自動的にtrueとする危険な設計だった。

今回の[修正済みbuilder](../../scripts/build_v73_candidates.py)は公開元ファイルのリサーチ計画と未承認レビュー資料のみ生成し、承認をすべてfalse、approval_refをnullにする。approved-v73.jsonは作成しない。path traversal、サイズ0、重複パス、git OID/SHA不足の不正原本は拒否する。

さらに[取得実行側](../../scripts/preserve_execute.py)は、過去の自動生成approval_refであるv73-pinned-candidate系と、v73 effective portfolio pinned candidate sourcesというauthorization_sourceを持つファイルを拒否する。本人が真に個別審査したscopeの正常経路まで遮断しないことをunittestで確認した。

**重要**：この旧自動承認コードが本人Dで実行されたという証拠はない。存在するかもしれない旧承認ファイルを勝手に削除しない。しかし、以前の合成承認は実行側で信頼できないものとして扱う。

## 3. 小型無検閲モデルの確定研究順位

2026年11月27日の出版社HF APIで4repoの固定40桁revision、全53ファイルのpath、size、Git blob OIDとLFS SHAを取得し、現行265カタログ／133 VERIFIED取得台帳のIDと照合。いずれも既存IDとの重複なし。学習成果の区別は、独立した重み空間編集であり、新しい事前学習と同一視しない。

| 配布原本 | 出版社の全ファイル参照量 | 今回の結論・否定的証拠 |
|---|---:|---|
| [Peymandc/MiniCPM5-1B-Uncensored-Flawless-Peymandc](https://huggingface.co/Peymandc/MiniCPM5-1B-Uncensored-Flawless-Peymandc/tree/f6d05b4391b4a35b3b07a31f3d36e70e34fd5834) | 16ファイル・2,174,627,424 byte | **P0、次期CONDITIONAL昇格を推薦**。元MiniCPM5-1B 1.0806BからHeretic2.1 ARA編集した新しいBF16全重み。作者の拒否キーワード81/100→3/100、KL0.0070。ただし中立品質、Tool calling、日本語、中国語、長文性能を独立再評価していない。 |
| [NuclearDorfus/Luciole-1B-Instruct-1.1-Heretic](https://huggingface.co/NuclearDorfus/Luciole-1B-Instruct-1.1-Heretic/tree/b5e8bf34650ec6fc0aed2028758791905cef74cf) | 8ファイル・2,648,259,206 byte | **P1 HOLD**。フランス語系Nemotronの独立拒否編集。作者は拒否100/100→0/100を示すがKL0.4199と変化大。フランス語・中立タスクの再現試験なし。LICENSE実体なし。 |
| [Peymandc/LFM3-1.7B-Heretic-Uncensored](https://huggingface.co/Peymandc/LFM3-1.7B-Heretic-Uncensored/tree/72c1fa3b225c4663f9de0a682d6909cc14599125) | 19ファイル・3,476,041,387 byte | **P2 HOLD**。LiquidAIのLFM3ハイブリッド約1.729B原本、拒否98/100→3/100、KL0.0732は著者値。LFM1.0（license:other）とカスタムモデルPython3ファイルの権利・ABI未確認。 |
| [Sussysam/Qwen3-4B-Instruct-2507-heretic](https://huggingface.co/Sussysam/Qwen3-4B-Instruct-2507-heretic/tree/1df0100e297aa073f65e9295054e3ce235800f27) | 10ファイル・8,056,453,418 byte | **フル重み取得を非推奨**。一般Qwen系の大きな重複候補。作者拒否100/100→3/100に対しKL1.5593、編集後の中立性能やTool品質なし。 |

[4モデルと親のPublisher SHA固定](../../manifests/drafts/r168-2026-11-27-four-small-uncensored-source-frozen.candidate.json) ／ [未承認の研究順位キュー](../../queues/proposed-v73-r168-four-small-uncensored-ranked-UNAPPROVED.json) ／ [決定・安全修復の機械可読根拠](../../catalog/decisions/2026-11-27-r168-v73-small-uncensored-priority-and-false-approval-repair.json)。

異なるモデル間でKLの絶対値が共通の品質尺度になるとは限らない。上記はそれぞれの作者が対応する親に対して測った値であり、同一評価データ・tokenizer、第三者の再現がない。拒否キーワードの検出件数が少ないことも、回答が有益、安全、正確ということを意味しない。多数の最適化trialから最良のモデルを選ぶことによる過適合も要注意。

### 既取得親の重複防止

P0の再現設定が固定したopenbmb/MiniCPM5-1Bのcommit ac83f813ba7da263c51a9f3ec37c2072597e54afは、133件の取得台帳にある親の固定commitと同じ。編集後model.safetensorsと親のweight SHAは異なり、新しい編集状態の保存価値はある。**元親を再度2GB取得する必要はない**。ただしHeretic設定、GPU/torch、bnb4bit、tokenizerが記録されてもbit-exact再演算できる保証がないため、P0は編集後フルBF16 checkpointを保存原本として推薦する。本人の許可前には取得しない。

Luciole、LFM3、Qwen3-4Bの親は今回の133 VERIFIEDには含まれず、編集済み全重みの独立アーカイブと依存コードを区別する。

## 4.〈応用・転用例〉容量と実装

\[
 B_{\mathrm{four}}=B_{\mathrm{Mini}}+B_{\mathrm{Luciole}}+B_{\mathrm{LFM}}+B_{\mathrm{Qwen}}
 =2{,}174{,}627{,}424+2{,}648{,}259{,}206+3{,}476{,}041{,}387+8{,}056{,}453{,}418
 =16{,}355{,}381{,}435\ \mathrm{B}.
\]

| 記号 | 意味（日本語） | 単位（SI） | 定義 | 定義域・前提条件 | 型 |
|---|---|---|---|---|---|
| \(B_{\mathrm{four}}\) | 4原本すべての公開元参照バイト | B（byte） | 4項の和 | 非負整数、実所有者Dの純増容量ではない | 整数スカラー |
| \(B_{\mathrm{Mini}}\) | MiniCPM5-1B編集版全16ファイル | B | 2,174,627,424 | P0未承認 | 整数スカラー |
| \(B_{\mathrm{Luciole}}\) | Luciole編集版全8ファイル | B | 2,648,259,206 | HOLD | 整数スカラー |
| \(B_{\mathrm{LFM}}\) | LFM3編集版全19ファイル | B | 3,476,041,387 | LFM1.0とcustom code審査前 | 整数スカラー |
| \(B_{\mathrm{Qwen}}\) | Qwen3-4B編集版全10ファイル | B | 8,056,453,418 | full重み取得を非推奨 | 整数スカラー |

**次元チェック**：すべてbyte同士を加算した結果がbyteである。Publisher全原本バイトとOwner HDDの現在空き、量子化zero point・scale、cache/staging、推論VRAMは同義ではない。

**実装前提**：P0はLlamaForCausalLM、PyTorch、Transformers、tokenizer、長文KVメモリ、編集再現時にはPEFT/Hereticとbnb_4bit系実装。LucioleはNemotron互換実装、LFM3はcustom modeling_lfm3/lfm3_conv/configurationの安全監査、Qwenの編集後Tool/中立課題の独立評価が必要。作者コードの実行・モデルの転送は今回行っていない。

## 5. H／T／D／C／U と ERROR CHECK

**H**：既取得親1.08Bと独立編集済み2.174GBの全checkpointを別保存すれば、汎用8GB Qwen編集より小容量で異なる低拒否状態を保全できる。ただし低KLが中立性能の維持を保証するわけではない。

**T**：公開元4repo全53path／bytes／OID／LFS SHA、親固定コミットと133台帳、旧117ハッシュの不変性、v73合成承認遮断の独立テストを実施。今後は未使用の中立・コード・日本語・中国語・Tool各200題以上で同一評価手法を事前登録。速度は同一CPU/GPU・clock・batch1・Torch/Transformers/CUDA/量子化scale・zero-point・context長で最低30反復、中央値とばらつき。最小n以前で恣意的逐次停止をしない。

**D**：出版社SHA・親の非重複、旧117記録不変、合成承認の遮断はSTATIC PASS。所有者の用途別権利、HDD現物SHAと最低200GB空き床＋staging、完全offline runtime、各scopeへの本人明示許可がそろうまでDOWNLOAD STOP。偽承認、SHA不一致、無審査モデルコード実行、権利不成立はFAIL。

**C**：MiniCPM編集後の中立課題・Tool性能が悪化するかもしれない。元モデル＋将来のARA再演算で編集状態を復元できる可能性もある。Lucioleの言語多様性やLFM3のエッジ性能が測定後に優位となる可能性も否定しない。

**U**：著者n100拒否キーワード指標と1000 trialの選択バイアス、親と編集版の実装ABIや依存、owner D実体、利用権。独立反復測定がないため合成標準不確かさ\(u_c\)と包含係数\(k\)は算定不能。

学際的関連：暗号学的原本と承認経路の監査、モデル編集とアラインメント、統計的過適合の評価、ABI・GPUエンジニアリング、フランス語・多言語ML、知財・輸出管理。米BISの旧AI weight ECCN4E091撤回は、今後の全ローカルモデルの保有禁止を証明するものではない。

### ERROR CHECK

現行v73の265登録・211有効、取得台帳133 VERIFIEDの内容を変更しない。既取得親の再取得なし。未承認ファイルから本人許可を生成しない。合成承認の旧v73識別子は実行側でも拒否。モデル重量DL、Owner Dの変更、作者コード実行、新規承認はいずれも0。

## 6.〈次に考える問い〉

**配布が将来停止した際、既取得親と編集レシピだけでbit-exactに無検閲状態を再現できるか。それが未検証なら2.174GBの編集済みフル原本を別に保持すべきではないか。**

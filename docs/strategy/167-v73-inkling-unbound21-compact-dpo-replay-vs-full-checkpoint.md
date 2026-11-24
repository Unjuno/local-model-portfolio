# R167／v73（2026-11-25）—無検閲モデルの収集方向を修正：Inkling 2 Mini Unbound v2.1独自SFT＋DPO学習stateを、既取得親を再利用する16ファイルの再構築ソースでCONDITIONAL選定

## 1. 本論・結論

現行v72の264登録／210有効（SELECT56／CONDITIONAL154／HOLD35）を保持し、`nokeepai/Inkling-2-Mini-Unbound` **v2.1** を新しい独立後学習成果としてv73に1件CONDITIONAL追加する。v73は**265登録／211有効・CONDITIONAL155／HOLD35**。これは危険な出力を可能にする性能の証明でも、実際のダウンロード許可でもない。

保存目的は、単純な拒否方向の除去に留まらず、モデル自身の出力に対する**後続SFT＋DPO**を行った**別の学習済み状態**をアーカイブすること。すでに選定・過去の取得報告に存在する`thinkingmachines/Inkling-2-Mini`原版との重み再利用を優先し、さらにもう1件20GB級のマージ済み重みを無条件に取得することを避ける。

- [Publisher原本（固定rev `ef74b44edd2851b8e8d221a7313f36c419590430`）](https://huggingface.co/nokeepai/Inkling-2-Mini-Unbound/tree/ef74b44edd2851b8e8d221a7313f36c419590430)：**98ファイル／20,696,238,628byte**。Hugging Face cursor付きメタデータ一覧を3ページ最後まで取得し、39件のLFS SHA256と各path/Git OID／sizeを固定。重みペイロードは未取得。
- [選定した16ファイル・再学習差分の公開元SHA一覧](../../manifests/drafts/r167-2026-11-25-inkling2-mini-unbound-v21-compact-3stage-replay-scope.candidate.json)：**141,452,942byte**。`abliteration/edit.pt`（821,297byte）＋適用用Python source／manifest、v2 SFTのLoRA（35,033,840byte）、v2.1 SFT＋DPO後のLoRA（105,026,408byte）、training/adapter config・README・Publisher固有manifestを含む。
- [正式選定差分](../../catalog/revisions/v73-2026-11-25.json)、[判断・留保の機械可読記録](../../catalog/decisions/2026-11-25-r167-v73-inkling-unbound-v21-three-stage-compact-source.json)、[全211取得STOP台帳](../../catalog/readiness/v73-2026-11-25-r167-all211-gates.json)。

**重要**：この16ファイルは単体で起動できるモデルではない。`thinkingmachines/Inkling-2-Mini`の原本及び再構築コードが必須。公開元は編集の再現性を主張するが、指定の16ファイルと所有者実媒体から、**最終重みSHAをビット単位で再現できることはまだ独立検証されていない**。ダウンロードREADY判定は不可。

## 2. 親を再転送しない理由と、LoRA近似を誤採用しない理由

Publisherカードの学習元は`thinkingmachines/Inkling-2-Mini@ed40e7da625f594fc9c4990f5f66be24873c22d7`、現在の過去取得VERIFIED報告の親は`thinkingmachines/Inkling-2-Mini@1fb4134b9a74f9681054f4ef82e4bf1f458a2337`。両コミットのファイルpathと発行者Git OIDは**14中13一致**、残る`config.json`はkey `dtype=bfloat16`追加と報告され、重要な**main／MTP／TokenizerのLFS SHA256は一致**。これはR166の独立metadata監査を再照合した結果である。所有者HDD上の実ハッシュには改めてアクセスしておらず、現在のモデル実在を保証するものではない。

`lora_v2.1/peft-r64`には**140,030,976byteのPEFT近似原本**があるが、これは全重み差分のSVD近似であり、作者自身が**full v2.1比KLD 0.0033**と報告。**正確な最終学習状態ではない**。研究上の軽量運用代替として残し、正式な独立stateをもう一つ増やしたり、正確な3段階ソースと入れ替えたりはしない。

他の無検閲派生（`OpenUncensored/Inkling-2-Mini-Uncensored`、`dealignai/Inkling-2-Mini-UNCENSORED-NVFP4`）も固定ソースを調べた。前者は約20.192GBの別refusal編集で、既存の同作者`OpenUncensored/...Uncensored-LoRA`との過剰な重複収集を避ける。後者はDealignAI Community Model License 0.3であり、Apache2.0原版だけを見て再配布可能とみなさない。**いずれも追加保存はHOLD**。

## 3. 容量、親の再利用と実HDDの違い

| 記号 | 日本語の意味 | SI単位 | 定義 | 定義域・前提条件 | 型 |
|---|---|---|---|---|---|
| \(B_F\) | Unbound v2.1 Publisher公開元全体の参照容量 | byte | 固定98ファイルの全和 | 0以上の整数、実媒体増分ではない | 整数スカラー |
| \(B_P\) | 選んだ三段階編集・SFT・DPO復元情報の参照容量 | byte | 固定16ファイルの和 | 0以上の整数、親は別途必要 | 整数スカラー |
| \(B_A\) | 全Publisher公開元と16ファイルscopeの差 | byte | \(B_F-B_P\) | 非負、節約実測値ではない | 整数スカラー |

\[
B_A=B_F-B_P=20,696,238,628-141,452,942=20,554,785,686\ \mathrm{byte}.
\]

**次元／単位チェック**：byte−byte＝byte。十進20.55GBはPublisherの*選択外参照容量*であり、実機の節約量ではない。Parentの実在、キャッシュ/ステージング、PEFT/torch/runtime、差分での最終再構築の成否は別途検証が必要。最大4TB・最低200GB空きの正本制限は変更しない。

## 4. 品質・権利・runtimeに関する負の証拠

Publisherの測定条件は、**llama.cpp `19bc41dbb`、Q8_0、greedy（温度の異なる系列は別）、考察上限4096トークン、263件の未使用評価プロンプト**と報告している。作者の判定基準で役立つ回答はthinking off **83.7% [79.1, 87.8]**、on **85.2% [80.6, 89.4]**。MMLU-300は74.3（原版76.3）で確かな優位を証明しない。**自己蒸留の選別に用いたJev判定器が性能測定にも関わるため、独立同条件の自分自身の評価と同一視しない**。作者は別判定器Bisonでも順位を検査しているが、所有者のGPU型・クロック・バッチ・量子化backend・KV条件は不明。16.1%〜22.1%のthinking loop問題も報告されている。長文、画像、コード、実行ツール能力のv2.1独立ベンチは未実施。

PublisherモデルカードはApache-2.0だが、**原版のThinking Machines Acceptable Use Policyも適用**と明記。後学習差分の研究価値は、違法利用に対する許可や利用規約からの免除を意味しない。[Publisher公式モデルカード](https://huggingface.co/nokeepai/Inkling-2-Mini-Unbound)。外部[GitHub再現コード](https://github.com/nokeepai/inkling-2-mini-unbound/tree/b4a63660a178872ac1f8c63c4b01dfd6d4d46297)は固定revision `b4a63660...` と補助コードのGit OIDを記録したが、**コードrootにLICENSEは確認できず、全依存wheel/コンパイラ/ABIも未固定**。`edit.pt`は任意Pythonオブジェクトの危険な逆シリアライズを誘発し得るため、独立審査前に`torch.load`等で安易に読み込まない。

## 5. 合否の再現性設計（H／T／D／C／U）

**H（反証可能）**：既取得報告のある原版20.192GBを再利用し、16ファイル141.45MBの編集＋SFT＋DPO段階を固定すれば、同じ親を重複取得せず新しい独立後学習結果を復元できる可能性がある。

**T（最小検証）**：不変98ファイル＋16選定ファイル＋3主要LFS SHA・親前後14ファイルの13ファイルGit OID同一性を確認。必要コード/ライセンスの静的監査を行い、ownerHDD実SHA照合後、保護環境で段階的に編集出力の各tensor SHAをPublished `MANIFEST.json`と比較する。実機性能は同一GPU型・clock・backend/ABI・context・batch・KV/量子化zero-point条件で30反復以上、固定100問以上を推奨。owner実測は未実行。

**D**：原本Publisher SHA・選定16ファイル・親Publisher SHA共通・既取得IDの非重複・旧264資産保持・全211取得STOPは**PASS**。実験なしで16ファイルを単体モデルと主張、近似PEFT LoRAを完全一致、AUPやコード権利を無視したDL実行なら**FAIL**。現物、法的行為、再現された重み、GPU品質は**UNCERTAINで取得STOP**。

**C**：stage replayがBF16丸めで一致しない、作者の自己評価にバイアス、無検閲後学習が通常言語推論を悪化、親の実ファイルが実は不完全、AUPや依存コード権利が目標と衝突する。

**U**：公開元のみのSHA／性能情報、OWNER物理媒体、PyTorch pickling安全性、マージ演算float64/bfloat16、`lora`量子化適用範囲、SGLang/Transformers/llama.cpp commit、lawful intended act。測定分散未取得のため合成標準不確かさ\(u_c\)と包含係数\(k\)は算定不能。

**ERROR CHECK**：v72の264登録／210有効は不変更、v73**265登録／211有効／SELECT56・CONDITIONAL155・HOLD35**、既取得モデル親の再転送0、本人モデルDL承認0、モデル重みDL0、未審査外部実行コード0、OWNER実HDDの今回SHA0。

学際性：独立ポストトレーニング/アラインメント、暗号学的重複排除とデジタルアーカイブ、実験統計・LLM判定器のバイアス、Pythonシリアライゼーションとライセンス/AUPの法的要件。

###〈次に考える問い〉

**手持ち親モデルの正しい重みを再利用できることを実機で確認するまで、新しい20GBの編集済みフルモデルを取得する必要があるか。** 当面は必須差分の固定と権利・復元条件の検証を優先し、作者マージ済みフル原本を研究代替として保持する。

# Underdog AI / ConwayResearch 保存候補監査（2026-11-11）

> 指定ブランチ strategy/2026-11-03-01-risk。基準 1b38a156567e43bd921845cc8f289c0ebee36c3a。v27=173件/有効126件、承認0件を維持。取得、インストール、モデル実行は未実施。

## 1. 〈本論〉選定結果

音声AIの独立学習と端末再現性に価値。現行v27の通常量子化を無条件に追加しない。

| 資産 | 研究優先 | 全ファイル容量（B） | 権利 | 固定revision先頭 |
|---|---|---:|---|---|
| [ConwayResearch/Underdog-Woof-Japanese](https://huggingface.co/ConwayResearch/Underdog-Woof-Japanese) | P0 | 43,835,158 | underdog-non-commercial-1.0 | 2814985816be |
| [ConwayResearch/Underdog-Woof](https://huggingface.co/ConwayResearch/Underdog-Woof) | P1 | 45,258,148 | underdog-non-commercial-1.0 | be7029605397 |
| [ConwayResearch/Underdog-Bark-3.0-Clean](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0-Clean) | P1 | 180,405,622 | cc-by-nc-4.0 | 73775471a941 |
| [ConwayResearch/Underdog-Bark-3.0-Pro](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0-Pro) | P1 | 2,490,403,398 | cc-by-nc-4.0 | d87f288a9a0b |
| [ConwayResearch/Underdog-Bark-3.0-Plus](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0-Plus) | P2 | 591,247,778 | cc-by-nc-4.0 | 28a7d4234146 |
| [ConwayResearch/Underdog-Bark-3.0](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0) | P3 | 567,508,081 | cc-by-nc-4.0 | e7a641c0fdd4 |
| [ConwayResearch/Underdog-Saluki-27B-1.0](https://huggingface.co/ConwayResearch/Underdog-Saluki-27B-1.0) | P2 | 9,455,260,760 | cc-by-nc-4.0 | 442e28ec9d89 |
| [ConwayResearch/Underdog-Poodle-4B](https://huggingface.co/ConwayResearch/Underdog-Poodle-4B) | P2 | 12,404,368,132 | cc-by-nc-4.0 | 2ed6b9e2ee5a |

第1研究群：Woof Japanese、Woof English、Bark Clean、Bark Pro。Bark Plusは端末圧縮の価値を実測してから、Bark baseは現行Plusより明確な優位がなければDROP候補。Poodle 4BはQwen3.5-4Bの別後学習として保留。Salukiは主にQwen3.8-27Bの低bit量子化であり、既存同系列が多いので重複検証を優先。

## 2. 公開後ライセンス変更の現物確認

Saluki初回revision 903e38e7b8ea4976404a7c3b963480e76d1a25cc のREADMEにはApache-2.0、現行revision 442e28ec9d89d9e732ddea2f0b9e017db20730a8にはCC BY-NC 4.0。11月5日のライセンス更新は既存Git履歴上確認済。
本体GGUFは両revisionとも 7,898,369,152 B、同じLFS SHA256: 4a673518b11b1c4445f9b9a9d3c40356f5ba39f6a6260dcb25f3fbfd475d9efb。つまり重みが同一でも付属契約/NOTICEが変更された。遡及的な契約効力は未確認であり、どちらか一方を合法的に取得済みとみなさない。
旧README https://huggingface.co/ConwayResearch/Underdog-Saluki-27B-1.0/blob/903e38e7b8ea4976404a7c3b963480e76d1a25cc/README.md
新README https://huggingface.co/ConwayResearch/Underdog-Saluki-27B-1.0/blob/442e28ec9d89d9e732ddea2f0b9e017db20730a8/README.md

## 3. 学習済み独立性・代替性・実行依存

Woof Japaneseは2声、重み 40,512,554 B。必要ランタイムはNumPy>=1.24、pyopenjtalk-plus>=0.4、日本語辞書。作者M5 Max単一CPUスレッドで14.5x、437MB RSSは6文×3回の測定値で独立追試なし。
Woof Englishは2声、重み 40,595,426 B。作者の学習済み総数38.24Mは復号器を含む公称であり実体テンソルの検算なし。v27のPhonon31mとの比較が必要。
Woofの両言語版はTTSであり、Sophon・MiniCPM-oのような全二重対話モデルそのものではない。
Bark ProのBF16主重み 1,254,196,636 B、HF公開safetensorsは627,057,286。CoreMLも同じリポジトリに含むので両形式を無条件に重複保存しない。
Bark CleanはPlusからのフィラー・言い直し除去向け追加学習で、別ハッシュを持つ。メーカー自己評価のWERは評価用参照文の作りが異なるため、Pro/Plus/Cleanを同じ列で単純ランキングしない。
Poodleは4.66B程度のQwen3.5-4B後学習済みエージェントモデル。BF16とMLXの2形式を混ぜて12.4GBすべて選定するのは過剰。Salukiは元のISTA-DASLab低bit量子化の再加工で独立のフル学習成果は未証明。

## 4. 権利・ベンチマーク

Woofのライセンスは独自Underdog Non-Commercial License 1.0。非商用での表示、商用別契約、音声または重みによる他の音声AIの再学習禁止などの条件がある。日本語モデルのNOTICEはEmilia（CC BY-NC 4.0）利用も明示する。個別利用の適法性と本人承認を確認せず取得しない。
Woof Japaneseの日本語446文（281難例、165日常）の仮名誤り率は作者計測で、原文とASR書き起こしの双方をOpen JTalkで仮名化する。発声の自然性、韻律、方言、長文の評価ではない。Englishも500文での作者WER。
Bark Proの7英語セット平均WER4.286%とHojo4.291%の差は0.005百分率ポイント。作者測定は公式リーダーボード提出結果ではなく、統計的不確かさも不明なので最強と断定しない。

## 5. 容量・固定ソース・停止条件

v27既知source-only 3,417,685,712,585 B。Woof両repo LFS hash重複除外 89,093,306 B。優先4repo丸ごとの既知source-only上界は 2,759,741,850 B。v27に全追加した算術上界 3,420,445,454,435 B。
8repo全ファイル名・公開LFS payload SHA256・非LFS Git blob SHA1・40字revisionは機械可読JSONに格納。Git blob SHA1と実体SHA256を混同しない。現物重みのローカルハッシュ検証は0件。
追加容量は外部辞書、pip wheels、CoreML/MLX展開、Python/OS環境、実機の空き、既存v27との全ファイル重複まで包含していない。4TB上限と200GB床への実機PASSは未判定。
停止条件：モデル総学習済み数未確定、license/商用権未承認、本人ディスク未実測、全ソースハッシュ未検証、runtime ABIと辞書未固定、具体的取得マニフェストの本人承認なし。

## 6. H/T/D/C/UとERROR CHECK

H: Woof/独立学習済みBarkモデルは、v27で同用途を持つモデルと異なる復元価値を持つ。モデル重み系譜、公開SHA、独立の日本語音質評価・ASR WER・実機RAMと再現性で反証可能。
T: 8repo全ツリーを固定revisionで非実行監査。独立性能試験は本人の取得/実行承認後、同HW・OS・クロック・バッチ・コンテキスト・辞書・ABIで最低30例/条件。
D: ファイル数・バイト・公開LFS SHA・Salukiの旧/新同一重みhashは静的PASS。性能/権利/実機容量/完全復元はUNCERTAIN、取得不承認。
C: 作者ベンチ非再現、日本語辞書更新と表記揺れ、変換前後の精度差、非商用契約、LLM元重みとの機能重複。
U: 実機disk・依存辞書と環境・モデルのzip内全tensor数・地域/使用目的による権利・品質の推定分布が未測定。合成標準不確かさu_cと包含係数kは現時点で算定不可。
ERROR CHECK: 14件の静的チェックすべてPASS。v27未変更、承認0、モデル重み取得0。

## 7.〈次に考える問い〉

日本語CPU TTSの独立学習成果を、量子化が主体の巨大Qwen派生より優先して保全する基準を、モデル容量当たりの再現性/学習価値/適法性でどう定量化するか。

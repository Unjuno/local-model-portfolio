# R108 — v46原本選定・無検閲モデル・小型専門モデルのファイル確定（2026-11-18）

## 1.〈本論〉
v45の198資産/151 active（53 SELECT, 98 CONDITIONAL）は、独自学習済み成果の保全という目的に合致するため**1件も根拠なく降格・入替・削除しない**。今回のv46は、Hugging Face第一配布元から**12件の不変リビジョンと選択ファイルSHA**を照合し、現行正本の記録を修正する「**保存対象ファイル内容の確定**」である。所有者のアクセス権限・HDD・オフライン復元が未確定なので、**実ダウンロード承認は0件**。

[全151件の判定表](../../catalog/decisions/2026-11-18-r107-151-asset-preservation-and-download-gates.json) / [12件の逐一チェックサム付きsource manifest](../../manifests/drafts/r107-v45-12-original-sources-file-freeze.candidate.json) に保存した。データセット18件・モデル133件を含め、151全件を元の決定と保持。観測Gated20件、総数不明のactive9件は全て取得承認停止。

**ソース確定対象（byte数は配布元であり、実際に取得・検算した容量ではない）**

| モデル | ファイル数 | 公開元選択GB | 配布状態 | 残る個別条件 |
|---|---:|---:|---|---|
| [orcarouter/Qwen3.8-27B-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) | 31 | 55.586 | Gated | GATED_PERSONAL_ACCESS_NOT_VERIFIED |
| [InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF](https://huggingface.co/InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF) | 5 | 17.738 | 公開 | PUBLISHER_SOURCE_FROZEN |
| [0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF) | 4 | 17.177 | 公開 | SOURCE_SCOPE_CORRECT_RVN_WITH_EMBEDDED_TEMPLATE |
| [Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2](https://huggingface.co/Gryphe/Pantheon-Reasoning-26B-A4B-1.1-V2) | 12 | 53.122 | 公開 | LARGE_SOURCE_FROZEN_QUALITY_STILL_CONDITIONAL |
| [DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NM-DAU) | 25 | 55.590 | 公開 | LARGE_SOURCE_FROZEN_QUALITY_STILL_CONDITIONAL |
| [chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1) | 8 | 0.671 | 公開 | PARENT_RESEARCH_LICENSE_ACTION_REVIEW |
| [usezn/Galvanize-3](https://huggingface.co/usezn/Galvanize-3) | 9 | 0.597 | 公開 | PUBLISHER_SOURCE_FROZEN |
| [qvac/BotPsy-0.8B](https://huggingface.co/qvac/BotPsy-0.8B) | 11 | 1.726 | 公開 | PUBLISHER_SOURCE_FROZEN |
| [ibm-granite/granite-timeseries-ttm-r3](https://huggingface.co/ibm-granite/granite-timeseries-ttm-r3) | 5 | 0.006 | 公開 | PUBLISHER_SOURCE_FROZEN |
| [nvidia/Nemotron-3-Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization) | 11 | 0.397 | 公開 | OPENMDW_LICENSE_AND_ABI_REVIEW |
| [tencent/Qwen3.8-27B-DSpine-b16](https://huggingface.co/tencent/Qwen3.8-27B-DSpine-b16) | 5 | 4.052 | 公開 | TARGET_QWEN_VERSION_AND_RUNTIME_UNVERIFIED |
| [robbyant/lingbot-touch-tiny](https://huggingface.co/robbyant/lingbot-touch-tiny) | 5 | 0.022 | 公開 | SAFE_PT_RUNTIME_AND_EMBODIMENT_UNVERIFIED |

## 2. 交換を行った箇所と、行わなかった箇所
**0bserverx/Qwen3.8 Heretic/RVN**：作者の[README](https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF)は旧`Qwen3.8-27B-Heretic-Q4_K_M.gguf`を**legacy**と明記、RVNは2パス追加ARAによる別学習成果。現行台帳の提案ファイル名は**既にRVN-Q4 multilingual**だったため、これを無条件に他モデルへ交換したとは記載しない。ただし台帳の`chat_template.jinja`は実際の182ファイルの中に存在せず、chat templateはGGUFに埋め込まれている。v46では誤ったパスを削除し、別体の`mmproj-Qwen3.8-27B-Q8_0.gguf`を必要なら利用できる選択ファイルとして追加した。RVN-Q4多言語主重みの原本SHAとサイズ、およびprojectorを固定。旧Heretic/Q5/GGUFの全組合せを自動追加しない。強い拒否抑制性能の作者計測は**独立追試ではない**。

**InterpreticAI**：政治質問に対する過剰な回答拒否を選択的に編集した別目的の学習成果。作者報告の115問で100→4の政治回答抑制、危険な依頼への拒否を残したとする結果は**作者測定**であり、「無制限応答」と混同しない。正本で既に固定された`e6924b3a...`の2 GGUF SHAは現在の配布元の同名重みSHAと一致。余分な新リビジョン資料で重みを再ダウンロードしない。

**OrcaRouter**：55.586GBの全18 BF16 shardを配布元metadataで固定したが、HFは`gated:auto`。本人アカウントの利用条件受諾/アクセス認可が確認されるまで実ダウンロードしない。

**DavidAU / Gryphe**：いずれも独自の多段階SFT・RP/推論後学習成果を保全。ただし大型であり作者測定以外の同条件品質、統計区間、配布元LICENSE、運用時HW/clock/batch条件を計測するまで**conditional**からSELECTへ昇格しない。

**画像LoRA**：ChatRLabsはrank128の新しい重み差分だけを選定。Qwen Image 2.1親モデルを二重取得しない。固定版の`LICENSE`には**Qwen RESEARCH LICENSE（非商用）**の原文があり、Hugging Faceの`license:other`を「再配布自由」と解釈しない。

**小型・特殊専門モデル**：Galvanizeの元safetensorsとONNX翻訳版は同じ成果の別表現として扱い原本を優先。BotPsyは0.8Bツール呼出し後学習、TTM R3は約1.4M独立時系列Mixer、Nemotronは99M Sortformer話者分離原本、DSpineは親Qwenに必要な別学習draft、LingBotは独自触覚encoderの学習成果を保存。DSpineは一致親revisionと速度計測が必要、LingBotの`.pt`は安全なデシリアライゼーションを要求、NemotronはOpenMDW-1.1正文の利用条件が必要。

## 3.〈応用・転用例〉4TBの容量への影響
前回[R106容量監査](../strategy/106-v45-151-active-capacity-reconciliation-2026-11-18.md)は151件のsource代理値`3,732,164,752,962 byte`（約3.732TB）を出した。今回12件の選択元ファイルの公開元合計は`206,683,452,429 byte`だが、**12件とも既存151件に含まれるため加算しない**。特に0bserverx配布repo全量約1.645TBとRVN一式約17.177GBの差は、既に過去の16.56GB選別を部分的に行っていたため「いま新たに1.63TBの空きが出来た」という意味ではない。

実HDDのフォーマット後容量・残量、必須外部学習済み部品、コードwheelhouse、同一SHA重複、転送/展開領域を測らずに3.8TBへの物理合格を主張しない。計画上限4TB、常時空き200GB以上を維持する。

## 4. H/T/D/C/U
H：同一家族の通常変換版を減らし、無検閲・小型・特殊独立学習成果を原本1系列ずつ選ぶことで原本と依存のカバレッジが上がる。
T：v45有効151件、R107固定12件のHF出版社revision、保存ファイルSHA・LICENSE、実物ファイルリストを照合。モデルコード・ウエイトはダウンロード/実行しない。
D：151件一意の研究判定、12件source固定、RVN存在しないpathの修正、公開元LFS hash全選択重みに有る場合に選定研究PASS。**取得権利・実HDD・完全offline restoreはUNCERTAIN**。認可がなければダウンロードFAIL。
C：量子化の校正差で独立した能力が増す、親revision非互換、別学習codec必須、未検証ライセンスやHDD不足が生じれば選定/容量が破れる。
U：品質ベンチの独立性・HW/clock/batch・正確な物理バイト、推論バックエンドABI、第三者モデルライセンスが未確定。標準合成不確かさu_cや包含係数kは標本分布がなく算出できない。

**ERROR CHECK**：総198 ID、有効151（53 SELECT/98 CONDITIONAL）、研究source固定12、観測Gated20、有効パラメータ不明9、承認DL0。予算は十進byteで一貫。新たなGitHub branchなし、`main`のみ。

## 5.〈次に考える問い〉
安価な5〜700MB専門checkpointをさらに固定しつつ、最大200GB超の親モデルや同系列の重みを選ぶ根拠を、同条件の実際の性能・再取得不能性で定量的に区別できるか。

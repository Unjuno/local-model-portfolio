# R87（研究のみ）｜LTX-2.5特殊後学習モデル2件の原本優先・重複形式削減（2026-11-15）

**調査基準はv38-20261115（main）**。現行の`Stuubs/Stubelius_Remix_Ltx2.5`および`ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8`は**異なる学習済み改変の可能性があるため両方CONDITIONAL研究維持**。通常量子化を「別の強力モデル」と誤カウントしない。新規採用/交換/降格/取得承認はいずれも0。法的な配布制限の事実と将来規制予測は分離。

## 1. 公式ソースで確認した非重複の機構

| モデル | 公開者の改変説明（実体の識別） | 判定 |
|---|---|---|
| [Stuubs Remix](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/README.md?code=true) | LTX-2.3系Sulphur2/10Erosのtask-vector差をLTX-2.5へ層別注入。beta2でLoRA追加、v1でOmniNFT RL-LoRAも統合。[NOTICE provenance](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/commit/febb0f007e53b87e0859a2709eb044bec35b1e44)。配布者のAI判定48回はv1 29勝/旧beta2 9勝/引分10。独立品質評価とはしない | v1 BF16を**単一の優先原本候補**、追加形式は採用しない |
| [ChrisColeTech Uncensored v1.1](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8) | 作者カードはEros10やDMD/IC-LoRA系の複数学習差分をプリマージと説明。専用Gemma4-12B text encoderと別AV VAEを含む。権利メタデータは`unknown` | Stuubsへの**自動置換はしない**。別学習成果の可能性あり、親・複数donorのlicense/bytes/SHAを確認するまで研究のみ |

どちらもHFの`base_model:quantized`タグを持つが、`quantized`タグだけで**同一重みの単純量子化だと判断できない**。一方、作者の「性能改善」や「検閲除去」の宣伝だけでは独立能力を実証したことにもならない。

## 2. 保存対象を絞る原本ファイル監査

Stuubs配布元には旧beta1、旧beta2、最新版v1、INT8、NVFP4、GGUFが混在し、[repo表示は約196GB](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/tree/main)。[v1 BF16ファイル](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/ltx2.5-Stubelius_remix_v1_bf16.safetensors)には公開Xet SHA-256 `6e0ff9c9d8a1d0747579f1f50d10a9c3822a9a8f265322a5edd476044b0fbf4f`がある。**約42GBのこのファイルを原本候補1件**とし、int8 21.5GB・nvfp4 14.4GB・GGUF 12.5GB、旧betaの重みをデフォルト保存対象から外す。ただし**Xet上の公開SHAであり自分のHDDに保存したファイルのSHAではない**。

| 記号 | 意味 | SI準拠単位 | 定義・定義域・前提条件 | 型 |
|---|---|---|---|---|
| `B_r` | Stuubs repo全表示サイズ | byte | 約196×10⁹、表示丸め・全repo | 非負実数スカラー |
| `B_o` | 原本v1 BF16の公開表示サイズ | byte | 約42×10⁹、厳密byte未確認 | 非負実数スカラー |
| `B_d` | 全repo一括取得を避ける参考量 | byte | `B_r - B_o`、約154×10⁹。依存・付属小ファイルは別計上 | 非負実数スカラー |

導出：196GB − 42GB ≈ **154GB**。次元はbyte − byte = byteで整合。**これは将来のsource範囲候補の差であって既存HDD削減実績でも、実際の保存後空き容量でもない**。厳密bytes・40字revision・他のLICENSE/README/NOTICE、共通Gemma4 encoder・映像/音声VAE・runtimeコードは別に固定する。選択元1ファイルだけでオフライン起動できるとは主張しない。

## 3. 2026-10の権利変化と危険な見落とし

[Lightricksの現行`LICENSE-2_x`](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x)は冒頭に**2026-10-29 amended**と明記。LTX-2.xの派生モデルを対象にし、用途制限や一定規模以上の企業の商用利用条件を規定する。Stuubsには2026年1月版・現行版およびApache2.0の異なるdonor noticeが混在する。**最新版licenseを古いreleaseに機械的遡及適用する、逆に古い版だけが現在有効と断言する、の両方を避ける**。実際の本人の利用権限と各donor配布権の確認が必要。ChrisColeTechの`license:unknown`は無制限利用権を意味しない。次元の異なる各modelとライセンスをそれぞれ照合する。

## 4. H/T/D/C/UとERROR CHECK

**H**：2つの合成checkpointは少なくとも作者の説明上は異なる統合学習状態で、各repoの通常量子化形式は別学習成果ではない。  
**T**：n_min=2モデル・Lightricks原文license・Stuubs固定NOTICEとBF16公開SHAを検証。将来の昇格では同一版の全tensor/40桁commit/権利/依存と品質を測定する。  
**D**：Stuubsのv1 BF16公開SHAと複数形式の重複は**PASS（配布元の公開メタデータ）**、別モデル間のtensor非同一・利用権と最終manifestは**UNCERTAIN**、認可なくGatedや第三者配布を迂回するのは**FAIL**。  
**C**：両モデルが同一改変を共有する、非デフォルトbetaの独立研究価値が判明する、該当版licenseが異なる場合は方針を再評価。  
**U**：公開元のblob versionや表示GB丸め、直接tensor未閲覧、独立実機測定欠如、法的適用の未確定。分布がないため`u_c`・`k`は定量不可。

**ERROR CHECK**：既存2件研究維持／原本候補はStuubs v1 BF16 1ファイルと付属必須資料の準備のみ／新モデル0・モデル削除0・量子化重複追加0／モデル本体DL0／実行0／認可キュー0。詳細は[機械可読証拠](../../catalog/research/2026-11-15-ltx25-distinct-merge-scope-audit.json)。

学際接続：機械学習の後学習・モデル合成、デジタル保全の重複排除、ソフトウェア供給網のSHA証跡、ライセンス法。

## 5.〈次に考える問い〉

両方の合成チェックポイントを独立に残す根拠は、**入力出力の品質差**よりも、あとから再構成できない**学習済み差分そのもの**にあるか。

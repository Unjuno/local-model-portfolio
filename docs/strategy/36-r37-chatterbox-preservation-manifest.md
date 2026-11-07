# R37｜ChatterboxのV3・特化言語・Turbo/Nanoを学習済み重み単位で保存する

2026-11-08、**研究のみ**。現行v19でSELECTの`ResembleAI/chatterbox`の中身を見直した。既定選定53件／CONDITIONAL52件、4TB枠、Nanbeige4.3-33B SELECT、取得承認0件は変更しない。[固定9repo／各ファイルSHAの台帳](../../catalog/research/2026-11-08-r37-chatterbox-versioned-source-manifest.json)。

## 1. 〈本論〉— メンテナンス終了とV3の正しい読み込み方

[Resemble AI公式GitHub](https://github.com/resemble-ai/chatterbox/blob/master/README.md)は**2026年8月に研究が退役し、保守は終了**したと明記した。コードはMITライセンスの研究アーカイブとして残る。**重みの削除・Gated化が予告されたとは書かれていない**。将来の改修が期待できない状態は事実だが、保存禁止の予測とは別。

同READMEでは**Chatterbox Multilingual V3**が日本語を含む23言語の新しい推奨TTS。公式[src/chatterbox/mtl_tts.py](https://github.com/resemble-ai/chatterbox/blob/master/src/chatterbox/mtl_tts.py)は`from_pretrained(device, t3_model=None)`の既定を**V2**に設定する。V3を使うときは次のように明示する。

```python
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
tts = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
```

このコードは調査用の記法で、実行もインストールもしていない。**公式V3ローダーは`t3_mtl23ls_v3.safetensors`と従来の`s3gen.pt`を組み合わせて読む**。同repoの`s3gen_v3.pt`/`.safetensors`は別途配布されているが、元ローダーが自動でV3 S3Genをロードするわけではない。バージョン混在に注意。

## 2. V3の固定ファイル構成

HFコミット`5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18`の公開ファイル・ハッシュを使用。公式`allow_patterns`に合わせた6ファイルの合計は**3,208,951,924 byte**。組込み既定音声を使わない場合の`conds.pt`は任意だが、再現性を考えて含む。

| パス | byte | 配布元提示ハッシュ（weightはSHA-256） |
|---|---:|---|
| `t3_mtl23ls_v3.safetensors` | 2,143,989,928 | `5abca8321ede76f8e61f1cc0d19aea6c946b28871017ce8726f8a69203f05953` |
| `s3gen.pt` | 1,057,165,844 | `9b9ff07e60b20c136e2b1b3d7563a24604e8d2c4c267888d1ee929dd0151d2a3` |
| `ve.pt` | 5,698,626 | `4b16d836bc598509860f6fa068165a8bb5e9ac84f05582dfcf278a5a372879f1` |
| `grapheme_mtl_merged_expanded_v1.json` | 69,989 | Git blob／テキスト |
| `Cangjie5_TC.json` | 1,920,163 | Git blob／テキスト |
| `conds.pt` | 107,374 | `6552d70568833628ba019c6b03459e77fe71ca197d5c560cef9411bee9d87f4e` |

V3 T3は**2,143,989,928 byte**。V2 T3は**2,143,989,752 byte**で、新旧の追加学習の違いがあり、単にQ4とQ8の形式違いではない。V3の共有デコーダーや声encoderは再利用できるが、V2を加えるとT3重み分だけ**2.144GB**追加される。新版の独立した性能優位は作者の主張であり、長文と日本語の独立同条件評価は未完。

## 3. 合計9リポジトリ：保存対象と共有部品

| 正規配布元（完全な固定SHAのリンク） | repo全量 (byte) | 特化した学習成果・候補byte | 区分 |
|---|---:|---|---|
| [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox/tree/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18) | 13,866,212,931 | 3,208,951,924 byte（V3標準6ファイル） | MAIN_MULTILINGUAL_V2_V3 |
| [ResembleAI/Chatterbox-Multilingual-zh-cmn](https://huggingface.co/ResembleAI/Chatterbox-Multilingual-zh-cmn/tree/2432cb141088d54f666894996d959294a74a13ce) | 4,263,120,842 | 2,143,989,880 byte（独自T3） | LANGUAGE_ZH_CMN |
| [ResembleAI/Chatterbox-Multilingual-es-mx-latam](https://huggingface.co/ResembleAI/Chatterbox-Multilingual-es-mx-latam/tree/27e595bf2fe7be0533ca299d9afafcde08b7cca7) | 4,257,349,567 | 2,143,990,280 byte（独自T3） | LANGUAGE_ES_MX |
| [ResembleAI/Chatterbox-Multilingual-pt-br](https://huggingface.co/ResembleAI/Chatterbox-Multilingual-pt-br/tree/b3952f18bc2eaa72b9bd7c17d2c4653bcad4770d) | 4,257,349,523 | 2,143,990,296 byte（独自T3） | LANGUAGE_PT_BR |
| [ResembleAI/Chatterbox-Multilingual-es-es](https://huggingface.co/ResembleAI/Chatterbox-Multilingual-es-es/tree/7262b364e3222ba9446c9289e7485eadc47ed902) | 4,257,349,472 | 2,143,990,264 byte（独自T3） | LANGUAGE_ES_ES |
| [ResembleAI/Chatterbox-Multilingual-pt-pt](https://huggingface.co/ResembleAI/Chatterbox-Multilingual-pt-pt/tree/d728f1a01d7d2c634462ae33e8dd16fe56f6d874) | 4,257,349,528 | 2,143,990,296 byte（独自T3） | LANGUAGE_PT_PT |
| [ResembleAI/Chatterbox-Multilingual-hi](https://huggingface.co/ResembleAI/Chatterbox-Multilingual-hi/tree/82ca71273cc2a9ab19efdf8315f865c1a5af0ee7) | 4,257,349,363 | 2,143,990,224 byte（独自T3） | LANGUAGE_HI |
| [ResembleAI/chatterbox-turbo](https://huggingface.co/ResembleAI/chatterbox-turbo/tree/749d1c1a46eb10492095d68fbcf55691ccf137cd) | 4,044,184,736 | 1,915,480,052 byte（独自T3） | TURBO_EN_350M |
| [ResembleAI/chatterbox-nano](https://huggingface.co/ResembleAI/chatterbox-nano/tree/71ccd1d0081b430592cea481f4307e764e07bc64) | 2,998,605,148 | 869,899,204 byte（独自T3） | NANO_EN_110M |

**六つの言語特化版は同じモデルの単純量子化ではない**：中国語、メキシコ向けスペイン語、ブラジル向けポルトガル語、スペイン向けスペイン語、ポルトガル向けポルトガル語、ヒンディー語の**各T3重みSHAはすべて異なる**。日本語専用の言語パックはこの6件に含まれない。日本語は多言語V3で検証する。

一方、6言語repoが持つ`s3gen_v3.pt`は**同一SHA256**、`s3gen_v3.safetensors`も**同一SHA256**。6件を全部丸ごと保存すると**25,549,868,295 byte**。6つの異なるT3重みをすべて残し、S3Gen V3 `.pt`を1回だけ持つ研究構成なら**13,920,844,934 byte**（必要な声Encoder/条件データ/コードは別）。モデルの学習成果を損なわず、共通デコーダーを6回重複保存しない案となる。

**TurboとNano**は500M級の多言語V3を通常量子化したものではなく、英語の低遅延用独自T3。Turbo T3とNano T3は異なるSHA、MeanFlow 1-stepデコーダー`s3gen_meanflow.safetensors`と声encoderは2repo間で**同一SHA**。公式[tts_turbo.py](https://github.com/resemble-ai/chatterbox/blob/master/src/chatterbox/tts_turbo.py)が読んでいるのはMeanFlowデコーダーで、repoにある別の`s3gen.safetensors`はそのローダーからは読み込まれない。両モデルの独自T3＋MeanFlow 1つで**3,850,254,292 byte**。Tokenizer・任意`conds.pt`や環境は別途必要。省容量でもNanoにはCPU推論など別用途の価値がある。

## 4. 保存判断と否定証拠

**既存Chatterbox SELECTの具体的な第一候補はV3**。旧V2は前段学習の比較、独自の失敗例の再現など、用途があれば別に保持可能。6言語パックは地域訛り・音質改善の独立学習を保存できるが、**作者以外の同一プロンプト比較を確認できないため全件を自動採用しない**。Turbo/Nanoは英語低遅延・CPU端末という別のトレードオフとして研究する。

独立した[5言語のTTS比較](https://soniqo.audio/blog/voice-cloning-benchmarks)はあるが、**固定V3対V2の日本語を含む直接対照ではない**。その数値をV3の優位性の確証として記録しない。コードのfullコミットとPython・PyTorch・CUDA/Metal/CPU・safetensors・perth/watermark・phonemizer等のABIと参照音声の利用許諾を別に固定する必要がある。`.pt`はTorch pickleベースで、公式では`torch.load(weights_only=True)`だが、外部コードの安全性確認なしに実行しない。

## 5. H/T/D/C/U・変数表と次元検査

| 記号 | 意味 | 単位（SI） | 定義・条件・型 |
|---|---|---|---|
| B_V3 | V3を公式ローダーで再現する6ファイル容量 | byte | 3,208,951,924、非負整数スカラー。外部実行環境は除く |
| B_T3 | 特化版T3重みの容量 | byte | 個別固定SHAに基づく各重み容量、非負整数スカラー |
| B_S3 | 共有S3Gen V3ファイル容量 | byte | `.pt`代表1,056,903,694、非負整数スカラー |
| N_lang | 言語特化モデル数 | 1 | 6、整数スカラー |
| N_case | 品質比較の独立音声例 | 1 | 日本語/英語の各200例を暫定目標、整数スカラー |
| R_peak | 実機RAMピーク | byte | CPU・GPU・OS・buffer・codec込み、未測定はnull |

**H**：別学習のT3は異なる機能を持ちうるが、共通S3Genの二重取得は品質を高めない。**T**：独立話者（同意済み）、日本語・英語の各200文、3種のseed、共通音声・ローダー・HW/clock/backend・context/batch、話者類似度/ASR-CER・破綻率・RTFを対照測定。**D**：地域音韻・低遅延・一般品質でV3より明確な改善なら特殊版を保存審査PASS、単なる同一SHAの複製取得はFAIL。未測定はUNCERTAIN。**C**：v3という名前でもV2がデフォルト、S3Gen V3と旧S3Genの組み合わせ不一致、`.pt`と`.safetensors`の未検証数値同等性、声の参照権利の誤認。**U**：品質比較・環境・話者/言語の誤差が未測定でu_cと包含係数kは未算定。**次元確認**：B_V3/B_T3/B_S3/R_peakはbyte、N_lang/N_caseは個数で無次元。RAMと保存byteは同単位でも別。

## 6. ERROR CHECKと〈次に考える問い〉

**ERROR CHECK**：9リポジトリの40文字固定SHA、公式V3の6ファイル合計、6つの異なる言語T3のSHA、共通S3Gen・Turbo/Nano共有MeanFlowのSHAとbyteを一致検査。取得承認0・重みDL0、正式150資産の状態不変。

**学際性**：多言語音声工学（訛り・話者同一性）、統計/品質評価（日本語CER・非対応の検出）、数値ソフトウェア（shared decoder/ABI）、デジタル保存（退役研究ソースの系譜）、権利（同意済み音声）に転用。

**問い**：高精度の一般V3を先に保管した後、6言語特化版のうちどの音韻・地域差がV3では再現できず、別の学習済み重みを保存する理由になるか。

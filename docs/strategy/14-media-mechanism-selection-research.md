# 追加推薦：画像LoRA・声質変換・編集可能な音声（2026-11-04）

## 反映範囲

これは調査資料と候補差分の追加である。**現行v17の142資産・有効研究選定97件は変更していない。** 自動書き戻しワークフロー、実行コード、権限変更を含めない。モデル取得・推論・Torrent・ローカルHDD操作は行っていない。

[候補JSON](../../catalog/proposals/18-media-mechanism-selection-2026-11-04.json)に一次資料、負の証拠、ファイル識別情報を記録した。

## 今回の追加推薦3件

| repo ID | 追加する能力 | 判断と弱点 |
|---|---|---|
| `chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1` | ネイティブ画像生成/編集LoRA。既存のQwen-Image-2.1を再利用 | 条件付き研究選定を推薦。実際のrank128学習とファイルを確認。独立画質比較は未完 |
| `laion/Humaneness-Voice-Converter` | 元音声の演技・感情を残す声質変換。通常TTSとは別 | 条件付き研究選定を推薦。感情代理指標は改善するが、話者一致は低下。日本語と独立MOS/WERは未検証 |
| `fishaudio/drama-3` | 音声の部分編集、自然言語による再演出、多話者シーン | 条件付き研究選定を推薦。全35.8996B級モデルで、活性3Bだけで小型扱いしない。ローカルRAM/速度は未確認 |

### 1. ChatR Labs：小さい追加学習成果を優先

[作者GitHub](https://github.com/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA)、[HF](https://huggingface.co/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1)、[Release API](https://api.github.com/repos/chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA/releases/tags/v0.1)を確認した。

GitHub asset ID `659921001`、重み`chatrlabs-omni-lora-v0.1-bf16.safetensors`、配布元記録は**671,151,136 bytes**、SHA256 `5991a9845bc5251240febf944f653505a00966515b77073f2c639c4dfcba672a`。releaseは`immutable:false`。取得時にID・サイズ・ハッシュを再照合する。**配布元記録の確認であって、取得後のローカルハッシュ実測ではない。**

rank128・224モジュール・448 BF16テンソル・step32000。作者の基盤版は`790c92633540aa0cb11d9abf19eb46d861714758`。基盤・encoder・VAEの同一性が確認できる場合に既存ファイルを再利用する。671MBは実行一式の容量ではない。

Qwen Research Licenseの非商用研究・評価用途が記述されている。独立品質比較はなく、2枚のRTX4090での作者の個別動作時間を普遍的性能として扱わない。

### 2. Humaneness Voice Converter：有用性と劣化を両方記録

[モデル](https://huggingface.co/laion/Humaneness-Voice-Converter)、[再現記録](https://huggingface.co/laion/Humaneness-Voice-Converter/blob/main/REPRODUCING.md)、[速度測定](https://huggingface.co/laion/Humaneness-Voice-Converter/blob/main/SPEED.md)、[export証跡](https://huggingface.co/laion/Humaneness-Voice-Converter/blob/main/EXPORT_PROOF.json)を確認。

本体`model.safetensors`は作者証跡で**1,056,773,004 bytes**、SHA256 `45bbf058ea2a82f1840dc6161f01be929217d28843003f5354336c81b11ea3dd`。Ears、設定、依存を含む完全総容量ではない。LAION追加部分CC BY4.0、Chatterbox由来MITのNOTICEを保持する。

40音声×2対象話者の作者比較で感情MSE0.113→0.092、話者cosine0.821→0.773。報酬judge再利用・訓練データ重複・人の独立試験不足がある。英独中心で日本語保証はない。GH200120GB・BF16・10step・候補1つでは6.53秒入力の生成中央値0.558秒（3run）だが、前処理、ロード、ランキング、I/Oを除外した値である。

### 3. Drama3：ライセンスタグでなく本文を読む

[モデル](https://huggingface.co/fishaudio/drama-3)、[開発元コード](https://github.com/fishaudio/fish-speech/blob/main/docs/en/index.md)、[現在のLICENSE](https://huggingface.co/fishaudio/drama-3/blob/main/LICENSE)を確認。

README frontmatterはResearch License/`LICENSE.md`だが、現在のLICENSEは2026-10-13版Fish Audio Community License。SectionIIには研究・非商用用途の利用・複製等の許諾が条件付きで書かれている。タグotherを理由に除外しない。Hosted Service等は個人ローカル研究と別に審査する。

作者のH200速度表は事前符号化済み参照、Seed-TTS英語、concurrency1でTTFA p50 88.9ms/p95 90.8ms、平均RTF0.131。4run集計で、個人環境の速度保証ではない。全シャード、codec、FP8対応バックエンドの構成は未確定。

## 今回追加しないもの

[YueFongのUncensored GGUF](https://huggingface.co/YueFong/Qwen-Image-2.1-Uncensored-GGUF/blob/main/README.md)はoriginal upstream weightsの量子化と説明されている。追加学習の独自能力を示す証拠がないので、新規能力の枠には加えない。量子化形式として有用かどうかは別判断であり、全ファイルの同一性を実測したという主張ではない。

[Humaneness Voice Small](https://huggingface.co/laion/Humaneness-Voice-Small)は既存TTSと重複し、制御された品質比較が不足。今回は音声から音声への変換を優先する。

## H/T/D/C/Uと次の判定

H：既存で代替しにくい編集・変換能力が同条件比較で有用である。
T：画像LoRAは基盤単独との同seed、VCは同意済みの同じ音声対、Drama3はS2-Pro/Qwen TTSとの編集精度・声・遅延を比較。閾値を測定前に決める。
D：改善が再現され資源・権利・ファイル条件を満たせば実用採用。無効や顕著な劣化なら不採用。未実測はUNCERTAIN。
C：報酬への過適合、版違いLoRA、話者一致低下、FP8非対応、メモリ超過、mutableタグ更新。
U：入力選別、judge系統誤差、実機差は未定量。合成不確かさ・実用速度を捏造しない。

## ERROR CHECK

3件を追加推薦した。正式カタログ/取得候補の件数は142/97のまま。Nanbeigeの維持と既存6件除外は不変。新規取得承認0、ローカル削除0、P2Pシード0。提案を反映済みの選定と呼ばない。

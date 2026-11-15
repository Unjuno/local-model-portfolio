# v40 R91：原本重複を削減し、9件の残課題と地域制限を明文化

## 1.〈本論〉
現行v40（195登録/有効148）を変更せず、総パラメータ数が未確定の有効9件を全数再監査。9件とも完全な学習済みtensor全数が分からないため、正式取得ゲートは未解除。

**確定した原本選択：Qwen Image 2.1 Consistency LoRA**。作者固定モデルカードはstep1500をstart hereと明示。固定revision 58897a02f4f60f88376eab5676738dd45e5ed1a2 で、元重み1ファイル159,436,496byte、SHA256 4f44ada1be2189cc23b3d010f9603543403f48454e2f76842a3d30109b20bd63、原本候補5ファイル159,544,753byteとした。step2000は異なるcheckpointだが、同一学習タスクを後続訓練した版であり初期保存から除外。作者比較の36件restyleではstep1500位置ずれ1.6px／step2000 0.9px、15件色差6.3／10.9。色忠実性と作者推奨を優先した選択であり独立再測定ではない。既存有効Qwen/Qwen-Image-2.1の親重みは別資産としてすでに選定済み。実HDDに共有親があるとの証拠はない。
QwenのResearch Licenseは非商用の研究評価目的に制限し、商用使用には別契約が必要。LoRAも親条件の拘束を受ける。作者のComfy-Org INT8構成を親のBF16モデル実機テスト結果として再利用しない。

**PrunaAI/P-H3-Imageの重要な制限**。MiniMax H3原文LICENSEのExcluded TerritoriesはEU、英国、韓国、米国。これらの地域での当該標準許諾による利用/配布は認められておらず、別許諾が必要。日本は列挙されないが、すべての用途が無条件に許されるわけではない。NOTICEはMiniMax由来transformer、VAE、text encoder/connectorと、Apache2.0 Qwen由来prompt upsamplerを分ける。他AIモデルをOutputsで改善する行為も原文で制限。ファイル形式を変えても原ライセンスは消えない。
Prunaのpublisher tensor countの既知3部はH3 transformer 33,122,992,896、prompt upsampler 9,409,813,744、text encoder 4,437,815,808、合計46,970,622,448。しかしVAEとtext connectorは未計数なので、33Bないし46.97Bを完全パイプライン総数と宣言しない。既存原本44ファイル99,840,428,064byteはpublisherソース参照。modular_model_index.jsonで各componentのrevisionがnullのため、ランタイムは明示的にローカル固定ファイルルートを使用し、最新版の混入を防ぐ必要がある。

その他：Maya2はMimi/ECAPAの外部learned dependency、Drama3はcodec.pth、SteerTTSは主モデル以外のVocos/WavLM/MiniLM/Flow、LTX2.5二派生はtext/audio/VAE、Kumo-Relationalは.pt正確tensor全数、Kumo-Anomalyは2.44Mと8Mの不一致および旧unsafe loaderが停止条件。9件の詳細は機械可読監査台帳を参照。

## 2.〈変数表〉と次元チェック
| 記号 | 意味（日本語） | 単位（SI準拠） | 定義・範囲・前提 | 型 |
|---|---|---|---|---|
| Ba | step1500学習済みLoRA重量 | byte | 159,436,496、publisher | 非負整数スカラー |
| Bs | 5候補ファイル合計 | byte | 159,544,753、publisher | 非負整数スカラー |
| Pt | Pruna transformer総数 | 1（個） | 33,122,992,896、publisher | 非負整数スカラー |
| Pu | Pruna upsampler総数 | 1（個） | 9,409,813,744、publisher索引 | 非負整数スカラー |
| Pe | Pruna text encoder総数 | 1（個） | 4,437,815,808、publisher索引 | 非負整数スカラー |
| P3 | Pruna既知3部合算 | 1（個） | 46,970,622,448、VAEとconnector除外 | 非負整数スカラー |
BaとBsはbyte、Pt/Pu/Pe/P3は個数であり互いに加算しない。Bs−Ba=108,257byte、P3=Pt+Pu+Pe=46,970,622,448個。誤差分布なしでu_c・kは計算不可。

## 3. H/T/D/C/UおよびERROR CHECK
H：作者推奨step1500と共有親を採用する方が同学習run後続step2000の無差別保存より合理的。T：元11公開ファイルから選択5、除外6、9パラメータ未確定の全数比較。D：出版社source件数・容量・重みSHAはPASS、実機・ライセンスの個別適用と完全tensorはUNCERTAIN、無許可取得はFAIL。C：厳密位置合わせ優先時のstep2000有利、INT8/BF16差、地域別の追加ライセンス条件。U：作者データの偏り、アクセス/実HDD/コードABIの未確認。
ERROR CHECK：v40正式195／148、active未知9、取得承認0を維持。モデル重量DLと実行0。学際：モデル学習・画像編集、デジタルアーカイブ、サプライチェーン、ライセンス・国際法。

## 4.〈次に考える問い〉
モデル数をさらに増やす前に、本人所有HDDの実空き、各原本のSHA、オフライン復元を何件まで確定させるか。

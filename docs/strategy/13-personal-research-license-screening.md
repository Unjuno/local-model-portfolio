# v17 個人の非商用研究とライセンス・メタデータを分ける

**修正した誤り**：Hugging Faceの`license: unknown`を、個人研究用の保存候補から自動除外する根拠として扱っていた。これは妥当でない。タグは利用条件そのものではない。公開重みを研究候補として優先調査することと、権利・容量を満たしてダウンロードすること、第三者に再配布することを分ける。

[日本の著作権法](https://laws.e-gov.go.jp/law/345AC0000000048)第30条は一定の私的複製、第30条の4は一定の非享受目的利用を規定するが、いずれも例外要件があり「研究ならすべて適法」を意味しない。文化庁[FAQ](https://www.bunka.go.jp/seisaku/bunka_gyosei/kibankyoka/faq/index.html)も個人利用と業務利用を区別している。

[開発元LightricksのQ&A](https://huggingface.co/Lightricks/LTX-2.5/discussions/6)は所定条件下のコミュニティfine-tuneと派生配布時のライセンス継承を説明。[Stuubs NOTICE](https://huggingface.co/Stuubs/Stubelius_Remix_Ltx2.5/blob/main/NOTICE.txt)はLTX-2.x派生ライセンス、元重み、複数の提供元を列挙。[ChrisColeTech README](https://huggingface.co/ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8/blob/main/README.md)は公開したLTX2.5派生重み・テキストエンコーダ・VAEを示している。作者が規制を避けるため意図的にタグを欠落させたとの主張は未確認。

両モデルを**HOLD → conditional（研究専用）**へ変更し、優先して配布元・完全重み・権利を調べる。**総パラメータ数は未確定のため`UNVERIFIED_BLOCK_FINAL_LOCK`を維持**。実行可能な取得lockを作るには、正規のアクセス、対象行為の権利根拠、親/派生の条件、全学習済み部品の総数、固定ハッシュと必要容量、ユーザー承認が必要。Pirate Faceのseedは公開再配布なので個人研究と同列に扱わない。

## ERROR CHECK

142資産・有効97件、conditional44、HOLD27。総数不明14のうち研究conditional2。取得承認0、HDD削除0、Torrent0。研究候補と承認済みダウンロードを混同しない。

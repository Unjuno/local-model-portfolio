# R154／v65：112取得報告の完全照合と5M時系列・6MB Heretic・動画音声・ロボット権利監査（2026-11-22）

## 1.〈本論〉正式判断

**正本 v65：240登録・192有効（SELECT56／CONDITIONAL136／HOLD29）**。旧v64の236項目と採否は完全保存。取得台帳は**112モデルVERIFIED、1,714ファイル、2,020,548,143,087 byte、Gated HOLD1**を報告するが、これは今回の所有者Windows Dドライブを独立再SHAした値ではない。完全なオフライン復元と個別利用権利も未確認である。

- **取得済みを正式収録（新規転送0）**：Mistral Timestral-5M（SELECT）とTencent WeMM-Video-2B（CONDITIONAL）は112取得報告に含まれ、旧v64カタログだけにIDがなかった。公開元40桁revision、選定パス・ファイル数とbyteが台帳と一致。合計6,611,554,027 byteは既報告範囲なので再取得しない。
- **小型無検閲編集をCONDITIONAL収録（未取得）**：nchapman/Qwen3.5-0.8B-Heretic-LoRAの16Publisherファイル計6,165,749byte。学習済みSafetensorsの独立2 state合計2,006,488byte。root/trial002はLFS SHA一致で重複状態、trial004のみ別state。GGUFは変換品として別学習成果に数えない。既保全Qwen 0.8B親を再取得しない。ただし公開adapter_configの親revisionはnullで、完全一致の訓練親・ABI・本人ローカルハッシュは不明。
- **Cartwheel Controlを正式HOLD（未取得）**：RP1・Menlo Asimov-1・Unitree G1の独立3ロボットpolicyは154ファイル304,057,444byte。RP1の付属モデルに上流LICENSEが無く、第三者robot mesh/MJCFの適法配布権が未証明。シミュレーション用途のみ、実ロボット実装・安全性能を検証していない。重みもモデルコードも取得実行不可。
- **Kitten Picoの任意INT8追加を研究HOLD**：既報告33ファイルと同一40桁revisionの別8言語ONNX、計63,628,208byte。公開元LFS SHA256・Git OIDの8件を今回すべて特定。作者が独立再学習したか、既存INT4/F32からの変換かは未確証。新しいモデルIDにカウントせず、性能差/ONNX Runtimeと権利を審査する。

### 原本比較表

| モデル・固定公開元 | Publisherファイル・bytes（十進） | 採否 | 主な停止条件 |
|---|---:|---|---|
| [Timestral-5M](https://huggingface.co/mistralai/Timestral-5M/tree/bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f) | 6／20,854,471 | SELECT | 5,208,960 F32要素の独立時系列学習成果。Modified MIT：前月企業・雇用主の全世界連結月商USD20m超では権利制限。ユーザー本人の適格性・CPU実測未確認 |
| [WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B/tree/821690998399cac0f55bb7f7f805ebafa650c3a4) | 27／6,590,699,556 | CONDITIONAL | 3,283,624,264総要素、動画＋音声同期理解。custom Python・映像/音声codec・CUDA等ABI未検証。[作者研究arXiv:2611.26409](https://arxiv.org/abs/2611.26409) |
| [Qwen0.8B-Heretic-LoRA](https://huggingface.co/nchapman/Qwen3.5-0.8B-Heretic-LoRA/tree/92e2ae29c379d7378c696511ec9c70ace8be1434) | 16／6,165,749 | CONDITIONAL | 2独立rank3小型差分、同SHA重複を排除。学習親revision null、PEFT・llama.cpp・GatedDeltaNet ABI、LICENSE本文不在（Hub Apacheタグのみ） |
| [Cartwheel Control](https://huggingface.co/GetCartwheelInc/cartwheel-control/tree/24fc279af8f70097f503767b81db5384d779aae5) | 154／304,057,444 | HOLD | モデル・第三者meshに別契約、RP1付属資産の上流LICENSE不明。実機検証なし、学習済み総要素未計数 |

Publisher公式の4source全203参照・6,921,777,220byteのSHA・OIDは[固定マニフェスト](../../manifests/drafts/r154-2026-11-22-four-primary-sources-after112.candidate.json)。Kittenの8 SHAは[追加差分](../../catalog/research/2026-11-22-r154-pico-eight-int8-extra-publisher-sha.json)。

## 2. 無検閲の品質と親同一性を混同しない

作者はroot版の特定拒否評価4/100、無編集親93/100、first-token KL 0.0714 nats、trial004は6/100と0.0275 natsを報告。ただし独立した中立知識やコーディング性能比較を実施しておらず、拒否低下を一般能力の向上とみなさない。

rootのadapter_model.safetensorsとtrial002の同名ファイルは**同一LFS SHA 269cee632d7b2dc1cb5163d6f1b2a378df3b2130e51c8b08c686709997c28679**。trial004は**26836a1374eb43aef39f04970b558f347a62558ebce8c0e00388ff217146ba6e**。既存親の取得台帳revisionは 2fc06364715b967f1860aea9cf38778875588b17、しかし作者の訓練親revisionは公開されておらず、一致を推定してはいけない。

## 3. 112全件の重複排除と次のsource

[112検証報告ID全件join](../../catalog/audits/2026-11-22-r154-all112-ledger-and-new-source-delta.json)：旧v64には2 ID欠けたが、新v65では**112/112が正式カタログに存在**する。これはファイル復元完了の証明ではない。

[R155次期取得研究キュー](../../queues/proposed-v65-r155-after112-unapproved-source-scopes.json)は旧R152の14候補中、13件が既にVERIFIEDという最新報告に合わせて二重取得を除外。差分候補はHeretic約6MB（未承認）、Kitten任意INT8約64MB（学習独立性未証明）、Cartwheel304MB HOLD、Ripple65B約130GB HOLD。後二者は取得対象に含めない。数字は公開元で観測された参照byteであり、ユーザー媒体に必要な転送・占有量ではない。

## 4. 規制判断：推論ではなく一次資料

米BISの2026年11月19日公布規則（[91 FR 74970](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23529.htm)）は旧AI Diffusion Ruleのモデル重みECCN 4E091を撤廃した。一律のopen-weight所有禁止が目前という断定は一次資料では支持されない。別の輸出・用途規制、モデル固有LICENSE、Gated配布、第三者権利は独立したゲート。公開終了・規制確率の数値予測はできず、保存対象は再構築不能な学習結果と適法な権利確認から優先する。

## 5. H・T・D・C・U

- **H（反証可能仮説）**：独立の小型時系列・音声動画・可逆LoRA差分を保存候補に加えれば、重複モデルを増やさず能力多様性を高められる。RP1権利不明資産をHOLDにしても元の公開メタデータは保全できる。
- **T（最小検証）**：112 VERFIEDのIDを正確にjoin、旧236行のJSON同一性、4公開元203ファイルの40桁commitとsha/OID、Heretic重み2種、Kitten8補完SHAを無通信テスト。性能は将来同一HW・clock・driver・backend・batch・context・量子化zero-pointを明記して中立・拒否タスク別100件以上を事前固定して検証。今回モデル推論・コード実行0。
- **D（PASS／FAIL／UNCERTAIN）**：Publisher証拠の一意性、240/192、既取得112 ID全包含、承認0なら静的PASS。無権利mesh取得、親を無断再ダウンロード、無審査コード実行、量子化を別学習状態と数えたらFAIL。本人Dの現物SHA、適法使用、運用ABI、オフライン復元と品質はUNCERTAINで引き続き取得STOP。
- **C（破れ方）**：Timestral5Mの品質が既存28Mに劣る、WeMM同期不良、Hereticが中立性能を害する、Kitten INT8が変換のみ、Cartwheel第三者許諾が無い。
- **U（不確かさ）**：取得レシート報告と本人媒体の独立検証差、学習親null、作者ベンチの偏り、Tensor census、OS/driver/CUDA・KV/zero-point/ABI、法的契約当事者、HDD/cache/staging。反復測定が無いため合成標準不確かさu_cと包含係数kを数値化できない。

**ERROR CHECK**：旧236資産不変、240件ID一意、SELECT56・CONDITIONAL136・HOLD29、112/112 ledger-ID整合、4公開元203ファイル、2独立LoRA LFS重み、Kitten追加8 SHA、新重量DL0、owner D編集0、未審査コード実行0、Gated回避0、approved queue 0。

連携分野：時系列統計と省電力予測、音声動画の時間同期、低ランクモデル編集・統計的評価、ロボット制御と第三者知財、デジタル保存・国際取引規制。

###〈次に考える問い〉
完全オフライン復元が未証明の112既取得モデルを検証する価値と、6MBの新規無検閲差分を先に保存する価値を、どのように容量・独立性・権利に分解して比較するべきか。

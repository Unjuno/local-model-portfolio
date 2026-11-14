# R64｜v32・135資産の取得準備ゲート統合監査（2026-11-15）

## 1.〈本論〉監査結果

正本 `main` commit `6b3617641dbbea1cb6799d5d77453df97f20cab5`。182登録、53 SELECT＋82 CONDITIONAL＝135有効資産を全数照合。重複IDなし。

過去v27の126件は配布元ファイルスコープ監査済みだが、完全依存・現物SHA・実機HDDを再検証したわけではない。v28〜v32追加9件は個別の40桁source revision／ファイルサイズ範囲に照合済み。

有効モデルで総数不明7件、Gated副台帳上の現在のGated 17 件、正本にライセンス本文確認済みと記載3件。本人の権利、最終取得許可とHDD／オフライン復元は一件もPASS認定できない。

## 2. 優先する14件

1. `ibm-granite/granite-timeseries-ttm-r3` — Tiny independent time-series model; first offline recovery pilot
2. `robbyant/lingbot-touch-tiny` — Tactile trained encoder; pickle and sensor ABI static preflight
3. `nvidia/Nemotron-3-Diarization` — Diarization rather than ASR; official Safetensors and NeMo runtime
4. `nvidia/RFD4-Proteina` — Rare biochemical Flow+AE; author runtime source closure
5. `qvac/BotPsy-0.8B` — Independent agent SFT/RL; tokenizer/tool execution schema
6. `tencent/Qwen3.8-27B-DSpine-b16` — Independent drafter; parent Qwen SHA reuse and SGLang ABI
7. `nvidia/Alpamayo2-Edge` — Autonomous-driving VLA; processor / external rights
8. `ACE-Step/acestep-v15-xl-turbo` — Music generator; R63 code auto-download blocker
9. `InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF` — Selective control-adjustment unique research; original R21 source pin
10. `orcarouter/Qwen3.8-27B-Uncensored` — Gated rights/access before any payload
11. `OpenMOSS-Team/MOSS-TTS-v1.5` — TTS and mandatory external audio codec dependency
12. `nvidia/Granary-v2` — Unique voice annotation labels; source audio absent in label hub
13. `PrunaAI/P-H3-Image` — Image distillation, ~100GB original; full tensor total and license
14. `maya-research/maya2-native` — Multilingual TTS requires Mimi and speaker encoder

## 3. 合否基準

保存価値：独立した学習状態、再現困難なデータ/アーキテクチャ、特殊モダリティを重視。一般ベンチマーク優越不要。

取得準備：正規ライセンス・本人Gated権利・完全ファイルrev/SHA/bytes・CodecとProcessorの学習済み状態・実HDD空き200GB・依存ランタイム・明示承認が非補償型ゲート。どれか不足なら取得不可。

## 4. H/T/D/C/U

H：135件に確定済み根拠と不足ゲートを一対一対応させれば、取得段階の誤認を減らせる。T：182 IDの一意性、135 active、126歴史source scope、9新規source scope、7未知総数、Gated台帳を全件照合。D：カタログ照合PASS、取得READYは0、許諾・復元はUNCERTAIN。C：同じSHAでもABI不一致や契約違反により復元不能。U：実機容量・本人権利・追加wheel/依存が不明のため合成u_c/kは算定不可。

ERROR CHECK：53+82=135、126+9=135、登録総数182、総数不明の有効7。取得承認0、実モデル取得0、実行0。

機械学習、デジタルアーカイブ、ソフトウェア供給網、知財/契約の4分野に関連する。

## 5.〈次に考える問い〉

公開元の一意な重みを整理した後、次の1モデルを完全オフライン復元できるようにするには、何が最初に不足するのか？

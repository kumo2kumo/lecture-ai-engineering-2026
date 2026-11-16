# 第4回 宿題（実装）用のファイル

宿題（実装）で自分の評価セット `data/eval/my_cases.jsonl` を作り、ラベル付けと採点をした結果を置くフォルダ。
講師の評価セット（`data/eval/lec04_cases.jsonl`）の結果は、1つ上の `lectures/04/` にある。

## このフォルダのファイル

| ファイル | 中身 | 作り方 |
|---|---|---|
| `labels.jsonl` | `my_cases.jsonl` の10件に付けた自分のラベル。1行1件で、`id`、5つの基準（grounding / scope / hint / clarity / lecture_mark）の pass/fail、`unsure_flag`、`note` | `tools/annotate.py` の「ラベル付け」画面で、評価セットを `data/eval/my_cases.jsonl`、ラベルの保存先をこのファイルにして保存 |
| `judge_result.json` | `my_cases.jsonl` を LLM に採点させた結果。モデル名、実行時刻、件数ごとの各基準の判定と理由 | 下の「採点する」のコマンド（`--out` でここに出力） |

## lec04に関係するファイル（このフォルダの外）

- `data/eval/my_cases.jsonl`：自分の評価セット（質問、種類、参照する用語集の id、期待するふるまい、回答）
- `data/eval/rubric.md`：採点の基準（LLM に渡す）
- `data/glossary.json`：用語集（`reference.glossary` の id の参照先）

## 使う Python ファイル

| ファイル | 役割 | 使う場面 |
|---|---|---|
| `app/judge.py` | 第4回の中心。次の4つをする。<br>① `--generate`：評価セットの各質問をエージェントに投げ、`answer` を埋める<br>② 採点：`rubric.md` を渡した採点用のエージェント（LLM）に、1件ずつ4つの基準を判定させる<br>③ 「第N回」の判定：`check_lecture_mark` が、回答の最後の行に「第N回」があるかを正規表現で調べる（LLM には聞かない）<br>④ 一致率：自分のラベルと LLM の判定を比べ、基準ごとの一致率、要確認（unsure）、不一致（見逃し・過検出）を出す。`--compare` を付けると、LLM を呼ばずにラベル同士だけを比べる | 回すときのコマンドの 1 と 3 |
| `tools/annotate.py` | ラベル付けの Streamlit 画面。「ラベル付け」「比べる（講師のラベルと）」「作問」の3画面がある。評価セットを1件ずつ表示し、基準ごとの pass/fail と「迷った」を保存する。`app.tools` から用語集を読み、参照欄に表示する | 回すときのコマンドの 2 |
| `app/agent.py` | 第3回で作ったエージェント。システムプロンプト（`INSTRUCTIONS`）と、用語集検索などのツールを持つ。第4回では、回答を作る側（評価される側）として、`--generate` のときだけ `judge.py` から呼ばれる。5つの基準は、この `INSTRUCTIONS` の指示から作ってある。採点用のエージェントとは別物 | コマンドの 1 だけ |
| `app/tools.py` | エージェントが使う関数（`search_glossary`、`get_lecture_summary` など）と `load_glossary`。`annotate.py` も用語集の読み込みに使う | 間接的に使う |

- `app/agent.py` の指示を変えたら、`--generate` で回答を作り直す。その後でラベルを付けること。回答を作り直すと、すでに付けたラベルと合わなくなる。

## 回すときのコマンド

リポジトリのルートで実行する。

```
# 1. 回答を作る（API を呼ぶ。my_cases.jsonl の answer を上書きする）
uv run python -m app.judge --generate --cases data/eval/my_cases.jsonl

# 2. ラベルを付ける
uv run --with streamlit==1.66.1 streamlit run tools/annotate.py
#   サイドバーで「評価セット」= data/eval/my_cases.jsonl
#              「ラベルの保存先」= lectures/04/hw/labels.jsonl

# 3. 採点する（LLM の判定と自分のラベルの一致率が出る）
uv run python -m app.judge --cases data/eval/my_cases.jsonl \
  --labels lectures/04/hw/labels.jsonl --out lectures/04/hw/judge_result.json
```

## 注意

- 評価セット（`--cases`）とラベル（`--labels`）の組み合わせを間違えない。講師の評価セットと自分の評価セットは、どちらも `id` が `01`〜`10` なので、間違えてもエラーにならず、一致率だけがずれる。
- `judge_result.json` は再実行すると上書きされる。残したい結果は `--out` で別の名前にする。
- 回答の末尾の「第N回」は、エージェントがシステムプロンプトの指示で書く。書き忘れることがあり、その場合は `lecture_mark` が fail になる（判定はコードが行う）。

# 第5回 演習メモ：RAGの取得方式とデータの流れ

[problem.md](../problem.md) を読み解くための整理メモ。

---

## 1. TreeもGraphもRAGと言えるか

**言える。** RAG（Retrieval-Augmented Generation）は「外部資料から必要な部分を**取ってきて**（Retrieval）、プロンプトに**足して**（Augmented）、それを根拠に**生成する**（Generation）」という仕組み全体の名前で、取得の手段がベクトル検索である必要はない。

| 方式 | 取得（R）をする主体 | 取得の手がかり | RAGか |
|---|---|---|---|
| 全文投入 `--full-context` | 誰も選ばない（438ページ全部を渡す） | なし | **RAGではない**（比較用の基準） |
| ベクトル検索（通常） | 埋め込みの類似度 | 意味の近さ | 典型的なRAG |
| Tree `--tree` | **LLM自身**が目次を見て選ぶ | 資料→章→ページの階層 | RAG（埋め込みを使わない「vectorless RAG」の系統） |
| Graph `--graph` | ベクトル検索で入口を決め、関係をたどって広げる | 前後ページ・共通用語のつながり | RAG（GraphRAGの簡易版） |

### 演習で効いてくる違い

- **Tree**（[app/retrieval.py](../../../app/retrieval.py) の `browse_tree`）
  - 目次と各ページの先頭文だけを返し、どこを開くかはモデルが決める。そのためツール呼び出しが何往復にもなりやすい。
  - 人が目次を見て本を探すのと同じ動きなので、traceで「どの章を選び、どのページで全文を取ったか」を追うと判断の筋道が見える。
  - 検索DBは使わない。
- **Graph**（[app/retrieval.py](../../../app/retrieval.py) の `search_graph`）
  - 上位3ページを入口に、最大2 hop・10ページまで機械的に広げる。普通は1回の呼び出しで終わる。
  - 返す本文が多いので、入力トークンは増えやすい。
  - 共通用語でつながっていることは、答えが書いてあることを意味しない。関係の薄いページも混ざる。
- **補足**：Microsoft の GraphRAG は、LLMでエンティティを抽出し、コミュニティ要約まで作る大がかりな方式。ここの Graph は「ページと用語のグラフの近傍探索」だけの軽い実装で、名前が同じでも中身は別物と考える。

### 比較するときの観点

「RAGかどうか」より「**何を手がかりに、誰がページを選んでいるか**」で比べる。

- 予想1：Treeは往復回数が多いので時間がかかるが、入力トークンは少なめになりやすい。
- 予想2：Graphは1回で広く取るので、根拠の取りこぼしは減るが、ノイズも増える。

どちらも仕組みからの予想にすぎない。実際の数値は `[time]` と `[usage]` で確かめる。

---

## 2. lectures.json はベクトル検索用か

**違う。** [lectures.json](../../../data/rag_data/lectures.json) は**全方式が共通で使う元データ（教材の原本）**。ベクトル検索が実際に検索しているのは、これから作った [index.sqlite3](../../../data/rag_data/index.sqlite3)。

### データの流れ

```
lectures.json（原本：資料 → 章 → ページ、全9資料・438ページ）
   │
   ├─ 全文投入 ── get_all_materials() で全部を1つの文字列にして渡す
   │
   ├─ Tree ────── tree.json（目次の階層）でたどり、本文は lectures.json から取る
   │
   ├─ Graph ───── 入口は index.sqlite3 のベクトル検索、広げる先は graph.json、本文は lectures.json
   │
   └─ build_rag_index.py ──（1ページずつ Gemini で埋め込む）──▶ index.sqlite3
                                                                   │
                                                          ベクトル検索 search() はここだけを見る
```

### 根拠になったコード

- [app/config.py](../../../app/config.py)
  - `RAG_SOURCE = data/rag_data/lectures.json`。Tree・Graph・全文投入のどれもがここを読む。
  - `RAG_DOCUMENT_IDS = ("lec01-main", "lec02-main", "lec03-main")`。DBに入れる対象は第1〜3回の本講義（214ページ）だけ。全文投入は438ページ全部を使うので、方式ごとに対象範囲が違う。
- [scripts/build_rag_index.py](../../../scripts/build_rag_index.py)
  - `load_pages()` で lectures.json を「1ページ＝1行」に平らにする。
  - 講義・章・タイトル・本文をつないだ文章を埋め込み、`chunks` テーブルに本文とベクトルを一緒に保存する。
- [app/retrieval.py](../../../app/retrieval.py) の `search()`
  - `index.sqlite3` の `chunks` から近い順に取る。本文もDBから取り出すので、実行時に lectures.json は読まない。

### 注意点

- lectures.json を編集しても、`--rebuild` で索引を作り直さない限り、ベクトル検索の結果は変わらない。
- Tree・全文投入にはすぐ反映される。
- Graph は、入口を選ぶ部分には反映されず、返す本文には反映される。

宿題で本文を変えるときに「`AIE_RAG_DB` で実験用DBを指定してから索引を作る」よう求められているのはこのため。

---

## 3. `uv run python -m app.retrieval "LoRA QLoRA 違い"` は何をしているか

RAGの「**R（取得）だけ**」を単体で動かすコマンド。LLMは回答を作らない。

入口は [app/retrieval.py](../../../app/retrieval.py) 末尾の `if __name__ == "__main__":` で、`search(query)` を呼んで結果を表示するだけ。

### 処理の流れ

1. **質問をベクトルにする**（`embed_text`）
   - Gemini の `gemini-embedding-001` に検索語を送り、768次元のベクトルに変換する。
   - 検索語には `task_type="RETRIEVAL_QUERY"` を指定する。索引のページ側は `RETRIEVAL_DOCUMENT` で埋め込まれている。
   - ベクトルの長さを1にそろえる（正規化）。
2. **検索DBと比べる**（`search`）
   - `index.sqlite3` を読み取り専用で開く。
   - 214ページの埋め込みとの**コサイン距離**を計算し、近い順に `RAG_TOP_K = 5` 件を取る。
   - 距離計算は SQLite 拡張の `sqlite-vec` が担当する。
3. **表示する**
   - 講義名・章・タイトル・PDFページ番号・本文を出力する。

### ポイント

- **APIの使い方**：呼ぶのは埋め込みAPIを1回だけで、回答生成のLLMは呼ばない。速くて安い。`GEMINI_API_KEY` は必要。
- **「意味が近い」と「答えが書いてある」は別物**：用語が出てくるだけのページが上位に来ることもある。STEP 2で「第2回 p.52が入っているか」「根拠ページと、似た用語があるだけのページを区別できるか」を見るのはこのため。
- **検索語はSTEP 3と同じとは限らない**
  - このコマンドは人が考えた検索語を直接使う。
  - STEP 3のエージェントでは、モデルが質問文から自分で検索語を作って `search_materials` を呼ぶ。
  - `[tool call]` に出る検索語と見比べると、失敗の原因が「取得できなかった」のか「取得した根拠を使えなかった」のかを切り分けやすい。

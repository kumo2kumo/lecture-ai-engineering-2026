[model] gemini-3.5-flash-lite
第2回の講義資料によると、LoRAおよびQLoRAの仕組みについて以下の通り説明されています。

* **LoRA（Low-Rank Adaptation）**
  * **固定するもの**：元の重み（本体）は固定して学習しない（第2回・PDF p.52）。
  * **学習するもの**：変化分を表す小さな行列（細長い2つの行列の積、低ランクの追加部分）だけを学習する（第2回・PDF p.51, p.52）。

* **QLoRA**
  * **加えるもの**：LoRAの手法に加えて、**元の重みを4bitに圧縮（数値を粗く保存）**する処理を加える（第2回・PDF p.51, p.52）。これにより、さらに少ないメモリで大きなモデルの微調整が可能になります。

--- trace ---
[tool call]   search_materials({'query': 'LoRA QLoRA 固定 学習'})
[tool return] search_materials -> {"results": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "s…
[time] 回答完了まで 3.26 秒（検索・埋め込みを含む）
[usage] 入力 5,715 tokens / 出力 208 tokens / モデル応答 2 回
[cost] 生成APIの推定コスト: $0.002234 USD（埋め込み・索引構築分は含まない）

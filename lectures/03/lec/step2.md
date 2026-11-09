uv run python -m app.agent --trace  "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
[model] gemini-3.5-flash-lite
AIE2026の講座における「3レベル」とは、宿題の構成を表す3段階の難易度・アプローチのことです。

具体的には以下の3つのレベルに分かれています。

1. **基礎**：講義内容の確認
2. **実装**：自分でコードを書く
3. **発展**：調査や試行（応用的なチャレンジ）

それぞれの受講生自身のスキルや目的に合わせて、**この中のどれか1つ**に取り組めばその回の宿題は完了となります。なお、原則として宿題の採点は行われません。

第1回（関係する回：第1回）

--- trace ---
[tool call]   search_glossary({'query': '3レベル'})
[tool return] search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…
[usage] RunUsage(cost=Decimal('0.0006324'), details={'text_prompt_tokens': 783}, input_text_tokens=783, input_tokens=783, output_tokens=159, requests=2, tool_calls=1)
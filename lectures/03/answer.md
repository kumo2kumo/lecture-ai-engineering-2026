# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
    - glssary.json内で定義されている用語を表示するようになった
- `--trace` で見えたツール呼び出し（ツール名と引数）：
    - LoRAとQLoRAを引数に`search_glossay`関数が2回呼ばれている
        - search_glossary({'query': 'LoRA'})
        - search_glossary({'query': 'QLoRA'})
    - 詳細は`lectures/03/lec/step2.md`
- 1つの質問での LLM 呼び出し回数（`requests`）：
    - requests=2
- 追加したツールと、docstring に書いた説明：
    - 指定した回の用語問題を出題するmake_quiz関数
    - docstringの内容→「指定した回（1始まりの整数）の用語から一つ選び、確認問題として答えを返す。
    「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。」
          

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：

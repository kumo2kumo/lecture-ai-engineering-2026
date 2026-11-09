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

- 取り組んだレベル： 発展
- やったこと：coding agentのPiを動かし、公開されているPiのシステムプロンプトと、自分のエージェントのINSTRUCTIONSを比べる
- 結果：
    - [Pi(GitHub)_system-prompt.ts](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/system-prompt.ts)
    - Piが吐いたログは `lectures/03/hw/pi_log/2026-11-09T00-31-57-488Z_01a1bdb8-0a2f-75d7-99ec-d2bf593c5e2b.jsonl`参照
        - "role":"system"部分がシステムプロンプト 

- 気づき・疑問：
    - INSTRUCTIONSの場合は、xxxの場合はxxxのカスタムtoolを使う、とカスタムtoolの指定ができるが、Piの場合は、ツールは[read, write, bash, edit]という汎用的なツールが指定されている
        - そのため、同じ質問をしたときに、Piの場合はカスタムtoolsを使わないこともあり、意図しない返答や創作の返答が返ってくるときもある。
    - 最初の役割も
        - Pi「あなたは、コーディングエージェントハーネスであるpi内で動作するコーディングアシスタントです」
        - INSTRUCTIONS「あなたはAIエンジニアリング講座（AIE2025）の学習支援エージェントです。」
    で、INSTRUCTIONSの方は具体的な役割の指示をしている。
    - Piのシステムプロンプトにはほかに、ルールや参照ドキュメントパス項目がある。
    - Piにカスタムtoolを足したい時はTypeScriptでExetenstionを作成する
    - 実際にAIエージェントを自作・カスタマイズするうま味は何か？claudeやChatGPTでなく、これを使う意味は？
        - モデルを自由に選べる
        - 軽く最小構成、自分好みに拡張できる

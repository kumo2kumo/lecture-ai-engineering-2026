from google.adk.agents import Agent
from app.tools import get_lecture_summary, make_quiz, search_glossary
from app.agent import INSTRUCTIONS

# =============================================================================
# エージェントの定義
# =============================================================================
# Agent クラスを使ってエージェントを作成します。
# - name: エージェントの識別名
# - model: 使用するLLMモデル
# - description: エージェントの説明（マルチエージェント時に使用）
# - instruction: エージェントの振る舞いを定義するプロンプト
# - tools: エージェントが使用できるツールのリスト

root_agent = Agent(
    name="glossary_agent",
    model="gemini-3.5-flash-lite",
    description="用語集と講義要約、クイズ作成を行うアシスタント",
    instruction=INSTRUCTIONS,
    tools=[search_glossary, get_lecture_summary, make_quiz],
)
from my_agent.utils.state import AgentState
from my_agent.prompts import SurveyPrompts
from my_agent.utils.nodes import _get_model

class TopicClarificationChain:
    """
    ユーザーの初期入力を基に、研究テーマを明確化・洗練させるスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Survey MAGI: 1. Clarifying Topic ---")
        
        # --- ここからが修正点 ---
        # まず'research_theme'キーを探し、なければ最後のメッセージの内容を使う
        initial_theme = state.get("research_theme")
        if not initial_theme:
            # messagesキーが存在し、中身があれば最後のメッセージを取得
            messages = state.get("messages", [])
            if messages:
                initial_theme = messages[-1].content
            else:
                initial_theme = "No theme provided by user."
        # --- ここまでが修正点 ---
                
        prompt = SurveyPrompts.TOPIC_CLARIFIER.format(
            research_theme=initial_theme
        )
        try:
            response = self.llm.invoke(prompt)
            clarified_theme = response.content
        except Exception as e:
            print(f"Error while clarifying topic: {e}")
            clarified_theme = initial_theme

        print(f"  > Clarified Theme: {clarified_theme}")
        
        # 元のテーマと明確化されたテーマの両方を返す
        return {
            "research_theme": initial_theme,
            "clarified_theme": clarified_theme
        }

# クラスの単一インスタンスを作成
topic_clarification_chain_instance = TopicClarificationChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def topic_clarification_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return topic_clarification_chain_instance.run(state)


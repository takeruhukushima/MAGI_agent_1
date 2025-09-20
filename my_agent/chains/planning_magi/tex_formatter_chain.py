from my_agent.utils.state import AgentState
from my_agent.prompts import PlanningPrompts
from my_agent.utils.nodes import _get_model

class TexFormatterChain:
    """
    全ての計画要素を統合し、TeX形式のレポートに整形するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Planning MAGI: 5. Formatting TeX Report ---")
        
        # Stateから全ての計画要素を取得
        prompt = PlanningPrompts.TEX_FORMATTER.format(
            research_goal=state.get("research_goal", "N/A"),
            methodology=state.get("methodology", "N/A"),
            experimental_design=state.get("experimental_design", "N/A"),
            timeline=state.get("timeline", "N/A")
        )
        
        try:
            # LLMを呼び出し、整形されたTeXコンテンツを生成
            response = self.llm.invoke(prompt)
            tex_content = response.content
        except Exception as e:
            print(f"Error while formatting TeX: {e}")
            tex_content = "Failed to generate TeX report."

        print("  > TeX content generated successfully.")
        return {"research_plan_tex": tex_content}

# クラスの単一インスタンスを作成
tex_formatter_chain_instance = TexFormatterChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def tex_formatter_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return tex_formatter_chain_instance.run(state)
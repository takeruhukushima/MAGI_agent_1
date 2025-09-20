# << 生成された図表や統計結果を自然言語で解釈する
from my_agent.utils.state import AgentState
from my_agent.prompts import AnalysisPrompts
from my_agent.utils.nodes import _get_model

class ResultInterpreterChain:
    """
    分析コードの実行結果（図表や統計量）を自然言語で解釈するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Analysis MAGI: 4. Interpreting Results ---")
        
        # ここでは、分析コードは別途実行され、その結果がStateにあると仮定
        # 例: state['analysis_output'] = {"plot_image": "...", "statistics": "..."}
        analysis_output = state.get("analysis_output", "No analysis output available.")
        research_goal = state.get("research_goal", "N/A")

        prompt = AnalysisPrompts.RESULT_INTERPRETER.format(
            research_goal=research_goal,
            analysis_results=str(analysis_output)
        )
        try:
            response = self.llm.invoke(prompt)
            interpretation = response.content
        except Exception as e:
            print(f"Error during result interpretation: {e}")
            interpretation = "Failed to interpret the results."

        print("  > Results interpreted successfully.")
        return {"result_interpretation": interpretation}

# クラスの単一インスタンスを作成
result_interpreter_chain_instance = ResultInterpreterChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def result_interpreter_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return result_interpreter_chain_instance.run(state)

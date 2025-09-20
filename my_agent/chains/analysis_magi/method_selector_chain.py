# << データと目的に最適な統計・分析手法を選択する
from my_agent.utils.state import AgentState
from my_agent.prompts import AnalysisPrompts
from my_agent.utils.nodes import _get_model

class MethodSelectorChain:
    """
    データと研究目的に最適な統計・分析手法を選択するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Analysis MAGI: 2. Selecting Analysis Method ---")
        research_goal = state.get("research_goal", "N/A")
        execution_results = state.get("execution_results", {})
        dataset_preview = str(execution_results.get("output_data", {}).get("dataset", "N/A"))[:500]

        prompt = AnalysisPrompts.METHOD_SELECTOR.format(
            research_goal=research_goal,
            dataset_preview=dataset_preview
        )
        try:
            response = self.llm.invoke(prompt)
            method = response.content
        except Exception as e:
            print(f"Error during method selection: {e}")
            method = "Standard statistical analysis."

        print(f"  > Selected Method: {method}")
        return {"analysis_method": method}

# クラスの単一インスタンスを作成
method_selector_chain_instance = MethodSelectorChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def method_selector_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return method_selector_chain_instance.run(state)

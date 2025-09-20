# << Stateから各セクションに必要な情報を集約する
from my_agent.utils.state import AgentState
import json

class ContentAggregatorChain:
    """
    AgentStateから各セクションの執筆に必要な情報を集約するスキルクラス。
    このChainはLLMを必要とせず、データの整形と集約に特化する。
    """
    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Report MAGI: 2. Aggregating Content ---")
        
        # Stateから全ての関連情報を取得し、一つの辞書にまとめる
        aggregated_content = {
            "Research Theme": state.get("research_theme", "N/A"),
            "Research Goal": state.get("research_goal", "N/A"),
            "Survey Summary": state.get("survey_summary", "N/A"),
            "Methodology": state.get("methodology", "N/A"),
            "Experimental Design": state.get("experimental_design", "N/A"),
            "Execution Log": state.get("execution_results", {}).get("log", "N/A"),
            "Simulation Output": state.get("execution_results", {}).get("output_data", {}),
            "Result Interpretation": state.get("analysis_results", {}).get("interpretation", "N/A"),
            "Conclusion": state.get("analysis_results", {}).get("conclusion", "N/A"),
        }
        
        # 扱いやすいようにJSON文字列に変換
        content_json_string = json.dumps(aggregated_content, indent=2)

        print("  > All content aggregated successfully.")
        return {"aggregated_content": content_json_string}

# クラスの単一インスタンスを作成
content_aggregator_chain_instance = ContentAggregatorChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def content_aggregator_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return content_aggregator_chain_instance.run(state)

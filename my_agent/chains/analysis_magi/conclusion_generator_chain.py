# << 解釈に基づき、研究全体の結論と今後の展望を生成する
from my_agent.utils.state import AgentState
from my_agent.prompts import AnalysisPrompts
from my_agent.utils.nodes import _get_model

class ConclusionGeneratorChain:
    """
    解釈に基づき、研究全体の結論と今後の展望を生成するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Analysis MAGI: 5. Generating Conclusion ---")
        research_goal = state.get("research_goal", "N/A")
        interpretation = state.get("result_interpretation", "No interpretation available.")

        prompt = AnalysisPrompts.CONCLUSION_GENERATOR.format(
            research_goal=research_goal,
            interpretation=interpretation
        )
        try:
            response = self.llm.invoke(prompt)
            conclusion = response.content
        except Exception as e:
            print(f"Error during conclusion generation: {e}")
            conclusion = "Failed to generate a conclusion."

        print("  > Conclusion generated successfully.")
        
        # このエージェントの最終成果物としてStateを更新
        analysis_summary = {
            "interpretation": interpretation,
            "conclusion": conclusion
        }
        return {"analysis_results": analysis_summary}

# クラスの単一インスタンスを作成
conclusion_generator_chain_instance = ConclusionGeneratorChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def conclusion_generator_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return conclusion_generator_chain_instance.run(state)

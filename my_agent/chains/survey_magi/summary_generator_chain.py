from my_agent.utils.state import AgentState
from my_agent.prompts import SurveyPrompts
from my_agent.utils.nodes import _get_model

class SummaryGeneratorChain:
    """
    関連文献のリストを基に、調査結果の要約を生成するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Survey MAGI: 5. Generating Summary ---")
        
        # 修正点：'filtered_documents'ではなく'relevant_docs'を安全に参照
        relevant_docs = state.get("relevant_docs", [])
        clarified_theme = state.get("clarified_theme", "N/A")

        if not relevant_docs:
            print("  > No relevant documents to summarize.")
            return {"survey_summary": "No relevant documents were found to generate a summary."}

        prompt = SurveyPrompts.SUMMARY_GENERATOR.format(
            research_theme=clarified_theme,
            relevant_docs=str(relevant_docs)
        )
        try:
            response = self.llm.invoke(prompt)
            summary = response.content
        except Exception as e:
            print(f"Error during summary generation: {e}")
            summary = "Failed to generate summary."

        print("  > Survey summary generated successfully.")
        return {"survey_summary": summary}

# クラスの単一インスタンスを作成
summary_generator_chain_instance = SummaryGeneratorChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def summary_generator_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return summary_generator_chain_instance.run(state)

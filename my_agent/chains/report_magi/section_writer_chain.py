# << 各セクション（緒言、方法、結果など）を執筆する
from my_agent.utils.state import AgentState
from my_agent.prompts import ReportPrompts
from my_agent.utils.nodes import _get_model

class SectionWriterChain:
    """
    集約された情報と構成案を基に、論文の各セクションを執筆するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Report MAGI: 3. Writing Paper Sections ---")
        structure = state.get("paper_structure", ["Introduction", "Conclusion"])
        aggregated_content = state.get("aggregated_content", "{}")

        prompt = ReportPrompts.SECTION_WRITER.format(
            paper_structure=structure,
            aggregated_content=aggregated_content
        )
        try:
            response = self.llm.invoke(prompt)
            draft_content = response.content
        except Exception as e:
            print(f"Error during section writing: {e}")
            draft_content = "Failed to write paper content."

        print("  > Paper sections drafted successfully.")
        return {"draft_content": draft_content}

# クラスの単一インスタンスを作成
section_writer_chain_instance = SectionWriterChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def section_writer_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return section_writer_chain_instance.run(state)

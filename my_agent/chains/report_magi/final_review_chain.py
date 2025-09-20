# << 完成した論文の論理的整合性や誤字をチェックする
from my_agent.utils.state import AgentState
from my_agent.prompts import ReportPrompts
from my_agent.utils.nodes import _get_model

class FinalReviewChain:
    """
    完成した論文の論理的整合性や誤字をチェックするスキルクラス（自己修正）。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Report MAGI: 5. Final Review ---")
        compiled_tex = state.get("compiled_tex", "")

        prompt = ReportPrompts.FINAL_REVIEWER.format(
            tex_document=compiled_tex
        )
        try:
            response = self.llm.invoke(prompt)
            final_report = response.content.strip().replace("```latex", "").replace("```", "")
        except Exception as e:
            print(f"Error during final review: {e}")
            final_report = compiled_tex # エラー時はレビュー前のものを返す

        print("  > Final review complete. Report is ready.")
        # このエージェントの最終成果物としてStateを更新
        return {"final_report_tex": final_report}

# クラスの単一インスタンスを作成
final_review_chain_instance = FinalReviewChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def final_review_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return final_review_chain_instance.run(state)

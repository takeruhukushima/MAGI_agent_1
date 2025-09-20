from langgraph.types import interrupt
from my_agent.utils.state import AgentState

class HumanApprovalChain:
    """
    'Manus'の概念を実装する、人間の承認を待つためのノードクラス。
    """
    def run(self, state: AgentState):
        """ノードの主処理。グラフの実行を一時停止する。"""
        print("--- [Node] Execution MAGI: 3. Awaiting Human Approval ---")
        generated_code = state.get("generated_code", "# No code generated.")
        
        print("\n" + "="*40)
        print("ACTION REQUIRED: HUMAN INTERVENTION (MANUS)")
        print("="*40)
        print("The following code has been generated for execution.")
        print("Please review the code and provide your approval to continue.")
        print("-" * 40)
        print(generated_code)
        print("-" * 40)
        
        # グラフの実行をここで一時停止し、人間の入力を待つ
        return interrupt("Please approve the generated code to continue.")

# クラスの単一インスタンスを作成
human_approval_node_instance = HumanApprovalChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def human_approval_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return human_approval_node_instance.run(state)

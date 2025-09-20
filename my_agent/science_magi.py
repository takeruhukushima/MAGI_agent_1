from langgraph.graph import StateGraph, END
from langgraph.errors import Interrupt
from my_agent.utils.state import AgentState
from langchain_core.messages import HumanMessage

# --- 各sub_agentのエントリーポイント関数をインポート ---
from my_agent.sub_agent.survey_magi import run_survey_magi
from my_agent.sub_agent.planning_magi import run_planning_magi
from my_agent.sub_agent.execution_magi import run_execution_magi
from my_agent.sub_agent.analysis_magi import run_analysis_magi
from my_agent.sub_agent.report_magi import run_report_magi

# --- 'Manus'（人間の介入）を実現するための共通ノード ---
def human_in_the_loop_node(state: AgentState):
    """
    人間の監査と承認を待つためのノード。
    処理を一時停止し、ユーザーからの入力を促す。
    """
    print("\n--- Waiting for Human Intervention (Manus) ---")
    print("Please review the progress and provide approval or feedback to continue.")
    # Interruptに空のvalueを渡す
    return Interrupt(value={})

# --- ★★★ 新しいノード ★★★ ---
def process_human_feedback(state: AgentState):
    """
    人間からのフィードバックを`messages`に追加する。
    `Interrupt`の後にユーザーが入力した内容は、最後のメッセージとして入ってくる。
    """
    last_message = state.get("messages", [])[-1]
    # 特別な処理は不要。add_messagesが自動でやってくれるので、stateをそのまま返す。
    print(f"--- Human Feedback Processed: '{last_message.content}' ---")
    return state

class ScienceMagiAgent:
    """
    研究プロセス全体を統括するメインのMAGIエージェント（オーケストレーター）。
    """
    def __init__(self):
        self.graph = self._create_graph()

    def _create_graph(self):
        """MAGIシステム全体のワークフローを定義・コンパイルする"""
        workflow = StateGraph(AgentState)

        # 各sub_agentを独立したノードとして追加
        workflow.add_node("survey", run_survey_magi)
        workflow.add_node("planning", run_planning_magi)
        workflow.add_node("execution", run_execution_magi)
        workflow.add_node("analysis", run_analysis_magi)
        workflow.add_node("report", run_report_magi)
        
        # 人間の介入ノードと、そのフィードバックを処理するノードを追加
        workflow.add_node("human_approval", human_in_the_loop_node)
        workflow.add_node("process_feedback", process_human_feedback)

        # 研究プロセス全体の流れ（エッジ）を定義
        workflow.set_entry_point("survey")
        
        # --- ★★★ エッジの繋ぎ方を修正 ★★★ ---
        # 各専門家の仕事 -> 監査 -> フィードバック処理 -> 次の専門家
        workflow.add_edge("survey", "human_approval")
        workflow.add_edge("human_approval", "process_feedback")
        
        workflow.add_edge("process_feedback", "planning")
        workflow.add_edge("planning", "human_approval")
        # 'process_feedback'から次の専門家へ向かう条件分岐も将来的に追加可能
        # ... このパターンを繰り返す ...
        
        # 簡単化のため、残りは直接つなぎます（必要に応じて上記パターンを適用してください）
        workflow.add_edge("planning", "execution")
        workflow.add_edge("execution", "analysis")
        workflow.add_edge("analysis", "report")
        
        workflow.set_finish_point("report")
        
        return workflow.compile()

# --- 実行用の準備 ---

# ScienceMagiAgentの単一インスタンスを作成
science_magi_instance = ScienceMagiAgent()

# 外部から呼び出すためのエントリーポイント
graph = science_magi_instance.graph


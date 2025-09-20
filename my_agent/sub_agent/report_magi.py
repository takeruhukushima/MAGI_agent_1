from langgraph.graph import StateGraph, END
from my_agent.utils.state import AgentState

# --- chainsディレクトリから各専門スキルをインポート ---
from my_agent.chains.report_magi.structure_planner_chain import structure_planner_chain
from my_agent.chains.report_magi.content_aggregator_chain import content_aggregator_chain
from my_agent.chains.report_magi.section_writer_chain import section_writer_chain
from my_agent.chains.report_magi.tex_compiler_chain import tex_compiler_chain
from my_agent.chains.report_magi.final_review_chain import final_review_chain

class ReportMagiAgent:
    """
    研究成果を統合し、最終的な学術レポートを生成するMAGIエージェント。
    内部に自身のワークフロー（グラフ）を持つ。
    """
    def __init__(self):
        self.graph = self._create_graph()

    def _create_graph(self):
        """Report MAGIの内部ワークフローを定義・コンパイルする"""
        workflow = StateGraph(AgentState)

        # インポートしたスキル（Chain/Node）をノードとして追加
        workflow.add_node("plan_structure", structure_planner_chain)
        workflow.add_node("aggregate_content", content_aggregator_chain)
        workflow.add_node("write_sections", section_writer_chain)
        workflow.add_node("compile_tex", tex_compiler_chain)
        workflow.add_node("final_review", final_review_chain)
        
        # 内部の仕事の流れを定義
        workflow.set_entry_point("plan_structure")
        workflow.add_edge("plan_structure", "aggregate_content")
        workflow.add_edge("aggregate_content", "write_sections")
        workflow.add_edge("write_sections", "compile_tex")
        workflow.add_edge("compile_tex", "final_review")
        workflow.set_finish_point("final_review")
        
        return workflow.compile()

    def run(self, state: AgentState):
        """エージェントの処理を実行する"""
        print("\n>>> Entering Report MAGI Sub-Agent...")
        final_state = self.graph.invoke(state)
        print("<<< Exiting Report MAGI Sub-Agent...")
        
        # このMAGIが生成した成果物だけを返す
        return {"final_report_tex": final_state.get("final_report_tex")}

# --- science_magi.py からインポートするための準備 ---

# ReportMagiAgentの単一インスタンスを作成
report_magi_agent_instance = ReportMagiAgent()

# Main Agentが呼び出すためのエントリーポイント関数
def run_report_magi(state: AgentState):
    """
    Main Agentから呼び出されるためのエントリーポイント関数。
    Report MAGIのインスタンスのrunメソッドを呼び出す。
    """
    return report_magi_agent_instance.run(state)

# --- langgraph upで可視化するためのグラフを公開 ---
# この一行が最後のピースです
graph =report_magi_agent_instance.graph

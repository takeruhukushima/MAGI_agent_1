from langgraph.graph import StateGraph, END
from my_agent.utils.state import AgentState

# --- chainsディレクトリから各専門スキルをインポート ---
# フォルダ名とパスの綴りを正しく修正しました
from my_agent.chains.planning_magi.goal_setting_chain import goal_setting_chain
from my_agent.chains.planning_magi.methodology_suggester_chain import methodology_suggester_chain
from my_agent.chains.planning_magi.experimental_design_chain import experimental_design_chain
from my_agent.chains.planning_magi.timeline_generator_chain import timeline_generator_chain
from my_agent.chains.planning_magi.tex_formatter_chain import tex_formatter_chain


class PlanningMagiAgent:
    """
    研究計画の立案を担当するMAGIエージェント。
    内部に自身のワークフロー（グラフ）を持つ。
    """
    def __init__(self):
        self.graph = self._create_graph()

    def _create_graph(self):
        """Planning MAGIの内部ワークフローを定義・コンパイルする"""
        workflow = StateGraph(AgentState)

        # インポートしたスキル（Chain）をノードとして追加
        workflow.add_node("goal_setting", goal_setting_chain)
        workflow.add_node("suggest_methodology", methodology_suggester_chain)
        workflow.add_node("design_experiment", experimental_design_chain)
        workflow.add_node("generate_timeline", timeline_generator_chain)
        workflow.add_node("format_tex", tex_formatter_chain)
        
        # 内部の仕事の流れを定義
        workflow.set_entry_point("goal_setting")
        workflow.add_edge("goal_setting", "suggest_methodology")
        workflow.add_edge("suggest_methodology", "design_experiment")
        workflow.add_edge("design_experiment", "generate_timeline")
        workflow.add_edge("generate_timeline", "format_tex")
        workflow.set_finish_point("format_tex")
        
        return workflow.compile()

    def run(self, state: AgentState):
        """エージェントの処理を実行する"""
        print("\n>>> Entering Planning MAGI Sub-Agent...")
        final_state = self.graph.invoke(state)
        print("<<< Exiting Planning MAGI Sub-Agent...")
        
        # このMAGIが生成した成果物だけを返す
        return {"research_plan_tex": final_state.get("research_plan_tex")}

# --- science_magi.py からインポートするための準備 ---

# PlanningMagiAgentの単一インスタンスを作成
planning_magi_agent_instance = PlanningMagiAgent()

# Main Agentが呼び出すためのエントリーポイント関数
def run_planning_magi(state: AgentState):
    """
    Main Agentから呼び出されるためのエントリーポイント関数。
    Planning MAGIのインスタンスのrunメソッドを呼び出す。
    """
    return planning_magi_agent_instance.run(state)

# --- langgraph upで可視化するためのグラフを公開 ---
# この一行が最後のピースです
graph = planning_magi_agent_instance.graph

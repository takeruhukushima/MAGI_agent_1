from langgraph.graph import StateGraph, END
from my_agent.utils.state import AgentState

# --- chainsディレクトリから各専門スキルをインポート ---
from my_agent.chains.analysis_magi.data_validator_chain import data_validator_chain
from my_agent.chains.analysis_magi.method_selector_chain import method_selector_chain
from my_agent.chains.analysis_magi.analysis_code_generator_chain import analysis_code_generator_chain
from my_agent.chains.analysis_magi.result_interpreter_chain import result_interpreter_chain
from my_agent.chains.analysis_magi.conclusion_generator_chain import conclusion_generator_chain

class AnalysisMagiAgent:
    """
    実験データの分析と解釈を担当するMAGIエージェント。
    内部に自身のワークフロー（グラフ）を持つ。
    """
    def __init__(self):
        self.graph = self._create_graph()

    def _create_graph(self):
        """Analysis MAGIの内部ワークフローを定義・コンパイルする"""
        workflow = StateGraph(AgentState)

        # インポートしたスキル（Chain）をノードとして追加
        workflow.add_node("validate_data", data_validator_chain)
        workflow.add_node("select_method", method_selector_chain)
        workflow.add_node("generate_analysis_code", analysis_code_generator_chain)
        workflow.add_node("interpret_results", result_interpreter_chain)
        workflow.add_node("generate_conclusion", conclusion_generator_chain)
        
        # 内部の仕事の流れを定義
        workflow.set_entry_point("validate_data")
        workflow.add_edge("validate_data", "select_method")
        workflow.add_edge("select_method", "generate_analysis_code")
        workflow.add_edge("generate_analysis_code", "interpret_results")
        workflow.add_edge("interpret_results", "generate_conclusion")
        workflow.set_finish_point("generate_conclusion")
        
        return workflow.compile()

    def run(self, state: AgentState):
        """エージェントの処理を実行する"""
        print("\n>>> Entering Analysis MAGI Sub-Agent...")
        final_state = self.graph.invoke(state)
        print("<<< Exiting Analysis MAGI Sub-Agent...")
        
        # このMAGIが生成した成果物だけを返す
        return {"analysis_report": final_state.get("analysis_report")}

# --- science_magi.py からインポートするための準備 ---

# AnalysisMagiAgentの単一インスタンスを作成
analysis_magi_agent_instance = AnalysisMagiAgent()

# Main Agentが呼び出すためのエントリーポイント関数
def run_analysis_magi(state: AgentState):
    """
    Main Agentから呼び出されるためのエントリーポイント関数。
    Analysis MAGIのインスタンスのrunメソッドを呼び出す。
    """
    return analysis_magi_agent_instance.run(state)

# --- langgraph upで可視化するためのグラフを公開 ---
graph = analysis_magi_agent_instance.graph

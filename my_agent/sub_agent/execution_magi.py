from langgraph.graph import StateGraph, END
from my_agent.utils.state import AgentState

# --- chainsディレクトリから各専門スキルをインポート ---
from my_agent.chains.execution_magi.plan_parser_chain import plan_parser_chain
from my_agent.chains.execution_magi.code_generator_chain import code_generator_chain
from my_agent.chains.execution_magi.human_approval_chain import human_approval_chain
from my_agent.chains.execution_magi.simulation_executor_chain import simulation_executor_chain
from my_agent.chains.execution_magi.data_logger_chain import data_logger_chain

class ExecutionMagiAgent:
    """
    実験・シミュレーションの実行を担当するMAGIエージェント。
    内部に自身のワークフロー（グラフ）を持つ。
    """
    def __init__(self):
        self.graph = self._create_graph()

    def _create_graph(self):
        """Execution MAGIの内部ワークフローを定義・コンパイルする"""
        workflow = StateGraph(AgentState)

        # インポートしたスキル（Chain/Node）をノードとして追加
        workflow.add_node("parse_plan", plan_parser_chain)
        workflow.add_node("generate_code", code_generator_chain)
        workflow.add_node("human_approval", human_approval_chain) # 人間による監査
        workflow.add_node("execute_simulation", simulation_executor_chain)
        workflow.add_node("log_data", data_logger_chain)
        
        # 内部の仕事の流れを定義
        workflow.set_entry_point("parse_plan")
        workflow.add_edge("parse_plan", "generate_code")
        workflow.add_edge("generate_code", "human_approval")
        workflow.add_edge("human_approval", "execute_simulation")
        workflow.add_edge("execute_simulation", "log_data")
        workflow.set_finish_point("log_data")
        
        return workflow.compile()

    def run(self, state: AgentState):
        """エージェントの処理を実行する"""
        print("\n>>> Entering Execution MAGI Sub-Agent...")
        final_state = self.graph.invoke(state)
        print("<<< Exiting Execution MAGI Sub-Agent...")
        
        # このMAGIが生成した成果物だけを返す
        return {"execution_data": final_state.get("execution_data")}

# --- science_magi.py からインポートするための準備 ---

# ExecutionMagiAgentの単一インスタンスを作成
execution_magi_agent_instance = ExecutionMagiAgent()

# Main Agentが呼び出すためのエントリーポイント関数
def run_execution_magi(state: AgentState):
    """
    Main Agentから呼び出されるためのエントリーポイント関数。
    Execution MAGIのインスタンスのrunメソッドを呼び出す。
    """
    return execution_magi_agent_instance.run(state)

# --- langgraph upで可視化するためのグラフを公開 ---
# この一行が最後のピースです
graph = execution_magi_agent_instance.graph

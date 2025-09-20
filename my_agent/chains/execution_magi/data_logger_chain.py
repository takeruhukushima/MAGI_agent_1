# << 実行結果とログを体系的に記録する
from my_agent.utils.state import AgentState
import datetime

class DataLoggerChain:
    """
    実行結果とログをAgentStateに体系的に記録するスキルクラス。
    """
    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Execution MAGI: 5. Logging Data ---")
        
        # Stateから実行結果を取得
        log = state.get("execution_log", "No log available.")
        output = state.get("simulation_output", {})

        # 記録用のデータ構造を作成
        execution_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "log": log,
            "output_data": output
        }
        
        print("  > Execution results have been logged.")
        
        # このエージェントの最終成果物としてStateを更新
        return {"execution_results": execution_record}

# クラスの単一インスタンスを作成
data_logger_chain_instance = DataLoggerChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def data_logger_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return data_logger_chain_instance.run(state)

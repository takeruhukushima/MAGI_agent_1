# << 承認されたコードをCodeInterpreterで実行する
from my_agent.utils.state import AgentState
import datetime
import json

class SimulationExecutorNode:
    """
    承認されたコードを実行するノードクラス（現在はシミュレーション）。
    """
    def run(self, state: AgentState):
        """ノードの主処理。コードの実行をシミュレートする。"""
        print("--- [Node] Execution MAGI: 4. Executing Simulation ---")
        code_to_run = state.get("generated_code", "")

        # --- ここでサンドボックス環境などで実際にコードを実行する ---
        # この例では、実行をシミュレートし、ダミーの結果を返す
        
        if "# Failed" in code_to_run or not code_to_run:
            print("  > Execution skipped due to invalid code.")
            log = "Execution failed or skipped."
            output = {"error": "Invalid code provided."}
        else:
            print("  > Simulating code execution...")
            log = f"Execution successful at {datetime.datetime.now().isoformat()}"
            # 科学計算でよく見られるような、辞書形式のダミーデータを生成
            output = {
                "result_summary": "Simulation completed successfully.",
                "dataset": [
                    {"time": 0, "value": 1.0},
                    {"time": 1, "value": 2.7},
                    {"time": 2, "value": 7.3},
                    {"time": 3, "value": 20.0},
                ],
                "parameters": {
                    "initial_condition": "A",
                    "iterations": 1000
                }
            }
            print("  > Execution simulation finished.")
            
        print(f"  > Execution Log: {log}")
        
        return {
            "execution_log": log,
            "simulation_output": output
        }

# クラスの単一インスタンスを作成
simulation_executor_node_instance = SimulationExecutorNode()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def simulation_executor_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return simulation_executor_node_instance.run(state)


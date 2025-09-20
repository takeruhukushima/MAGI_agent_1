from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END
from my_agent.utils.nodes import call_model, should_continue, tool_node
from my_agent.utils.state import AgentState


# Define the config (これはクラスの外にあってもOK)
class GraphConfig(TypedDict):
    model_name: Literal["anthropic", "openai","google"]


class SimpleAgent:
    def __init__(self):
        # グラフの定義からコンパイルまでを__init__内で行う
        workflow = StateGraph(AgentState, config_schema=GraphConfig)

        # ノードを定義
        workflow.add_node("agent", call_model)
        workflow.add_node("action", tool_node)

        # エッジ（繋がり）を定義
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "action",
                "end": END,
            },
        )
        workflow.add_edge("action", "agent")

        # グラフをコンパイルして、インスタンス変数として保持
        self.graph = workflow.compile()

# --- 使い方 ---

# 1. クラスからエージェントの実体（インスタンス）を作成
my_agent = SimpleAgent()

# 2. langgraph up から見えるようにグラフを公開する
#    この行を追加するだけでOK！
graph = my_agent.graph

# 3. 実行テスト（これはそのままでOK）
# result = graph.invoke(
#     {"messages": [("user", "some input")]},
#     config={"model_name": "google"}
# )
# print(result)
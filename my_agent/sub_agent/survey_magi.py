from langgraph.graph import StateGraph, END
from my_agent.utils.state import AgentState

# --- chainsディレクトリから各専門スキルをインポート ---
from my_agent.chains.survey_magi.topic_clarification_chain import topic_clarification_chain
from my_agent.chains.survey_magi.query_generator_chain import query_generator_chain
from my_agent.chains.survey_magi.search_executor_chain import search_executor_chain
from my_agent.chains.survey_magi.relevance_filter_chain import relevance_filter_chain
from my_agent.chains.survey_magi.summary_generator_chain import summary_generator_chain

class SurveyMagiAgent:
    """
    調査を担当するMAGIエージェント。
    内部に自身のワークフロー（グラフ）を持つ。
    """
    def __init__(self):
        self.graph = self._create_graph()

    def _create_graph(self):
        """Survey MAGIの内部ワークフローを定義・コンパイルする"""
        workflow = StateGraph(AgentState)

        workflow.add_node("clarify_topic", topic_clarification_chain)
        workflow.add_node("generate_queries", query_generator_chain)
        workflow.add_node("execute_search", search_executor_chain)
        workflow.add_node("filter_relevance", relevance_filter_chain)
        workflow.add_node("summarize_results", summary_generator_chain)
        
        workflow.set_entry_point("clarify_topic")
        workflow.add_edge("clarify_topic", "generate_queries")
        workflow.add_edge("generate_queries", "execute_search")
        workflow.add_edge("execute_search", "filter_relevance")
        workflow.add_edge("filter_relevance", "summarize_results")
        workflow.set_finish_point("summarize_results")
        
        return workflow.compile()

    def run(self, state: AgentState):
        """エージェントの処理を実行する"""
        print("\n>>> Entering Survey MAGI Sub-Agent...")
        final_state = self.graph.invoke(state)
        print("<<< Exiting Survey MAGI Sub-Agent...")
        
        return {"survey_results": final_state.get("survey_results")}

# --- science_magi.py からインポートするための準備 ---

# SurveyMagiAgentの単一インスタンスを作成
survey_magi_agent_instance = SurveyMagiAgent()

# Main Agentが呼び出すためのエントリーポイント関数
def run_survey_magi(state: AgentState):
    """
    Main Agentから呼び出されるためのエントリーポイント関数。
    Survey MAGIのインスタンスのrunメソッドを呼び出す。
    """
    return survey_magi_agent_instance.run(state)

# --- langgraph upで可視化するためのグラフを公開 ---
# この一行が最後のピースです
graph = survey_magi_agent_instance.graph

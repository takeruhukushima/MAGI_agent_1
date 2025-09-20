from my_agent.utils.state import AgentState
from my_agent.prompts import SurveyPrompts
from my_agent.utils.nodes import _get_model
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Dict, Any

class RelevantDoc(BaseModel):
    """A single relevant document with its summary."""
    url: str = Field(description="The URL of the relevant document.")
    content: str = Field(description="A concise summary of why the document is relevant to the research theme.")

class FilteredResults(BaseModel):
    """A list of documents deemed relevant to the research theme."""
    relevant_documents: List[RelevantDoc]

class RelevanceFilterChain:
    """
    生の検索結果から、研究テーマに関連する文献のみをフィルタリングするスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name).with_structured_output(FilteredResults)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Survey MAGI: 4. Filtering Relevance ---")
        
        # 修正点：.get()を使い、キーが存在しなくても安全に空リストを取得
        raw_results = state.get("raw_search_results", [])
        clarified_theme = state.get("clarified_theme", "N/A")

        if not raw_results:
            print("  > No search results to filter.")
            return {"relevant_docs": []}

        prompt = SurveyPrompts.RELEVANCE_FILTER.format(
            research_theme=clarified_theme,
            search_results=str(raw_results)
        )
        try:
            response = self.llm.invoke(prompt)
            relevant_docs = [doc.dict() for doc in response.relevant_documents]
        except Exception as e:
            print(f"Error during relevance filtering: {e}")
            relevant_docs = []

        print(f"  > Filtered down to {len(relevant_docs)} relevant documents.")
        return {"relevant_docs": relevant_docs}

# クラスの単一インスタンスを作成
relevance_filter_chain_instance = RelevanceFilterChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def relevance_filter_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return relevance_filter_chain_instance.run(state)

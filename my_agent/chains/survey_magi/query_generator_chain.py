from my_agent.utils.state import AgentState
from my_agent.prompts import SurveyPrompts
from my_agent.utils.nodes import _get_model
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

# LLMに出力してほしい形式を定義するPydanticモデル
class GeneratedQueries(BaseModel):
    """A list of search queries."""
    queries: List[str] = Field(description="A list of 3 to 5 diverse and specific search queries for academic databases.")

class QueryGeneratorChain:
    """
    研究テーマを基に、複数の具体的な検索クエリを生成するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        # 構造化された出力をさせるために、with_structured_outputを使用
        self.llm = _get_model(model_name).with_structured_output(GeneratedQueries)

    def run(self, state: AgentState):
        """
        チェーンの主処理を実行するメソッド。
        """
        print("--- [Chain] Survey MAGI: 2. Generating Search Queries ---")
        
        # .get()を使い、安全にテーマを取得します
        # これが今回のKeyErrorの直接的な解決策です
        clarified_theme = state.get("clarified_theme", state.get("research_theme", "No theme provided"))

        prompt = SurveyPrompts.QUERY_GENERATOR.format(
            research_theme=clarified_theme
        )

        try:
            # LLMを呼び出し、構造化されたクエリリストを生成
            response = self.llm.invoke(prompt)
            queries = response.queries
        except Exception as e:
            print(f"Error while generating queries: {e}")
            # エラーが発生した場合は、テーマ自体をクエリとして使用
            queries = [clarified_theme]

        print(f"  > Generated Queries: {queries}")
        
        return {"search_queries": queries}

# クラスの単一インスタンスを作成
query_generator_chain_instance = QueryGeneratorChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def query_generator_chain(state: AgentState):
    """
    `sub_agent`から呼び出されるエントリーポイント。
    """
    return query_generator_chain_instance.run(state)

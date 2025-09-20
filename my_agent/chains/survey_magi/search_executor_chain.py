from my_agent.utils.state import AgentState
# Tavilyツールをインポートする想定
from my_agent.utils.tools import tavily_tool 

class SearchExecutorChain:
    """
    生成されたクエリをTavilyツールで実行し、生の検索結果を取得するスキルクラス。
    """
    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Survey MAGI: 3. Executing Search ---")
        queries = state.get("search_queries", [])
        
        if not queries:
            print("  > No queries to execute.")
            return {"raw_search_results": []}

        # 全てのクエリを結合して一つの大きな検索にする
        combined_query = " ".join(queries)
        print(f"  > Executing combined query: {combined_query[:100]}...")

        try:
            # Tavilyツールを実行
            results = tavily_tool.invoke({"query": combined_query})
        except Exception as e:
            print(f"Error during search execution: {e}")
            results = []
        
        print(f"  > Found {len(results)} raw results.")
        
        # 修正点：必ず 'raw_search_results' というキーで結果を返す
        return {"raw_search_results": results}

# クラスの単一インスタンスを作成
search_executor_chain_instance = SearchExecutorChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def search_executor_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return search_executor_chain_instance.run(state)

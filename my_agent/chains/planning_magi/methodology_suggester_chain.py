# << 目的に合った研究手法を複数提案する
from my_agent.utils.state import AgentState
from my_agent.prompts import PlanningPrompts
from my_agent.utils.nodes import _get_model

class MethodologySuggesterChain:
    """
    研究目的に基づいて研究手法を提案するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Planning MAGI: 2. Suggesting Methodology ---")
        goal = state.get("research_goal", "No goal set.")

        prompt = PlanningPrompts.METHODOLOGY_SUGGESTER.format(research_goal=goal)

        try:
            response = self.llm.invoke(prompt)
            methodology = response.content
        except Exception as e:
            print(f"Error while suggesting methodology: {e}")
            methodology = "Failed to suggest methodology."

        print(f"  > Methodology Suggested: {methodology[:100]}...")
        return {"methodology": methodology}

methodology_suggester_chain_instance = MethodologySuggesterChain()

def methodology_suggester_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return methodology_suggester_chain_instance.run(state)


# << 実験の具体的な手順、対照群などを設計する
from my_agent.utils.state import AgentState
from my_agent.prompts import PlanningPrompts
from my_agent.utils.nodes import _get_model

class ExperimentalDesignChain:
    """
    目的と手法に基づき、詳細な実験計画を設計するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- Planning MAGI: 3. Designing Experiment ---")
        goal = state.get("research_goal", "No goal set.")
        methodology = state.get("methodology", "No methodology suggested.")

        prompt = PlanningPrompts.EXPERIMENTAL_DESIGN.format(
            research_goal=goal,
            methodology=methodology
        )

        try:
            response = self.llm.invoke(prompt)
            design = response.content
        except Exception as e:
            print(f"Error while designing experiment: {e}")
            design = "Failed to design experiment."

        print(f"Experimental Design Created: {design[:100]}...")
        return {"experimental_design": design}

experimental_design_chain_instance = ExperimentalDesignChain()

def experimental_design_chain(state: AgentState):
    return experimental_design_chain_instance.run(state)

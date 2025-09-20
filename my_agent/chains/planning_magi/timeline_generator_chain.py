# << マイルストーンを含むタイムラインを生成する
from my_agent.utils.state import AgentState
from my_agent.prompts import PlanningPrompts
from my_agent.utils.nodes import _get_model

class TimelineGeneratorChain:
    """
    実験計画に基づき、タイムラインとマイルストーンを生成するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- Planning MAGI: 4. Generating Timeline ---")
        design = state.get("experimental_design", "No design created.")

        prompt = PlanningPrompts.TIMELINE_GENERATOR.format(experimental_design=design)

        try:
            response = self.llm.invoke(prompt)
            timeline = response.content
        except Exception as e:
            print(f"Error while generating timeline: {e}")
            timeline = "Failed to generate timeline."

        print(f"Timeline Generated: {timeline[:100]}...")
        return {"timeline": timeline}

timeline_generator_chain_instance = TimelineGeneratorChain()

def timeline_generator_chain(state: AgentState):
    return timeline_generator_chain_instance.run(state)
    
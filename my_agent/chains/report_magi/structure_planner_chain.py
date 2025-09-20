# << 論文全体の構成（IMRADなど）を計画する
from my_agent.utils.state import AgentState
from my_agent.prompts import ReportPrompts
from my_agent.utils.nodes import _get_model
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class PaperStructure(BaseModel):
    """The structure of the academic paper."""
    sections: List[str] = Field(description="A list of section titles for the paper, e.g., ['Introduction', 'Methods', 'Results', 'Discussion'].")

class StructurePlannerChain:
    """
    論文全体の構成（IMRADなど）を計画するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name).with_structured_output(PaperStructure)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Report MAGI: 1. Planning Paper Structure ---")
        research_goal = state.get("research_goal", "N/A")
        
        prompt = ReportPrompts.STRUCTURE_PLANNER.format(research_goal=research_goal)
        
        try:
            response = self.llm.invoke(prompt)
            structure = response.sections
        except Exception as e:
            print(f"Error during structure planning: {e}")
            structure = ["Introduction", "Methods", "Results", "Discussion", "Conclusion"]

        print(f"  > Paper structure planned: {structure}")
        return {"paper_structure": structure}

# クラスの単一インスタンスを作成
structure_planner_chain_instance = StructurePlannerChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def structure_planner_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return structure_planner_chain_instance.run(state)

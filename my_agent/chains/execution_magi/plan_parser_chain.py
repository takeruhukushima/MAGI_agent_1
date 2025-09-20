# << 計画書を読み込み、実行タスクを抽出する
from my_agent.utils.state import AgentState
from my_agent.prompts import ExecutionPrompts
from my_agent.utils.nodes import _get_model
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Dict, Any

class ExecutableTask(BaseModel):
    """A single, executable task parsed from the research plan."""
    task_id: int = Field(description="A unique identifier for the task.")
    description: str = Field(description="A clear, concise description of the task to be performed.")
    required_parameters: Dict[str, Any] = Field(description="A dictionary of parameters needed for the simulation or experiment.")

class ParsedPlan(BaseModel):
    """A list of executable tasks parsed from the research plan."""
    tasks: List[ExecutableTask] = Field(description="The list of tasks to be executed.")

class PlanParserChain:
    """
    TeX形式の研究計画書を解析し、実行可能なタスクリストに変換するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name).with_structured_output(ParsedPlan)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Execution MAGI: 1. Parsing Research Plan ---")
        plan_tex = state.get("research_plan_tex", "No plan available.")

        prompt = ExecutionPrompts.PLAN_PARSER.format(research_plan_tex=plan_tex)

        try:
            response = self.llm.invoke(prompt)
            parsed_plan = response.tasks
        except Exception as e:
            print(f"Error while parsing plan: {e}")
            parsed_plan = []

        print(f"  > Plan parsed into {len(parsed_plan)} tasks.")
        return {"parsed_plan": parsed_plan}

plan_parser_chain_instance = PlanParserChain()

def plan_parser_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return plan_parser_chain_instance.run(state)


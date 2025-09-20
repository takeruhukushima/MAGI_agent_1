# << シミュレーションや解析のためのコードを生成する
from my_agent.utils.state import AgentState
from my_agent.prompts import ExecutionPrompts
from my_agent.utils.nodes import _get_model

class CodeGeneratorChain:
    """
    解析されたタスクリストに基づき、シミュレーション用のPythonコードを生成するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Execution MAGI: 2. Generating Code ---")
        parsed_plan = state.get("parsed_plan", [])
        
        # 実際のアプリケーションでは、タスクごとにコードを生成するループ処理が必要
        # ここでは最初のタスクに対してのみコードを生成する
        if not parsed_plan:
            print("  > No tasks to generate code for.")
            return {"generated_code": "# No tasks found in the plan."}

        # 最初のタスクの説明を取得
        # 属性アクセスを安全に行う
        first_task = parsed_plan[0]
        if hasattr(first_task, 'description'):
             task_description = first_task.description
        elif isinstance(first_task, dict):
             task_description = first_task.get('description', 'No description found.')
        else:
             task_description = 'No description found.'


        prompt = ExecutionPrompts.CODE_GENERATOR.format(
            task_description=task_description
        )

        try:
            # LLMは```python ... ```のようなMarkdown形式でコードを返すことを想定
            response = self.llm.invoke(prompt)
            # Markdownブロックからコード部分のみを抽出
            code = response.content.strip().replace("```python", "").replace("```", "").strip()
        except Exception as e:
            print(f"Error while generating code: {e}")
            code = f"# Failed to generate code for task: {task_description}"

        print("  > Simulation code generated.")
        return {"generated_code": code}

code_generator_chain_instance = CodeGeneratorChain()

def code_generator_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return code_generator_chain_instance.run(state)

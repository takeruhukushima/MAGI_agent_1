# << 選択した手法で分析・可視化するコードを生成する
from my_agent.utils.state import AgentState
from my_agent.prompts import AnalysisPrompts
from my_agent.utils.nodes import _get_model

class AnalysisCodeGeneratorChain:
    """
    選択された手法で分析・可視化するPythonコードを生成するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Analysis MAGI: 3. Generating Analysis Code ---")
        analysis_method = state.get("analysis_method", "Perform a basic analysis.")
        execution_results = state.get("execution_results", {})
        # 実際のデータは `execution_results['output_data']` にある想定
        dataset = execution_results.get("output_data", {})
        
        prompt = AnalysisPrompts.ANALYSIS_CODE_GENERATOR.format(
            analysis_method=analysis_method,
            dataset_json=str(dataset) # データを文字列として渡す
        )
        try:
            # LLMは```python ... ```形式でコードを返すことを期待
            response = self.llm.invoke(prompt)
            # ```python と ``` を取り除く
            generated_code = response.content.strip().replace("```python", "").replace("```", "")
        except Exception as e:
            print(f"Error during code generation: {e}")
            generated_code = "# Failed to generate analysis code."

        print("  > Analysis code generated successfully.")
        return {"analysis_code": generated_code}

# クラスの単一インスタンスを作成
analysis_code_generator_chain_instance = AnalysisCodeGeneratorChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def analysis_code_generator_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return analysis_code_generator_chain_instance.run(state)

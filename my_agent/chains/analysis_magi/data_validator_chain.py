# << 生データの品質（欠損値など）を検証・前処理する
from my_agent.utils.state import AgentState
from my_agent.prompts import AnalysisPrompts
from my_agent.utils.nodes import _get_model
from langchain_core.pydantic_v1 import BaseModel, Field

class ValidationResult(BaseModel):
    """Data validation results."""
    is_valid: bool = Field(description="Whether the data is valid and ready for analysis.")
    reason: str = Field(description="A brief explanation of the validation result, noting any issues or preprocessing steps taken.")

class DataValidatorChain:
    """
    生データの品質（欠損値など）を検証・前処理するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name).with_structured_output(ValidationResult)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Analysis MAGI: 1. Validating Data ---")
        execution_results = state.get("execution_results", {})
        
        # 実際のデータは execution_results['output_data']['dataset'] にあると仮定
        data_to_validate = execution_results.get("output_data", {}).get("dataset", "No dataset found.")

        prompt = AnalysisPrompts.DATA_VALIDATOR.format(
            dataset_preview=str(data_to_validate)[:500] # プレビューとして先頭500文字を渡す
        )

        try:
            response = self.llm.invoke(prompt)
            if response.is_valid:
                print(f"  > Data validation successful: {response.reason}")
                return {"is_data_valid": True, "data_validation_summary": response.reason}
            else:
                print(f"  > Data validation failed: {response.reason}")
                # ここでデータクレンジングの処理を追加することも可能
                return {"is_data_valid": False, "data_validation_summary": response.reason}
        except Exception as e:
            print(f"Error during data validation: {e}")
            return {"is_data_valid": False, "data_validation_summary": "Failed to validate data."}


# クラスの単一インスタンスを作成
data_validator_chain_instance = DataValidatorChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def data_validator_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return data_validator_chain_instance.run(state)

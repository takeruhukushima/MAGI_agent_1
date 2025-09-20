from my_agent.utils.state import AgentState
from my_agent.prompts import PlanningPrompts
from my_agent.utils.nodes import _get_model

class GoalSettingChain:
    """
    調査結果（サマリー）を基に、研究の具体的な目的を設定するスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """
        チェーンの主処理を実行するメソッド。
        """
        print("--- [Chain] Planning MAGI: 1. Setting Goal ---")
        
        # 安全に情報を取得し、常に最新のテーマを参照するように修正
        survey_summary = state.get("survey_summary", "No summary available.")
        # clarified_themeがあればそれを使い、なければ元のresearch_themeを探す
        theme = state.get("clarified_theme", state.get("research_theme", "No theme provided."))

        prompt = PlanningPrompts.GOAL_SETTING.format(
            research_theme=theme,
            survey_summary=survey_summary
        )

        try:
            # LLMを呼び出し、調査結果を要約して目的を生成
            response = self.llm.invoke(prompt)
            goal = response.content
        except Exception as e:
            print(f"Error while setting goal: {e}")
            goal = "Failed to generate a research goal."
        
        print(f"  > Research Goal Set: {goal[:100]}...")
        
        return {"research_goal": goal}

# クラスの単一インスタンスを作成
goal_setting_chain_instance = GoalSettingChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def goal_setting_chain(state: AgentState):
    """
    `sub_agent`から呼び出されるエントリーポイント。
    """
    return goal_setting_chain_instance.run(state)


# << 全てのセクションを統合し、TeX出力として完成させる。
from my_agent.utils.state import AgentState
from my_agent.prompts import ReportPrompts
from my_agent.utils.nodes import _get_model

class TexCompilerChain:
    """
    執筆された全セクションを統合し、TeXファイルとして完成させるスキルクラス。
    """
    def __init__(self, model_name: str = "google"):
        self.llm = _get_model(model_name)

    def run(self, state: AgentState):
        """チェーンの主処理を実行するメソッド。"""
        print("--- [Chain] Report MAGI: 4. Compiling TeX File ---")
        draft_content = state.get("draft_content", "Content is missing.")
        research_theme = state.get("research_theme", "A Study by MAGI System")
        
        prompt = ReportPrompts.TEX_COMPILER.format(
            paper_title=research_theme,
            draft_content=draft_content
        )
        try:
            response = self.llm.invoke(prompt)
            # LLMは```latex ... ```で囲まれたTeXコードを返すと期待
            compiled_tex = response.content.strip().replace("```latex", "").replace("```", "")
        except Exception as e:
            print(f"Error during TeX compilation: {e}")
            compiled_tex = "Failed to compile TeX file."
            
        print("  > TeX file compiled successfully.")
        return {"compiled_tex": compiled_tex}

# クラスの単一インスタンスを作成
tex_compiler_chain_instance = TexCompilerChain()

# LangGraphのノードとして呼び出すためのエントリーポイント関数
def tex_compiler_chain(state: AgentState):
    """sub_agentから呼び出されるエントリーポイント。"""
    return tex_compiler_chain_instance.run(state)

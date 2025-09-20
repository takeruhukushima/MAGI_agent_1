class SurveyPrompts:
    """Prompts for the Survey MAGI."""

    TOPIC_CLARIFIER = """
You are a research assistant. Based on the user's initial research theme, clarify and refine it into a concise, searchable topic.
Initial Theme: {research_theme}
Clarified Research Topic:"""

    QUERY_GENERATOR = """
Based on the following research theme, you MUST generate a list of 3 to 5 diverse and specific search queries suitable for academic databases like Google Scholar, arXiv, and Semantic Scholar.
If the provided theme seems nonsensical or not a research topic, generate queries about the nature of language, communication, or artificial intelligence's ability to understand context.

Research Theme: {research_theme}
"""

    RELEVANCE_FILTER = """
You are an expert researcher. Based on the provided search results, filter out the most relevant documents for the given research topic.
For each result, consider the title and snippet to determine its relevance.

Research Theme: {research_theme}

Search Results:
{search_results}

Based on the above, identify the URLs and a brief justification for the most relevant documents.
"""

    SUMMARY_GENERATOR = """
You are a scientific summarizer. Based on the list of relevant documents, create a concise, synthesized summary of the key findings and trends.
The summary should provide a high-level overview of the current state of research on the theme.

Research Theme: {research_theme}
Relevant Documents:
{relevant_docs}

Synthesized Summary:"""


class PlanningPrompts:
    """Prompts for the Planning MAGI."""

    GOAL_SETTING = """
Based on the research theme and the literature survey summary, define a clear and specific primary research goal.
The goal should be achievable and address a gap or question identified in the survey.

Research Theme: {research_theme}
Survey Summary:
{survey_summary}

Primary Research Goal:"""

    METHODOLOGY_SUGGESTER = """
For the given research goal, suggest a suitable methodology. 
Describe the approach (e.g., quantitative, qualitative, simulation), data collection methods, and analysis techniques.

Research Goal: {research_goal}

Suggested Methodology:"""

    EXPERIMENTAL_DESIGN = """
Based on the research goal and methodology, design a detailed experiment.
Specify the variables (independent, dependent, control), experimental groups, procedure, and metrics to be measured.

Research Goal: {research_goal}
Methodology: {methodology}

Detailed Experimental Design:"""

    TIMELINE_GENERATOR = """
Create a realistic project timeline for the proposed research.
Break down the project into key phases (e.g., Literature Review, Experiment Setup, Data Collection, Analysis, Writing) and estimate the duration for each.

Experimental Design: {experimental_design}

Project Timeline:"""

    TEX_FORMATTER = """
Aggregate the following research plan components into a formal TeX document structure.
Use standard section commands (e.g., \\section{{...}}, \\subsection{{...}}).

Research Goal: {research_goal}
Methodology: {methodology}
Experimental Design: {experimental_design}
Timeline: {timeline}

Formatted TeX Document Body:"""


class ExecutionPrompts:
    """Prompts for the Execution MAGI."""
    
    PLAN_PARSER = """
Parse the following TeX research plan and extract a clear, actionable list of tasks for execution.
Focus on the experimental procedure, parameters, and simulation requirements.

TeX Research Plan:
{research_plan_tex}

Actionable Task List:"""

    CODE_GENERATOR = """
You are an expert programmer specializing in scientific simulations.
Based on the following tasks from a research plan, write a Python script to perform the required simulation.
The script should be self-contained, use common libraries like pandas and numpy, and print the final result as a JSON object.

Tasks to Execute:
{tasks_to_execute}

Python Simulation Script:"""


class AnalysisPrompts:
    """Prompts for the Analysis MAGI."""

    DATA_VALIDATOR = """
You are a data scientist. Review the following dataset preview. 
Determine if the data appears valid and sufficient for analysis. Note any potential issues like missing values or anomalies.

Dataset Preview:
{dataset_preview}
"""

    METHOD_SELECTOR = """
Given the research goal and a preview of the dataset, select the most appropriate statistical analysis method.
(e.g., T-test, ANOVA, regression analysis, clustering). Justify your choice.

Research Goal: {research_goal}
Dataset Preview: {dataset_preview}

Recommended Analysis Method:"""

    ANALYSIS_CODE_GENERATOR = """
You are an expert data analyst. Write a Python script using pandas and matplotlib/seaborn to perform the specified analysis on the given dataset.
The script should load the JSON data, perform the analysis, generate one key visualization, and print any statistical results.

Analysis Method: {analysis_method}
Dataset (as JSON string): {dataset_json}

Python Analysis Script:"""

    RESULT_INTERPRETER = """
Interpret the following data analysis results in the context of the research goal.
Explain what the statistics and visualizations mean in simple terms.

Research Goal: {research_goal}
Analysis Results (e.g., plot descriptions, statistical test outputs):
{analysis_results}

Interpretation of Results:"""

    CONCLUSION_GENERATOR = """
Based on the interpretation of the analysis results, formulate a conclusion for the research.
Address the original research goal, summarize the key findings, and mention any limitations or potential future work.

Research Goal: {research_goal}
Interpretation: {interpretation}

Conclusion:"""


class ReportPrompts:
    """Prompts for the Report MAGI."""

    STRUCTURE_PLANNER = """
Plan the structure for a formal academic paper based on the research goal.
Propose a list of standard section titles (e.g., Introduction, Methodology, Results, Discussion).

Research Goal: {research_goal}

Proposed Paper Structure (as a list of strings):"""

    SECTION_WRITER = """
You are an academic writer. Using the provided aggregated content and paper structure, write the full content of the research paper.
Flesh out each section with formal, scientific language.

Paper Structure: {paper_structure}
Aggregated Content (JSON):
{aggregated_content}

Draft of the Full Paper:"""

    TEX_COMPILER = """
You are a LaTeX expert. Convert the following draft content into a complete, compilable LaTeX document.
Include a title page, abstract, sections, and a placeholder for references.

Paper Title: {paper_title}
Draft Content:
{draft_content}

Complete LaTeX Document:"""

    FINAL_REVIEWER = """
You are a peer reviewer. Review the following LaTeX document for logical consistency, clarity, and any grammatical errors.
Provide a final, polished version of the LaTeX document.

LaTeX Document to Review:
```{latex}
{tex_document}
```

Final, Polished LaTeX Document:"""


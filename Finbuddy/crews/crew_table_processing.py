from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff

@CrewBase
class TableProcessingCrew:

    agents_config = 'config/agents.yaml'  # 에이전트 설정 파일 경로
    tasks_config = 'config/tasks.yaml'   # 태스크 설정 파일 경로

    @before_kickoff
    def prepare_inputs(self, inputs):
        # 입력 데이터를 초기화하거나 추가 정보를 준비
        inputs['table'] = "Sample markdown table data"  # 예시 테이블 데이터
        return inputs

    @agent
    def tableAnalysisAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['table_analysis_agent'],
            verbose=True,
            tools=['table_analyzer'],
            llm='gpt-4o-mini'
        )

    @agent
    def tableConversionAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['table_conversion_agent'],
            verbose=True,
            tools=['markdown_to_dataframe'],
            llm='gpt-4o-mini'
        )

    @agent
    def tableVisualizationAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['table_visualization_agent'],
            verbose=True,
            tools=['graph_visualizer'],
            llm='gpt-4o-mini'
        )

    @task
    def analyze_table(self) -> Task:
        return Task(
            agent=self.tableAnalysisAgent(),
            inputs={"table_data": "inputs['table']"},
            outputs=["analysis_summary"]
        )

    @task
    def convert_table(self) -> Task:
        return Task(
            agent=self.tableConversionAgent(),
            inputs={"markdown_table": "inputs['table']"},
            outputs=["dataframe"]
        )

    @task
    def visualize_table(self) -> Task:
        return Task(
            agent=self.tableVisualizationAgent(),
            inputs={"dataframe": "outputs['dataframe']"},
            outputs=["graph_visualization"]
        )

    @crew
    def tableProcessingCrew(self) -> Crew:
        return Crew(
            agents=[
                self.tableAnalysisAgent(),
                self.tableConversionAgent(),
                self.tableVisualizationAgent()
            ],
            tasks=[
                self.analyze_table(),
                self.convert_table(),
                self.visualize_table()
            ],
            process=Process.sequential,
            verbose=True,
            description="Crew for processing and visualizing table data"
        )

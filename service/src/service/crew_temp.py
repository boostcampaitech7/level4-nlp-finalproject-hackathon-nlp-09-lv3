from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from .tools.markdown_to_dataframe import markdown_to_dataframe
from .tools.graph_visualizer import create_visualization

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Service():
	"""Service crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, table=None):
		super().__init__()
		self.table = table  # 입력 테이블 저장

	@before_kickoff
	def prepare_inputs(self, inputs=None):
		"""기본 테이블 데이터 초기화"""
		if not inputs:
			inputs = {}
		
		# self.table이 있으면 그것을 사용, 없으면 기본값 사용
		inputs['table'] = self.table if self.table is not None else """
| 항목               | 2022       | 2023       | 2024F      | 2025F      |
|--------------------|------------|------------|------------|------------|
| 매출액 (십억원)    | 50,983.3   | 55,249.8   | 60,440.3   | 37,471.5   |
| 영업이익 (십억원)  | 2,979.4    | 2,529.2    | 1,056.5    | 2,837.0    |
| 세전이익 (십억원)  | 2,778.3    | 2,298.6    | 692.2      | 2,452.5    |
| 순이익 (십억원)    | 1,845.4    | 1,373.7    | 764.2      | 1,118.4    |
| EPS                | 29,574     | 19,709     | 4,441      | 5,293      |
| PER                | 1.49       | 1.21       | 0.81       | 0.79       |
| PBR                | 9.08       | 10.26      | 7.93       | 6.09       |
| EV/EBITDA          | 6.94       | 4.20       | 2.36       | 3.38       |
| ROE                | 401,768    | 111,247    | 417,505    | 428,287    |
| BPS                | 10,000     | 3,500      | 3,500      | 3,500      |
| DPS                |            |            |            |            |"""
		return inputs

	@agent
	def table_conversion_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['table_conversion_agent'],
			tools=[markdown_to_dataframe],
			verbose=True
		)

	@agent
	def table_visualization_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['table_visualization_agent'],
			tools=[create_visualization],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def convert_table(self) -> Task:
		return Task(
			config=self.tasks_config['convert_task'],
			context=[{
				"description": "마크다운 테이블을 DataFrame으로 변환",
				"expected_output": "pandas DataFrame",
				"input": self.table if self.table is not None else inputs.get('table')
			}],
			output_file='dataframe.csv'
		)

	@task
	def visualize_table(self) -> Task:
		return Task(
			config=self.tasks_config['visualize_task'],
			context=[{
				"description": "DataFrame을 시각화",
				"expected_output": "시각화된 그래프",
				"input": "dataframe.csv"
			}],
			output_file='report.png'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Service crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
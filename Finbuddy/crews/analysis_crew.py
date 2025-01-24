from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools import markdown_to_df, bar_visualize, line_visualize, image_processor

@CrewBase
class RetrievalAnalysisCrew:
    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    @agent
    def retrieval_scheduler(self) -> Agent:
        return Agent(
            config=self.agents_config['retrieval_scheduler'],
            verbose=True,
            llm='gpt-4o-mini',
        )

    @agent
    def table_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['table_analyzer'],
            verbose=True,
            tools=[markdown_to_df, bar_visualize, line_visualize],
            llm='gpt-4o-mini',  # 멀티모달로 바꿔야할듯
        )

    @agent
    def graph_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['graph_analyzer'],
            verbose=True,
            tools=[image_processor],
            llm='gpt-4o-mini',  # 멀티모달로 바꿔야할듯
        )

    @agent
    def context_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['context_analyzer'],
            verbose=True,
            llm='gpt-4o-mini',
        )

    @agent
    def visualizer(self) -> Agent:
        return Agent(
            config=self.agents_config['visualizer'],
            verbose=True,
            tools=[bar_visualize, line_visualize],
            llm='gpt-4o-mini',  # 멀티모달로 바꿔야할듯
        )

    @agent
    def final_answer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['final_answer_agent'],
            verbose=True,
            llm='gpt-4o-mini',  # 멀티모달로 바꿔야할듯
        )

    @task
    def process_retrieval_results(self) -> Task:
        return Task(
            config=self.tasks_config['process_retrieval_results']
        )

    @task
    def analyze_table(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_table']
        )

    @task
    def analyze_graph(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_graph']
        )

    @task
    def analyze_context(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_context']
        )

    @task
    def visualize_table(self) -> Task:
        return Task(
            config=self.tasks_config['visualize_table']
        )

    @task
    def generate_final_answer(self) -> Task:
        return Task(
            config=self.tasks_config['generate_final_answer']
        )

    @crew
    def retrieval_analysis_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # @agent 데코레이터로 정의된 에이전트를 자동으로 가져옴
            tasks=self.tasks,    # @task 데코레이터로 정의된 태스크를 자동으로 가져옴
            process=Process.sequential,
            verbose=True,
        )

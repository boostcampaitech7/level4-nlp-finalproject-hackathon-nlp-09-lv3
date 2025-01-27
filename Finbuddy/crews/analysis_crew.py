from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from tools import markdown_to_df, image_processor, bar_visualize, line_visualize

@CrewBase
class AnalysisCrew:
    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    @agent
    def retrieval_scheduler(self) -> Agent:
        return Agent(
            config=self.agents_config['retrieval_scheduler'],
            verbose=True,
            llm='gpt-4o-mini'
        )
    
    @agent
    def table_changer(self) -> Agent:
        return Agent(
            config=self.agents_config['table_changer'],
            verbose=True,
            # tools=[markdown_to_df],
            llm='gpt-4o-mini'
        )
    
    @agent
    def table_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['table_analyzer'],
            verbose=True,
            llm='gpt-4o-mini'
        )
    
    @agent
    def graph_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['graph_analyzer'],
            verbose=True,
            # tools=[image_processor],
            llm='gpt-4o-mini'
        )
    
    @agent
    def context_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['context_analyzer'],
            verbose=True,
            llm='gpt-4o-mini'
        )
    
    @agent
    def visualizer(self) -> Agent:
        return Agent(
            config=self.agents_config['visualizer'],
            verbose=True,
            # tools=[bar_visualize, line_visualize],
            llm='gpt-4o-mini'
        )
    
    @agent
    def code_executor(self) -> Agent:
        return Agent(
            config=self.agents_config['code_executor'],
            verbose=True,
            llm='gpt-4o-mini'
        )
    
    @agent
    def final_answer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['final_answer_agent'],
            verbose=True,
            llm='gpt-4o-mini'
        )
    
    @task
    def retrieval_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieval_task']
        )
    
    @task
    def table_conversion_task(self) -> Task:
        return Task(
            config=self.tasks_config['table_conversion_task']
        )
    
    @task
    def table_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['table_analysis_task']
        )
    
    @task
    def graph_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['graph_analysis_task']
        )
    
    @task
    def context_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['context_analysis_task']
        )
    
    @task
    def visualization_task(self) -> Task:
        return Task(
            config=self.tasks_config['visualization_task']
        )
    
    @task
    def code_execution_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_execution_task']
        )
    
    @task
    def answer_task(self) -> Task:
        return Task(
            config=self.tasks_config['answer_task']
        )
    
    @crew
    def analysis_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # @agent 데코레이터로 감싸진 에이전트를 자동으로 가져옴
            tasks=self.tasks,    # @task 데코레이터로 감싸진 태스크를 자동으로 가져옴
            process=Process.sequential,
            verbose=True,
        )

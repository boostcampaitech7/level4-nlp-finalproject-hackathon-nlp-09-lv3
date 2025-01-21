from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools import ducducsearch

@CrewBase
class BlogCrew:
    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['researcher'],
            verbose = True,
            tools = [ducducsearch.search],
            llm = 'gpt-4o-mini'
        )
    @agent
    def writer(self) -> Agent:
        return Agent(
            config = self.agents_config['writer'],
            verbose = True,
            llm = 'gpt-4o-mini',
        )
    
    @task
    def research(self) -> Task:
        return Task(
            config = self.tasks_config['search_task']
        )
    
    @task
    def write(self) -> Task:
        return Task(
            config = self.tasks_config['write_task']
        )
    
    @crew
    def blog_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # @agent 데코레이터로 감싸진 애들을 자동으로 가져옴
            tasks=self.tasks,    # @task 데코레이터로 감싸진 애들을 자동으로 가져옴
            process=Process.sequential,
            verbose=True,
        )
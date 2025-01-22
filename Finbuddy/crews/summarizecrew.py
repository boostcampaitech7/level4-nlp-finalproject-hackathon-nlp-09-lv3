from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import SerperDevTool

@CrewBase
class SummarizeCrew:

    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    @before_kickoff
    def prepare_inputs(self, inputs):
        inputs['topic'] = "Some extra information" # 주제, 주가 같은 쿼리
        return inputs
    

    @agent
    def news_collector(self) -> Agent:
        return Agent(
            config = self.agents_config['news_collector_agent'],
            verbose = True,
            tools = [SerperDevTool()] # 검색엔진
        )
    
    @agent
    def news_summarizer(self) -> Agent:
        return Agent(
            config = self.agents_config['summary_agent'],
            verbose = True
        )
    
    @task
    def news_collect(self) -> Task:
        return Task(
            config = self.tasks_config['news_collectiong_task']
        )
    
    @task
    def news_summarize(self) -> Task:
        return Task(
            config = self.tasks_config['summarization_task']
        )
    
    @crew
    def summarization_crew(self) -> Crew:
        return Crew(
            agents = [
                self.news_collector,
                self.news_summarizer,
            ],
            tasks = [
                self.news_collect,
                self.news_summarize,
            ],
            process = Process.sequential
        )
    
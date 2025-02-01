from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from tools import retrieve_information

@CrewBase
class Service:
    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 
    
    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs 

    @agent
    def retriever(self) -> Agent:
        return Agent(
            config = self.agents_config['retriever'],
            verbose = True,
            tools = [retrieve_information],
        )
    @task
    def retriever(self) -> Task:
        return Task(
            config = self.tasks_config['retrieve_task']
        )
    
    @crew
    def retriever_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # @agent 데코레이터로 감싸진 애들을 자동으로 가져옴
            tasks=self.tasks,    # @task 데코레이터로 감싸진 애들을 자동으로 가져옴
            process=Process.sequential,
            verbose=True,
        )
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from .tools import code_executetool

@CrewBase
class ContextCrew:
    agents_config = 'config/context_agents.yaml' 
    tasks_config = 'config/context_tasks.yaml' 

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed

    @agent
    def context_analyzer(self) -> Agent:
        return Agent(
            config = self.agents_config['context_analyzer'],
            verbose = True,
            llm = 'gpt-4o-mini',
        )
    @task
    def context_analysis_task(self) -> Task:
        return Task(
            config = self.tasks_config['context_analysis_task']
        )

    def context_crew(self) -> Crew:
        return Crew(
            agents=[self.context_analyzer()],  # @agent 데코레이터로 감싸진 애들을 자동으로 가져옴
            tasks=[self.context_analysis_task()],    # @task 데코레이터로 감싸진 애들을 자동으로 가져옴
            process=Process.sequential,
            verbose=True,
        )
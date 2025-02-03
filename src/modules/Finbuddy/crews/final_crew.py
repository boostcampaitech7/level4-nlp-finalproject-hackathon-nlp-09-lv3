from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from .tools import code_executetool

@CrewBase
class FinalCrew:
    agents_config = 'config/final_agents.yaml' 
    tasks_config = 'config/final_tasks.yaml' 

    @before_kickoff
    def before_kickoff_function(self, inputs):
        return inputs # You can return the inputs or modify them as needed

    @agent
    def final_answerman(self) -> Agent:
        return Agent(
            config = self.agents_config['final_answerman'],
            verbose = True,
            llm = 'gpt-4o',
        )
    @task
    def final_answer_task(self) -> Task:
        return Task(
            config = self.tasks_config['final_answer_task']
        )

    def final_crew(self) -> Crew:
        return Crew(
            agents=[self.final_answerman()],  # @agent 데코레이터로 감싸진 애들을 자동으로 가져옴
            tasks=[self.final_answer_task()],    # @task 데코레이터로 감싸진 애들을 자동으로 가져옴
            process=Process.sequential,
            verbose=True,
        )
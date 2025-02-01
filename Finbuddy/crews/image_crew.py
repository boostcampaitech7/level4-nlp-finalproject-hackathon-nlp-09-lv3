from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from .tools import code_executetool

@CrewBase
class ImageCrew:
    agents_config = 'config/image_agents.yaml' 
    tasks_config = 'config/image_tasks.yaml' 

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed

    @agent
    def graph_analyzer(self) -> Agent:
        return Agent(
            config = self.agents_config['graph_analyzer'],
            verbose = True,
            llm = 'gpt-4o',
        )
    @task
    def graph_analysis_task(self) -> Task:
        return Task(
            config = self.tasks_config['graph_analysis_task']
        )

    def image_crew(self) -> Crew:
        return Crew(
            agents=[self.graph_analyzer()],  # @agent 데코레이터로 감싸진 애들을 자동으로 가져옴
            tasks=[self.graph_analysis_task()],    # @task 데코레이터로 감싸진 애들을 자동으로 가져옴
            process=Process.sequential,
            verbose=True,
        )
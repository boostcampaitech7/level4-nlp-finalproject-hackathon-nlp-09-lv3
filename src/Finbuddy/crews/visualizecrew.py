from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff

@CrewBase
class VisualizeCrew:

    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    @before_kickoff
    def prepare_inputs(self, inputs):
        inputs['table or image'] = "Some extra information" # 테이블, 그래프같은거
        return inputs
    
    @agent
    def visualator(self) -> Agent:
        return Agent(
            config = self.agents_config['visualization_agent'],
            verbose = True,
            # tools = visualizationTool tool 만들어야함
        )
    
    @task
    def visualize(self) -> Task:
        return Task(
            config = self.tasks_config['visualization_task']
        )
    
    @crew
    def visualization_crew(self) -> Crew:
        return Crew(
            agents = [
                self.visualator()
            ],
            tasks = [
                self.visualize()
            ],
            process = Process.sequential
        )
    
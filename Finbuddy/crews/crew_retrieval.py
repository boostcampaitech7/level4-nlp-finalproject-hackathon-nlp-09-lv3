from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff

@CrewBase
class RetrievalCrew:

    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    print(agents_config)

    @before_kickoff
    def prepare_inputs(self, inputs):
        inputs['table or image'] = "Some extra information" # 테이블, 그래프같은거
        return inputs
    
    @agent
    def retrievalAgent(self) -> Agent:
        return Agent(
            config = self.agents_config['retrieval_scheduler'],
            verbose = True,
        )

    @agent
    def contextAgent(self) -> Agent:
        return Agent(
            config = self.agents_config['context_analyzer'],
            verbose = True,
        )

    
    @task
    def finalAnswerAgent(self) -> Task:
        return Task(
            config = self.tasks_config['final_answer_agent']
        )
    
    @crew
    def visualization_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,    
            process=Process.sequential,
            verbose=True,
        )
    
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff

@CrewBase
class RetrievalCrew:

    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed
    
    # @agent
    # def retrieval_agent(self) -> Agent:
    #     return Agent(
    #         config = self.agents_config['retrieval_scheduler'],
    #         verbose = True,
    #         llm='gpt-4o-mini'
    #     )

    @agent
    def context_agent(self) -> Agent:
        return Agent(
            config = self.agents_config['context_analyzer'],
            verbose = True,
            llm='gpt-4o-mini'
        )
    
    @agent
    def final_answer_agent(self) -> Agent:
        return Agent(
            config = self.agents_config['final_answer_agent'],
            verbose = True,
            llm='gpt-4o-mini'
        )

    # @agent
    # def graph_agent(self) -> Agent:
    #     return Agent(
    #         config = self.agents_config['graph_analyzer'],
    #         verbose = True,
    #         llm='gpt-4o-mini'
    #     )
    # @task
    # def retrieval_task(self) -> Task:
    #     return Task(
    #         config = self.tasks_config['retrieval_task']
    #     )
        
    @task
    def context_analysis_task(self) -> Task:
        return Task(
            config = self.tasks_config['context_analysis_task']
        )
    
    # @task
    # def graph_analysis_task(self) -> Task:
    #     return Task(
    #         config = self.tasks_config['graph_analysis_task']
    #     )   

    @task
    def final_answer_task(self) -> Task:
        def run_task(inputs):
            return self.final_answer_agent.execute(inputs)

        def validate_output(output, inputs):
            query = inputs.get("query", "")  
            return query in output
          
        return Task(
            description="Final answer generation task",
            config = self.tasks_config['answer_task'],
            feedback=validate_output  # 검증 로직 추가
        )
    
    @crew
    def retrieval_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,    
            process=Process.sequential,
            verbose=True,
        )
    
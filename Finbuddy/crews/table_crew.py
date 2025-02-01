from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from .tools import code_executetool
from pydantic import BaseModel

class Codeoutput(BaseModel):
    description: str
    code: str
@CrewBase
class TableCrew:
    agents_config = 'config/table_agents.yaml' 
    tasks_config = 'config/table_tasks.yaml' 

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed

    @agent
    def code_generator(self) -> Agent:
        return Agent(
            config = self.agents_config['code_generator'],
            verbose = True,
            llm = 'gpt-4o',
        )
    @agent
    def code_executor(self) -> Agent:
        return Agent(
            config = self.agents_config['code_executor'],
            verbose = True,
            llm = 'gpt-4o',
            tools = [code_executetool.execute_code],
            
        )
    @agent
    def table_answerman(self) -> Agent:
        return Agent(
            config = self.agents_config['table_answerman'],
            verbose = True,
            llm = 'gpt-4o',
        )

    @task
    def code_generate_task(self) -> Task:
        return Task(
            config = self.tasks_config['code_generate_task'],
            output_pydantic=Codeoutput
        )

    @task
    def code_execution_task(self) -> Task:
        return Task(
            config = self.tasks_config['code_execution_task'],
        )

    @task
    def answer_task(self) -> Task:
        return Task(
            config = self.tasks_config['table_answer_task']
        )

    @crew
    def table_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # @agent 데코레이터로 감싸진 애들을 자동으로 가져옴
            tasks=self.tasks,    # @task 데코레이터로 감싸진 애들을 자동으로 가져옴
            process=Process.sequential,
            verbose=True,
        )
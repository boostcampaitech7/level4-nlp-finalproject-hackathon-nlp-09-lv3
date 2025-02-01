from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff

# 도구(tool) 임포트
# from tools.document_retrieval_tool import retrieve_information
# from tools.generate_visualization_code_tool import generate_visualization_code
# from tools.execute_visualization_code_tool import execute_visualization_code

from tools import document_retrieval_tool
from tools import generate_visualization_code_tool
from tools import execute_visualization_code_tool

@CrewBase
class Service:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"[Before Kickoff] inputs: {inputs}")
        return inputs

    # 1) 문서(및 테이블) 검색 agent / task
    @agent
    def retriever(self) -> Agent:
        return Agent(
            config=self.agents_config['retriever'],
            verbose=True,
            tools=[document_retrieval_tool],
        )
    
    @task
    def retrieve_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieve_task']
        )
    
    # 2) LLM을 활용하여 시각화 코드 생성 agent / task
    @agent
    def code_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['code_generator'],
            verbose=True,
            tools=[generate_visualization_code_tool],
        )
    
    @task
    def code_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_generation_task']
        )
    
    # 3) 생성된 코드를 실행하여 시각화 생성 agent / task
    @agent
    def code_executor(self) -> Agent:
        return Agent(
            config=self.agents_config['code_executor'],
            verbose=True,
            tools=[execute_visualization_code_tool],
        )
    
    @task
    def code_execution_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_execution_task']
        )
    
    # 4) 전체 프로세스 관리 crew (순차적 실행)
    @crew
    def processing_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # 모든 @agent 등록 agent 자동 집합
            tasks=self.tasks,    # 모든 @task 등록 task 자동 집합
            process=Process.sequential,
            verbose=True,
        )
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from .tools.markdown_to_csv import process_markdown_folder
from .tools.graph_visualizer import create_visualization
import os

@CrewBase
class Service():
    """Service crew"""

    def __init__(self, md_folder: str = None, csv_file: str = None):
        super().__init__()
        base_path = os.path.dirname(os.path.abspath(__file__))

        # YAML 설정 파일 경로
        self.agents_config = os.path.join(base_path, 'config', 'agents.yaml')
        self.tasks_config = os.path.join(base_path, 'config', 'tasks.yaml')

        # 입력 폴더 및 출력 파일 경로 기본값 설정
        # self.md_folder = md_folder or os.path.join(base_path, 'markdowns')
        self.md_folder = "/data/level4-nlp-finalproject-hackathon-nlp-09-lv3/service/markdowns"


    @before_kickoff
    def prepare_inputs(self, inputs=None):
        """
        크루 시작 전에 md_folder, csv_file 등을 context에 넣어둔다.
        """
        if not inputs:
            inputs = {}

        # 혹시 생성자에서 None 이었으면 디폴트값 지정
        if not self.md_folder:
            self.md_folder = os.path.join(os.getcwd(), "markdowns")

        # crewai context에 저장하면, "{md_folder}" 식으로 태스크에서 치환 가능
        inputs["md_folder"] = self.md_folder
        return inputs

    @agent
    def markdown_to_csv_agent(self) -> Agent:
        """
        마크다운(.md) -> CSV 변환 에이전트 (config=로 YAML에서 설정을 로딩)
        """
        return Agent(
            config=self.agents_config["markdown_to_csv_agent"],  # agents.yaml의 키
            tools=[process_markdown_folder],
            verbose=True
        )

    @agent
    def csv_visualization_agent(self) -> Agent:
        """
        CSV -> 시각화 에이전트
        """
        return Agent(
            config=self.agents_config["csv_visualization_agent"],  # agents.yaml의 키
            tools=[create_visualization],
            llm=None,
            verbose=True
        )

    @task
    def convert_markdown_task(self) -> Task:
        """
        (1) 마크다운 폴더 -> CSV 변환
        - config=self.tasks_config[...]로 tasks.yaml에서 설정을 가져온다.
        - 추가로 context, output_file 등을 코드에서 override 가능
        """
        return Task(
            config=self.tasks_config["convert_markdown_task"],  # tasks.yaml의 키
            tool_arguments={"base_folder": "{md_folder}"},
            context=[{
                "description": "마크다운 폴더에서 표 및 텍스트를 추출하여 CSV로 변환",
                "expected_output": "csv file",
                "input": "{md_folder}"
            }],
            output_file="markdown_process_result.json"
        )

    @task
    def visualize_csv_task(self) -> Task:
        """
        (2) 변환된 CSV를 이용해 그래프 생성
        """
        return Task(
            config=self.tasks_config["visualize_csv_task"],     # tasks.yaml의 키
            tool_arguments={
            "csv_path": "/data/level4-nlp-finalproject-hackathon-nlp-09-lv3/service/tables"
            },
            context=[{
                "description": "tables 폴더 내 CSV들을 표 이미지로 변환",
                "expected_output": "tables_image 폴더에 여러 PNG 생성",
            }],
        )

    @crew
    def crew(self):
        """
        전체 작업을 순차적으로 실행하는 Crew
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            # tasks=[
            #     self.convert_markdown_task(),
            #     self.visualize_csv_task()
            # ],
            process=Process.sequential,
            verbose=True
        )

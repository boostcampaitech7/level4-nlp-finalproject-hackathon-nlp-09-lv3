# import os
# import re
# import pandas as pd
# from io import StringIO
# from crewai.tools import tool

# @tool("markdown_to_csv")
# def process_markdown_folder(base_folder: str) -> str:
#     """
#     특정 폴더에서 마크다운(.md) 파일을 읽어 표를 추출하고,
#     CSV 및 텍스트 파일로 저장합니다.

#     Args:
#         base_folder (str): .md 파일들이 들어 있는 최상위 폴더 경로.

#     Returns:
#         str: 작업 완료 메시지.
#     """
#     md_files = []
#     for root, dirs, files in os.walk(base_folder):
#         for file in files:
#             if file.endswith(".md"):
#                 md_files.append(os.path.join(root, file))

#     if not md_files:
#         return f"No .md files found in folder: {base_folder}"

#     def markdown_to_dataframe(markdown_table: str) -> pd.DataFrame:
#         """
#         실제 마크다운 문자열에서 표 부분만 Pandas DataFrame으로 변환
#         """
#         try:
#             lines = markdown_table.strip().split("\n")
#             # 표 헤더구분선(----)만 있는 줄 제거
#             filtered_lines = [line for line in lines
#                               if not set(line.strip()).issubset({"|", "-", " "})]
#             filtered_table = "\n".join(filtered_lines)

#             # 구분자를 | 로 하여 CSV 읽기
#             df = pd.read_csv(StringIO(filtered_table), sep="|",
#                              engine="python", skipinitialspace=True)
#             # Unnamed 등 자동 생성된 컬럼 제거
#             df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
#             df.columns = df.columns.str.strip()
#             return df
#         except:
#             return None

#     for md_file in md_files:
#         with open(md_file, "r", encoding="utf-8") as file:
#             content = file.read()

#         # 정규표현식으로 마크다운 표만 추출
#         tables = re.findall(r"(\|.*?\|(?:\n\|[-| ]+\|)?(?:\n\|.*?\|)+)",
#                             content, re.DOTALL)
#         # 표를 제외한 텍스트 부분도 저장하기 위해
#         text_data = re.sub(r"(\|.*?\|(?:\n\|[-| ]+\|)?(?:\n\|.*?\|)+)",
#                            "", content).strip()

#         for i, table_str in enumerate(tables, start=1):
#             df = markdown_to_dataframe(table_str)
#             if df is not None:
#                 # 같은 md 파일 내 여러 표가 있으면 _table_1, _table_2... 로
#                 csv_name = f"{os.path.splitext(os.path.basename(md_file))[0]}_table_{i}.csv"
#                 output_csv = os.path.join(os.path.dirname(md_file), csv_name)
#                 df.to_csv(output_csv, index=False, encoding="utf-8-sig")

#         # 원문 텍스트 부분도 별도 .txt 로 저장
#         text_name = f"{os.path.splitext(os.path.basename(md_file))[0]}_text.txt"
#         text_output = os.path.join(os.path.dirname(md_file), text_name)
#         with open(text_output, "w", encoding="utf-8") as text_file:
#             text_file.write(text_data)

#     return f"Processed {len(md_files)} .md files in folder: {base_folder}"

# src/tools/markdown_to_csv.py

import os
import re
import pandas as pd
from io import StringIO
from crewai.tools import tool

@tool("markdown_to_csv")
def process_markdown_folder(base_folder: str) -> str:
    """
    특정 폴더에서 마크다운(.md) 파일을 읽어 표를 추출하고,
    CSV 파일로 저장합니다. (tables 폴더에 저장)

    Args:
        base_folder (str): .md 파일들이 들어 있는 최상위 폴더 경로.

    Returns:
        str: 작업 완료 메시지.
    """

    # tables 디렉토리 생성 (base_folder의 상위 폴더에 만든다고 가정)
    output_folder = os.path.join(os.path.dirname(base_folder), "tables")
    os.makedirs(output_folder, exist_ok=True)

    # 폴더 내 모든 .md 파일 탐색
    md_files = []
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))

    if not md_files:
        return f"No .md files found in folder: {base_folder}"

    # 표 파싱 함수 (마크다운 테이블 -> DataFrame)
    def markdown_to_dataframe(markdown_table: str) -> pd.DataFrame:
        """
        표 문자열을 DataFrame으로 변환 (행 열 개수를 표준화)
        """
        try:
            lines = markdown_table.strip().split("\n")
            # 헤더 구분선(--- 등)만 있는 줄 제거
            filtered_lines = [
                line for line in lines
                if not set(line.strip()).issubset({"|", "-", " "})
            ]
            filtered_table = "\n".join(filtered_lines)

            rows = filtered_table.split("\n")
            max_columns = max(len(row.split("|")) for row in rows)  # 최대 열 개수

            # 모든 행의 컬럼 수를 max_columns에 맞춰 빈 칸으로 채움
            standardized_rows = []
            for row in rows:
                split_row = row.split("|")
                if len(split_row) < max_columns:
                    split_row += [""] * (max_columns - len(split_row))
                standardized_rows.append("|".join(split_row))

            standardized_table = "\n".join(standardized_rows)

            df = pd.read_csv(
                StringIO(standardized_table),
                sep="|",
                engine="python",
                skipinitialspace=True
            )
            # Unnamed 컬럼 제거
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
            df.columns = df.columns.str.strip()
            return df

        except Exception as e:
            print(f"[Error] Converting table: {e}")
            return None

    # .md 파일별로 표 추출 및 CSV 저장
    file_count = 0
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as file:
            content = file.read()

        # 정규표현식으로 표를 추출
        # (새 방식) 행이 '|'로 시작하는 구간을 여러 줄 매칭
        tables = re.findall(r"((?:\|.*?\|(?:\n|$))+)", content)

        # 표가 하나 이상 있으면 CSV 파일로 변환
        for i, table_str in enumerate(tables, start=1):
            df = markdown_to_dataframe(table_str)
            if df is not None and not df.empty:
                # 출력 파일명: {마크다운 파일명}_table_{i}.csv
                md_filename = os.path.splitext(os.path.basename(md_file))[0]
                csv_name = f"{md_filename}_table_{i}.csv"
                output_csv = os.path.join(output_folder, csv_name)

                df.to_csv(output_csv, index=False, encoding="utf-8-sig")
                print(f"[Saved] {output_csv}")
                file_count += 1

    return f"Processed {len(md_files)} .md files in folder: {base_folder}, created {file_count} CSVs in '{output_folder}'."

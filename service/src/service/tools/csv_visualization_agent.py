# # src/tools/graph_visualizer.py
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from crewai.tools import tool

# @tool("create_visualization")
# def create_visualization(csv_path: str) -> str:
#     """
#     주어진 CSV 파일을 불러와 간단한 라인 그래프 등을 그려 report.png 로 저장.
#     """
#     try:
#         df = pd.read_csv(csv_path)

#         plt.style.use('dark_background')
#         plt.figure(figsize=(12, 8))

#         # 예시로 항목이 '매출액 (십억원)', '영업이익 (십억원)', '순이익 (십억원)' 등일 경우
#         metrics = ['매출액 (십억원)', '영업이익 (십억원)', '순이익 (십억원)']
#         # 첫 번째 컬럼이 "항목", 나머지는 연도별 수치라고 가정
#         if '항목' not in df.columns:
#             raise ValueError("CSV에 '항목' 컬럼이 없으므로 예시 그래프 작성 불가")

#         # 항목별 라인 그래프
#         for metric in metrics:
#             if metric in df['항목'].values:
#                 row_data = df[df['항목'] == metric].iloc[:, 1:].values[0]  # 연도별 값
#                 col_labels = df.columns[1:]  # 실제로는 연도 (2022, 2023, 2024F 등)
#                 plt.plot(col_labels, row_data, marker='o', label=metric)

#         plt.title('주요 재무지표 추이', fontsize=16, pad=20)
#         plt.legend(fontsize=12)
#         plt.grid(True, alpha=0.3)

#         plt.savefig('report.png', dpi=300, bbox_inches='tight')
#         plt.close()

#         return "report.png가 생성되었습니다."
#     except Exception as e:
#         raise ValueError(f"시각화 생성 오류: {e}")


# src/tools/csv_visualization_agent.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.table import Table
from matplotlib import rcParams
import matplotlib.font_manager as fm
from crewai.tools import tool

@tool("create_visualization")
def create_visualization(csv_path: str) -> str:
    """
    'csv_path' 경로 내 모든 CSV 파일을 순회하여,
    테이블 형태의 PNG 이미지를 'tables_image' 폴더에 생성합니다.

    Args:
        csv_path (str): CSV 파일들이 들어 있는 폴더 경로.

    Returns:
        str: 처리 완료 메시지 (생성된 이미지 파일 목록 등).
    """

    # 한글 폰트 설정 (원하는 폰트 경로가 있을 경우 사용)
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        rcParams["font.family"] = font_prop.get_name()
        print(f"[Info] Using font: {font_prop.get_name()}")
    else:
        print("[Warning] 지정한 한글 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")

    # 결과 이미지를 저장할 폴더: csv_path와 같은 상위 디렉토리에 "tables_image" 생성
    images_folder = os.path.join(os.path.dirname(csv_path), "tables_image")
    os.makedirs(images_folder, exist_ok=True)

    # 테이블 폴더 내 CSV 목록 확인
    if not os.path.exists(csv_path):
        return f"Folder does not exist: {csv_path}"

    csv_files = [f for f in os.listdir(csv_path) if f.endswith(".csv")]
    if not csv_files:
        return f"No CSV files found in folder: {csv_path}"

    # CSV 파일마다 표 이미지를 생성
    saved_images = []
    for csv_file in csv_files:
        csv_path = os.path.join(csv_path, csv_file)
        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                print(f"[Warning] {csv_file} is empty. Skipped.")
                continue

            # 이미지 파일명 설정
            image_name = os.path.splitext(csv_file)[0] + ".png"
            image_path = os.path.join(images_folder, image_name)

            # matplotlib으로 표 렌더링
            fig, ax = plt.subplots(
                figsize=(max(10, df.shape[1]),
                         max(5, df.shape[0] * 0.6))
            )
            ax.axis("tight")
            ax.axis("off")

            # Matplotlib의 Table 객체 생성
            table = Table(ax, bbox=[0, 0, 1, 1])
            nrows, ncols = df.shape

            # 열너비/행높이 설정
            # (열너비는 데이터 길이에 따라 적당히 계산)
            col_widths = [
                max(df[col].astype(str).map(len).max(), len(col)) / 30
                for col in df.columns
            ]
            row_height = 1.0 / (nrows + 1)  # 헤더 포함

            # 헤더 행 그리기
            for col_index, column in enumerate(df.columns):
                cell = table.add_cell(
                    row=0, col=col_index,
                    width=col_widths[col_index], height=row_height,
                    loc="center", facecolor="white", edgecolor="black"
                )
                cell.get_text().set_text(column)
                cell.get_text().set_fontsize(12)
                cell.get_text().set_color("black")

            # 데이터 행
            for row_index in range(nrows):
                for col_index in range(ncols):
                    value = df.iloc[row_index, col_index]
                    cell = table.add_cell(
                        row=row_index + 1, col=col_index,
                        width=col_widths[col_index], height=row_height,
                        loc="center", facecolor="white", edgecolor="black"
                    )
                    cell.get_text().set_text(str(value))
                    cell.get_text().set_fontsize(10)
                    cell.get_text().set_color("black")

            # Table 객체를 Axes에 추가
            ax.add_table(table)

            # 이미지 저장
            plt.savefig(image_path, dpi=300, bbox_inches="tight")
            plt.close()

            saved_images.append(image_path)
            print(f"[Saved] table visualization -> {image_path}")

        except Exception as e:
            print(f"[Error] processing {csv_file}: {e}")

    if saved_images:
        return f"Created {len(saved_images)} table images in '{images_folder}'."
    else:
        return f"No valid CSV to visualize in '{csv_path}' (all empty or error)."

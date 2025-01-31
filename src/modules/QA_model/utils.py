import glob
import pandas as pd

def load_csv_data_from_dirs(base_dir: str) -> pd.DataFrame:
    csv_files = glob.glob(f"{base_dir}/**/*.csv", recursive=True)
    all_df_list = []
    for csv_path in csv_files:
        try:
            df = pd.read_csv(csv_path, keep_default_na=False)
            df["__csv_path__"] = csv_path
            all_df_list.append(df)
        except Exception as e:
            print(f"[WARN] CSV 로드 오류: {csv_path}, {e}")
    return pd.concat(all_df_list, ignore_index=True) if all_df_list else pd.DataFrame()

def build_rag_data(df: pd.DataFrame) -> list:
    return [
        {
            "id": row.get("id", f"row_{idx}"),
            "summary": row.get("summary", ""),
            "original_content": row.get("original_content", ""),
        }
        for idx, row in df.iterrows()
    ]

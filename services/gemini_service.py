e# gpt_service.py - Generate chapter titles using Gemini model
import pandas as pd
from tqdm import tqdm
import google.generativeai as genai
import os

# .env에서 API 키 가져오기
genai.configure(api_key=os.getenv("AIZaSyANaWrhmztst9WVHq-FFA6juk1IDoQtbp"))
model = genai.GenerativeModel("models/gemini-1.5-flash")


def generate_chapter_titles(input_path, video_id):
    try:
        # 데이터 로드
        df = pd.read_csv(input_path)
        df = df[['block_index', 'text', 'timestamp']].dropna()
        df.columns = ['index', 'text', 'timestamp']

        # 챕터 제목 생성
        chapter_data = []
        for idx, group in tqdm(df.groupby("index")):
            text_block = " ".join(group["text"].tolist())[:1500]
            timestamp = group["timestamp"].iloc[0]

            prompt = f"""
        다음 자막 내용을 대표할 수 있는 간결한 한국어 챕터 제목을 **한 문장으로** 작성해 주세요.
            - 설명하지 마세요
            - 제목 후보를 나열하지 마세요.
            _ '**' 또는 인용 부호 없이 제목 **내용만** 출력하세요.
            - 자막 내용이 부족해도 임의로 가장 적절한 제목을 만들어 주세요.
            [자막 내용]
            {text_block}
            """

            try:
                response = model.generate_content(prompt)
                title = response.text.strip().split("\n")[0]
            except Exception as e:
                title = "내용 요약"

            chapter_data.append({
                "timestamp": timestamp,
                "chapter_title": title
            })

        # 결과 저장 경로
        output_path = f"static/uploads/{video_id}/chapters.csv"
        chapter_df = pd.DataFrame(chapter_data)
        chapter_df.to_csv(output_path, index=False)
        print("[INFO] 저장 완료:", output_path)
        return output_path
    except Exception as e:
        print(f"[ERROR] Chapter title generation failed: {str(e)}")
        return None

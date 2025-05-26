# gpt_service.py - Generate chapter titles using Gemini model
import pandas as pd
from tqdm import tqdm
import google.generativeai as genai
import os

# \ud658\uacbd \ubcc0\uc218\uc5d0\uc11c API \ud0a4 \uac00\uc838\uc624\uae30
genai.configure(api_key=os.getenv("AIZaSyANaWrhmztst9WVHq-FFA6juk1IDoQtbp"))
model = genai.GenerativeModel("models/gemini-1.5-flash")


def generate_chapter_titles(input_path, video_id):
    try:
        # \ub370\uc774\ud130 \ub85c\ub4dc
        df = pd.read_csv(input_path)
        df = df[['block_index', 'text', 'timestamp']].dropna()
        df.columns = ['index', 'text', 'timestamp']

        # \ucc55\ud130 \uc81c\ubaa9 \uc0dd\uc131
        chapter_data = []
        for idx, group in tqdm(df.groupby("index")):
            text_block = " ".join(group["text"].tolist())[:1500]
            timestamp = group["timestamp"].iloc[0]

            prompt = f"""
            \ub2e4\uc74c \uc790\ub9c9 \ub0b4\uc6a9\uc744 \ub300\ud45c\ud560 \uc218 \uc788\ub294 \uac04\uacb0\ud55c \ud55c\uad6d\uc5b4 \ucc55\ud130 \uc81c\ubaa9\uc744 **\ud55c \ubb38\uc7a5\uc73c\ub85c** \uc791\uc131\ud574 \uc8fc\uc138\uc694.
            - \uc124\uba85\ud558\uc9c0 \ub9c8\uc138\uc694.
            - \uc81c\ubaa9 \ud6c4\ubcf4\ub97c \ub098\uc5f4\ud558\uc9c0 \ub9c8\uc138\uc694.
            - '**' \ub610\ub294 \uc778\uc6a9 \ubd80\ud638 \uc5c6\uc774 \uc81c\ubaa9 **\ub0b4\uc6a9\ub9cc** \ucd9c\ub825\ud558\uc138\uc694.
            - \uc790\ub9c9 \ub0b4\uc6a9\uc774 \ubd80\uc871\ud574\ub3c4 \uc784\uc758\ub85c \uac00\uc7a5 \uc801\uc808\ud55c \uc81c\ubaa9\uc744 \ub9cc\ub4e4\uc5b4 \uc8fc\uc138\uc694.
            [\uc790\ub9c9 \ub0b4\uc6a9]
            {text_block}
            """

            try:
                response = model.generate_content(prompt)
                title = response.text.strip().split("\n")[0]
            except Exception as e:
                title = "\ub0b4\uc6a9 \uc694\uc57d"

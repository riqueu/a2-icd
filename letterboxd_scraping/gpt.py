import openai as ai
import pandas as pd

file = open("gpt_api.txt", "r")
key_gpt = file.read()

client = ai.OpenAI(api_key=key_gpt)

# TODO: TESTAR!!!

def get_response(prompt, max_tokens=150, model="gpt-3.5-turbo-0125", temperature = 0):
    response = client.chat.completions.create(
        messages = prompt, # ou prompt = prompt? TODO: VERIFICAR
        model = model,
        max_tokens = max_tokens,
        temperature = temperature
        )
    return response.choices[0].message.content


def summary_based_on_reviews(df):
    # TODO: REVISAR E MELHORAR E COMENTAR
    reviews = df["Review"].tolist()
    prompt = "Based on user reviews on Letterboxd, give me a brief summary of this movie:\n"
    for review in reviews:
        prompt += f"- {review}\n"
    return get_response(prompt)


def summary_public_opinion(df):
    # TODO: REVISAR E MELHORAR E COMENTAR
    mean = df["Scores"].mean()
    reviews = df["Review"].tolist()
    prompt = f"""Public opinion on the movie based on:\n
    Average score: {mean:.2f}\n
    and the following reviews:\n"""
    for review in reviews:
        prompt += f"- {review}\n"
    return get_response(prompt)


def keywords_for_movie(df):
    # TODO: REVISAR E MELHORAR E COMENTAR
    reviews = df["Review"].tolist()
    prompt = "Keywords that describe this movie based on its reviews:\n"
    for review in reviews:
        prompt += f"- {review}\n"
    return get_response(prompt)

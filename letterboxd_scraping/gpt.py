import openai as ai
import pandas as pd

file = open("gpt_api.txt", "r")
key_gpt = file.read()

client = ai.OpenAI(api_key="sk-proj-E654f2NNIYhVnMSuWRzvT3BlbkFJrAidSyfoXD0raVkttQhi")

# TODO: TESTAR!!!

def get_response(prompt, max_tokens=150, model="gpt-3.5-turbo-0125", temperature = 0):
    response = client.chat.completions.create(
        messages = [{'role': 'user', 'content': prompt}],
        model = model,
        max_tokens = max_tokens,
        temperature = temperature
        )
    
    return response.choices[0].message.content


def append_reviews_to_prompt(prompt, reviews):
    for review in reviews:
        prompt += f"- {review}\n"

    return prompt

def summary_based_on_reviews(reviews):
    # TODO: REVISAR E MELHORAR E COMENTAR
    prompt = "Based on user reviews on Letterboxd, give me a brief summary of this movie:\n"
    prompt = append_reviews_to_prompt(prompt, reviews)

    return get_response(prompt)


def summary_public_opinion(mean, reviews):
    # TODO: REVISAR E MELHORAR E COMENTAR
    prompt = f"""Public opinion on the movie based on:\n
    Average score: {mean:.2f}\n
    and the following reviews:\n"""
    prompt = append_reviews_to_prompt(prompt, reviews)

    return get_response(prompt)


def keywords_for_movie(reviews):
    # TODO: REVISAR E MELHORAR E COMENTAR
    prompt = "Keywords that describe this movie based on its reviews:\n"
    prompt = append_reviews_to_prompt(prompt, reviews)

    return get_response(prompt)

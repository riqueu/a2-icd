"""Módulo para geração de respostas com a API da OpenAI"""

import openai as ai
from dotenv import load_dotenv, find_dotenv
import os

# Pega chave da API do .env
_ = load_dotenv(find_dotenv())

client = ai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# MÉTODO ANTIGO:
# Pega chave da API do txt gpt_api.txt
"""file = open("gpt_api.txt", "r")
key_gpt = file.read()
client = ai.OpenAI(api_key=key_gpt)"""

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


def summary_based_on_reviews(name, reviews):
    prompt = f"""Based on user reviews on Letterboxd, 
    give me a brief summary of {name} (IN ENGLISH):\n"""
    prompt = append_reviews_to_prompt(prompt, reviews)

    return get_response(prompt)


def summary_public_opinion(name, mean, reviews):
    prompt = f"""Public opinion on {name} based on:\n
    Average score: {mean:.2f}\n
    and the following reviews:\n"""
    prompt = append_reviews_to_prompt(prompt, reviews)

    return get_response(prompt)


def keywords_for_movie(name, reviews):
    prompt = f"""Keywords (IN ENGLISH) that describe {name} based on its reviews, 
    please separate each keyword with a '-' and DO NOT use line breaks, only spaces and dashes, 
    example: 'ironical - funny - introspective - ...':\n"""
    prompt = append_reviews_to_prompt(prompt, reviews)

    return get_response(prompt)

from dotenv import load_dotenv
load_dotenv()

import openai
from retrying import retry

@retry(stop_max_attempt_number=5, wait_fixed=2000) # 等待 2 秒后重试，最多重试 5 次
def ask_gpt(prompt, model='gpt-3.5-turbo') -> str:
    result = openai.ChatCompletion.create(
        model=model, 
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    return result['choices'][0]['message']['content']

def ask_gpt_with_system(system, prompt, model='gpt-3.5-turbo') -> str:
    result = openai.ChatCompletion.create(
        model=model, messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    return result['choices'][0]['message']['content']
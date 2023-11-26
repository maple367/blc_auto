# %%
from openai import OpenAI
import __init__

client = OpenAI()

def gpt_response(message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是直播间答复助理小猫咪，所做答复简洁可爱不超过三十字"},
            {"role": "user", "content": message}
        ],
        max_tokens=35,
        temperature=1,
    )
    return completion.choices[0].message.content

# %%
if __name__ == "__main__":
    print(gpt_response("你好"))
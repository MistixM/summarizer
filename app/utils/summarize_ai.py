from openai import OpenAI
from configparser import ConfigParser

def summarize_messages(msgs):
    config = ConfigParser()
    config.read("./app/constants/config.ini")

    client = OpenAI(api_key=config['Bot']['OPEN_AI'])

    prompt = f"Summarize the following conversation: \n\n{''.join(msgs)}"
    setting = "You're language depends on chat's language. You are a summarizer who will summarize all the messages that comes from the Telegram chat. Please make the summaries short, but without loss of meaning. Also remember to summarize with the same language as the chat."
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": setting},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
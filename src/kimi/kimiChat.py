from openai import OpenAI

client = OpenAI(
    api_key="sk-qk0huCyKhlZBdu8hujNlNFOeBU6Sm0b5nJXKqH4T95mS3JsI",
    base_url="https://api.moonshot.cn/v1",
)


class kimiChat:

    def __init__(self):
        self.history = [
            {"role": "system",
             "content": "你叫Miles，是一个的性格活泼，可爱的私人智能助手。目前你的版本是1.0,你还在升级进化中，今后你可以发语音，发图片，还可以视频聊天。"}
        ]

    def chat(self,chatLog: []):
        # self.history += [{
        #     "role": "user",
        #     "content": query
        # }]
        messages = self.history + chatLog
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=0.3,
        )
        result = completion.choices[0].message.content
        # self.history += [{
        #     "role": "assistant",
        #     "content": result
        # }]
        return result
        # print(messages)

import json

import requests

# response = requests.post(
#     "http://localhost:8000/generate-blog/invoke",
#     json={"input": "What is your name? and what is the weather like in Mumbai"},
# )

response = requests.post(
    "https://pretty-wanda-ssreeramj-0048b972.koyeb.app/generate-blog/invoke",
    json={"input": "What are you doing?"},
)

# print(response)

r = json.loads(response.content)
print(r["output"])

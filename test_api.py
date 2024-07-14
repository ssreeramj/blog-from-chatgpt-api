import json

import requests

response = requests.post(
    "http://localhost:8000/generate-blog/invoke",
    json={"input": "https://chatgpt.com/share/3a3d6737-2a4d-45b9-9d0d-9cd88fdc2fd2"},
)

# response = requests.post(
#     "https://pretty-wanda-ssreeramj-0048b972.koyeb.app/generate-blog/invoke",
#     json={"input": "What is the weather in Chennai? Do I need to wear a sweater?"},
# )

# print(response)

r = json.loads(response.content)
print(r["output"])

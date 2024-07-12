import json

import requests

response = requests.post(
    "http://localhost:8000/generate-blog/invoke",
    json={"input": "What is your name? and what is the weather like in Mumbai"},
)

# response = requests.post(
#     "https://orange-chainsaw-9jqqqx6jx4v3xr7w-8000.app.github.dev/generate-blog/invoke",
#     json={"input": "what is the weather like in mumbai?"},
# )

# print(response)

r = json.loads(response.content)
print(r["output"])

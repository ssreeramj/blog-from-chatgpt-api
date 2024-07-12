import requests
import json

response = requests.post(
"http://localhost:8000/generate-blog/invoke",
json={'input': "Hi, How is the weather in Mumbai?"}
)

r = json.loads(response.content)
print(r["output"])
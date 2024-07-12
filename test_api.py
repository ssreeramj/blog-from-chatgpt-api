import requests
import json

response = requests.post(
"http://localhost:8000/generate-blog/invoke",
json={'input': "https://chatgpt.com/share/7e720abe-6786-431b-a4ae-bba433b3f17f"}
)

r = json.loads(response.content)
print(r["output"])
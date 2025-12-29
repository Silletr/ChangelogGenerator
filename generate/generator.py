from ollama import chat
from ollama import ChatResponse
from parse_commits import generate_changelog


with open("ai_prompt.txt", "r", encoding="utf-8") as file:
    prompt_text = file.read()

result = f"{prompt_text}\nThere`s changelog: {generate_changelog()}"

response: ChatResponse = chat(
    model="phi3:mini",
    messages=[
        {
            "role": "user",
            "content": result,
        },
    ],
)

print(response["message"]["content"])

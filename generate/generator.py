from ollama import chat
from ollama import ChatResponse

with open("ai_prompt.txt", "r", encoding="utf-8") as file:
    prompt_text = file.read()


response: ChatResponse = chat(
    model="phi3:mini",
    messages=[
        {
            "role": "user",
            "content": prompt_text,
        },
    ],
)

print(response["message"]["content"])

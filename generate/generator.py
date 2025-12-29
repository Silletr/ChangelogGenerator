from ollama import chat
from parse_commits import generate_changelog, write_to_file
from loguru import logger
from os import getcwd

with open("ai_prompt.txt", "r", encoding="utf-8") as file:
    prompt_text = file.read()

full_prompt = f"{prompt_text}\nThere`s changelog: {generate_changelog()}"

# Here will be full AI answer
full_response = ""


response = chat(
    model="phi3:mini", messages=[{"role": "user", "content": full_prompt}], stream=True
)

for chunk in response:
    content = chunk["message"]["content"]
    print(content, end="", flush=True)
    full_response += content  # Collecting AI answer to full answer

print("\n\n=== TLDR Generated ===")

write_to_file(full_response)

logger.info(f"Full answer writtten to: release.md in: {getcwd()}!")

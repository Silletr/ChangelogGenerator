from ollama import chat
from loguru import logger
from pathlib import Path
from importlib.resources import files


def get_prompt(prompt_path: str | None = None) -> str:
    """Load prompt from file or bundled resource."""
    if prompt_path and Path(prompt_path).exists():
        return Path(prompt_path).read_text(encoding="utf-8")

    try:
        return (
            files("changelog_gen.prompts")
            .joinpath("ai_prompt.txt")
            .read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            """No prompt found.
        Use --prompt or add prompts/ai_prompt.txt"""
        )


def generate_ai_changelog(
    changelog: str, model: str, output_file: str, prompt_path: str | None = None
) -> None:
    """Generate AI changelog and write to file with streaming."""
    prompt_text = get_prompt(prompt_path)
    full_prompt = f"{prompt_text}\nThere's changelog:\n{changelog}"

    print("🤖 AI generating...")
    with open(output_file, "w", encoding="utf-8") as outfile:
        response = chat(
            model=model,
            messages=[{"role": "user", "content": full_prompt}],
            stream=True,
        )

        for chunk in response:
            content = chunk["message"]["content"]
            if content:  # Skip empty chunks
                print(content, end="", flush=True)
                outfile.write(content)
                outfile.flush()

        print("\n\n✅ === Changelog Generated ===")
        logger.info(f"Written to: {output_file}")

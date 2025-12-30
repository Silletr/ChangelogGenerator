# -*- coding: utf-8 -*-
import click
from .generator import generate_ai_changelog
from .parse_commits import generate_changelog


@click.command()
@click.option("--model", default="phi3:mini", help="Ollama model to use")
@click.option("--output", "-o", default="release.md", help="Output file")
@click.option("--prompt", help="Custom prompt file path")
def main(model, output, prompt):
    """AI-powered changelog generator."""
    print("🔍 Generating changelog...")
    changelog = generate_changelog()

    print("🤖 AI generating changelog...")
    generate_ai_changelog(changelog, model, output, prompt)


if __name__ == "__main__":
    main()

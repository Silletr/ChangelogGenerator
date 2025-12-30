import pkg_resources

with pkg_resources.resource_stream(__name__, "ai_prompt.txt") as f:
    ai_prompt_txt = f.read().decode("utf-8")

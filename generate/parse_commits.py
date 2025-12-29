import subprocess
from shutil import which
from loguru import logger
from typing import cast


GIT_PATH = cast(str, which("git"))

if GIT_PATH is None:
    logger.critical("Git isnt define, install it!")
    raise RuntimeError("git not found in PATH")

GIT_PATH = str(GIT_PATH)


def write_to_file(content: str) -> None:
    with open("release.md", "w", encoding="utf-8") as f:
        f.write(content)


def last_tag() -> str:
    subprocess.run([GIT_PATH, "fetch", "--tags"], check=True)
    result = subprocess.run(
        [GIT_PATH, "describe", "--tags", "--abbrev=0"],
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def generate_changelog():
    to_tag = "HEAD"
    try:
        from_tag = last_tag()
    except subprocess.CalledProcessError:
        from_tag = None

    cmd = [GIT_PATH, "log", "--pretty=format:%B"]
    if from_tag:
        cmd.append(f"{from_tag}..{to_tag}")

    try:
        result = subprocess.run(cmd, text=True, capture_output=True, check=True)

        new_files_block = []
        changed_files_block = []
        deleted_files_block = []
        moved_files_block = []

        sections = []

        for line in result.stdout.splitlines():
            line_lower = line.lower().strip()

            if (
                "new file/dir:" in line_lower
                and "changed" not in line_lower
                and "deleted" not in line_lower
            ):
                new_files_block.append(line.strip())

            elif (
                "changed file/dir:" in line_lower
                and "new" not in line_lower
                and "deleted" not in line_lower
            ):
                changed_files_block.append(line.strip())

            elif (
                "deleted file/dir:" in line_lower
                and "new" not in line_lower
                and "changed" not in line_lower
            ):
                deleted_files_block.append(line.strip())

            elif (
                "moved file/dir: " in line_lower
                and "new" not in line_lower
                and "changed" not in line_lower
            ):
                moved_files_block.append(line.strip())

        if new_files_block:
            sections.append("        🆕 **NEW FILE/DIR**:")
            for file_line in new_files_block:
                sections.append(f"                {file_line}")
            sections.append("        " + "-" * 12)

        if changed_files_block:
            sections.append("\n        🗒️ **CHANGED FILE/DIR**:")
            for file_line in changed_files_block:
                sections.append(f"                {file_line}")
            sections.append("        " + "-" * 12)

        if deleted_files_block:
            sections.append("\n        ❌ **REMOVED FILE/DIR**:")
            for file_line in deleted_files_block:
                sections.append(f"                {file_line}")
            sections.append("        " + "-" * 12)

        if moved_files_block:
            sections.append("\n         ➡️ **MOVED FILE/DIR**:")
            for file_line in moved_files_block:
                sections.append(f"                {file_line}")
            sections.append("        " + "-" * 12)

        if not sections:
            full_changelog = "        (No changes detected)"

        else:
            full_changelog = "\n".join(sections)

        print(full_changelog)

        return full_changelog

    except subprocess.CalledProcessError as e:
        error_msg = f"❌ Git error: {e}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    generate_changelog()

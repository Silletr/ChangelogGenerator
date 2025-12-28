import subprocess


def last_tag():
    subprocess.run(["git", "fetch", "--tags"], check=True)
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
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

    cmd = ["git", "log", "--pretty=format:%B"]
    if from_tag:
        cmd.append(f"{from_tag}..{to_tag}")

    try:
        result = subprocess.run(cmd, text=True, capture_output=True, check=True)
        new_files_block = []
        changed_files_block = []
        deleted_files_block = []

        for line in result.stdout.splitlines():
            if (
                ("new file/dir: " in line.lower())
                and ("changed file/dir: " not in line.lower())
                and ("deleted file/dir: " not in line.lower())
            ):
                new_files_block.append(line.strip())

            if (
                ("changed file/dir: " in line.lower())
                and ("new file/dir: " not in line.lower())
                and ("deleted file/dir: " not in line.lower())
            ):
                changed_files_block.append(line.strip())

            if (
                ("deleted file/dir: " in line.lower())
                and ("changed file/dir: " not in line.lower())
                and ("new file/dir: " not in line.lower())
            ):
                deleted_files_block.append(line.strip())

        if new_files_block:
            print("\tNEW FILE/DIR:")
            for file_line in new_files_block:
                print(f"\t\t{file_line}")
            print("\t" + "-" * 12 + "\n")

        if changed_files_block:
            print("\tCHANGED FILE/DIR:")
            for file_line in changed_files_block:
                print(f"\t\t{file_line}")
            print("\t" + "-" * 12 + "\n")

        if deleted_files_block:
            print("\tDELETED FILE/DIR:")
            for file_line in deleted_files_block:
                print(f"\t\t{file_line}")
            print("\t" + "-" * 12 + "\n")

    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")


if __name__ == "__main__":
    generate_changelog()

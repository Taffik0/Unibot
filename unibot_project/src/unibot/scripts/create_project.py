from pathlib import Path
import sys
from importlib import resources
import shutil


def get_and_create() -> Path:
    cwd = Path.cwd()

    args = sys.argv[1:]
    path_to_create = Path.cwd()
    if args:
        if args[0] == ".":
            pass
        else:
            path_to_create /= Path(args[0])

    print(f"Creating in {path_to_create}")

    path_to_create.mkdir(parents=True, exist_ok=True)
    return path_to_create


def copy_bot_orchestration(path_to_copy: Path):
    source = resources.files("unibot.templates.bot_orchestration")

    with resources.as_file(source) as real_path:
        shutil.copytree(real_path, path_to_copy /
                        "bot_orchestration", dirs_exist_ok=True)


def create_src_structure(project_path: Path):
    src_path = project_path / "src"
    src_path.mkdir(parents=True, exist_ok=True)

    handlers_path = src_path / "handlers"
    message_handlers_path = handlers_path / "message"
    command_handlers_path = handlers_path / "command"

    handlers_path.mkdir(parents=True, exist_ok=True)
    message_handlers_path.mkdir(parents=True, exist_ok=True)
    command_handlers_path.mkdir(parents=True, exist_ok=True)

    open(src_path / "states.py", "a").close()
    open(src_path / "commands.py", "a").close()


def copy_run_scripts(project_path: Path):
    src_path = project_path / "src"
    source = resources.files("unibot.templates.scripts").joinpath("main.py")
    with resources.as_file(source) as real_path:
        shutil.copy(real_path, src_path)


if __name__ == "__main__":
    project_path = get_and_create()
    copy_bot_orchestration(project_path)
    create_src_structure(project_path)
    copy_run_scripts(project_path)

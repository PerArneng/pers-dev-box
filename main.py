from pathlib import Path

from devbox import ChangeEngine
from devbox.state_changers import CreateOrReplaceFile
from devbox.utils import DevBoxLogImpl


def main():
    log = DevBoxLogImpl()
    log.info("my message")
    log.warn("my other message")
    log.error("error occurred")

    engine = ChangeEngine()
    # engine.add_state_changer(CreateOrReplaceFile(Path("file1.txt"), "content 1"))
    # engine.add_state_changer(CreateOrReplaceFile(Path("file2.txt"), "content 2"))
    engine.apply_changes()  # Executes all changes


if __name__ == "__main__":
    main()

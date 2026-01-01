from pathlib import Path

from devbox import Container


def main():
    # Create and configure the DI container
    container = Container()

    # Get the logger from the container (Singleton)
    log = container.log()

    log.info("DevBox starting up")

    # Get the change engine from the container (Singleton)
    engine = container.change_engine()

    # Create state changers using the factory
    # The factory injects the log dependency automatically
    engine.add_state_changer(
        container.create_or_replace_file_factory(
            path=Path("file1.txt"),
            contents="content 1",
        )
    )
    engine.add_state_changer(
        container.create_or_replace_file_factory(
            path=Path("file2.txt"),
            contents="content 2",
        )
    )

    # Execute all changes
    engine.apply_changes()

    log.info("DevBox finished")


if __name__ == "__main__":
    main()
